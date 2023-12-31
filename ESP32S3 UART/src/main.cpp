// Need this for the lower level access to set them up.
#include <HardwareSerial.h>
#include <SoftwareSerial.h>

//Define two Serial devices mapped to the two internal UARTs
// HardwareSerial MySerial0(0);
// HardwareSerial MySerial1(1);

#define MYPORT_TX 44
#define MYPORT_RX 43

EspSoftwareSerial::UART myPort;

void setup()
{
    // For the USB, just use Serial as normal:
    Serial.begin(115200);
    while (!Serial);

    // MySerial1.begin(115200, SERIAL_8N1, 13, 14);
    // MySerial1.print("MySerial1");
    // initialize serial communication

    // initialize software serial
    myPort.begin(38400, SWSERIAL_8N1, MYPORT_RX, MYPORT_TX, false);
}

void loop()
{
  Serial.println("This is Serial");
  myPort.println("Hello World!");
  delay(1000);
  // MySerial0.println("This is MySerial0");
  // MySerial1.println("This is MySerial1");
}