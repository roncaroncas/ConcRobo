#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h> // Must include Wire library for I2C
#include <SFE_MMA8452Q.h> // Includes the SFE_MMA8452Q library

// Network
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = { 169, 254, 104, 100 };
byte gateway[] = { 192, 168, 0 , 1};
byte subnet[] = { 255, 255, 255, 0 };

EthernetServer server(23);  // create a server at port 23
EthernetClient client;

//Accelerometer
MMA8452Q accel;

// Flux Control Variables
boolean newMsg = false;
boolean newResp = false;

//Control Variables
byte lastOrder = 0x08;
int deltaTime = 100; //milliseconds
unsigned long tLim = 1000000000;
unsigned long tic;

//Message variables
int msgData;

//Response variables
byte resp[7];

// Protocol Variables
byte headByte = 0xFD;
byte endByte = 0xFE;

// Relays variables
boolean relA = false; // true=Vcc, false=Gnd
boolean relB = false;
boolean relC = false;
boolean relD = false;

// Pinos do relé  = (10, 11, 12, 13) -- Ajustar conforme necessidade
int pinRelA = 4;
int pinRelB = 5;
int pinRelC = 6;
int pinRelD = 7;

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

  // Inicializando pinos do relé
  //Pinos do relé
  pinMode(pinRelA, OUTPUT);
  pinMode(pinRelB, OUTPUT);
  pinMode(pinRelC, OUTPUT);
  pinMode(pinRelD, OUTPUT);
  Serial.println("Relays ready");


  //Pinos analógicos ??
  //pinMode(A0, OUTPUT);
  //pinMode(A1, OUTPUT);
  //pinMode(A2, OUTPUT);
  //pinMode(A3, OUTPUT);
  //pinMode(A4, OUTPUT);
  //pinMode(A5, OUTPUT);

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
    if (msgData <= 8) {
      setControlVars(); // msgData -> atualiza as variáveis de controle
      getControlResp(); // -> resp
    }
    //ASK INFO
    else if (msgData <= 37) {
      getAnalogicResp(); // -> resp
    }
  }
  //Variaveis de controle
  if (newResp == true) {
    newResp = false;
    sendResponse(); //print response in Serial.println
  }

  keepMoving(); //verifica a partir das variaveis de controle e do timeLeft se ja devem parar
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
  resp[3] = 0xFF;
  resp[4] = 0xFF;

  //END
  resp[5] = endByte;
  resp[6] = endByte;
}

///////////////////////////////////////////////////////////////////////////////

void getAnalogicResp() {

  ///!!!!!!!!!!!!!!TODO URGENTE: CONVERTER VALUE PARA BYTE!!!!!!!!!!!!!!!!!!!!!!!!!!
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



    // 0x13, 0x14, 0x15:
      case 0x13:
      case 0x14:
      case 0x15:
        val1 = 0xFF;
        val2 = 0xFF;
        break;
        
     
        val1 = 0xFF;
        val2 = 0xFF;
        

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

  //TODO, DESCOBRIR COMO COMPACTAR ISSO A BAIXO SEM AUMENTAR O LAG
  //tic = millis();

  //server.write(resp,7);
  server.write(resp[0]);
  server.write(resp[1]);
  server.write(resp[2]);
  server.write(resp[3]);
  server.write(resp[4]);
  server.write(resp[5]);
  server.write(resp[6]);

  //Serial.println("Resp: " + String(resp[0]) + " " + String(resp[1]) + " " + String(resp[2]) + " " + String(resp[3]) + " " + String(resp[4]) + " " + String(resp[5]) + " " + String(resp[6]));
}

///////////////////////////////////////////////////////////////////////////////////

///////////////////////////// ACT ////////////////////////////////////////////////

void keepMoving() {
  if (millis() > tLim) {
    lastOrder = 0x08;
    stopReles();
  }
}

// -------- SETTER FUNCTIONS -------

void setReles() {

  switch (msgData) {

    //UP
    case 0 :
      relA = true;
      relB = false;
      relC = true;
      relD = false;
      break;

    //UP_RIGHT
    case 1 :
      relA = true;
      relB = false;
      relC = false;
      relD = false;
      break;

    //RIGHT
    case 2 :
      relA = false;
      relB = true;
      relC = true;
      relD = false;
      break;

    //DOWN_RIGHT
    case 3 :
      relA = false;
      relB = false;
      relC = false;
      relD = true;
      break;

    //DOWN
    case 4 :
      relA = false;
      relB = true;
      relC = false;
      relD = true;
      break;

    //DOWN_LEFT
    case 5 :
      relA = false;
      relB = true;
      relC = false;
      relD = false;
      break;

    //LEFT
    case 6 :
      relA = true;
      relB = false;
      relC = false;
      relD = true;
      break;

    //UP_LEFT
    case 7 :
      relA = false;
      relB = false;
      relC = true;
      relD = false;
      break;

    //STOP
    case 8:
      relA = false;
      relB = false;
      relC = false;
      relD = false;
      break;

    default:
      Serial.println("ERROR: setReles() in default!");
  }
  updateReles();
}

void stopReles() {
  relA = false;
  relB = false;
  relC = false;
  relD = false;
  updateReles();
}

void updateReles() {

  //TEMP
  if (relA == true) {
    digitalWrite(pinRelA, HIGH);
  } else {
    digitalWrite(pinRelA, LOW);
  }

  if (relB == true) {
    digitalWrite(pinRelB, HIGH);
  } else {
    digitalWrite(pinRelB, LOW);
  }

  if (relC == true) {
    digitalWrite(pinRelC, HIGH);
  } else {
    digitalWrite(pinRelC, LOW);
  }

  if (relD == true) {
    digitalWrite(pinRelD, HIGH);
  } else {
    digitalWrite(pinRelD, LOW);
  }

}
