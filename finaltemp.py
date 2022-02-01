from keras.models import model_from_json
from local_utils import detect_lp
import matplotlib.image as im
import numpy as np
import pytesseract
import functools
import datetime
import imutils
import cv2

c = "&"

try:
    arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
except:
    print("not received")

while 1:
    data = str(arduino.readline())
    index = data.find(c)
    # print(data)
    # print((arduino.readline()))
    if(index != -1):
        temp = ''.join(x for x in data if (x.isdigit() or x == "."))
        # print(temp)

        # License Plate Detection
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        cv2.imshow('Original Image', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with open('wpod-net.json', 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('wpod-net.h5')
        wpod_net = model

        vehicle = img / 255
        ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
        side = int(ratio * 256)
        bound_dim = min(side, 608)
        _, LpImg, _, cor = detect_lp(
            wpod_net, vehicle, bound_dim, lp_threshold=0.5)

        img = np.float32(LpImg[0])
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow('Car License Plate', img)
        im.imsave('plate.jpg', img)

        # License Plate Character Recognition

        img = cv2.imread('plate.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Grayscale", gray)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        #cv2.imshow("Gaussian Blur", gray)
        # print(type(blur))
        thresh = cv2.adaptiveThreshold(blur, 255,
                                       cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 45, 15)
        #cv2.imshow("Threshold", thresh)

        _, labels = cv2.connectedComponents(thresh)
        mask = np.zeros(thresh.shape, dtype="uint8")

        total_pixels = gray.shape[0] * gray.shape[1]
        lower = total_pixels // 70
        upper = total_pixels // 20

        for (i, label) in enumerate(np.unique(labels)):

            if label == 0:
                continue

            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)

            if numPixels > lower and numPixels < upper:
                mask = cv2.add(mask, labelMask)

        cv2.imshow("mask advanced", mask)

        '''# uncomment this block to show character segmentation

	cnts, _ = cv2.findContours(
			mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		boundingBoxes = [cv2.boundingRect(c) for c in cnts]

		for c in boundingBoxes:
			x, y, w, h = c
			cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 255), 2)

		cv2.imshow("mask blobbed", gray)
		'''

        text = pytesseract.image_to_string(mask, config='--psm 11')

        f = open("data.txt", "a")
        f.write("\nTemp: %s\t Car License Plate: %s\t Date/Time: %s\n" %
                (temp, text, datetime.datetime.now()))
        f.close()

        cv2.waitKey(0)
