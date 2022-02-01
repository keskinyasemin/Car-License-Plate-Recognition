# Car-License-Plate-Recognition
License plate detection and license plate character recognition using OpenCV.

This project is designed to create a noncontact infrared smart gate to reduce the spread risk of Covid-19 using Arduino UNO with Digital Non-Contact Infrared Thermometer (MLX90614) and save the license plates of the entered vehicles in EMU university.

- final.py: Captures an image from the camera and saves the license plate number in a text file with local date/time.
- finaltemp.py: Must be run after the Arduino code to get the temperature from the sensor and save it in a text file with the plate number, local date/time.  
Data shared from Arduino Serial port to finaltemp.py is given below:  
`data = "&"+ String(temperature,2);`  
`Serial.print(data);`  

## License Plate Detection and Character Recognition
![license1](/screenshots/license1.jpg "license1")
![license2](/screenshots/license2.jpg "license2")
![license3](/screenshots/license3.jpg "license3")

## Output
![licenseoutfinal](/screenshots/licenseoutfinal.jpg "licenseoutfinal")
![licenseoutfinaltemp](/screenshots/licenseoutfinaltemp.jpg "licenseoutfinaltemp")

## Smart Gate Demonstration with a Model
<img src="/screenshots/demo1.jpeg" alt="demo1" width="500" height="650"/>
<img src="/screenshots/demo2.jpeg" alt="demo2" width="500" height="450"/>
