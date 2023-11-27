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

  // Initialize UART
  Serial1.setRX(13);
  Serial1.setTX(12);
  Serial1.begin(115200);
  analogWriteFreq(50);
  
  // // Initialize thruster
  servo.attach(PWM_PIN);
  servo.writeMicroseconds(1500); // send "stop" signal to ESC.
  delay(7000);
}

void loop() {
  if (Serial1.available() == 2) {
    // Turn on LED to awknowlege that UART is working
    digitalWrite(2, HIGH);

    // Check if the message is for us
    int address = Serial1.read();
    Serial1.read();
    if (address == ADDRESS || address == ALL_CALL_ADDRESS) {
      // Blink LED to awknowlege that we're receiving data correctly
      digitalWrite(1, HIGH);
      delay(1000);
      digitalWrite(1, LOW);
    }
  }
}
