import serial
import socket

from .config import *

######## PROTOCOLO DE COMUNICACAO ###########
		
# MSG
# Python -> Arduino
# Client -> Server
# startChar		+ data		+ endChar
# 1 byte		+ 1 byte	+ 1byte

# FUNCTION
#		START	DATA	END

# Moves
# N		0xFD	0x00	0xFE
# NE	0xFD	0x01	0xFE
# E		0xFD	0x02	0xFE
# SE	0xFD	0x03	0xFE
# S		0xFD	0x04	0xFE
# SO	0xFD	0x05	0xFE
# O		0xFD	0x06	0xFE
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

#Infos


#ERROR		0xFD	0xFD	0xFF	0xFF	0xFF	0xFE	0xFE



class Ethernet():

	def __init__(self):
		self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(5)
		
	def connect(self):
		try:
			self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(5)
			print('Connecting to {}:{} ...'.format(IP,PORT))
			self.sock.connect((IP, PORT))
			print('Connected')
			return True
		except:
			print('Connection failed!')
			return False
			
		
	def disconnect(self):
		try:
			print('Connection Closed!')
			self.sock.close()
			return True
		except:
			return False
			
	def sendMsg(self,msg):
		try:
			self.sock.sendall(msg.toProtocol())
			return True
		except:
			return False
		
	def getResp(self):
		try:
			i, j = b'', b''
			resp = b''
			i = self.sock.recv(1)
			while (True):
				j = self.sock.recv(1)
				if i == j == HEADCHAR:
					resp = b''
				elif i == j == ENDCHAR:
					resp = resp[:-1]
					return (True, resp)
				else:
					resp += j
				i = j
		except:
			return (False, False)
				  
#TODO: ATUALIZAR!
class Serial():

	def __init__(self):
		print('Connecting...')
		self.ser = serial.Serial(COM_PORT, 9600, timeout=4)
		print('Connected')
		
	def connect (self):
		pass

	def sendMsg(self,msg):
		self.ser.write(msg.toProtocol())
		print("Sent ", msg.toProtocol() ," to arduino")
			 
	def getResp(self):
		print("Waiting for arduino response")
		return ser.readline()

		
class FakeConnect():

	def __init__(self):
		print('Fake Connected')
		
	def connect(self):
		return True
		
	def disconnect (self):
		return True

	def sendMsg(self,msg):
		#print("Sent fake msg")
		#print(msg)
		return True
			 
	def getResp(self):
		#return b'\xfd\xfd\x15\xfc\xfc\xfe\xfe'
		return True, b'\x01\xff\xff'

