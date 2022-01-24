int counter = 1;
int motor_pin = 3;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(motor_pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(counter);
  counter++;
  digitalWrite(motor_pin, HIGH);
  delay(3000);
  digitalWrite(motor_pin, LOW);
  delay(1000);
}
