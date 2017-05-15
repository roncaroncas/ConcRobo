import serial
import socket

### PROTOCOLO (HEADCHAR, ENDCHAR)
HEADCHAR = b'\xfd'
ENDCHAR = b'\xfe'
BYTES_IN_MSG = 3
BYTES_IN_RESP = 8


###ETHERNET: (IP, PORT)
######ARDUINO:
IP = "192.168.0.120"
PORT = 23
#####LOCAL:
#IP = "127.0.0.1"
#PORT = 8080

#SERIAL:
COM_PORT = "com3"



class Ethernet():

	def __init__(self):
		self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print('Connecting to {}:{} ...'.format(IP,PORT))
		self.sock.settimeout(5)
		self.sock.connect((IP, PORT))
		print('Connected')

	def sendMsg(self,msg):
		self.sock.sendall(msg.toProtocol())
		
	def getResp(self):
		i, j = b'', b''

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

class FakeConnect():

	def __init__(self):
		print('Fake Connected')

	def sendMsg(self,msg):
		print("Sent fake msg")
			 
	def getResp(self):

		#return b'\xfd\xfd\x15\xfc\xfc\xfe\xfe'
		return b'\x15\xfc\xfc'

