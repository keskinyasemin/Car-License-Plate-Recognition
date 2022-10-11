#include <Servo.h>
#include <Adafruit_MLX90614.h>

#define led_g 9
#define led_r 8
double angle_rad = PI/180.0;
double angle_deg = 180.0/PI;
double distance;
double temperature;
String data="";
Servo servo_3;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

float getDistance(int trig,int echo){
  pinMode(trig,OUTPUT);
  digitalWrite(trig,LOW);
  delayMicroseconds(2);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  pinMode(echo,INPUT);
  return pulseIn(echo,HIGH,30000)/58.0;
 
}
void setup(){
  servo_3.attach(3);
  servo_3.write(0);
  delay(0.5);
  pinMode(led_g,OUTPUT);
  pinMode(led_r,OUTPUT);
  mlx.begin(); 
  Serial.begin(9600);
 
  
}
void loop(){    


  
 distance=getDistance(7,6);
  temperature=mlx.readObjectTempC();
  data = "&"+ String(temperature,2);
  
  // Serial.print("distance");
 //  Serial.println(distance);
//Serial.print("temperature");
//Serial.print(temperature);
 
 if(distance<5){
 delay(1500);
if((temperature)<(38)){  
   
    digitalWrite(8,LOW);
    digitalWrite(9,HIGH);
     Serial.print(data);
   delay(1000);
    servo_3.write(90);  
    
    
  }
  else{
      
    digitalWrite(8,HIGH);
    digitalWrite(9,LOW); 
    delay(1000);
    servo_3.write(0);
     
    }   
 }
 else{
  
    digitalWrite(9,LOW); 
    digitalWrite(8,LOW);
    delay(1000);
     servo_3.write(0);
     delay(0.5);
     
 }
}
