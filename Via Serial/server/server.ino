//TODO:
//Atualizar protocolo de: Pino-Set-High para Funcao-Set
//Atualizar comunicacao de: Serial para Ethernet
//Colocar variaveis de controle de funcoes para tempo (pesquisar sobre "millis()")

#include <SPI.h>
#include <Ethernet.h>

// Network
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = { 169, 254, 104, 100 };
byte gateway[] = { 192, 168, 0 , 1};
byte subnet[] = { 255, 255, 255, 0 };

EthernetServer server(23);  // create a server at port 80
EthernetClient client;

// Control Variables
int i = 0;
boolean gotResp = false;

//Message variables
bool msgReady = false;
int msgSize = 1; //Apenas do Data
byte msg[2]; //o parametro de msg tem que ser msgSize+1
String message;



// Protocol Variables
int msgData;

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

  Ethernet.begin(mac, ip, gateway, subnet); // initialize Ethernet device
  server.begin();           // start to listen for clients

  Serial.begin(9600); // Debugging

  //Pinos do relé
  pinMode(pinRelA, OUTPUT);
  pinMode(pinRelB, OUTPUT);
  pinMode(pinRelC, OUTPUT);
  pinMode(pinRelD, OUTPUT);

  Serial.println("Setup Ready");
  Serial.print("IP: ");
  Serial.println(Ethernet.localIP());

  delay(100); //espera 0,2 segundos para estabilizar conexao
}

void loop() {
  readFromClient(); // Verifica se existe um client tentando mandar msg -> msg, msgReady, [decodeMsg() -> msgData]
  applyMsg(); // msgData -> atualiza os pinos de acordo com msg
  sendResponse(); //print response in Serial.println
}

void readFromClient() {
  byte headByte = 0xFD;
  byte endByte = 0xFE;

  client = server.available();  // try to get client

  // TENTA PEGAR UMA LETRA DO CLIENT
  // SE ESSA LETRA FOR UM START -> Zerar Mensagem
  // SE ESSA LETRA FOR UM END -> TESTAR PARIDADE DA MENSAGEM -> Mensagem pronta/Atualiza o bool msgReady
  // SE FOR UM CARACTER COMUM, ACRESCENTAR AO FIM DA STRING

  // SE O CLIENT ENVIOU ALGUMA INFORMAÇÃO
  if (client.available() > 0 && !msgReady) {
    byte b = client.read();
    Serial.println(b);
    if (b == headByte || i == msgSize + 2) {
      Serial.println("Clearing msg");
      for (i = 0; i < msgSize; i++) {
        msg[i] = (char)0;
      }
      i = 0;
    } else if (b == endByte) {
      Serial.println("endByte msg");
      decodeMsg();
      gotResp = true;
    } else {
      Serial.println("elseByte msg");
      msg[i] = b;
      i++;
    }
  }
}

void decodeMsg() {

  //TODO: verificar se o comando é valido

  //converte um array de chars (msg) para uma string (message)
  /////FOR DEBUGGIN
  Serial.println("Start decoding");
  message = "";
  for (i = 0; i < msgSize; i++) {
    message += msg[i];
  }
  Serial.println(message);
  /////FOR DEBUGGING

  //atribui os valores de cada caracter de "msg" para as devidas variáveis"
  msgData = byte(msg[0]);
}

void applyMsg() {
  if (msgData <= 8) { //CONDICAO DE MOVIMENTO
    msgDataToReles();
  }
}

void sendResponse() {

  byte resp[3];

  if (gotResp == true) {
    gotResp = false;

    if (msgData <= 8) {

      resp[0] = msgData;
      resp[1] = 0xFE;
      resp[2] = 0xFE;
      server.write(resp[0]);
      server.write(resp[1]);
      server.write(resp[2]);
    }

    String response;
    response = "--Relay A:" + String(relA) + "Relay B:" + String(relB) + "Relay C:" + String(relC) + "Relay D:" + String(relD)  ;
    Serial.println(response);
    //Serial.println(msgData);
  }
}


// -------- SETTER FUNCTIONS -------

void msgDataToReles() {
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
      Serial.println("ERROR: msgToDataReles() in default!");
  }
  setReles();
}

void setReles() {

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
