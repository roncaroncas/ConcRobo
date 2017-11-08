'''
Nesse programa se definem o objeto responsável pelo gerenciamento de comunicação

Aqui está o objeto responsável por:
-ESTABELECER CONEXAO
-MANDAR MENSAGEM
-RECEBER RESPOSTA

Por motivos de organização e de desenvolvimento, existem 2 objetos que server para esse propósito:
-Ethernet (que deve ser usado durante a operação)
-FakeConnect (que é um objeto que simula um Zinho falso, serve para poder programar sem ter que ter de fato o zinho)

Obs: O FakeConnect funciona aproximadamente como um echo, ele REPETE a mensagem da resposta com o que foi enviado para ele.
(Não é apenas uma repetição direta porque o formato da mensagem é diferente do formato da resposta)

Já que esses dois objetos são muito parecidos, eles importam funções de uma classe-Pai chamada Network.

Para entender esse objeto, basta-se entender que ele é composto de 3 partes:
-ESTABELECER CONEXAO (connect/disconnect)
-MESSAGE (sendMessage = getMessage + codeMessage + writeStream)
-RESPONSE (receiveResponse = readStream + decodeResponse + updateModel)

O protocolo de comunicação do stream é feito via Ethernet e possui a mensagem no seguinte formato:

################ MENSAGEM ###############
########### PYTHON -> ARDUINO ###########

# SIGNIFICADO		START	INDICE	END

# WRITE
# N					0xFD	0x00	0xFE
# NE				0xFD	0x01	0xFE
# E					0xFD	0x02	0xFE
# SE				0xFD	0x03	0xFE
# S					0xFD	0x04	0xFE
# SO				0xFD	0x05	0xFE
# O					0xFD	0x06	0xFE
# NO				0xFD	0x07	0xFE
# STOP				0xFD	0x08	0xFE

# READ				
# accelX			0xFD	0x10	0xFE
# accelY			0xFD	0x11	0xFE
# accelY			0xFD	0x12	0xFE
# temperature		0xFD	0x13	0xFE
# pressure			0xFD	0x14	0xFE
# bateriaV			0xFD	0x15	0xFE
# bateriaA			0xFD	0x19	0xFE
# ANYINFO			0xFD	0x30	0xFE


################ RESPONSE ###############
########### ARDUINO -> PYTHON ###########

# SIGNIFICADO		START	START	INDICE	VALOR	VALOR	END		END

# MOVE
# N					0xFD	0xFD	0x00	0xFC	0xFC	0xFE	0xFE
# NE				0xFD	0xFD	0x01	0xFC	0xFC	0xFE	0xFE
# E					0xFD	0xFD	0x02	0xFC	0xFC	0xFE	0xFE
# SE				0xFD	0xFD	0x03	0xFC	0xFC	0xFE	0xFE
# S					0xFD	0xFD	0x04	0xFC	0xFC	0xFE	0xFE
# SO				0xFD	0xFD	0x05	0xFC	0xFC	0xFE	0xFE
# O					0xFD	0xFD	0x06	0xFC	0xFC	0xFE	0xFE
# NO				0xFD	0xFD	0x07	0xFC	0xFC	0xFE	0xFE
# STOP				0xFD	0xFD	0x08	0xFC	0xFC	0xFE	0xFE

# INFO				
# accelX			0xFD	0xFD	0x10	0x0000~ 0x03FE	0xFE	0xFE
# accelY			0xFD	0xFD	0x11	0x0000~ 0x03FE	0xFE	0xFE
# accelY			0xFD	0xFD	0x12	0x0000~ 0x03FE	0xFE	0xFE
# temperature		0xFD	0xFD	0x13	0x0000~ 0xFFFE	0xFE	0xFE
# pressure			0xFD	0xFD	0x14	0x0000~ 0xFFFE	0xFE	0xFE
# bateriaV			0xFD	0xFD	0x15	0x0000~ 0xFFFE	0xFE	0xFE
# bateriaA			0xFD	0xFD	0x19	0x0000~ 0xFFFE	0xFE	0xFE

Obs:
O protocolo dos stream é feito com caracteres HEAD e END.
O 0xFC em RESPONSE para os movimentos, são apenas para completar.
accel em RESPONSE tem um range entre 0x0000 e 0x03FE

A conversão do valor em hexadecimal para a unidade real da medida, se dá por funções de acordo com o componente que faz essa medição
Normalmente esses casos são uma função: Y = A*X+B, onde X é o valor hexadecimal da comunicação e Y o valor de fato.
Os valores A e B podem ser encontrados nos datasheets de cada componente.

A conversão Y(X) não é feita nesse arquivo, é feita no model/zinho.py

A mensagem ANYINFO é um "coringa", ele pede para ler qualquer informação (e obviamente, ele responderá com o indice relacionado
a informação que ele leu e não com o indice do ANYINFO)

'''

import socket
import config

class Network():
	def __init__(self, client):
		self.client = client
		self.connected = False

	##### ESTABELECER CONEXAO ######

	def connect(self):
		self.connected = True
		print("Esse modulo precisa ser sobreescrito pelas outras classes!")

	def disconnect(self):
		self.connected = False
		print("Esse modulo precisa ser sobreescrito pelas outras classes!")

	##### MESSAGE ######

	def sendMessage(self):
		if self.connected:
			#get message
			message = self.getMessage()

			#code message
			message = self.codeMessage(message)

			#send message
			self.writeStream(message)
	
	def getMessage(self):
		if self.client.writeTurn:
			self.client.writeTurn = False
			message = self.client.models['User']['move']
		else:
			self.client.writeTurn = True
			message = 'ANYINFO'
		return (message)

	def codeMessage(self, message):

		data = {
		'UP':			b'\x00', #W
		'UP_RIGHT':		b'\x01', #E
		'RIGHT':		b'\x02', #D
		'DOWN_RIGHT':	b'\x03', #C
		'DOWN':			b'\x04', #X
		'DOWN_LEFT':	b'\x05', #Z
		'LEFT':			b'\x06', #A
		'UP_LEFT':		b'\x07', #Q
		'STOP':			b'\x08', #S
		'ANYINFO':		b'\x30', #ANYINFO
		}.get(message, b'\x08')

		return(b'\xFD' + data + b'\xFE')

	def writeStream(self, message):
		raise("Esse modulo precisa ser sobreescrito pelas outras classes!")

	###### RESP #####

	def receiveResponse(self):

		if self.connected:

			#rcvResp
			resp = self.readStream()

			if resp:
				#decodeResp
				name, value = self.decodeResp(resp)

				#updateModel
				self.client.models['Zinho'].updateModel(name, value)

			else:
				self.client.cont = False

		# 	def decodeResp(self, data):
		# self.client.models['Zinho'].processRcvdResp(data)


	def readStream(self):
		raise("Esse modulo precisa ser sobreescrito pelas outras classes!")

	def decodeResp(self, resp):

		ind = resp[2:3]
		value = int.from_bytes(resp[3:5], byteorder='big', signed=False)

		name, value = {
			#MOVES
			b'\x00': ('N',		None),
			b'\x01': ('NE',		None),
			b'\x02': ('E',		None),
			b'\x03': ('SE',		None),
			b'\x04': ('S',		None),
			b'\x05': ('SO',		None),
			b'\x06': ('O',		None),
			b'\x07': ('NO',		None),
			b'\x08': ('STOP',	None),

			#Accel
			b'\x10': ('accelX',	value),
			b'\x11': ('accelY',	value),
			b'\x12': ('accelZ',	value),

			#Temp e Press (I2C)		
			b'\x13': ('temp',	value),
			b'\x14': ('press',	value),

			#Analogics
			b'\x15': ('analog1',value),
			b'\x19': ('analog2',value),

		}.get(ind, ('ANYINFO', None))

		return (name, value)

class Ethernet(Network):

	def __init__(self, client):
		Network.__init__(self, client)
		self.sock = None

	##### ESTABELECER CONEXAO ######

	def connect(self):
		
		try:	
			self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(5)

			print('Connecting to {}:{} ...'.format(config.IP_ZINHO,config.PORT_ZINHO))
			self.sock.connect((config.IP_ZINHO, config.PORT_ZINHO))

			print('Connected')
			self.connected = True

		except:
			print('Connection failed!')
			self.connected = False

	def disconnect(self):
		if self.connected:
			print('Connection Closed!')
			self.sock.close()
			self.connected = False

	##### MESSAGE #####

	def writeStream(self, data):
		try:
			self.sock.sendall(data)
		except:
			self.connected = False

    ##### RESPONSE #####

	def readStream(self):
		try:
			i, j = b'', b''
			resp = b''
			i = self.sock.recv(1)
			while (True):
				j = self.sock.recv(1)
				if i == j == b'\xFD':
					resp = b'\xfd\xfd'
				elif i == j == b'\xFE':
					resp += j
					return(resp)
				else:
					resp += j
				i = j
		except:
			self.connected = False
			return (None)

		
		
class FakeConnect(Network):

	def __init__(self, client):
		Network.__init__(self, client)

		self.fakeData = b'\x08'
		
	##### ESTABELECER CONEXAO #####

	def connect(self):
		self.connected = True
		
	def disconnect (self):
		self.connected = False

	##### MESSAGE #####

	def writeStream(self, data):
		self.fakeData = data[1:2]
		# print("DATA: ", data)

    ##### RESPONSE #####

	def readStream(self):
		return(b'\xFD'+b'\xFD'+self.fakeData+b'\xFE'+b'\xFE')	