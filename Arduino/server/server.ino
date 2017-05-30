#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h> // Must include Wire library for I2C
#include <SFE_MMA8452Q.h> // Includes the SFE_MMA8452Q library
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <SerialRelay.h> // Include Serial Relay

// Network
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = {192, 168, 0, 120};
byte gateway[] = { 192, 168, 0 , 1};
byte subnet[] = { 255, 255, 255, 0 };

EthernetServer server(23);  // create a server at port 23
EthernetClient client;

//Accelerometer
MMA8452Q accel;

//Pressao e Temperatura
Adafruit_BMP280 bmp; // I2C

// Flux Control Variables
boolean newMsg = false;
boolean newResp = false;

//Control Variables
byte lastOrder = 0x08;
int deltaTime = 1000; //milliseconds
unsigned long tLim = 1000000000;
unsigned long tLastConnect = 1000000000;
unsigned long tic;

//Message variables
byte priorityMsg = 0xE0;  //Default value (reserved in protocol)
byte msgData;
byte infoCycle [] = {0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x18};
int iInfo = 0;

//Response variables
byte resp[8];

// Protocol Variables
byte headByte = 0xFD;
byte endByte = 0xFE;

// Relays variables
boolean rel[] = {false, false, false, false};
//boolean relA = false; // true=Vcc, false=Gnd
//boolean relB = false;
//boolean relC = false;
//boolean relD = false;

// Pinos do relé  = (4 (data) e 5 (clock))
SerialRelay relay(4,5,1); // (data, clock, number of modules)

// Pino do sensor de tensão:
int AnalogPin = 0;

void setup() {


  // Inicializando serial
  Serial.begin(9600); // Debugging
  Serial.println("Init...");

  // Inicializando internet
  Ethernet.begin(mac, ip, gateway, subnet); // initialize Ethernet device
  server.begin();           // start to listen for clients
  Serial.println("Server ready");

  // Inicializando acelerometro
  accel.init();
  Serial.println("Accelerometer ready");

  if (!bmp.begin()){
    Serial.println("BMP Failed");
  }
  Serial.println("BMP ready");

  
  // Inicializando pinos do relé
  //Pinos do relé
  relay.Info(&Serial,BIN); // for debugging
  
  //pinMode(pinRelA, OUTPUT);
  //pinMode(pinRelB, OUTPUT);
  //pinMode(pinRelC, OUTPUT);
  //pinMode(pinRelD, OUTPUT);
  Serial.println("Relays ready");

  delay(1000); //espera 0,2 segundos para estabilizar conexao

  Serial.println("Setup Ready");
  Serial.print("IP: ");
  Serial.println(Ethernet.localIP());
}

//FUNCAO PRINCIPAL QUE CONTROLA O FLUXO DO PROGRAMA (SEGUE POWER POINT)
void loop() {
  //Comunicacao
  readFromClient(); // Verifica se existe um client tentando mandar msg -> msg, [decodeMsg() -> msgData], newMsg

  //MOVEMENT
  if (newMsg == true) {
    newMsg = false;
    if (msgData <= 0x08) { // se msgData é uma mensagem de movemento
      setControlVars(); // msgData -> atualiza as variáveis de controle
      getControlResp(); // -> resp
    }
    //ASK INFO (accels, temperature, pressure, battery, light

    else if (msgData <= 0x20) {
      getAnalogicResp(); // -> resp
    }
    
    else if (msgData == 0x30) {
      if (priorityMsg != 0xE0){
        msgData = priorityMsg;
        priorityMsg = 0xE0; //Reset value to default
      } else {
        msgData = infoCycle[iInfo];
        iInfo = (iInfo+1)%(sizeof(infoCycle)-1);
      }
      getAnalogicResp(); // -> resp     
    }
  }
  //Variaveis de controle
  if (newResp == true) {
    newResp = false;
    sendResponse();
  }

  keepMoving(); //verifica a partir das variaveis de controle e do timeLeft se ja devem parar

  closeServer(); //
}


//////////////////////////////////COMUNICACAO - READ/////////////////////////////////////////


void readFromClient() {

  client = server.available();  // try to get client

  // TENTA PEGAR UMA LETRA DO CLIENT
  // SE ESSA LETRA FOR UM START -> Zerar Mensagem
  // SE ESSA LETRA FOR UM END -> decodeMsg()
  // SE FOR UM CARACTER COMUM, ACRESCENTAR AO FIM DA STRING

  // SE O CLIENT ENVIOU ALGUMA INFORMAÇÃO
  if (client.available() > 0) {
    tLastConnect = millis();
    byte b = client.read();
    //Serial.println(b);
    if (b == headByte) {
      //Serial.println("Clearing msg");
      msgData = (char)0;
    } else if (b == endByte) {
      //Serial.println("endByte msg");
      newMsg = true;
    } else {
      //Serial.println("elseByte msg");
      msgData = b;
    }
  }
}


/////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////

void setControlVars() {
  if (msgData == lastOrder) {
    tLim = millis() + deltaTime;
  } else {
    lastOrder = msgData;
    tLim = millis() + deltaTime;
    setReles();
  }

}

void getControlResp() {
  newResp = true;

  //HEAD
  resp[0] = headByte;
  resp[1] = headByte;

  //DATA + COMPLETE
  resp[2] = msgData;
  resp[3] = 0xFC;
  resp[4] = 0xFC;

  //END
  resp[5] = endByte;
  resp[6] = endByte;
}

///////////////////////////////////////////////////////////////////////////////

void getAnalogicResp() {

  newResp = true;
  int analogPin;
  int value;
  byte val1;
  byte val2;

  //analogPin = int(msgData)-16;

  //value = analogRead(analogPin);
  
  switch (msgData) {

    // 0x10: ACCEL.X
    case 0x10:
      if (accel.available()) {
        accel.read();
        value = int(1024 * accel.cx + 2048);
        val1 = byte(value / 256);
        val2 = byte(value % 256);
      } else {
        val1 = 0xFF;
        val2 = 0xFF;
      }
      break;

    // 0x11: ACCEL.Y
    case 0x11:
      if (accel.available()) {
        accel.read();
        value = int(1024 * accel.cy + 2048);
        val1 = byte(value / 256);
        val2 = byte(value % 256);
      } else {
        val1 = 0xFF;
        val2 = 0xFF;
      }
      break;

    // 0x12: ACCEL.Z
    case 0x12:
      if (accel.available()) {
        accel.read();
        value = int(1024 * accel.cz + 2048);
        val1 = byte(value / 256);
        val2 = byte(value % 256);
      } else {
        val1 = 0xFF;
        val2 = 0xFF;
      }
      break;



    // 0x13: Temperature
    case 0x13:
      //Precisao de 0.1ºC
      // value = 0    equivale a    Temperatura =   0 ºC
      // value = 1    equivale a    Temperatura = 0.1 ºC
      
      value = int(bmp.readTemperature()*10);
      val1 = byte(value / 256);
      val2 = byte(value % 256);
      
      //Serial.print("Temperature = ");
      //Serial.print(bmp.readTemperature());
      //Serial.println(" *C");
      //Serial.print("Val: ");
      //Serial.println(String(val1) + " " + String(val2));
      //Serial.println();
      break;

    //0x14: Pressure
    case 0x14:
      // Precisao de 100 Pa,,, max possivel: 2mca, min: 0
      // value = 0    equivale a    Pressão =   0 Pa
      // value = 1    equivale a    Pressão = 100 Pa
    
      value = int(bmp.readPressure()/100);
      val1 = byte(value / 256);
      val2 = byte(value % 256);
      
      //Serial.print("Pressure = ");
      //Serial.print(bmp.readPressure());
      //Serial.println(" Pa");
      //Serial.print("Val: ");
      //Serial.println(String(val1) + " " + String(val2));
      
      //Serial.println();
      break;

    //0x15: Battery     -------------  TODO
    case 0x15:
    
      value = analogRead(analogPin);
      //value = 1000;
      val1 = byte(value / 256);
      val2 = byte(value % 256);
      //Serial.println("Voltage value: ," + String(value));
      
      break;

    //0x16: Light -    --------------- TODO
    case 0x16:
      val1 = 0xFF;
      val2 = 0xFF;
      break; 

  
    //0x16: Light +    --------------- TODO
    case 0x17:
      val1 = 0xFF;
      val2 = 0xFF;
      break; 

    
    //0x17: Light     ---------------- TODO
    case 0x18:
      val1 = 0xFF;
      val2 = 0xFF;
      break; 
  }


  //CORRECAO DE BUG PARA val2 = endbyte:
  if (val2 == endByte){
    val2 = val2 + 1;
  }

  //HEAD
  resp[0] = headByte;
  resp[1] = headByte;

  //DATA + COMPLETE
  resp[2] = msgData;
  resp[3] = val1;
  resp[4] = val2;

  //END
  resp[5] = endByte;
  resp[6] = endByte;

}

////////////////////////////////// COMUNICACAO - SEND /////////////////////////
void sendResponse() {
  server.write(resp,8);
}

///////////////////////////////////////////////////////////////////////////////////

///////////////////////////// ACT ////////////////////////////////////////////////

void keepMoving() {
  if (millis() > tLim && lastOrder != 0x08) {
    lastOrder = 0x08;
    stopReles();
    priorityMsg = 0x08;
    //Serial.println("Move time out!");
  }
}

// -------- SETTER FUNCTIONS -------

void setReles() {

  switch (msgData) {
    //UP
    case 0x00 :
      Serial.println("Indo para frente!");
      updateRelay(1,true);
      updateRelay(2,false);
      updateRelay(3,true);
      updateRelay(4,false);
      break;

    //UP_RIGHT
    case 0x01 :
      updateRelay(1,false);
      updateRelay(2,false);
      updateRelay(3,true);
      updateRelay(4,false);
      break;

    //RIGHT
    case 0x02 :    
      updateRelay(1,false);
      updateRelay(2,true);
      updateRelay(3,true);
      updateRelay(4,false);
      break;

    //DOWN_RIGHT
    case 0x03 :
      updateRelay(1,false);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,true);
      break;

    //DOWN
    case 0x04 :
      Serial.println("Indo para Tras!");
      updateRelay(1,false);
      updateRelay(2,true);
      updateRelay(3,false);
      updateRelay(4,true);
      break;

    //DOWN_LEFT
    case 0x05 :
      updateRelay(1,false);
      updateRelay(2,true);
      updateRelay(3,false);
      updateRelay(4,false);
      break;

    //LEFT
    case 0x06 :
      updateRelay(1,true);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,true);
      break;

    //UP_LEFT
    case 0x07 :
      updateRelay(1,true);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,false);
      break;

    //STOP
    case 0x08:
    
      Serial.println("Parando por comando!");
      updateRelay(1,false);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,false);
      break;
  }
}

void stopReles() {
  
  Serial.println("Parando por timeout!");
  updateRelay(1,false);
  updateRelay(2,false);
  updateRelay(3,false);
  updateRelay(4,false);
}

void updateRelay(int numRelay, boolean ligar){
  delay(5);
  if (rel[numRelay-1] == false && ligar == true){
    rel[numRelay-1] = true;
    relay.SetRelay(numRelay, SERIAL_RELAY_ON, 1);
  }
  else if (rel[numRelay-1] == true && ligar == false){
    rel[numRelay-1] = false;
    relay.SetRelay(numRelay, SERIAL_RELAY_OFF, 1);
  }
}

void closeServer() {
  if ((millis() - tLastConnect) > 5000){
    Serial.println("Client Timeout!");
    client.stop();
  }
}

