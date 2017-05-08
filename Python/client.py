import serial
import socket
from time import sleep
import pygame

# CONFIGURACOES GERAIS

#
PRINT = False
DELAY = False

### PROTOCOLO (HEADCHAR, ENDCHAR)
HEADCHAR = b'\xfd'
ENDCHAR = b'\xfe'
BYTES_IN_MSG = 3
BYTES_IN_RESP = 8
ETHERNET = True		#True: via Ethernet, False: via Serial

###ETHERNET: (IP, PORT)
######ARDUINO:
IP = "169.254.104.100"
PORT = 23
#####LOCAL:
#IP = "127.0.0.1"
#PORT = 8080

#SERIAL:
COM_PORT = "com3"

	
class Protocol:
	
	def __str__(self):
		return str(self.head + self.data + self.end)

	def toProtocol(self):
		return (self.head + self.data + self.end)

class Message(Protocol):

	def __init__(self):
		self.head = HEADCHAR
		self.data = b'\x08'
		self.end = ENDCHAR
		self.infoCycle = [
			b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15'] #GARANTIR QUE InfoCycle Segue o protocolo para as informações dos dados analogicos
		self.iInfo = 0
		
	def forceStop(self):
		self.data = b'\x08'

	def fromKey(self,key):
		#Gets a key
		#Return a list of actions in protocol format

		#Q - UP_LEFT
		if key == 113:
			self.data = b'\x07'

		#W - UP
		elif key == 119:
			self.data = b'\x00'

		#E - UP_RIGHT
		elif key == 101:
			self.data = b'\x01'

		#A - LEFT
		elif key == 97:
			self.data = b'\x06'

		#S - STOP
		elif key == 115:
			self.data = b'\x08'

		#D - RIGHT
		elif key == 100:
			self.data = b'\x02'

		#Z - DOWN_LEFT
		elif key == 122:
			self.data = b'\x05'

		#X - DOWN
		elif key == 120:
			self.data = b'\x04'

		#C - DOWN_RIGHT
		elif key == 99:
			self.data = b'\x03'

		else:
			self.data = b'\x20'

	def nextInfo(self):
		self.data = self.infoCycle[self.iInfo]
		self.iInfo = (self.iInfo + 1)%len(self.infoCycle)

class Response(Protocol):
	
	def __init__(self):
		self.head = HEADCHAR + HEADCHAR
		self.data = b'\x00' + b'\x00'
		self.end = ENDCHAR + ENDCHAR
		
	def setData(self, data):
		self.data = data
		
class GUI:
	def __init__(self):

		pygame.init()

		#definindo a surface
		pygame.display.set_caption('Robo')
		self.screen = pygame.display.set_mode((300,600))

		#definindo o periodo de repetição de key_down
		pygame.key.set_repeat(1)

		#definindo a fonte dos textos
		myfont = pygame.font.SysFont("arial", 15)

		#definindo a cor de fundo
		self.screen.fill([220,220,220])
		
		imgNames = [
			'N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO', 'STOP',
			'angleX', 'angleY',		
					]
		self.img      = {
                name: pygame.image.load("./img/{}.jpeg".format(name)).convert()
                for name in imgNames
                }
		
		#setting transparency
		for name in self.img:
			self.img[name].set_colorkey((255,0,255))
		
		#print(self.img)
		#input()
				
		self.movePos = [50,50]

		#atualizando as imagens
		pygame.display.update()

	def getKey(self): #Gets if any key is pressed and what key
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#TODO:
				#Sair do programa sem Error
				pygame.quit()
			elif event.type == pygame.KEYDOWN:
				if PRINT:
					#print (("You pressed {}").format(event.key))
					pass
					
				return (True, int(event.key))
		return (False, 0)

	def drawMove(self, move, update=True):
		movePos = [50,50]
	
		moveImg = self.img[move]
		moveRect = moveImg.get_rect(center=movePos)
		self.screen.blit(moveImg, moveRect)
		
		if update:
			pygame.display.update()
			
	def drawAngleX(self, angleX, update=True):
		angleXPos = [75, 200]
		angleXImg = pygame.transform.rotate(self.img['angleX'],angleX)
		
		angleXRect = angleXImg.get_rect(center=angleXPos)
		self.screen.blit(angleXImg, angleXRect)
		if update:
			pygame.display.update()
		
		
	def drawAngleY(self, angleY, update=True):
		angleYPos = [225, 200]
		angleYImg =  pygame.transform.rotate(self.img['angleY'],angleY)
		angleYRect = angleYImg.get_rect(center=angleYPos)
		self.screen.blit(angleYImg, angleYRect)
		if update:
			pygame.display.update()
		pass
	
	
	def update(self,database):
	
		#self.screen.fill([220,220,220])
		
		#Updating move:
		self.drawMove(database.db['move']['value'],True)
		
		#Updating move:
		angleX = database.db['Accel.x']['value']*90.0
		self.drawAngleX(angleX,True)
		
		#Updating move:
		angleY = database.db['Accel.y']['value']*90.0
		self.drawAngleY(angleY,True)
		
		print(angleX, angleY)
				
		#pygame.display.update()
		
		
class DataBase():
	def __init__(self):
		self.db = {
					'move' : {'value': 'STOP'},
					'Accel.x': {'value': 0}, #b'\x10'
					'Accel.y': {'value': 0}, #b'\x11'
					'Accel.z': {'value': 0}, #b'\x12'
					'?':	{},
					}
					
		self.indMap = {
				b'\x00': {'func': 'move',	'value':'N'} ,
				b'\x01': {'func': 'move',	'value':'NE'} ,
				b'\x02': {'func': 'move',	'value':'E'} ,
				b'\x03': {'func': 'move',	'value':'SE'} ,
				b'\x04': {'func': 'move',	'value':'S'} ,
				b'\x05': {'func': 'move',	'value':'SO'} ,
				b'\x06': {'func': 'move',	'value':'O'} ,
				b'\x07': {'func': 'move',	'value':'NO'} ,
				b'\x08': {'func': 'move',	'value':'STOP'} ,	
				
				b'\x10': {'func': 'Accel.x'},			
				b'\x11': {'func': 'Accel.y'},			
				b'\x12': {'func': 'Accel.z'},			
				b'\x13': {'func': '?'},			
				b'\x14': {'func': '?'},			
				b'\x15': {'func': '?'},
				
				b'\x20': {'func': '?'},
			}

	def __str__(self):
		s = 'DataBase:\n' 
		for indice in self.db:
			value = self.db[indice]
			s += str(indice) + ": " + str(value) +"\n"
		return s
		
	def store(self, indice, value):
		#print(indice, value)
		func = self.indMap[indice]['func']
		if func == 'move':
			value = self.indMap[indice]['value']
		elif func == 'Accel.x' or func == 'Accel.y' or func == 'Accel.z':
			value = (int.from_bytes(value,'big') - 2048)/1024.0
			#rounding:
			value = int(30*value)/30
		self.db[func]['value'] = value
		print(self)

		
######################	NETWORK	 #################
		
class Ethernet():

	def __init__(self):
		self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print('Connecting to {}:{} ...'.format(IP,PORT))
		self.sock.settimeout(5)
		self.sock.connect((IP, PORT))
		print('Connected')

	def sendMsg(self,msg):
		self.sock.sendall(msg.toProtocol())
		if PRINT:
			print("Sent ", msg.toProtocol() ," to arduino")
		
	def getResp(self):
		i, j = b'', b''
		if PRINT:
			print("Waiting for arduino response")

		resp = b''

		i = self.sock.recv(1)
		while (True):
			j = self.sock.recv(1)
			if i == j == HEADCHAR:
				resp = b''
			elif i == j == ENDCHAR:
				resp = resp[:-1]
				return resp
			else:
				resp += j
			i = j
		  
#TODO: VERIFICAR SE SERIAL ESTÁ FUNCIONANDO, AINDA NAO FOI DEBUGADO!!
class Serial():

	def __init__(self):
		print('Connecting...')
		self.ser = serial.Serial(COM_PORT, 9600, timeout=4)
		print('Connected')

	def sendMsg(self,msg):
		self.ser.write(msg.toProtocol())
		print("Sent ", msg.toProtocol() ," to arduino")
			 
	def getResp(self):
		print("Waiting for arduino response")
		return ser.readline()

#####################  /NETWORK	 #################


class Client():
	
	def __init__(self):
		if ETHERNET:
			self.conex = Ethernet()	   
		else:
			self.conex = Serial()
		self.msg = Message()
		self.resp = Response()
		self.gui = GUI()
		self.db = DataBase()

		self.getKey = True #altera-se entre true e false para enviar informacoes de movimento ou para pedir informacoes analogicas


	def getMsg(self):
		if DELAY:
			sleep(0.5)
		if (self.getKey):
			#ver se existe alguma key pressionada
			success, key = self.gui.getKey()
			if PRINT:
				print("Success: ", success)
			if (success):
				self.msg.fromKey(key)
				self.getKey = False
			else:
				self.msg.nextInfo()
				#self.msg.forceStop()
				self.getKey = False
		else:
			if PRINT:
				print()
			self.msg.nextInfo()
			self.getKey = True

	def sendMsg(self):
		self.conex.sendMsg(self.msg)

	def getResp(self):
		#pega-se a resp da conexao
		resp = self.conex.getResp()
		
		#altera-se o valor de resp de acordo com o que foi recebido
		self.resp.setData(resp)
		
		#guarda a resp no db
		self.storeResp()

	def storeResp(self):
		respData = self.resp.data
		respI = respData[0:1]
		respVal = respData[1:3]
		self.db.store(respI, respVal)

	def dispResp(self):
		if PRINT:
			print('Received: ' + str(self.resp))
			print(self.db)

	def main(self):

		######## PROTOCOLO DE COMUNICACAO ###########
		
		# MSG
		# Python -> Arduino
		# Client -> Server
		# startChar		+ data		+ endChar
		# 1 byte		+ 1 byte	+ 1byte
		
		# FUNCTION
		#		START	DATA	END

		# Moves
		# N	0xFD	0x00	0xFE
		# NE	0xFD	0x01	0xFE
		# E	0xFD	0x02	0xFE
		# SE	0xFD	0x03	0xFE
		# S	0xFD	0x04	0xFE
		# SO	0xFD	0x05	0xFE
		# O	0xFD	0x06	0xFE
		# NO	0xFD	0x07	0xFE
		# STOP	0xFD	0x08	0xFE

		# Infos				
		# A0	0xFD	0x10	0xFE
		# A1	0xFD	0x11	0xFE
		# A2	0xFD	0x12	0xFE
		# A3	0xFD	0x13	0xFE
		# A4	0xFD	0x14	0xFE
		# A5	0xFD	0x15	0xFE
		
		#################################

		# RESP
		# Arduino -> Python
		# Server  -> Client

		#			START			FUNC	+ VALUE			+ end
		# bytes:	2				1		2				2

		#FUNCTION
		#			START	START	FUNC	VAL1	VAL2	END		END 

		#Moves
		#N		0xFD	0xFD	0x00	0xFC	0xFC	0xFE	0xFE
		#NE		0xFD	0xFD	0x01	0xFC	0xFC	0xFE	0xFE
		#E		0xFD	0xFD	0x02	0xFC	0xFC	0xFE	0xFE
		#SE		0xFD	0xFD	0x03	0xFC	0xFC	0xFE	0xFE
		#S		0xFD	0xFD	0x04	0xFC	0xFC	0xFE	0xFE
		#SO		0xFD	0xFD	0x05	0xFC	0xFC	0xFE	0xFE
		#O		0xFD	0xFD	0x06	0xFC	0xFC	0xFE	0xFE
		#NO		0xFD	0xFD	0x07	0xFC	0xFC	0xFE	0xFE
		#STOP		0xFD	0xFD	0x08	0xFC	0xFC	0xFE	0xFE

		#Infos
		#A0		0xFD	0xFD	0x10	VAL1	VAL2	0xFE	0xFE
		#A1		0xFD	0xFD	0x11	VAL1	VAL2	0xFE	0xFE
		#A2		0xFD	0xFD	0x12	VAL1	VAL2	0xFE	0xFE
		#A3		0xFD	0xFD	0x13	VAL1	VAL2	0xFE	0xFE
		#A4		0xFD	0xFD	0x14	VAL1	VAL2	0xFE	0xFE
		#A5		0xFD	0xFD	0x15	VAL1	VAL2	0xFE	0xFE

		#ERROR		0xFD	0xFD	0xFF	0xFF	0xFF	0xFE	0xFE
	 
		cont = True

		while (cont):

			self.gui.update(self.db)
			
			#getMsg (inputs -> msg)
			self.getMsg()

			#sendMsg (msg -> )
			self.sendMsg()

			#getResp (server -> resp)
			self.getResp()

			#dispResp (print resp)
			self.dispResp()


if __name__ == "__main__":
	Client().main()
