/*--------------------------------------------------------------

  --------------------------------------------------------------*/

#include <SPI.h>
#include <Ethernet.h>

// Network
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = { 169, 254, 104, 100 };
byte gateway[] = { 192, 168, 0 , 1};
byte subnet[] = { 255, 255, 255, 0 };
byte resp = 6;

EthernetServer server(23);  // create a server at port 80
EthernetClient client;

void setup(){
  Ethernet.begin(mac, ip, gateway, subnet); // initialize Ethernet device
  server.begin();           // start to listen for clients
  Serial.begin(9600);       // for debugging
  Serial.println("Setup Ready");
  Serial.println(Ethernet.localIP());
  
}

void loop(){
  byte c;
  // if an incoming client connects, there will be bytes available to read:
  client = server.available();
  
  if (client.available() >0) {
    Serial.println("client connected!");
    // read bytes from the incoming client and write them back
    // to any clients connected to the server:
    c = client.read();
    Serial.println(c);
    server.write(c);
  }
}
