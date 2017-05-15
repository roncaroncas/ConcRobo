
from time import sleep
from gui import GUI
from network import Ethernet, Serial, FakeConnect
from protocol import Message, Response

import math

# CONFIGURACOES GERAIS
#
PRINT = False
DELAY = False
OFFLINE = False
ETHERNET = True		#True: via Ethernet, False: via Serial

class DataBase():
	def __init__(self):
	
		# self.db = {
					# 'move' : {'value': 'STOP'},
					# 'Accel.x': {'value': ""}, #b'\x10'
					# 'Accel.y': {'value': ""}, #b'\x11'
					# 'Accel.z': {'value': ""}, #b'\x12'
					# 'Temperatura': {'value': ""}, #b'\x13'
					# 'Pressao': {'value': ""}, #b'\x14'
					
					# '?':	{},
					# }					
				
				#value = (K)*(A*valueInByte + B) + (1-K)*oldValue 

				# K = 1   ->>> o novo valor substitui completamente o valor antigo
				# K = 0   ->>> o valor antigo não se altera
					
		self.db = {
				
				b'\x00': {'type': 'move',			'value':'N'		,'A': 0., 'B': 0., 'K': 0} ,
				b'\x01': {'type': 'move',			'value':'NE'	,'A': 0., 'B': 0., 'K': 0} ,
				b'\x02': {'type': 'move',			'value':'E'		,'A': 0., 'B': 0., 'K': 0} ,
				b'\x03': {'type': 'move',			'value':'SE'	,'A': 0., 'B': 0., 'K': 0} ,
				b'\x04': {'type': 'move',			'value':'S'		,'A': 0., 'B': 0., 'K': 0} ,
				b'\x05': {'type': 'move',			'value':'SO'	,'A': 0., 'B': 0., 'K': 0} ,
				b'\x06': {'type': 'move',			'value':'O'		,'A': 0., 'B': 0., 'K': 0} ,
				b'\x07': {'type': 'move',			'value':'NO'	,'A': 0., 'B': 0., 'K': 0} ,
				b'\x08': {'type': 'move',			'value':'STOP'	,'A': 0., 'B': 0., 'K': 0} ,	
				
				b'\x10': {'type': 'Accel.x',		'value': 0		,'A': 1/1024., 'B': -2., 'K': .8},			
				b'\x11': {'type': 'Accel.y',		'value': 0		,'A': 1/1024., 'B': -2., 'K': .8},		
				b'\x12': {'type': 'Accel.z',		'value': 1		,'A': 1/1024., 'B': -2., 'K': .8},	
				
				b'\x13': {'type': 'Temperatura',	'value': 25		,'A': 0.1, 'B': 0., 'K': .8},			
				b'\x14': {'type': 'Pressão',		'value': 0		,'A': 100., 'B': 0., 'K': .8},
				
				b'\x15': {'type': '?',				'value': -1		,'A': 0., 'B': 0., 'K': .8},
				
				b'\x20': {'type': '?',				'value': -1		,'A': 0., 'B': 0., 'K': .8},	
			}
			
		self.resultDb = {
				'lastMove': 	"STOP",		# String
				'angleX' : 		0,			# º
				'angleY' : 		0,			# º
				'temperature': 	25.0, 		# ºC
				'pressure':		10000, 		# Pa
		}

	def __str__(self):
	
		#s = 'DataBase:\n' 
		#for indice in self.db:
		#	value = self.db[indice]
		#	s += str(indice) + ": " + str(value) +"\n"
		#return s
	
		s = 'DataBase:\n' 
		for indice in self.resultDb:
			value = self.resultDb[indice]
			s += str(indice) + ": " + str(value) +"\n"
		return s
		
	def store(self, indice, bValue):
	
	
		#print("INDICE:", indice, "  VALUEEEE:                 ", value)
	
		value = int.from_bytes(bValue, 'big')
	
		K = self.db[indice]['K']
		
		if K != 0:
		
			#newValue = (K)*(A*oldValue + B) + (1-K)*oldValue 

			oldValue = self.db[indice]['value']
		
			A = self.db[indice]['A']
			B = self.db[indice]['B']
			
			newValue = K*(A*value + B)	+ (1-K)*oldValue		
		
			self.db[indice]['value'] = newValue
		
		
		funcType = self.db[indice]['type']
		
		if funcType == 'move':
			lastMove = self.db[indice]['value']
			self.resultDb['lastMove'] = lastMove

		
	
		self.sintese()
	
	def sintese(self):

		self.getAngles()
		self.getTemp()
		self.getPress()
	
	def getAngles(self):
	
		#CONVENCAO: A frente do carrinho aponta na mesma direção do eixo Y, a parte superior aponta para o eixo Z.
		
		# Sendo g = (x,y,z) em uma base ortonormal
		# Sabe-que que o triangulo (0,0,0)~(x,0,0)~(x,y,z) é um triangulo retangulo
		# Analogamente para y
		# Logo, |angleXG| = acos(x/g) e |angleYG| = acos(y/g)
		
		x = self.db[b'\x10']['value']
		y = self.db[b'\x11']['value']
		z = self.db[b'\x12']['value']
		
		g = (x**2 + y**2 + z**2)**.5
		
		#print('g:' + str(g))
		
		#Se g > 1.5 ou o carrinho ta caindo, ou deu um erro de medição, se ele tiver caindo, nao adianta medir.
		if g > 1.5:
			return
		
		#em relacao ao g (sem sinal)
		angleXG = - math.acos(x/g)*180/math.pi
		angleYG = - math.acos(y/g)*180/math.pi
		
		#em relação a posição normal do robo:
		angleX = angleXG + 90
		angleY = angleYG + 90
		
		print("{:3.1f} {:3.1f} {:3.1f} {:3.1f}".format(x, y, z, g))
	
		self.resultDb['angleX'] = angleX
		self.resultDb['angleY'] = angleY
		
	def getTemp(self):
		self.resultDb['temperature'] = self.db[b'\x13']['value']
	
	def getPress(self):
		self.resultDb['pressure'] = self.db[b'\x14']['value']
		
		
		
######################	NETWORK	 #################
		


#####################  /NETWORK	 #################


class Client():
	
	def __init__(self):
		if OFFLINE:
			self.conex = FakeConnect()
		elif ETHERNET:
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

			self.gui.drawAll(self.db.resultDb)
			
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
