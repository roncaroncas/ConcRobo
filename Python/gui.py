import pygame

pygame.init()

pygame.display.set_caption('Robo')

#Initialize Surface
SCREEN = pygame.display.set_mode((300,600))

# Initialize font
FONT = pygame.font.SysFont("monospace", 15)


class Move:
	def __init__(self):

		imgNames = [
			'N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO', 'STOP']

		self.imgs      = {
				name: pygame.image.load("./img/moves/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		self.pos = [75,50]
		img = self.imgs['STOP']
		self.rect = img.get_rect(center=self.pos)		
		SCREEN.blit(img, self.rect)

	def update(self, move, autoDraw=False):
		img = self.imgs[move]
		SCREEN.blit(img, self.rect)

		if autoDraw:
			pygame.display.update()

class AngleX:
	def __init__(self):

		imgNames = [
			'AngleBG', 'AngleX']

		self.imgs      = {
				name: pygame.image.load("./img/angles/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#setting transparency
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		self.pos = [75,175]
		img = self.imgs['AngleBG']
		SCREEN.blit(img, img.get_rect(center=self.pos))
				
		label = FONT.render('Angle X: {:4.1f}º'.format(120.0), 1, (0,0,0))
		SCREEN.blit(label, (0+20, 235))
		

	def update(self, angleX, autoDraw=False):
		bg = self.imgs['AngleBG']#.copy()
		img = pygame.transform.rotate(self.imgs['AngleX'],angleX)
		SCREEN.blit(bg, bg.get_rect(center=self.pos))
		SCREEN.blit(img, img.get_rect(center=self.pos))
				
		label = FONT.render('Angle X: {:4.1f}º'.format(angleX*1.0), 1, (0,0,0))
		SCREEN.blit(label, (0+20, 235))

		if autoDraw:
			pygame.display.update()

class AngleY:
	def __init__(self):

		imgNames = [
			'AngleBG', 'AngleY']

		self.imgs      = {
				name: pygame.image.load("./img/angles/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#setting transparency
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		self.pos = [225,175]
		img = self.imgs['AngleBG']
		SCREEN.blit(img, img.get_rect(center=self.pos))
		label = FONT.render('Angle Y: {:4.1f}º'.format(0.0), 1, (0,0,0))
		SCREEN.blit(label, (150+20, 235))

	def update(self, angleY, autoDraw=False):
		bg = self.imgs['AngleBG']#.copy()
		img = pygame.transform.rotate(self.imgs['AngleY'],angleY)
		SCREEN.blit(bg, bg.get_rect(center=self.pos))
		SCREEN.blit(img, img.get_rect(center=self.pos))
		#bg.blit(img, img.get_rect(center=(bg.get_size()[0]/2,bg.get_size()[1]/2)))
		#SCREEN.blit(bg, bg.get_rect(center=self.pos))
		
		label = FONT.render('Angle Y: {:4.1f}º'.format(angleY*1.0), 1, (0,0,0))
		SCREEN.blit(label, (150+20, 235))

		if autoDraw:
			pygame.display.update()



class Light:
	def __init__(self):	
		imgNames = ['bar', 'minusBut', 'plusBut',
		]
		
		folderName = 'light'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#setting transparency
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		self.pos = [150,300]
		
		deltaBut1 = [-130,0]
		deltaBut2 = [+130,0]
		
		self.posBut1 = [self.pos[0] + deltaBut1[0], self.pos[1] + deltaBut1[1]]
		self.posBut2 = [self.pos[0] + deltaBut2[0], self.pos[1] + deltaBut2[1]]
		
		self.img = self.imgs['bar']	
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		self.imgBut1 = self.imgs['minusBut']	
		self.rectMinus = SCREEN.blit(self.imgBut1, self.imgBut1.get_rect(center=self.posBut1))
		
		self.imgBut2 = self.imgs['plusBut']	
		self.rectPlus = SCREEN.blit(self.imgBut2, self.imgBut2.get_rect(center=self.posBut2))
		
		
	def update(self, arg, autoDraw=False):
	
		barSize = 212
		yellowSize = 212*arg/100
		
		yellowBar = pygame.Rect(44,289,yellowSize, 21)
		
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		pygame.draw.rect(SCREEN, (255,255,0), yellowBar)
	
		SCREEN.blit(self.imgBut1, self.imgBut1.get_rect(center=self.posBut1))
		SCREEN.blit(self.imgBut2, self.imgBut2.get_rect(center=self.posBut2))
		
		if autoDraw:
			pygame.display.update()
			
class Temperature:
	def __init__(self):	
		imgNames = ['temp00', 'temp01', 'temp02', 'temp03', 'temp04', 'temp05', 'temp06', 'temp07', 'temp08', 'temp09', 
					'temp10', 'temp11', 'temp12'
		]
		
		folderName = 'temperature'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#setting transparency
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		self.pos = [250,350]
		self.img = self.imgs['temp00']	
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		label = FONT.render('Temperature: {} ºC'.format(0), 1, (0,0,0))
		SCREEN.blit(label, (0+20, 335))

	def update(self, arg, autoDraw=False):
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		label = FONT.render('Temperature: {:4.1f}ºC'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (0+20, 335))

		if autoDraw:
			pygame.display.update()
			
			
class Pressure:
	def __init__(self):	
		imgNames = ['bar', 'select',
		]

		folderName = 'pressure'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#setting transparency
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))		

		self.pos = [250,400]
		self.img = self.imgs['bar']	
		
		deltaSelect = [-29,-1]
		self.posSelect = [self.pos[0] + deltaSelect[0], self.pos[1] + deltaSelect[1]]
		
		self.img = self.imgs['bar']	
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		self.imgSelect = self.imgs['select']	
		SCREEN.blit(self.imgSelect, self.imgSelect.get_rect(center=self.posSelect))
		
		label = FONT.render('Pressure: {} Pa'.format(0), 1, (0,0,0))
		SCREEN.blit(label, (0+20, 385))
		
	def update(self, arg, autoDraw=False):
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		SCREEN.blit(self.imgSelect, self.imgSelect.get_rect(center=self.posSelect))
		
		if autoDraw:
			pygame.display.update()		

		label = FONT.render('Pressure: {:4.1f} Pa'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (0+20, 385))			
			
			
class Battery:
	def __init__(self):	
		imgNames = ['bat00', 'bat01', 'bat02', 'bat03', 'bat04', 'bat05', 'bat06',
		]

		folderName = 'battery'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
								
		#setting transparency
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		self.pos = [250,450]
		self.img = self.imgs['bat00']		
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		label = FONT.render('Battery:', 1, (0,0,0))
		SCREEN.blit(label, (0+20, 435))	

	def update(self, arg, autoDraw=False):
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		label = FONT.render('Battery:', 1, (0,0,0))
		SCREEN.blit(label, (0+20, 435))	

		if autoDraw:
			pygame.display.update()			
			
			
			
# class AtributeTemplate:
	# def __init__(self):	
		# imgNames = [
		# ]

		# folderName = 'battery'

		# self.imgs      = {
				# name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				# for name in imgNames
				# }

		# self.pos = [POSICAO_X,POSICAO_Y]
		# self.img = self.imgs['NOME DA IMAGEM DEFAULT']	
		# SCREEN.blit(self.img, self.img.get_rect(center=self.pos))

	# def update(self, arg, autoDraw=False):
		# SCREEN.blit(self.img, self.img.get_rect(center=self.pos))

		# if autoDraw:
			# pygame.display.update()


class GUI:
	def __init__(self):

		#definindo a surface
		pygame.display.set_caption('Robo')
		self.screen = SCREEN

		#definindo o periodo de repetição de key_down
		pygame.key.set_repeat(1)

		#definindo a fonte dos textos
		myfont = pygame.font.SysFont("arial", 15)

		#definindo a cor de fundo
		self.screen.fill([220,220,220])

		#imgNames = [
		#	'N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO', 'STOP',
		#	'angleX', 'angleY',		
		#			]
		# self.img      = {
		# 		name: pygame.image.load("./img/{}.jpeg".format(name)).convert()
		# 		for name in imgNames
		# 		}
		
		# #setting transparency
		# for name in self.img:
		# 	self.img[name].set_colorkey((255,0,255))
		
		self.move = Move()
		self.angleX = AngleX()
		self.angleY = AngleY()
		self.light = Light()
		self.temperature = Temperature()
		self.pressure = Pressure()
		self.bat = Battery()
				
		#atualizando as imagens
		pygame.display.update()

	def getKey(self): #Gets if any key is pressed and what key
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#TODO:
				#Sair do programa sem Error
				pygame.quit()
			elif event.type == pygame.KEYDOWN:
				return (True, int(event.key))
					
		return (False, 0)
			

	# def drawPressure(self, pressure, update=True):
	# 	pass
		
	# def drawTemperature(self, pressure, update=True):
	# 	pass

	# def drawBattery(self, pressure, update=True):
	# 	pass		
		
	def drawAll(self,dictParams):

		self.screen.fill([220,220,220])
		
		#Updating move:
		lastMove = dictParams['lastMove']
		self.move.update(lastMove)

		#Updating AngleX:
		angleX = dictParams['angleX']
		#print(angleX)
		self.angleX.update(angleX)
		
		#Updating AngleY:
		angleY = dictParams['angleY']
		self.angleY.update(angleY)
		
		#Update Light:
		self.light.update(25)
		
		#Update Temperature:
		temp = dictParams['temperature']
		self.temperature.update(temp)
		
		#Update Pressure:
		press = dictParams['pressure']
		self.pressure.update(press)
		
		#Update Battery:
		self.bat.update(0)
		
		pygame.display.update()

		#input()

		
if __name__ == "__main__":
	g = GUI()
	while True:
		g.drawAll({
				'lastMove': 'N',
				'angleX': 30,
				'angleY': 45,
				})
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#TODO:
				#Sair do programa sem Error
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				print(pos)
                ## check if cursor is on button ##
				if g.light.rectMinus.collidepoint(pos):
					print("You asked to reduce light")
				if g.light.rectPlus.collidepoint(pos):
					print("You asked to increase light")