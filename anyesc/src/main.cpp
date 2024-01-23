#include <Servo.h>
#include <Arduino.h>

// ------ DO NOT CHANGE THESE VALUES -------
#define PWM_PIN 3
#define ALL_CALL_ADDRESS 48

// -- Update for each individual thruster --
#define ADDRESS 49

// ---- Uncomment to enable debug mode -----
// #define DEBUG

Servo thruster;

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
  #ifdef DEBUG 
    Serial.print("Initializing Thruster");
    Serial.print(ADDRESS - 48);
  #endif

  thruster.attach(PWM_PIN);
  thruster.writeMicroseconds(1500); // send initialization signal to ESC.
  delay(7000); // wait for ESC to initialize

  #ifdef DEBUG
    Serial.print("Finished Initializing Thruster");
  #endif

  // Turn on LED to indicate finished initialization
  digitalWrite(0, HIGH);
}

void loop() {
  if (Serial1.available() == 2) {
    // Turn on LED to indicate that UART is working
    digitalWrite(1, HIGH);

    int address = Serial1.read();
    int throttle = Serial1.read();

    #ifdef DEBUG
      Serial.print("\n");
      Serial.print(address);
      Serial.print(" ");
      Serial.print(throttle);
      Serial.print(" ");
    #endif

    if (address == ALL_CALL_ADDRESS || address == ADDRESS) {
      // Turn on LED to indicate that MASCP is working
      digitalWrite(2, HIGH);
      
      int pulse = map(throttle, 0, 255, 1000, 2000);
      if (throttle == 127) { pulse = 1500; } // Deadzone

      #ifdef DEBUG
        Serial.print(pulse);
      #endif

      thruster.writeMicroseconds(pulse);
    }
  }
}