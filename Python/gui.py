import pygame

pygame.init()

pygame.display.set_caption('Robo')

SCREEN = pygame.display.set_mode((300,600))

class Move:
	def __init__(self):

		imgNames = [
			'N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO', 'STOP']

		self.imgs      = {
				name: pygame.image.load("./img/moves/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		self.pos = [75,75]
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

		self.pos = [75,200]
		img = self.imgs['AngleBG']
		self.rect = img.get_rect(center=self.pos)		

		SCREEN.blit(img, self.rect)

	def update(self, angleX, autoDraw=False):
		bg = self.imgs['AngleBG']#.copy()
		img = pygame.transform.rotate(self.imgs['AngleX'],angleX)
		SCREEN.blit(bg, bg.get_rect(center=self.pos))
		SCREEN.blit(img, img.get_rect(center=self.pos))
		#bg.blit(img, img.get_rect(center=(bg.get_size()[0]/2,bg.get_size()[1]/2)))
		#SCREEN.blit(bg, bg.get_rect(center=self.pos))

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

		self.pos = [225,200]
		img = self.imgs['AngleBG']
		self.rect = img.get_rect(center=self.pos)		

		SCREEN.blit(img, self.rect)

	def update(self, angleY, autoDraw=False):
		bg = self.imgs['AngleBG']#.copy()
		img = pygame.transform.rotate(self.imgs['AngleY'],angleY)
		SCREEN.blit(bg, bg.get_rect(center=self.pos))
		SCREEN.blit(img, img.get_rect(center=self.pos))
		#bg.blit(img, img.get_rect(center=(bg.get_size()[0]/2,bg.get_size()[1]/2)))
		#SCREEN.blit(bg, bg.get_rect(center=self.pos))

		if autoDraw:
			pygame.display.update()


class Temperature:
	def __init__(self):	
		imgNames = [
		]

		self.imgs      = {
				name: pygame.image.load("./img/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		self.pos = [POSICAO_X,POSICAO_Y]
		self.img = self.imgs['NOME DA IMAGEM DEFAULT']
		self.rect = self.img.get_rect(center=self.pos)		
		SCREEN.blit(self.img, self.rect)

		def update(self, arg, autoDraw=False):
			self.img = pygame.transform.rotate(self.imgs['AngleX'],0)
			SCREEN.blit(self.img, self.rect)

		if autoDraw:
			pygame.display.update()


class AtributeTemplate:
	def __init__(self):	
		imgNames = [
		]

		self.imgs      = {
				name: pygame.image.load("./img/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		self.pos = [POSICAO_X,POSICAO_Y]
		self.img = self.imgs['NOME DA IMAGEM DEFAULT']
		self.rect = self.img.get_rect(center=self.pos)		
		SCREEN.blit(self.img, self.rect)

		def update(self, arg, autoDraw=False):
			self.img = pygame.transform.rotate(self.imgs['AngleX'],0)
			SCREEN.blit(self.img, self.rect)

		if autoDraw:
			pygame.display.update()




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

		#Updating move:
		angleX = dictParams['angleX']
		#print(angleX)
		self.angleX.update(angleX)
		
		#Updating move:
		angleY = dictParams['angleY']
		self.angleY.update(angleY)

		pygame.display.update()


		
if __name__ == "__main__":
	g = GUI()
	while True:
		g.drawAll({
				'lastMove': 'N',
				'angleX': 30,
				'angleY': 45,
				})
		for event in pygame.event.get():
			pass