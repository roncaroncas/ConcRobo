# This is using the libraries: pygame and pyserial

import serial
from time import sleep
import pygame

ENDCHAR = "\n"

class Message:

    def __init__(self, PIN, SET, HIGH):
        self.p = PIN
        self.s = SET
        self.h = HIGH

    def __str__(self):
        strPin = hex(int(self.p))[2] 
        strSet = str(self.s*1)
        strHigh = str(self.h*1)
        s = strPin + strSet + strHigh + ENDCHAR
        return s

    def setPin(self, PIN):
        self.p = PIN

    def setSet(self, SET):
        self.s = SET

    def setHigh(self, HIGH):
        self.h = HIGH

    def fromKey(self,key,pressed):
        #Gets a key and if it is being pressed or released
        #Return a list of actions in protocol format
        self.__init__(key-48,True,pressed)

    #legacy
    def setMessage(self):
        x = input("Qual a mensagem a ser enviada? (PSH)")
        if len(x) == 3:
            self.setPin(x[0])
            self.setSet(x[1])
            self.setHigh(x[2])
            print("Message set to: "+str(self))
            return True
        else:
            print("Message incorrect")
            return False

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
                    return (event.key, True)
                elif event.type == pygame.KEYUP:
                    print (("You released {}").format(event.key))
                    return (event.key, False)

def main():

    #Setup
    ser = serial.Serial("com3", 9600, timeout=4)
    msg = Message(0,False,False)

    sleep(2)

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
        ser.write(msg.toProtocol())

        print("Sent ", msg.toProtocol() ," to arduino")
        print("Waiting for arduino response")

        #get response
        response = ser.readline()

        #display response
        #print (response.decode('utf-8'))
        print(response, "\n")

        
if __name__ == "__main__":
    main()
