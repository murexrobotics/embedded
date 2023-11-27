#include <Servo.h>
#include <Arduino.h>

#define pwm_pin 3
#define pulse_width 1500
Servo servo;

void setup() {
  // Turn on the LEDs
  pinMode(0, OUTPUT);
  digitalWrite(0, HIGH);
  pinMode(1, OUTPUT);
  digitalWrite(1, HIGH);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
  

  // Initialize thruster
  servo.attach(pwm_pin);
  servo.writeMicroseconds(pulse_width);
}

void loop() {
  delay(100);
}
