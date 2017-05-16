from time import sleep
from gui import GUI
from network import Ethernet, Serial, FakeConnect
from protocol import Message, Response
from utils import accelToAngle
from config import *

class DataBase():
	def __init__(self):
				
		self.state = {
				'lastMove': 	"STOP",		# String
				
				'accelX' :		0,			# g
				'accelY' :		0,			# g
				'accelZ' :		1,			# g
				
				'angleX' : 		0,			# º
				'angleY' : 		0,			# º
				
				'light':		80,			# %
				'temperature': 	25.0, 		# ºC
				'pressure':		200000, 	# Pa
				'battery': 		40,			# %

				'distance':		10000,		#TODO
				'velocity': 	100,		#TODO
				
				
				}	
					
		self.map = {
				
				b'\x00': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'N'		},
				b'\x01': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'NE'	},
				b'\x02': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'E'		},
				b'\x03': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'SE'	},
				b'\x04': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'S'		},
				b'\x05': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'SO'	},
				b'\x06': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'O'		},
				b'\x07': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'NO'	},
				b'\x08': {'pointTo': 'lastMove',	'setter': 'setValue',		'value':'STOP'	},
				
				b'\x10': {'pointTo': 'accelX',		'setter': 'accelABK',		'A': 1/1024., 	'B': -2., 	'K': .8},			
				b'\x11': {'pointTo': 'accelY',		'setter': 'accelABK',		'A': 1/1024., 	'B': -2., 	'K': .8},		
				b'\x12': {'pointTo': 'accelZ',		'setter': 'accelABK',		'A': 1/1024., 	'B': -2., 	'K': .8},	
				
				b'\x13': {'pointTo': 'temperature',	'setter': 'ABK',			'A': 0.1, 		'B': 0., 	'K': .8},			
				b'\x14': {'pointTo': 'pressure',	'setter': 'ABK',			'A': 100., 		'B': 0., 	'K': .8},	
				b'\x15': {'pointTo': 'battery',		'setter': 'ABK',			'A': 1., 		'B': 0., 	'K': 1.},
				
				b'\x16': {'pointTo': 'light',		'setter': 'ABK',			'A': 1., 		'B': 0., 	'K': 1.},
				b'\x17': {'pointTo': 'light',		'setter': 'ABK',			'A': 1., 		'B': 0., 	'K': 1.},
				
				b'\x18': {'pointTo': '?',			'setter': '?',				'A': 1., 		'B': 0., 	'K': 0.},
				b'\x19': {'pointTo': '?',			'setter': '?',				'A': 1., 		'B': 0., 	'K': 0.},
				
				b'\x20': {'pointTo': '?',			'setter': '?',				'A': 1., 		'B': 0., 	'K': .8},	
			}

	def __str__(self):
	
		s = 'DataBase:\n' 
		for indice in self.state:
			value = self.state[indice]
			s += str(indice) + ": " + str(value) +"\n"
		return s
		
	def store(self, indice, bValue):

		if not (indice in self.map):
			return
	
		stateToChange = self.map[indice]['pointTo']
		setter = self.map[indice]['setter']
		
		if setter == 'setValue':
			#Replace value with set value
			self.state[stateToChange] = newValue
			
		elif setter == 'ABK':
			#newValue = (K)*(A*valueInByte + B) + (1-K)*oldValue
			
			value = int.from_bytes(bValue, 'big')
			memValue = self.state[stateToChange]
			
			A = self.map[indice]['A']
			B = self.map[indice]['B']
			K = self.map[indice]['K']
			
			newValue = 	K*(A*value + B)	+ (1-K)*memValue	

			self.state[stateToChange] = newValue
			
		elif setter == "accelABK":
			#newValue = (K)*(A*valueInByte + B) + (1-K)*oldValue
			#tambem atualiza o angulo
		
			value = int.from_bytes(bValue, 'big')
			memValue = self.state[stateToChange]
			A = self.map[indice]['A']
			B = self.map[indice]['B']
			K = self.map[indice]['K']
			
			newValue = 	K*(A*value + B)	+ (1-K)*memValue	
			self.state[stateToChange] = newValue
			
			accelX, accelY, accelZ = self.state['accelX'], self.state['accelY'], self.state['accelZ']
			angleX, angleY, _ = accelToAngle(accelX, accelY, accelZ)
			self.state['angleX'], self.state['angleY'] = angleX, angleY
	

class Client():
	
	def __init__(self):
		if CONEX == "OFFLINE":
			self.conex = FakeConnect()
		elif CONEX == "ETHERNET":
			self.conex = Ethernet()	   
		elif CONEX == "SERIAL":
			self.conex = Serial()
		else:
			print("Wrong Connection type!")
			
		self.msg = Message()
		self.resp = Response()
		self.gui = GUI()
		self.db = DataBase()
		self.writeTurn = True #altera-se entre true e false para enviar informacoes de movimento ou para pedir informacoes analogicas

	def getMsg(self):
		if DELAY:
			sleep(0.5)

		if (self.writeTurn):
			#ver se existe alguma acao requisitada pressionada
			success, key = self.gui.getAction()
			if (success):
				self.msg.fromKey(key)
				self.writeTurn = False
			else:
				self.msg.nextInfo()
				self.writeTurn = True
		else:
			if PRINT:
				print()
			self.msg.nextInfo()
			self.writeTurn = True

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
	 
		while (True):

			self.gui.drawAll(self.db.state)
			
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
