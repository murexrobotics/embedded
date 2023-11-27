#include <Servo.h>
#include <Arduino.h>

int PWM_PIN = 3;
Servo servo;

int ADDRESS = 54;
int ALL_CALL_ADDRESS = 48;

void setup() {
  /// ANYESC MASCP CODE
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  
  digitalWrite(0, HIGH);
  digitalWrite(1, HIGH);
  digitalWrite(2, HIGH);

  // Initialize UART
  Serial1.setRX(13);
  Serial1.setTX(12);
  Serial1.begin(115200);
  
  // Initialize thruster
  servo.attach(PWM_PIN);

  // MIN: 1000, MAX: 2000
  servo.writeMicroseconds(1500);

  // ... whatever you want next
}

void loop() {
  delay(100);
}
