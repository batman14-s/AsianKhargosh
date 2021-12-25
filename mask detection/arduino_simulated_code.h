#include <Servo.h>
Servo servo_motor;

int mask = 0;
long duration, distance;
int mask_detector_pin = 2;
int led_pin = 3;
int buzzor_pin = 4;
int ultra_pin = 8;
int servo_pin = 9;

int baselineTemp = 0;
int celsius = 0;
int fahrenheit = 0;


void setup()
{
    Serial.begin(9600);
    servo_motor.attach(servo_pin ,500,2500);

    pinMode(mask_detector_pin, INPUT);
  	pinMode(A0, INPUT);
	pinMode(led_pin, OUTPUT);	
    pinMode(buzzor_pin, OUTPUT);
}

void loop()
{
  baselineTemp = 40;
  
  celsius = map(((analogRead(A0) - 20) * 3.04), 0, 1023, 30, 45);
  fahrenheit = ((celsius * 9) / 5 + 32);
	
  mask = digitalRead(mask_detector_pin);
  distance = findDistance();

  if(distance > 100){
    digitalWrite(led_pin, LOW);
    digitalWrite(buzzor_pin, LOW);
    servo_motor.write(0);
  } else if (mask == 0 || fahrenheit > 98.6) {
    servo_motor.write(0);
    digitalWrite(buzzor_pin, HIGH);
    digitalWrite(led_pin, LOW);
  } else {
    servo_motor.write(90);
    digitalWrite(led_pin, HIGH);
    digitalWrite(buzzor_pin, LOW);
  }
  
  delay(100);
}

int findDistance(){
  pinMode(ultra_pin, OUTPUT);
  digitalWrite(ultra_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(ultra_pin, HIGH);
  delayMicroseconds(5);
  digitalWrite(ultra_pin, LOW);

  pinMode(ultra_pin, INPUT);
  duration = pulseIn(ultra_pin, HIGH);

  distance = duration/29/2;
  return distance;
}
