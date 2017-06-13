from math import sin, cos, pi
from time import time
from .utils import *

class State():
	def __init__(self, x0=0, y0=0, z0=0, alpha=90, dist=0, id=0, listX=[0], listY=[0]):
	
		self.t = time()
				
		self.state = {
				'lastMove': 	"STOP",		# String
				
				'accelX' :		0,			# g
				'accelY' :		-1,			# g
				'accelZ' :		0,			# g
				
				'angleA' : 		0,			# ?
				'angleB' : 		0,			# ?
				
				'light':		100,		# %
				'temperature': 	-1, 		# ?C
				'pressure':		-1, 		# Pa
				'battery': 		-1,			# %

				'distance':		dist,			# TODO
				'velocity': 	0,			# TODO
				
				
				'alpha':		alpha,			# ?
				'wVelocity':	0,
				
				'x0':   x0,
				'y0':	y0,
				'z0': 	z0,
				
				'listX':	listX,
				'listY':	listY,
				
				'ping':			0,
				
				'message':		"",
				
				'id':			id,
				'newRoute':		False,
				
				'flag':			False
				
				
				}	
					
		self.map = {
		
				#TODO:
				#MEDIR AS VELOCIDADES LINEARES E ANGULAS PARA CADA MOVIMENTO E ATUALIZAR TABELA
				
				b'\x00': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'N'		,	'vel': +Krv , 	'w': 0}, 	#vel em m/s, w em voltas/s (sentido anti-horario)
				b'\x01': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'NE'	,	'vel': +Kdv , 	'w': -Kdw}, #variaveis guardadas no config
				b'\x02': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'E'		,	'vel': 0 , 		'w': -Klw},
				b'\x03': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'SE'	,	'vel': -Kdv , 	'w': +Kdw},
				b'\x04': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'S'		,	'vel': -Krv , 	'w': 0},
				b'\x05': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'SO'	,	'vel': -Kdv , 	'w': -Kdw},
				b'\x06': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'O'		,	'vel': 0 ,		'w': +Klw},
				b'\x07': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'NO'	,	'vel': +Kdv , 	'w': +Kdw},
				b'\x08': {'pointTo': 'lastMove',	'setter': 'setMoveValue',		'value':'STOP'	,	'vel': 0 , 		'w': 0},
				
				b'\x10': {'pointTo': 'accelX',		'setter': 'accelABK',		'A': 1/1024., 	'B': -2., 	'K': .2},			
				b'\x11': {'pointTo': 'accelY',		'setter': 'accelABK',		'A': 1/1024., 	'B': -2., 	'K': .2},		
				b'\x12': {'pointTo': 'accelZ',		'setter': 'accelABK',		'A': 1/1024., 	'B': -2., 	'K': .2},	
				
				b'\x13': {'pointTo': 'temperature',	'setter': 'ABK',			'A': 0.1, 		'B': 0., 	'K': 1.},			
				b'\x14': {'pointTo': 'pressure',	'setter': 'ABK',			'A': 100., 		'B': 0., 	'K': 1.},	
				b'\x15': {'pointTo': 'battery',		'setter': 'ABK',			'A': 0.028571, 	'B': 0., 	'K': .5},
				
				b'\x16': {'pointTo': 'light',		'setter': 'ABK',			'A': 1., 		'B': 0., 	'K': 1.},  ### O programa nunca vai entrar nessa linha
				b'\x17': {'pointTo': 'light',		'setter': 'ABK',			'A': 1., 		'B': 0., 	'K': 1.},  ### O programa nunca via entrar nessa linha
				b'\x18': {'pointTo': 'light',		'setter': 'ABK',			'A': 1., 		'B': 0., 	'K': 1.},
				
				b'\x19': {'pointTo': '?',			'setter': '?',				'A': 1., 		'B': 0., 	'K': 0.},
				
				b'\x20': {'pointTo': '?',			'setter': '?',				'A': 1., 		'B': 0., 	'K': .8},	
			}

	def __str__(self):
	
		s = 'State:\n'
		s += '\nLast Move:        	' + self.state['lastMove']
		s += '\nAccel X, Y, Z:         {:5.2f} {:5.2f} {:5.2f}'.format(self.state['accelX'], self.state['accelY'], self.state['accelZ']) 
		s += '\nDist, x0y0z0:          {:5.2f} {:5.2f} {:5.2f} {:5.2f}'.format(self.state['distance'], self.state['x0'], self.state['y0'], self.state['z0'])
		s += '\nTemperature:           {:5.2f}'.format(self.state['temperature'])
		s += '\nPressure:              {:5.2f}'.format(self.state['pressure'])
		s += '\nBattery:               {:5.2f}'.format(self.state['battery'])

		return s
		
	def store(self, indice, bValue):

		if not (indice in self.map):
			print("ERROR!!")
			return
	
		stateToChange = self.map[indice]['pointTo']
		setter = self.map[indice]['setter']
		
		if setter == 'setMoveValue':
			#Replace value with set value
			now = time()
			deltaT = now - self.t
			self.t = now

			vel = self.state['velocity']
			w = self.state['wVelocity']
			
			vx0 = vel*cos(pi/180*self.state['alpha'])*cos(pi/180*self.state['angleB'])
			vy0 = vel*sin(pi/180*self.state['alpha'])*cos(pi/180*self.state['angleB'])
			vz0 = vel*sin(pi/180*self.state['angleB'])
			
			self.state['distance'] 	+= deltaT*vel
			self.state['z0'] 		+= deltaT*vz0
			
			
			#if False:
			if w != 0:
				r = vel/w /(2*pi)
				alp = self.state['alpha']*pi/180	#em radianos
				alpNovo = deltaT*w*2*pi+alp			#em radianos
				
				x0 = self.state['x0']
				y0 = self.state['y0']
				
				xc = x0 + r/vel * -vy0
				yc = y0 + r/vel * vx0
				
				vx1 = vel*cos(alpNovo)*cos(pi/180*self.state['angleB'])
				vy1 = vel*sin(alpNovo)*cos(pi/180*self.state['angleB'])
				
				x1 = xc - r/vel * -vy1
				y1 = yc - r/vel * vx1
				
				self.state['x0'] 		= x1
				self.state['y0'] 		= y1
			
			else:
			
				self.state['x0'] 		+= deltaT*vx0
				self.state['y0'] 		+= deltaT*vy0
			
			
			self.state['alpha']    	= (self.state['alpha']+(360*deltaT*self.state['wVelocity']))%360d	#em graus
			self.state['velocity'] 	= self.map[indice]['vel']
			self.state['wVelocity'] = self.map[indice]['w']
			
			self.state['lastMove'] 	= self.map[indice]['value']
			
			
		elif setter == 'ABK':
			#newValue = (K)*(A*valueInByte + B) + (1-K)*oldValue
			
			if bValue == b'\xff\xff':
				return
			
			value = int.from_bytes(bValue, 'big')
			memValue = self.state[stateToChange]
			
			A = self.map[indice]['A']
			B = self.map[indice]['B']
			if memValue == -1:
				K = 1
			else:
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
			success, angles =  accelToAngle(accelX, accelY, accelZ)
			if success:
				angleA, angleB 		= angles[0], angle[1]
				self.state['angleA'], self.state['angleB'] = angleA, angleB