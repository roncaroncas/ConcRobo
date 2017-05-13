//TODO:
//Atualizar protocolo de: Pino-Set-High para Funcao-Timeleft
//Atualizar comunicacao de: Serial para Ethernet 
//Atualizar de programação simples para protomultithread para atuar paralelamente: Read signal e Varredura de funcoes
//Colocar variaveis de controle de funcoes para tempo (pesquisar sobre "millis()")

int i = 0;
char c;

int msgSize = 3;
char msg[5];
String message;
int pin;
boolean setter; //true: setter, false: getter
boolean high; //true: HIGH, false: LOW

// funcoes de varredura
float func0tl = 0; //time left for function 1 to work
float func1tl = 0; //...
float func2tl = 0;

void setup() {
  Serial.begin(9600);

  //TODO: settar corretamente os pinos por funcao

  //Setando todos os pinos como output
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

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

  //---------EXECUÇÃO-----------
  varrerFuncoes(); //loop em cima de comandos (TODO)
  
}

//------ FUNCOES DE COMUNICACAO -----

void readSerial() {  
  String endChar = "\n";
  //int t = 0;
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
  setter = (msg[1] - '0'); //boolean
  high = (msg[2] - '0'); //boolean
}

void sendResponse(){
  
  //retorna uma mensagem no formato "--MESSAGE 311   PIN: 3   SETTER: 1   HIGH: 1"
  String response;
  response = "--MESSAGE: " + message + "   PIN: " + pin + "   SETTER: " + setter + "   HIGH: " + high;
  Serial.println(response);
}

void exeMsg(){
  
  //Atualiza de fato os valores dos pinos
  if (setter == true) {
    if (high == true) {
      digitalWrite(pin, HIGH);
    } else {
      digitalWrite(pin, LOW);
    }
  }
  
}

// -------- VARREDURA FUNCTIONS -------

void varrerFuncoes(){
  if (func0tl>0){
    function0();
  }
  if (func1tl>0){
    function1();
  }
  if (func2tl>0){
    function2();
  }
}

//-ABORT FUNCTION
void function0(){
  
}

void function1(){
  
}

void function2(){
  
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
