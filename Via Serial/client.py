# This is using the libraries: pygame and pyserial

#import serial
import socket
from time import sleep
import pygame

HEADCHAR = "\t"
ENDCHAR = "\n"

class Message:

    def __init__(self, PIN, SET, HIGH):
        self.f = PIN
        self.s = SET
        self.h = HIGH

    def __str__(self):
        strPin = str(self.f)[0] 
        strSet = str(self.s*1)
        strHigh = str(self.h*1)
        s = HEADCHAR + strPin + strSet + strHigh + ENDCHAR
        return s

    def fromKey(self,key,pressed):
        #Gets a key and if it is being pressed or released
        #Return a list of actions in protocol format

        #Q - UP_LEFT
        if key == 113:
            self.__init__(7,True,pressed)

        #W - UP
        elif key == 119:
            self.__init__(0,True,pressed)

        #E - UP_RIGHT
        elif key == 101:
            self.__init__(1,True,pressed)

        #A - LEFT
        elif key == 97:
            self.__init__(6,True,pressed)

        #S - STOP
        elif key == 115:
            self.__init__(8,True,pressed)

        #D - RIGHT
        elif key == 100:
            self.__init__(2,True,pressed)

        #Z - DOWN_LEFT
        elif key == 122:
            self.__init__(5,True,pressed)

        #X - DOWN
        elif key == 120:
            self.__init__(4,True,pressed)

        #C - DOWN_RIGHT
        elif key == 99:
            self.__init__(3,True,pressed)

        #TEMP:
        #ELSE: USE NUMBERS

        else:
            self.__init__(key-48,True,pressed)
            print("Não está sendo utilizada uma tecla de comando padrão")

    def toProtocol(self):
        return str(self).encode('utf-8')

class GUI:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Robo')

        #definindo a surface
        self.screen = pygame.display.set_mode((200,150))

        myfont = pygame.font.SysFont("arial", 15)

        self.screen.fill([220,220,220])

        pygame.display.update()

    def getKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #TODO:
                    #Sair do programa sem Error
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    print (("You pressed {}").format(event.key))
                    return (int(event.key), True)
                #elif event.type == pygame.KEYUP:
                #    print (("You released {}").format(event.key))
                #    return (event.key, False)



def main():


    #Setup
    #ser = serial.Serial("com3", 9600, timeout=4)
    ###SOCKET

    sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    
    print('a')
    sock.connect(("localhost", 80))

    msg = Message(0,False,False)

    gui = GUI()

    #deve-se definir o protocolo de comunicação:
    # Client (python) to Server (arduino)
    # 1) Pin: XX 0~E (4 bits) TODOS DIGITAIS
    # 2) Set/Get: 0(s)/1(g) (1 bit)
    # 3) Set to: 0~1 (1 bit)
    # e.g. Set pin 4 to HIGH: msg = "411"
    # e.g. Get pin 11:  msg = "b00"

    print("A Mensagem a ser enviada necessita ter 3 caracteres:")
    print("Pino em hexadecimal (de 0 a d)")
    print("Get/Set (0/1)")
    print("LOW/HIGH (0/1)")
    print()

    #Loop
    while (True):

        #get Comando
        key, pressed = gui.getKey()
        print("Key: " + str(key) + " Pressed: " + str(pressed))

        #sleep(5)

        msg.fromKey(key, pressed) #TODO


        #send Comando
        #ser.write(msg.toProtocol())
        sock.sendall(msg.toProtocol())

        print("Sent ", msg.toProtocol() ," to arduino")
        print("Waiting for arduino response")
        
        #get response
        #response = ser.readline()

        response = sock.recv(1024)

        #display response
        #print (response.decode('utf-8'))
        print('Received', response)

        
if __name__ == "__main__":
    main()
