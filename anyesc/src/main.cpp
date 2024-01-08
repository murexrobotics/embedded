#include <Servo.h>
#include <Arduino.h>

int PWM_PIN = 3;
Servo servo;

int ADDRESS = 49;
int ALL_CALL_ADDRESS = 48;

void setup() {
  /// ANYESC MASCP CODE
  delay(5000);
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);

  // Initialize UART
  Serial1.setRX(13); // default: 13, backup: 5
  Serial1.setTX(12); // default: 12, backup: 4
  Serial1.begin(115200);
  Serial.begin(115200);

  while (!Serial1);
  
  // Initialize thruster
  Serial.print("Initializing thruster...\n");
  servo.attach(PWM_PIN);
  servo.writeMicroseconds(1500); // send initialization signal to ESC.
  delay(7000);
  Serial.print("Done initializing thruster...\n");
  digitalWrite(0, HIGH);
}

void loop() {
  if (Serial1.available() == 2) {
    int address = Serial1.read();
    int throttle = Serial1.read();
    Serial.print("\n");
    Serial.print(address);
    Serial.print(" ");
    Serial.print(throttle);
    Serial.print(" ");

    if (address == ALL_CALL_ADDRESS || address == ADDRESS) {
        int pulse = map(throttle, 0, 255, 1000, 2000);
        if (throttle == 127) { pulse = 1500; }
        Serial.print(pulse);
        servo.writeMicroseconds(pulse);

        digitalWrite(1, HIGH);
        delay(500);
        digitalWrite(1, LOW);
    }
  }
}
