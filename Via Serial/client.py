# This is using the libraries: pygame and pyserial

#import serial
import socket
from time import sleep
import pygame

HEADCHAR = b'\xfd'
ENDCHAR = b'\xfe'

IP = "169.254.104.100"
PORT = 23

class Message:

    def __init__(self, FUNC):
        self.f = FUNC

    def __str__(self):
        s = str(HEADCHAR + self.f + ENDCHAR)
        return s

    def fromKey(self,key):
        #Gets a key and if it is being pressed or released
        #Return a list of actions in protocol format

        #Q - UP_LEFT
        if key == 113:
            self.__init__(b'\x07')

        #W - UP
        elif key == 119:
            self.__init__(b'\x00')

        #E - UP_RIGHT
        elif key == 101:
            self.__init__(b'\x01')

        #A - LEFT
        elif key == 97:
            self.__init__(b'\x06')

        #S - STOP
        elif key == 115:
            self.__init__(b'\x08')

        #D - RIGHT
        elif key == 100:
            self.__init__(b'\x02')

        #Z - DOWN_LEFT
        elif key == 122:
            self.__init__(b'\x05')

        #X - DOWN
        elif key == 120:
            self.__init__(b'\x04')

        #C - DOWN_RIGHT
        elif key == 99:
            self.__init__(b'\x03')

        #TEMP:
        #ELSE: USE NUMBERS

        #else:
        #    self.__init__((key-48).to_bytes(1,'big'))
        #    print("Não está sendo utilizada uma tecla de comando padrão.\nEventos não espereados podem acontecer")

    def toProtocol(self):
        return (HEADCHAR + self.f + ENDCHAR)

class GUI:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Robo')

        #definindo a surface
        self.screen = pygame.display.set_mode((1000,750))

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
    
    print('connecting...')
    sock.connect((IP, PORT))
    print('connected')

    msg = Message(b'\x00')

    gui = GUI()

    #deve-se definir o protocolo de comunicação:
    # Client (python) to Server (arduino)
    # 1) Pin: XX 0~E (4 bits) TODOS DIGITAIS
    # 2) Set/Get: 0(s)/1(g) (1 bit)
    # 3) Set to: 0~1 (1 bit)
    # e.g. Set pin 4 to HIGH: msg = "411"
    # e.g. Get pin 11:  msg = "b00"

    print()

    #Loop
    while (True):

        #get Comando
        key, _ = gui.getKey()
        print("Key: " + str(key))

        msg.fromKey(key) #TODO

        #send Comando
        #ser.write(msg.toProtocol())
        #sock.sendall(b'511')
        sock.sendall(msg.toProtocol())

        print("Sent ", msg.toProtocol() ," to arduino")
        print("Waiting for arduino response")
        
        #get response
        #response = ser.readline()

        response = sock.recv(3)

        #display response
        #print (response.decode('utf-8'))
        print('Received', response)

        
if __name__ == "__main__":
    main()
