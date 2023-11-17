#include <Servo.h>
#include <Arduino.h>

int PWM_PIN = 3;
Servo servo;

int ADDRESS = 54;
int ALL_CALL_ADDRESS = 48;

void setup() {
  // Initialize LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  // Initialize UART
  Serial1.begin(115200);

  // Initialize thruster
  servo.attach(PWM_PIN);
  servo.writeMicroseconds(1500); // send "stop" signal to ESC.
  delay(7000);
}

void loop() {
  if (Serial1.available() == 2) {
    // Check if the message is for us
    int address = Serial1.read();
    if (address == ADDRESS || address == ALL_CALL_ADDRESS) {
      // Blink LED to awknowlege that we're receiving data correctly
      digitalWrite(LED_BUILTIN, LOW);
      delay(1000);
      digitalWrite(LED_BUILTIN, HIGH);

      int ds_u8 = Serial1.read();
      // Convert from 0-255 (percentage) to 1000-2000 (pulse width)
      int ds = (int) (1000.0 + 1000.0 * (ds_u8 / 255.0));
      // Send the pulse width to the ESC
      servo.writeMicroseconds(ds);
    }
  }
}
