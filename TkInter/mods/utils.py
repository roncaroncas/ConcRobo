from math import acos, pi
from config import *

def accelToAngle(x, y, z):
	#CONVENCAO: A frente do carrinho aponta na mesma direção do eixo Y, a parte superior aponta para o eixo Z.
	
	A = -x	#eixo A
	B = -y 	#eixo B
	C = -z  #cima
	
	# Sendo g = (x,y,z) em uma base ortonormal
	
	# Vamos achar os angulos entre (x,0,0) e (xg,  0, zg)	%considerando zg para cima
	# Vamos achar os angulos entre (0,y,0) e ( 0, yg, zg)	%considerando zg para cima
	
	# Assim, direto temos que:
	# angleA = acos(zg/gx)
	# angleB = acos(zg/gy)

	g = (A**2 + B**2 + C**2)**.5
	
	#Se g > 1.5 ou o carrinho ta caindo, ou deu um erro de medição, se ele tiver caindo, nao adianta medir.
	if g == 0 or g > 1.2:
		return (False, None)
	
	gA = (A**2 + C**2)**.5
	gB = (B**2 + C**2)**.5
	
	#sem sinal:
	if A == 0:
		angleA = 0
	else:
		angleA = acos(C/gA)*180/pi*abs(A)/A
	if B == 0:
		angleB = 0
	else:
		angleB = acos(C/gB)*180/pi*abs(B)/B

#	print("{:3.1f} {:3.1f} {:3.1f} {:3.1f}".format(A, B, C, g))
	
	return (True, [angleA, angleB])
	
def keysBool2key(keysBool):
	keyVect = []
	for keyName in KEYS:
		key = KEYS[keyName]
		if keysBool[key] == 1:
			return(keyName)
	return None
