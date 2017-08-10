/*
  Zinho Server

  Esse programa define o arduino como um servidor que receberá comandos via ethernet
  Tais comandos devem alterar configurações do Robo como direção.
  Ou também podem pedir informação ao arduino
  Ele também é capaz de enviar medições via ethernet

  
  Serão necessários os seguintes componentes para esse projeto:
  -Arduino
  -Sheild Ethernet
  -Shield Multirelés
  -Sensores:
  -- Pressão e Temperatura (BMP 280)
  -- Accelerometro (MMA845X)
  -- Tensão (para as baterias)
  -- Corrente
  
  O circuito é feito da seguinte maneira:
    
    
    POTENCIA:

    Bateria 12V ----CHAVE ON/OFF --------SENSOR CORRENTE ------- DERIVACAO
        12V ------------ A
                         B ------------------- A
                                               B --------------- DERIVACAO(+)
        GND ------------ C
                         D ------------------------------------- DERIVACAO(-)                                       
                                               
   
                  DERIVACAO(+)      SENSOR TENSAO    ARDUINO    CAM1     CAM2
    DERIVACAO (+) -----|------------------ A
                       |----------------------------- PWR (+)
                       |--------------------------------------- PWR(+)
                       |------------------------------------------------ PWR(+)

                  DERIVACAO(-)      SENSOR TENSAO    ARDUINO    CAM1     CAM2
    DERIVACAO (-) -----|------------------ A
                       |----------------------------- PWR (-)
                       |--------------------------------------- PWR(-)
                       |------------------------------------------------ PWR(-)

    SINAIS:

    ARDUINO -------------- SENSOR CORRENTE
      5V    ---------------     VCC
 analogPin 1---------------     OUT                 *Alterar o analogPin na próxima seção desse programa caso necessário
      GND   ---------------     GND

   ARDUINO --------------- SENSOR TENSAO
      12V   ---------------     12V
      GND   ---------------     GND
 analogPin 2---------------     DATA                *Alterar o analogPin na próxima seção desse programa caso necessário
      
    ARDUINO ---------------   MMA8452Q (Acelerometro)
      3.3V  ---------------     VCC
      GND   ---------------     GND
      SDA   ---------------     SDA
      SCL   ---------------     SCL

    ARDUINO ---------------    BMP280 (Temp. e Pres.)
      3.3V  ---------------     VCC
      GND   ---------------     GND
      SDA   ---------------     SDA
      SCL   ---------------     SCL
      SA0   ---------------     +5V

    ARDUINO ---------------    Multi-Relés
      12V   ---------------     12V
      GND   ---------------     GND
  digPin 4  ---------------     DATA                *Alterar o digPin na próxima seção desse programa caso necessário
  digPin 5  ---------------     CLK                 *Alterar o digPin na próxima seção desse programa caso necessário

    ARDUINO ---------------  ETHERNET SHIELD
  digPin 10  ---------------     digPin10           *Esses pinos não podem ser alterados devido ao próprio encaixe do shield
  digPin 11  ---------------     digPin11           *Esses pinos não podem ser alterados devido ao próprio encaixe do shield
  digPin 12  ---------------     digPin12           *Esses pinos não podem ser alterados devido ao próprio encaixe do shield
  digPin 13  ---------------     digPin13           *Esses pinos não podem ser alterados devido ao próprio encaixe do shield

  Criado 08/08/2017
  Por Victor Roncalli e Fabio Subtil - Concremat
  victor.roncalli.souza@gmail.com
*/

//-------------------------------BIBLIOTECAS-----------------------------------//

#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h> // Must include Wire library for I2C
#include <SFE_MMA8452Q.h> // Includes the SFE_MMA8452Q library
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <SerialRelay.h> // Include Serial Relay

//------------------------CONFIGURAÇÕES PARA ALTERAR---------------------------//

///////////////////// Network ////////////////////
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = {192, 168, 0, 125};
byte DNS[] = {192, 168, 0, 1};
byte gateway[] = {192, 168, 0, 1};
byte subnet[] = {255, 255, 255, 0 };

////////////////// Pinos Digitais ////////////////
int relayDataPin = 4;
int relayClockPin = 5;

///////////////// Pinos Analogicos ///////////////
int analogBatAPin = 4;   //Amostragem de corrente
int analogBatVPin = 3;   //Amostragem de tensão


//------------------------DECLARAÇÃO DE VARIÁVEIS -----------------------------//


///////////////////// Network ////////////////////
EthernetServer server(23);  // create a server at port 23
EthernetClient client;

//////////////////// Acelerometro ////////////////
MMA8452Q accel;

//////////////// Pressao e Temperatura ///////////
Adafruit_BMP280 bmp;

//////////////// Fluxo Lógico ////////////////////
boolean newMsg = false;
boolean newResp = false;

////////// Movimento /////////////////////////////
byte lastOrder = 0x08; //byte relacionado ao movimento STOP
int deltaTime = 1000; //milliseconds
unsigned long tLim = 1000000000;
unsigned long tLastConnect = 1000000000;
unsigned long tic;

/////////// Protocolo ////////////////////////////
byte priorityMsg = 0xE0;  //Default value (reserved in protocol)
byte msgData;
byte infoCycle [] = {0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x18};
int iInfo = 0;
byte resp[8];
byte headByte = 0xFD;
byte endByte = 0xFE;

//////////// Relés ///////////////////////////////
boolean rel[] = {false, false, false, false};
SerialRelay relay(relayDataPin, relayClockPin, 1); // data; clock; number of modules=1

void setup() {


  Serial.begin(9600); // Debugging                // Inicializando serial
  Serial.println("Init...");

  Ethernet.begin(mac, ip, DNS, gateway, subnet);  // Inicializa a ethernet
  server.begin();                                 // Inicializa o servidor
  Serial.println("Server ready");
  Serial.print("IP: ");
  Serial.println(Ethernet.localIP());

  relay.Info(&Serial,BIN);                        // "Inicializa" os relés
  Serial.println("Relays ready");
  
  if (!bmp.begin()){                              // Inicializa o BMP
    Serial.println("BMP Failed");                
  } else {
  Serial.println("BMP ready");
  accel.init();                                   // Inicializa o Acelerometro (apenas se conseguir inicializar o BMP)
  Serial.println("Accelerometer ready");
  }
  
  Serial.println("Setup Ready");                  // Indica que o Setup acabou 
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
  int value;
  byte val1;
  byte val2;

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
      value = analogRead(analogBatVPin);
      //value = 1000;
      val1 = byte(value / 256);
      val2 = byte(value % 256);      
      break;

    //0x16: Light -    --------------- TODO
    case 0x16:
      val1 = 0xFF;
      val2 = 0xFF;
      break; 

    //0x17: Light +    --------------- TODO
    case 0x17:
      val1 = 0xFF;
      val2 = 0xFF;
      break; 
    
    //0x18: Light     ---------------- TODO
    case 0x18:
      val1 = 0xFF;
      val2 = 0xFF;
      break; 
   
    //0x19: Battery     -------------  TODO
    case 0x19:
      value = analogRead(analogBatAPin);
      val1 = byte(value / 256);
      val2 = byte(value % 256);
      //Serial.println("Current value: ," + String(value));
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
  }
}

// -------- SETTER FUNCTIONS -------

void setReles() {

  switch (msgData) {
    //UP
    case 0x00 :
      updateRelay(1,true);
      updateRelay(2,false);
      updateRelay(3,true);
      updateRelay(4,false);
      break;

    //UP_RIGHT
    case 0x01 :
      updateRelay(1,true);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,false);
      break;

    //RIGHT
    case 0x02 :    
      updateRelay(1, true);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,true);
      break;

    //DOWN_RIGHT
    case 0x03 :
      updateRelay(1,false);
      updateRelay(2,true);
      updateRelay(3,false);
      updateRelay(4,false);
      break;

    //DOWN
    case 0x04 :
      updateRelay(1,false);
      updateRelay(2,true);
      updateRelay(3,false);
      updateRelay(4,true);
      break;

    //DOWN_LEFT
    case 0x05 :
      updateRelay(1,false);
      updateRelay(2,false);
      updateRelay(3,false);
      updateRelay(4,true);
      break;

    //LEFT
    case 0x06 :
      updateRelay(1,false);
      updateRelay(2,true);
      updateRelay(3,true);
      updateRelay(4,false);
      break;

    //UP_LEFT
    case 0x07 :
      updateRelay(1,false);
      updateRelay(2,false);
      updateRelay(3,true);
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
  if ((millis() - tLastConnect) > 1000){
    client.stop();
  }
}

