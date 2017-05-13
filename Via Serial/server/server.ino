//TODO:
//Atualizar protocolo de: Pino-Set-High para Funcao-Set
//Atualizar comunicacao de: Serial para Ethernet
//Colocar variaveis de controle de funcoes para tempo (pesquisar sobre "millis()")

#include <SPI.h>
#include <Ethernet.h>

// Network Variables
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
//byte ip[] = { 169, 254, 104, 100 };
//byte gateway[] = { 192, 168, 0 , 1};
//byte subnet[] = { 255, 255, 255, 0 };
byte ip[] = { 169, 254, 2, 180 };
byte gateway[] = { 169, 254, 2 , 1};
byte subnet[] = { 255, 255, 0, 0 };

EthernetServer server = EthernetServer(80);  // create a server at port 80

// Control Variables
int i = 0;

//Message variables
bool msgReady = false;
int msgSize = 15;
char msg[16];
String message;

// Protocol Variables
int dir;
boolean setter; //true: setter, false: getter
//boolean high; //true: HIGH, false: LOW

// Relays variables
boolean relA = false; // true=Vcc, false=Gnd
boolean relB = false;
boolean relC = false;
boolean relD = false;

int pinRelA = 4;
int pinRelB = 5;
int pinRelC = 6;
int pinRelD = 7;


void setup() {

  Ethernet.begin(mac, ip, gateway, subnet); // initialize Ethernet device
  server.begin();           // start to listen for clients

  Serial.begin(9600); // Debugging

  //TODO: settar corretamente os pinos por funcao

  //Setando todos os pinos como output
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);

  //Pinos do relé (10, 11, 12, 13)
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);


  delay(200); //espera 0,2 segundos para estabilizar conexao
}

void loop() {

  //--------COMUNICACAO----------
  //Pega msg do Serial
  //if (Serial.available()>0){
  //  readSerial(); // Serial -> msg
  //  decodeMsg(); // msg -> message, pin, setter, high
  //  exeMsg(); // atualiza os pinos de acordo com msg
  //  sendResponse(); //print response in Serial.println
  //}

  readFromClient(); // Verifica se existe um client tentando mandar msg -> msg, msgReady
  decodeMsg(); // msg, msgReady -> message, dir, setter
  exeMsg(); // dir, setter -> atualiza os pinos de acordo com msg
  sendResponse(); //print response in Serial.println

}

//------ FUNCOES DE COMUNICACAO -----

//void readSerial() {
//  String endChar = "\n";
//  //resetting i and msg
//  for (i = 0; i < msgSize; i++) {
//    msg[i] = (char)0;
//  }
//  i = 0;
//  while (i < 4) {
//    delay(10);
//    if (Serial.available()>0) {
//      c = Serial.read();
//      if (String(c) == endChar) {
//        return;
//      } else {
//        msg[i] = c;
//        i++;
//      }
//    }
//  }
//}

void readFromClient() {
  char headChar = '\t';
  char endChar = '\n';
  
  EthernetClient client = server.available();  // try to get client

  // TENTA PEGAR UMA LETRA DO CLIENT
  // SE ESSA LETRA FOR UM START -> Zerar Mensagem
  // SE ESSA LETRA FOR UM END -> TESTAR PARIDADE DA MENSAGEM -> Mensagem pronta/Atualiza o bool msgReady
  // SE FOR UM CARACTER COMUM, ACRESCENTAR AO FIM DA STRING

  if (client.available() && !msgReady) {
    char c = client.read();
    if (c == headChar || i == 14) {
      for (i = 0; i < msgSize; i++) {
        msg[i] = (char)0;
      }
    } else if (c == endChar) {
      msgReady == true;
    } else {
      msg[i] = c;
    }
  }
}

void decodeMsg() {

  //converte um array de chars (msg) para uma string (message)
  message = "";
  for (i = 0; i < msgSize; i++) {
    message += msg[i];
  }

  //atribui os valores de cada caracter de "msg" para as devidas variáveis"
  dir = (msg[0] - '0'); // int
  setter = (msg[1] - '0'); //boolean
  //high = (msg[2] - '0'); //boolean

}

void exeMsg() {
  if (msgReady) {
    msgReady = false;
    if (setter == true) {
      dirToReles();
      setReles();
    }
  }
}

void sendResponse() {
  
  String response;
  response = "--MESSAGE: " + message + "   relA: " + relA +   "   relB: " + relB + "   relC: " + relC + "    relD:   " + relD;
  Serial.println(response);
}


// -------- SETTER FUNCTIONS -------

void dirToReles() {
  switch (dir) {

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
      Serial.println("nao entrou em nenhum case");
  }
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
