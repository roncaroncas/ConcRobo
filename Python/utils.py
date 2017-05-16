import math

def accelToAngle(x, y, z):
	#CONVENCAO: A frente do carrinho aponta na mesma direção do eixo Y, a parte superior aponta para o eixo Z.
		
	# Sendo g = (x,y,z) em uma base ortonormal
	# Sabe-que que o triangulo (0,0,0)~(x,0,0)~(x,y,z) é um triangulo retangulo
	# Analogamente para y
	# Logo, |angleXG| = acos(x/g) e |angleYG| = acos(y/g)
	
	g = (x**2 + y**2 + z**2)**.5
	
	#print('g:' + str(g))
	
	#Se g > 1.5 ou o carrinho ta caindo, ou deu um erro de medição, se ele tiver caindo, nao adianta medir.
	#if g > 1.5:
	#	return
	
	#em relacao ao g (sem sinal)
	angleXG = - math.acos(x/g)*180/math.pi
	angleYG = - math.acos(y/g)*180/math.pi
	angleZG = - math.acos(z/g)*180/math.pi
	
	#em relação a posição normal do robo:
	angleX = angleXG + 90
	angleY = angleYG + 90
	angleZ = angleZG + 90
	
	print("{:3.1f} {:3.1f} {:3.1f} {:3.1f}".format(x, y, z, g))

	self.state['angleX'] = angleX
	self.state['angleY'] = angleY
	
	return (angleX, angleY, angleZ)