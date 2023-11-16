#include <Arduino.h>
#include <Wire.h>

void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
  Serial.begin(115200);
}

byte x = 0;

void loop()
{
  Serial.println("TX START");
  Wire.beginTransmission(4); // transmit to device #4
  Wire.write("x is ");        // sends five bytes
  Wire.write(x);              // sends one byte
  Wire.endTransmission();    // stop transmitting
  Serial.println("TX END");

  x++;
  delay(500);
}
