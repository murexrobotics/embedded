#include <OneWire.h>
#include <DallasTemperature.h>
#include <HardwareSerial.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2

HardwareSerial MySerial0(0);

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

void setup(void)
{
  // start serial port
  Serial.begin(115200);
  Serial.println("Dallas Temperature IC Control Library Demo");
  MySerial0.begin(9600, SERIAL_8N1, -1, -1);
  MySerial0.print("MySerial0");

  // Start up the library
  sensors.begin(); // IC Default 9 bit. If you have troubles consider upping it 12. Ups the delay giving the IC more time to process the temperature measurement
}


void loop(void)
{
  // call sensors.requestTemperatures() to issue a global temperature
  // request to all devices on the bus
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println("DONE");

  Serial.print("Temperature for Device 1 is: ");
  Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  MySerial0.print("SMART Cable Temperature: ");
  MySerial0.println(sensors.getTempCByIndex(0));
}