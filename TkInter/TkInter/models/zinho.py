'''
Esse objeto mantém o registro das informações do arduino.

Isto é:

Ele registra as variáveis em .data que definem o estado do arduino:
lastMove, angleA, angleB, temperature, pressure, batV, batA e ping
Além disso, os valores calculados indiretamente: distance, alpha(angulo), x, y, z

Além disso, registra em ._ valores temporários:
time, accelX, accelY e accelZ


Nesse arquivo também são feitas as conversões do valor recebido via Ethernet para o valor com a unidade certa.

As funções são no formato: Y = AX + B

Além disso, utiliza-se um parâmetro de filtro K (menor que 1) para suavizar as alterações da variável e os valores ficarem mais estáveis

Assim:
Y: K*Ynovo + (1-K)*Yvelho


A distância percorrida é calculada matematicamente conhecendo a velocidade linear, velocidade angular e tempo.

Assim, se calcula a posição xyz em relação a posição inicial.

Para o angleA e angleB, estes são funções de accelX, accelY e accelZ.
Deve-se accelToAngle() para ajustar a posição inicial em relação a posição do acelerômetro.
Mais detalhes está na própria função (nesse mesmo arquivo)

'''

from math import sin, cos, pi
from time import time
import config

class Zinho():
	def __init__(self, x=0, y=0, z=0, alpha=90, dist=0):
	
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
			raise Exception ("There is no >>",key, "<< key!")
			
	def __str__(self):
	
		s  = '\nLast Move:        	' + self['lastMove']
		s += '\nAccel X, Y, Z:         {:5.2f} {:5.2f} {:5.2f}'.format(self._['accelX'], self._['accelY'], self._['accelZ']) 
		s += '\nDist, x0y0z0:          {:5.2f} {:5.2f} {:5.2f} {:5.2f}'.format(self['distance'], self['x'], self['y'], self['z'])
		s += '\nTemperature:           {:5.2f}'.format(self['temperature'])
		s += '\nPressure:              {:5.2f}'.format(self['pressure'])
		s += '\nBatteryV:              {:5.2f}'.format(self['batteryV'])
		s += '\nBatteryA:              {:5.2f}'.format(self['batteryA'])

		return s

	def updateModel(self, name, value):

		func, param1, param2 = {
			#MOVES
			'N'		: 	(self.setMove,	'N'	,	None),
			'NE'	: 	(self.setMove,	'NE',	None),
			'E'		: 	(self.setMove,	'E'	,	None),
			'SE'	: 	(self.setMove,	'SE',	None),
			'S'		: 	(self.setMove,	'S'	,	None),
			'SO'	: 	(self.setMove,	'SO',	None),
			'O'		: 	(self.setMove,	'O'	,	None),
			'NO'	: 	(self.setMove,	'NO',	None),
			'STOP'	: 	(self.setMove,	'STOP',	None),

			#Accel
			'accelX': 	(self.setAccel,	'accelX', value),
			'accelY': 	(self.setAccel,	'accelY', value),
			'accelZ': 	(self.setAccel,	'accelZ', value),

			#Temp e Press (I2C)		
			'temp' : 	(self.setTemp,	value,	None),
			'press': 	(self.setPress,	value,	None),

			#Analogics
			'analog1': (self.setBatteryV,	value,	None),
			'analog2': (self.setBatteryA,	value,	None),


		}.get(name, (lambda *args: None, None, None))

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

		Krv = config.Krv
		Krw = config.Krw
		Kdv = config.Kdv
		Kdw = config.Kdw
		Klv = config.Klv
		Klw = config.Klw


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


#UTILS:

from math import acos, pi
from config import *

def accelToAngle(x, y, z):

	#	PARA AJUSTAR ESSA FUNÇÃO, DEVEM-SE ATRIBUIR AOS VALORES A, B e C aos equivalentes x, y e z do acelerômetro (com sinal)
	# 	A: eixo A
	#	B: eixo B
	#	C: cima

	###### CONFIGURAÇÃO #######

	A = -x	#eixo A
	B = -y 	#eixo B
	C = -z  #cima 

	###########################


	# DEDUÇÃO MATEMÁTICA:

	# Recomenda-se desenhar para acompanhar essa dedução.

	# O acelerômetro mede a componente de aceleração de gravidade em 3 eixos.
	
	# Sendo g = (x,y,z) em uma base ortonormal
	
	# Vamos achar os angulos entre (x,0,0) e (x,0,z)	%considerando zg para cima
	# Vamos achar os angulos entre (0,y,0) e (0,y,z)	%considerando zg para cima
	
	# Assim, direto temos que:
	# angleA = acos(z/x)
	# angleB = acos(z/y)

	#Calculando a amplitude de g
	g = (A**2 + B**2 + C**2)**.5
	
	#Se g > 1.2 ou o carrinho ta caindo, ou deu um erro de medição, se ele tiver caindo, nao adianta medir.
	if g == 0 or g > 1.2:
		return (False, None)
	
	#Calculando a componente de g nos planos perpendiculares a A e B 
	gA = (A**2 + C**2)**.5 		#Angulo y-0-z no triangulo (0,y,z)
	gB = (B**2 + C**2)**.5		#Angulo x-0-z no triangulo (x,0,z)
	
	#sem sinal:
	if A == 0 or gA == 0:
		angleA = 0
	else:
		angleA = acos(C/gA)*180/pi*abs(A)/A

	if B == 0 or gB == 0:
		angleB = 0
	else:
		angleB = acos(C/gB)*180/pi*abs(B)/B

#	print("{:3.1f} {:3.1f} {:3.1f} {:3.1f}".format(A, B, C, g))
	
	return (True, [angleA, angleB])