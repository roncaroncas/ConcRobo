import pygame

pygame.init()

pygame.display.set_caption('Robo')

#Initialize Surface
SCREEN = pygame.display.set_mode((300,600))

# Initialize font
FONT = pygame.font.SysFont("monospace", 15)


class Move:
	def __init__(self, pos):

		#SETTING IMAGES
		imgNames = [
			'N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO', 'STOP']

		self.imgs      = {
				name: pygame.image.load("./img/moves/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#SETTING POSITION
		self.pos = pos
		
		#GET AND BLIT DEFAULT IMAGE
		img = self.imgs['STOP']
		SCREEN.blit(img, img.get_rect(center=self.pos))

	def update(self, move):
		
		#UPDATE AND BLIT IMAGE
		img = self.imgs[move]
		SCREEN.blit(img, img.get_rect(center=self.pos))

class AngleX:
	def __init__(self, pos):

		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleX']

		self.imgs      = {
				name: pygame.image.load("./img/angles/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#SETTING TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SETTING POSITION
		self.pos = pos
		
		#GET AND BLIT DEFAULT IMAGE
		img = self.imgs['AngleBG']
		SCREEN.blit(img, img.get_rect(center=self.pos))
		

	def update(self, angleX):
	
		#GET AND BLIT BACKGROUND
		bg = self.imgs['AngleBG']
		SCREEN.blit(bg, bg.get_rect(center=self.pos))
		
		#GET AND BLIT ROTATED IMAGE
		img = pygame.transform.rotate(self.imgs['AngleX'],angleX)
		SCREEN.blit(img, img.get_rect(center=self.pos))
				
		#GET AND BLIT TEXT
		label = FONT.render('Angle X: {:4.1f}º'.format(angleX*1.0), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-55, self.pos[1]+60))

class AngleY:
	def __init__(self, pos):

		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleY']

		self.imgs      = {
				name: pygame.image.load("./img/angles/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#SETTING TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SET POSITION
		self.pos = pos
		
		#GET AND BLIT DEFAULT IMAGE
		img = self.imgs['AngleBG']
		SCREEN.blit(img, img.get_rect(center=self.pos))
	

	def update(self, angleY):
		
		#GET AND BLIT BACKGROUND
		bg = self.imgs['AngleBG']
		SCREEN.blit(bg, bg.get_rect(center=self.pos))
		
		#GET AND BLIT ROTATED IMAGE
		img = pygame.transform.rotate(self.imgs['AngleY'],angleY)
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
		#GET AND BLIT TEXT
		label = FONT.render('Angle Y: {:4.1f}º'.format(angleY*1.0), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-55, self.pos[1]+60))

class Light:
	def __init__(self, pos):
	
		#SETTING IMAGES
		imgNames = ['bar', 'minusBut', 'plusBut',
		]
		
		folderName = 'light'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#SET TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SET POSITIONS
		self.pos = pos
		deltaBut1 = [-130,0]
		deltaBut2 = [+130,0]
		
		self.posBut1 = [self.pos[0] + deltaBut1[0], self.pos[1] + deltaBut1[1]]
		self.posBut2 = [self.pos[0] + deltaBut2[0], self.pos[1] + deltaBut2[1]]
		
		#GET AND BLIT BAR IMAGE
		self.img = self.imgs['bar']	
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		#GET AND BLIT MINUS BUTTON (stores rect)
		self.imgBut1 = self.imgs['minusBut']	
		self.rectMinus = SCREEN.blit(self.imgBut1, self.imgBut1.get_rect(center=self.posBut1))
		
		#GET AND BLIT PLUS BUTTON (stores rect)
		self.imgBut2 = self.imgs['plusBut']	
		self.rectPlus = SCREEN.blit(self.imgBut2, self.imgBut2.get_rect(center=self.posBut2))

		
	def update(self, arg):
	
		#BLIT BAR IMAGE
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		#GETS YELLOW BAR WIDTH
		barWidth = 212
		yellowWidth = barWidth*arg/100
		
		#GETS AND BLIT YELLOW RECT
		yellowBar = pygame.Rect(44,289,yellowWidth, 21)
		pygame.draw.rect(SCREEN, (255,255,0), yellowBar)
	
		#BLIT MINUS AND PLUS BUTTONS
		SCREEN.blit(self.imgBut1, self.imgBut1.get_rect(center=self.posBut1))
		SCREEN.blit(self.imgBut2, self.imgBut2.get_rect(center=self.posBut2))
			
class Temperature:
	def __init__(self, pos):

		#GET IMAGES
		imgNames = ['temp00', 'temp01', 'temp02', 'temp03', 'temp04', 'temp05', 'temp06', 'temp07', 'temp08', 'temp09', 
					'temp10', 'temp11', 'temp12'
		]
		
		folderName = 'temperature'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#SET TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SET POSITION
		self.pos = pos
		
		#SET AND BLIT DEFAULT IMAGE
		img = self.imgs['temp00']	
		SCREEN.blit(img, img.get_rect(center=self.pos))

	def update(self, arg):

		#CHOOSING IMAGE:
		Tmin = 10
		Tmax = 50
		numImgs = len(self.imgs)
		
		if arg <= Tmin:
			img = self.imgs['temp00']
		elif arg <= Tmax:
			img = self.imgs['temp{:02}'.format(int((arg-Tmin)*numImgs/(Tmax-Tmin)))]
		else:
			img = self.imgs['temp{:02}'.format(numImgs-1)]
		
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
		#GET AND BLIT TEXT
		label = FONT.render('Temperature: {:4.1f}ºC'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
						
class Pressure:
	def __init__(self, pos):
	
		#SET IMAGES
		imgNames = ['bar', 'select',
		]

		folderName = 'pressure'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#SET TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))		

		#SET POSITION
		self.pos = pos
		self.posStartSelect = [self.pos[0] -29, self.pos[1] -1]
		
		#SET AND BAR IMAGE
		self.img = self.imgs['bar']	
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		#SET AND BLIT SELECTOR
		self.imgSelect = self.imgs['select']	
		SCREEN.blit(self.imgSelect, self.imgSelect.get_rect(center=self.posStartSelect))
			
	def update(self, arg):
	
		#SELECTOR distance
		
		Pmin =  	0
		Pmax = 200000
		maxWidth = 56
		
		if arg < Pmin:
			dist = 0
		elif arg < Pmax:
			dist = maxWidth*(arg-Pmin)/(Pmax-Pmin)
		else:
			dist = maxWidth
		
		selectorCenter = self.posStartSelect[:]
		selectorCenter[0] += dist		
		
		#BLIT BAR 
		SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		#BLIT SELECTOR
		SCREEN.blit(self.imgSelect, self.imgSelect.get_rect(center=selectorCenter))

		#SET AND BLIT TEXT
		label = FONT.render('Pressure: {:4.1f} Pa'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
class Battery:
	def __init__(self, pos):	
		
		#SET IMAGES
		
		imgNames = ['bat00', 'bat01', 'bat02', 'bat03', 'bat04', 'bat05', 'bat06',
		]

		folderName = 'battery'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
								
		#SET TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SET POSITION
		self.pos = pos
		
		#SET AND BLIT DEFAULT IMAGE
		img = self.imgs['bat00']		
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
	def update(self, arg):
	
		#CHOOSING IMAGE:
		Bmin = 0
		Bmax = 100
		numImgs = len(self.imgs)
		
		if arg <= Bmin:
			img = self.imgs['bat00']
		elif arg < Bmax:
			img = self.imgs['bat{:02}'.format(int((arg-Bmin)*numImgs/(Bmax-Bmin)))]
		else:
			img = self.imgs['bat{:02}'.format(numImgs-1)]
		
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
		#GET AND BLIT TEXT
		label = FONT.render('Battery: {:3d}%'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
												
class Distance:
	def __init__(self, pos):	
		
		#SET IMAGES
		#TODO

		#SET POSITION
		self.pos = pos
		
		#SET AND BLIT DEFAULT IMAGE
		#TODO
		
	def update(self, arg):
	
		#GET AND BLIT TEXT
		label = FONT.render('Distance: {:4.1f} m'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
class Velocity:
	def __init__(self, pos):	
		
		#SET IMAGES
		#TODO

		#SET POSITION
		self.pos = pos
		
		#SET AND BLIT DEFAULT IMAGE
		#TODO
		
	def update(self, arg):
	
		#GET AND BLIT TEXT
		label = FONT.render('Velocity: {:4.1f} m/s'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
				

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
		
		#Definindo os gráficos com as posições:
		self.move = Move([75,50])
		self.angleX = AngleX([75,175])
		self.angleY = AngleY([225,175])
		self.light = Light([150,300])
		self.temperature = Temperature([250,350])
		self.pressure = Pressure([250,400])
		self.bat = Battery([250,450])
		self.dist = Distance([250,500])
		self.vel = Velocity([250,550])
				
		#atualizando as imagens
		pygame.display.update()

	def getAction(self): #Gets if any key is pressed and what key
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#TODO:
				#Sair do programa sem Error
				pygame.quit()
			elif event.type == pygame.KEYDOWN:
				return (True, int(event.key))
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
                ## check if cursor is on button ##
				if self.light.rectMinus.collidepoint(pos):
					print("You asked to reduce light")
					return (True, 111)
				if self.light.rectPlus.collidepoint(pos):
					print("You asked to increase light")
					return (True, 112)
					
		return (False, 0)		
		
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
		light = dictParams['light']
		self.light.update(light)
		
		#Update Temperature:
		temp = dictParams['temperature']
		self.temperature.update(temp)
		
		#Update Pressure:
		press = dictParams['pressure']
		self.pressure.update(press)
		
		#Update Battery:
		batLvl = dictParams['battery']
		self.bat.update(batLvl)
		
		#Update Distance:
		distance = dictParams['distance']
		self.dist.update(distance)
		
		#Update Velocity:
		velocity = dictParams['velocity']
		self.vel.update(velocity)
		
		pygame.display.update()


#Desatualizado:		
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