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
			self.sock.sendall(msg)
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
					resp = b'\xfd\xfd'
				elif i == j == ENDCHAR:
					resp += j
					return (True, resp)
				else:
					resp += j
				i = j
		except:
			return (False, False)
		
class FakeConnect():

	def __init__(self):
		self.fakeData = b'\x08';
		
	def connect(self):
		print('Fake Connected')
		return True
		
	def disconnect (self):
		return True

	def sendMsg(self,msg):
		#print("Sent fake msg")
		if msg[1:2] < b'\x09':
			self.fakeData = msg[1:2]
		return True
			 
	def getResp(self):
		#return b'\xfd\xfd\x15\xfc\xfc\xfe\xfe'
		return True, b'\xfd\xfd' +self.fakeData + b'\xfc\xfc'
		#return True, b'\x00' + b'\xfc\xfc'

