from math import sin, cos, pi
from time import time
from config import *
from mods.utils import *

class Zinho():
	def __init__(self, x=0, y=0, z=0, alpha=90, dist=0, perc=[(0,0,"init")]):
	
		#Variaveis de estado
		self.data = {

			'lastMove': 	"STOP",		# String
				
			'angleA' : 		0,			# º
			'angleB' : 		0,			# º
			
			'temperature': 	-1, 		# ?C
			'pressure':		-1, 		# Pa
			'batteryV': 	-1,			# V
			'batteryA': 	-1,			# A

			'distance':		dist,		#
			'alpha':		alpha,		#
			
			'velocity': 	0,			# 	
			'wVelocity':	0,
			
			'x':   			x,
			'y':			y,
			'z': 			z,

			'ping':			0,
		}

		#Variaveis internas
		self._ = {

			'accelX':		0,
			'accelY':		0,
			'accelZ': 		-1,

			'time':			time(),	
		}	

					
	def __getitem__(self, key):
		return(self.data[key])

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			print("!!!!!!!!!!!!!!!!There is no >>",key, "<< key!")
			1/0

	def __str__(self):
	
		s  = '\nLast Move:        	' + self['lastMove']
		s += '\nAccel X, Y, Z:         {:5.2f} {:5.2f} {:5.2f}'.format(self._['accelX'], self._['accelY'], self._['accelZ']) 
		s += '\nDist, x0y0z0:          {:5.2f} {:5.2f} {:5.2f} {:5.2f}'.format(self['distance'], self['x'], self['y'], self['z'])
		s += '\nTemperature:           {:5.2f}'.format(self['temperature'])
		s += '\nPressure:              {:5.2f}'.format(self['pressure'])
		s += '\nBatteryV:              {:5.2f}'.format(self['batteryV'])
		s += '\nBatteryA:              {:5.2f}'.format(self['batteryA'])

		return s

	def processRcvdResp(self, msg):

		#msg deve ser uma sequencia de 3 Bytes
		ind = msg[2:3]
		bValue = msg[3:5]
		#print("IND, BVALUE:", ind, bValue)

		value = int.from_bytes(bValue, byteorder='big', signed=False)

		func, param1, param2 = {
			#MOVES
			b'\x00': (self.setMove,		'N',		None),
			b'\x01': (self.setMove,		'NE',		None),
			b'\x02': (self.setMove,		'E',		None),
			b'\x03': (self.setMove,		'SE',		None),
			b'\x04': (self.setMove,		'S',		None),
			b'\x05': (self.setMove,		'SO',		None),
			b'\x06': (self.setMove,		'O',		None),
			b'\x07': (self.setMove,		'NO',		None),
			b'\x08': (self.setMove,		'STOP',		None),

			#Accel
			b'\x10': (self.setAccel,	'accelX',	value),
			b'\x11': (self.setAccel,	'accelY',	value),
			b'\x12': (self.setAccel,	'accelZ',	value),

			#Temp e Press (I2C)		
			b'\x13': (self.setTemp,		value,		None),
			b'\x14': (self.setPress,	value,		None),

			#Analogics
			b'\x15': (self.setBatteryV,	value,		None),
			b'\x19': (self.setBatteryA,	value,		None),


		}.get(ind, (lambda _1,_2 : print("Wrong ind type!"), None, None))

		func(param1, param2)				


	def setMove(self, move, _):
	
		###########   ATUALIZANDO A POSIÇÃO   ###############

		#Replace value with set value
		now 			= time()
		deltaT			= now - self._['time']
		self._['time']	= now

		vel = self['velocity']
		w 	= self['wVelocity']
		
		vx0 = vel*cos(pi/180*self['alpha'])*cos(pi/180*self['angleB'])
		vy0 = vel*sin(pi/180*self['alpha'])*cos(pi/180*self['angleB'])
		vz0 = vel*sin(pi/180*self['angleB'])
		
		self['distance'] 	+= deltaT*vel
		self['z'] 			+= deltaT*vz0
		
		#DIAGONAL
		if w != 0 and vel != 0:
			r = vel/w /(2*pi)
			alp = self['alpha']*pi/180	#em radianos
			alpNovo = deltaT*w*2*pi+alp			#em radianos
			
			x0 = self['x']
			y0 = self['y']
			
			xc = x0 + r/vel * -vy0
			yc = y0 + r/vel * vx0
			
			vx1 = vel*cos(alpNovo)*cos(pi/180*self['angleB'])
			vy1 = vel*sin(alpNovo)*cos(pi/180*self['angleB'])
			
			x1 = xc - r/vel * -vy1
			y1 = yc - r/vel * vx1
			
			self['x'] 		= x1
			self['y'] 		= y1
		
		#RETO, PARADO, OU LATERAL
		else:
			self['x'] 		+= deltaT*vx0
			self['y'] 		+= deltaT*vy0
		
		self['alpha']    	= (self['alpha']+(360*deltaT*self['wVelocity']))%360	#em graus


		#############   ATUALIZANDO O MOVIMENTO   #######


		vel, w = {
			'N': 	( Krv,    0),
			'NE': 	( Kdv, -Kdw),
			'E': 	(   0, -Klw),
			'SE': 	(-Kdv,  Kdw),
			'S': 	(-Krv,    0),
			'SO': 	(-Kdv, -Kdw),
			'O': 	(   0,  Klw),
			'NO': 	( Kdv,  Kdw),
			'STOP':	(   0,    0),
		}[move]

		self['lastMove'] = move
		self['velocity'] = vel
		self['wVelocity']= w

	def setAccel(self, accel, value):
		
		#newValue = (K)*(A*valueInByte + B) + (1-K)*oldValue
		#tambem atualiza o angulo
	
		#accel deve ser 'accelX', 'accelY' ou 'accelZ'


		memValue = self._[accel]

		A = 1/1024.
		B = -2.
		K = .8

		newValue = 	K*(A*value + B)	+ (1-K)*memValue	
		self._[accel] = newValue
		
		accelX, accelY, accelZ = self._['accelX'], self._['accelY'], self._['accelZ']
		success, angles =  accelToAngle(accelX, accelY, accelZ)
		if success:
			angleA, angleB 		= angles[0], angles[1]
			self['angleA'], self['angleB'] = angleA, angleB



	def setTemp(self, value, _):

		#newValue = (K)*(A*value + B) + (1-K)*oldValue

		memValue = self['temperature']

		A = 0.1
		B = 0.
		K = 1.

		newValue = 	K*(A*value + B)	+ (1-K)*memValue	
		self['temperature'] = newValue

	def setPress(self, value, _):

		#newValue = (K)*(A*value + B) + (1-K)*oldValue

		memValue = self['pressure']

		A = 100.
		B = 0.
		K = 1.

		newValue = 	K*(A*value + B)	+ (1-K)*memValue	
		self['pressure'] = newValue

	def setBatteryV(self, value, _):
		#newValue = (K)*(A*value + B) + (1-K)*oldValue

		memValue = self['batteryV']

		A = 0.028571
		B = 0.
		K = .8

		newValue = 	K*(A*value + B)	+ (1-K)*memValue	
		self['batteryV'] = newValue

	def setBatteryA(self, value, _):
		#newValue = (K)*(A*value + B) + (1-K)*oldValue

		memValue = self['batteryA']

		A = 0.1
		B = 0.
		K = .8

		newValue = 	K*(A*value + B)	+ (1-K)*memValue	
		self['batteryA'] = newValue

	def getAllParams(self):
		return (self.data)
