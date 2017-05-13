//TODO:
//Atualizar protocolo de: Pino-Set-High para Funcao-Set
//Atualizar comunicacao de: Serial para Ethernet 
//Atualizar de programação simples para protomultithread para atuar paralelamente: Read signal e Varredura de funcoes
//Colocar variaveis de controle de funcoes para tempo (pesquisar sobre "millis()")

int i = 0;
char c;

int msgSize = 3;
char msg[5];
String message;
int pin;
int dir;
boolean setter; //true: setter, false: getter
boolean high; //true: HIGH, false: LOW

boolean relA = false; // true=Vcc, false=Gnd
boolean relB = false;
boolean relC = false;
boolean relD = false;

int pinRelA = 4;
int pinRelB = 5;
int pinRelC = 6;
int pinRelD = 7;

void setup() {
  Serial.begin(9600);

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
  if (Serial.available()>0){
    readSerial(); // Serial -> msg

    applyMsg(); // msg -> message, pin, setter, high

    exeMsg(); // atualiza os pinos de acordo com msg
  
    sendResponse(); //print response in Serial.println
  }

}

//------ FUNCOES DE COMUNICACAO -----

void readSerial() {  
  String endChar = "\n";
  //resetting i and msg
  for (i = 0; i < msgSize; i++) {
    msg[i] = (char)0;
  }
  i = 0;
  while (i < 4) {
    delay(10);
    if (Serial.available()>0) {
      c = Serial.read();
      if (String(c) == endChar) {
        return;
      } else {
        msg[i] = c;
        i++;
      }
    }
  }
}

void applyMsg(){

  //converte um array de chars (msg) para uma string (message)
  message = "";
  for (i = 0; i < msgSize; i++) {
    message += msg[i];
  }
  
  //atribui os valores de cada caracter de "msg" para as devidas variáveis"

  pin = charToPin(msg[0]);  //usa a funcao charToPin que converte um char para um Pino em int
  dir = (msg[0] - '0'); // int
  setter = (msg[1] - '0'); //boolean
  high = (msg[2] - '0'); //boolean

}

void sendResponse(){
  
  //retorna uma mensagem no formato "--MESSAGE 311   PIN: 3   SETTER: 1   HIGH: 1"
  String response;
  //response = "--MESSAGE: " + message + "   PIN: " + pin + "   SETTER: " + setter + "   HIGH: " + high;
  //response = "--MESSAGE: " + message + "   DIR: " + dir + "   SETTER: " + setter + "   HIGH: " + high;
  response = "--MESSAGE: " + message + "   relA: " + relA +   "   relB: " + relB + "   relC: " + relC + "    relD:   " + relD;
  Serial.println(response);
}

void exeMsg(){
  
  //Atualiza de fato os valores dos pinos
  //if (setter == true) {
  //  if (high == true) {
  //    digitalWrite(pin, HIGH);bata
  //  } else {
  //    digitalWrite(pin, LOW);
  //  }

  if (setter == true){
    dirToReles();  
    setReles();
  }
}


// -------- SETTER FUNCTIONS -------

void dirToReles(){
switch (dir){
    
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

void setReles(){
  
  //TEMP
  if (relA == true){
   digitalWrite(pinRelA, HIGH); 
  } else {
    digitalWrite(pinRelA, LOW);
  }
  
  if (relB == true){
   digitalWrite(pinRelB, HIGH); 
  } else {
    digitalWrite(pinRelB, LOW);
  }
  
  if (relC == true){
   digitalWrite(pinRelC, HIGH); 
  } else {
    digitalWrite(pinRelC, LOW);
  }

  if (relD == true){
   digitalWrite(pinRelD, HIGH); 
  } else {
    digitalWrite(pinRelD, LOW);
  }
    
}

//UTILS FUNCTIONS

int charToPin(char C) {
  switch (C) {
    case '0':
      return 0;
    case '1':
      return 1;
    case '2':
      return 2;
    case '3':
      return 3;
    case '4':
      return 4;
    case '5':
      return 5;
    case '6':
      return 6;
    case '7':
      return 7;
    case '8':
      return 8;
    case '9':
      return 9;
    case 'a':
      return 10;
    case 'b':
      return 11;
    case 'c':
      return 12;
    case 'd':
      return 13;
  }
}
