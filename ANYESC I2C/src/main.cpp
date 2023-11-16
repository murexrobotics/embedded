#include <Arduino.h>
#include <Wire.h>

#define I2C_ADDR 1
#define LED 2

void receiveEvent(int howMany)
{
  while (1 < Wire.available()) // loop through all but the last
  {
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);      // print the character
  }
  int x = Wire.read(); // receive byte as an integer
  Serial.println(x);   // print the integer
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
}

void setup()
{
  Wire.begin(I2C_ADDR);         // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(115200);         // start serial for output
  pinMode(LED, OUTPUT);
}

void loop()
{
  delay(100);
}