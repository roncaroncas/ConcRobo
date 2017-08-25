import socket
from .protocol import Message, Response
from config import *

#from config import IP_ZINHO, PORT_ZINHO
#from config import HEADCHAR, ENDCHAR

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

	def __init__(self, server):
		self.server 				= server
		self.sock 					= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(5)
		self.connected 				= False
		self.msg 					= Message()
		self.resp 					= Response()
		
	def connect(self):
		
		try:
			
			print('Connecting to {}:{} ...'.format(IP_ZINHO,PORT_ZINHO))
			self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(5)

			self.sock.connect((IP_ZINHO, PORT_ZINHO))

			print('Connected')
			self.connected = True

		except:

			print('Connection failed!')
			self.connected = False
			
	def disconnect(self):

		print('Connection Closed!')
		self.sock.close()
		self.connected = False
		

	def packMessage(self):
		if self.server.writeTurn:
			data = self.msg.key2data(self.server.models['User']['move'])
			self.server.writeTurn = False
		else:
			data = self.msg.askRead()
			self.server.writeTurn = True
		return data

	def sendMsg(self):

		data = self.packMessage()

		#print("SENDING: ",data)

		try:
			#print(data)
			self.sock.sendall(data)

			#print("SENT MSG SUCCESS!")
		except:
			self.connected = False
			#print("SENT MSG FAIL!")

	def unpackResp(self):
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
					return (resp)
				else:
					resp += j
				i = j
		except:
			self.connected = False
			return (None)

	def rcvResp(self):
		data = self.unpackResp()
		#print("RESP RECEBIDA: ", data)
		self.server.models['Zinho'].processRcvdResp(data)
		
		
class FakeConnect():

	def __init__(self, server):

		self.server 				= server
		self.connected 				= False
		self.msg 					= Message()
		self.resp 					= Response()

		self.fakeData 				= b'\x08'
		
	def connect(self):
		print('Fake Connected')
		self.connected = True
		
	def disconnect (self):
		self.connected = False

	def packMessage(self):
		if self.server.writeTurn:
			data = self.msg.key2data(self.server.models['User']['move'])
		else:
			data = self.msg.askRead()
		return data

	def sendMsg(self):

		data = self.packMessage()
		print("MESSAGE ENVIADA: ", data)
		if data[1:2] < b'\x09':
			self.fakeData = data[1:2]

	def unpackResp(self):
		return b'\xfd\xfd' + (self.fakeData + b'\xfc\xfc') + b'\xfe\xfe'
		
	def rcvResp(self):
		data = self.unpackResp()
		print("RESP RECEBIDA: ", data)
		print("FAKE DATA: ", self.fakeData)

		self.server.models['Zinho'].processRcvdResp(data)

