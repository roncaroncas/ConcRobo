import pygame

pygame.init()

pygame.display.set_caption('Robo')

#Initialize Surface
SCREEN = pygame.display.set_mode((300,600))

# Initialize font
FONT = pygame.font.SysFont("monospace", 15)

##################

class StartSprites(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		
		connect = ConnectButton([150,400])
		options = OptionButton([150,475])
	
		self.add(
			Title([150,80]),
			Message([150, 225]),
			connect,
			options,
		)
		
		self.buttons = {
			'connect': connect.rect,
			'options': options.rect,
		}
			
class Title(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'title']

		folderName = 'start'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		#SETTING TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))
		
		#SET POSITION
		self.pos = pos
		
		
	def update(self, _):
	
		#GET AND BLIT CONCREMAT
		font = pygame.font.SysFont("monospace", 30)
		label = font.render('Concremat', 1, (0,0,0))
		SCREEN.blit(label, label.get_rect(center=[self.pos[0], self.pos[1]]))
	
		#GET AND BLIT LOGO
		img = self.imgs['title']
		SCREEN.blit(img, img.get_rect(center=[self.pos[0], self.pos[1]+50]))
		
		#GET AND BLIT CONCREMAT
		font = pygame.font.SysFont("monospace", 22)
		label = font.render('Robo', 1, (0,0,0))
		SCREEN.blit(label, label.get_rect(center=[self.pos[0], self.pos[1]+100]))
			
class Message(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.pos = pos
		
	def update(self, params):
	
		arg = params['message']
	
		#GET AND BLIT MESSAGE
		font = pygame.font.SysFont("monospace", 16)
		label = font.render(arg, 1, (255,0,0))
		SCREEN.blit(label, label.get_rect(center=[self.pos[0], self.pos[1]]))
		
		pass
		
class ConnectButton(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'Connect']

		folderName = 'start'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['Connect']
		self.rect = img.get_rect(center=[self.pos[0], self.pos[1]])
		
		
	def update(self, _):
		
		#GET AND BLIT IMG
		img = self.imgs['Connect']
		SCREEN.blit(img, img.get_rect(center=[self.pos[0], self.pos[1]]))
		
class OptionButton(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'Options']

		folderName = 'start'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['Options']
		self.rect = img.get_rect(center=[self.pos[0], self.pos[1]])
		
		
		
	def update(self, _):
		
		#GET AND BLIT IMG
		img = self.imgs['Options']
		SCREEN.blit(img, img.get_rect(center=[self.pos[0], self.pos[1]]))
		
			
#########################
		
class ConnectedSprites (pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
			
		light = Light([5,275])
			
		self.add(
		Ping([0,0]),
		Move([55,45]),
		AngleX([15,115]),
		AngleY([165,115]),
		light,
		Temperature([20,335]),
		Pressure([250,400]),
		Battery([250,450]),
		Distance([250,500]),
		Velocity([250,550]),
		)
		
		self.buttons = {
			'lightMinus': light.rectMinus,
			'lightPlus': light.rectPlus,
		}
			
class Ping(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SET POSITION
		self.pos = pos
		self.i = 0
		self.sum = 0
		self.ping = 0
		
	def update(self, params):
	
		arg = params['ping']
	
		#Reduzir a velocidade de print
		self.sum += arg
		self.i += 1
		if self.i == 5:
			self.ping = self.sum/10
			self.sum = 0
			self.i = 0
		
		#GET AND BLIT TEXT	
		label = FONT.render('Ping: {:4.1f} ms'.format(self.ping), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0], self.pos[1]))	
	
class Move(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		#SETTING IMAGES
		imgNames = [
			'N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO', 'STOP']

		folderName = 'moves'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
		
		#SETTING POSITION
		self.pos = pos
		
		#GET AND BLIT DEFAULT IMAGE
		img = self.imgs['STOP']
		#SCREEN.blit(img, img.get_rect(topleft=self.pos))

	def update(self, params):
	
		arg = params['lastMove']
		
		#UPDATE AND BLIT IMAGE
		img = self.imgs[arg]
		SCREEN.blit(img, img.get_rect(topleft=self.pos))

class AngleX(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleX']

		folderName = 'angles'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#SETTING TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SETTING POSITION
		self.pos = pos
		
		#GET AND BLIT DEFAULT IMAGE
		img = self.imgs['AngleBG']
		#SCREEN.blit(img, img.get_rect(topleft=self.pos))
		

	def update(self, params):
	
		arg = params['angleX']
	
		#GET AND BLIT BACKGROUND
		bg = self.imgs['AngleBG']
		SCREEN.blit(bg, bg.get_rect(topleft=self.pos))
		
		#GET AND BLIT ROTATED IMAGE
		img = pygame.transform.rotate(self.imgs['AngleX'],arg)
		SCREEN.blit(img, img.get_rect(center=[self.pos[0]+60,self.pos[1]+60]))
		
		#GET AND BLIT TEXT
		label = FONT.render('Angle X: {:4.1f}º'.format(arg*1.0), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0], self.pos[1]+120))
				
class AngleY(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleY']

		folderName = 'angles'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#SETTING TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

		#SET POSITION
		self.pos = pos
		
		#GET AND BLIT DEFAULT IMAGE
		img = self.imgs['AngleBG']
		#SCREEN.blit(img, img.get_rect(topleft=self.pos))
	

	def update(self, params):
	
		arg = params['angleY']
		
		#GET AND BLIT BACKGROUND
		bg = self.imgs['AngleBG']
		SCREEN.blit(bg, bg.get_rect(topleft=self.pos))
		
		#GET AND BLIT ROTATED IMAGE
		img = pygame.transform.rotate(self.imgs['AngleY'],arg)
		SCREEN.blit(img, img.get_rect(center=[self.pos[0]+60,self.pos[1]+60]))
		
		#GET AND BLIT TEXT
		label = FONT.render('Angle Y: {:4.1f}º'.format(arg*1.0), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0], self.pos[1]+120))

class Light(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
	
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
		self.posBut1 = [pos[0], 	pos[1]]
		self.posBar  = [pos[0]+36, 	pos[1]]
		self.posBut2 = [pos[0]+260, pos[1]]
		
		
		#GET AND BLIT BAR IMAGE
		self.imgBar = self.imgs['bar']	
		#SCREEN.blit(self.imgBar, self.imgBar.get_rect(topleft=self.posBar))
		
		#GET AND BLIT MINUS BUTTON (stores rect)
		self.imgBut1 = self.imgs['minusBut']	
		self.rectMinus = self.imgBut1.get_rect(topleft=self.posBut1)
		
		#GET AND BLIT PLUS BUTTON (stores rect)
		self.imgBut2 = self.imgs['plusBut']	
		self.rectPlus = self.imgBut2.get_rect(topleft=self.posBut2)
		
		
	def update(self, params):
	
		arg = params['light']
	
		#BLIT BAR IMAGE
		SCREEN.blit(self.imgBar, self.imgBar.get_rect(topleft=self.posBar))
		
		#GETS YELLOW BAR WIDTH
		barWidth = 210
		yellowWidth = barWidth*arg/100
		
		#GETS AND BLIT YELLOW RECT
		yellowBar = pygame.Rect(self.posBar[0]+5,self.posBar[1]+5,yellowWidth, 21)
		pygame.draw.rect(SCREEN, (255,255,0), yellowBar)
	
		#BLIT MINUS AND PLUS BUTTONS
		SCREEN.blit(self.imgBut1, self.imgBut1.get_rect(topleft=self.posBut1))
		SCREEN.blit(self.imgBut2, self.imgBut2.get_rect(topleft=self.posBut2))
			
class Temperature(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		#GET IMAGES
		imgNames = ['temp-1', 'temp00', 'temp01', 'temp02', 'temp03', 'temp04', 'temp05',
					'temp06', 'temp07', 'temp08', 'temp09', 'temp10', 'temp11', 'temp12'
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
		img = self.imgs['temp-1']	
		#SCREEN.blit(img, img.get_rect(center=[self.pos[0]+230,self.pos[1]+15]))

	def update(self, params):
	
		arg = params['temperature']

		#CHOOSING IMAGE:
		Tmin = 10
		Tmax = 50
		numImgs = len(self.imgs)
		
		#SET AND BLIT IMAGE
		if arg == -1:
			img = self.imgs['temp-1']
		elif arg <= Tmin:
			img = self.imgs['temp00']
		elif arg <= Tmax:
			img = self.imgs['temp{:02}'.format(int((arg-Tmin)*numImgs/(Tmax-Tmin)))]
		else:
			img = self.imgs['temp{:02}'.format(numImgs-2)]
		
		SCREEN.blit(img, img.get_rect(center=[self.pos[0]+230,self.pos[1]+15]))
		
		#GET AND BLIT TEXT
		if arg == -1:
			label = FONT.render('Temperature:   ??.?ºC', 1, (0,0,0))
		else:
			label = FONT.render('Temperature: {:4.1f}ºC'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, self.pos)
			
class Pressure(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
	
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
		#SCREEN.blit(self.img, self.img.get_rect(center=self.pos))
		
		#SET SELECTOR (DONT BLIT)
		self.imgSelect = self.imgs['select']	
		
	def update(self, params):
	
		arg = params['pressure']
	
		#SELECTOR distance
		
		Pmin =  	0
		Pmax = 200000
		maxWidth = 56
		
		if arg == -1:
			dist = -1000000
		elif arg < Pmin:
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
		if arg == -1:
			label = FONT.render('Pressure: ?????.? Pa'.format(arg), 1, (0,0,0))
		else:
			label = FONT.render('Pressure: {:5.1f} Pa'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
class Battery(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		#SET IMAGES
		
		imgNames = ['bat-1', 'bat00', 'bat01', 'bat02', 'bat03', 'bat04', 'bat05', 'bat06',
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
		
		#GET AND BLIT DEFAULT TEXT
		label = FONT.render('Battery:  ??.?%', 1, (0,0,0))
		#SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
		#SET AND BLIT DEFAULT IMAGE
		img = self.imgs['bat-1']		
		#SCREEN.blit(img, img.get_rect(center=self.pos))
		
	def update(self, params):
	
		arg = params['battery']
	
		#CHOOSING IMAGE:
		Bmin = 0
		Bmax = 100
		numImgs = len(self.imgs)
		
		if arg == -1:
			img = self.imgs['bat-1']
		elif arg <= Bmin:
			img = self.imgs['bat00']
		elif arg < Bmax:
			img = self.imgs['bat{:02}'.format(int((arg-Bmin)*numImgs/(Bmax-Bmin)))]
		else:
			img = self.imgs['bat{:02}'.format(numImgs-2)]
		
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
		#GET AND BLIT TEXT
		if arg == -1:
			label = FONT.render('Battery:  ??.?%', 1, (0,0,0))
		else:
			label = FONT.render('Battery: {:3.0f}%'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
												
class Distance(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		#SET POSITION
		self.pos = pos
		
	def update(self, params):
	
		arg = params['distance']
	
		#GET AND BLIT TEXT
		label = FONT.render('Distance: {:4.1f} m'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
class Velocity(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		#SET IMAGES
		#TODO

		#SET POSITION
		self.pos = pos
		
		#SET AND BLIT DEFAULT IMAGE
		#TODO
		
	def update(self, params):
	
		arg = params['velocity']
	
		#GET AND BLIT TEXT
		label = FONT.render('Velocity: {:4.1f} m/s'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))				

class OptionSprites(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		
		self.add(
		)
		
		self.buttons = {
		}
		
class GUI:
	def __init__(self):

		#definindo a surface
		pygame.display.set_caption('Robo')
		self.screen = SCREEN

		#definindo o periodo de repetição de key_down
		pygame.key.set_repeat(1,1)
		#print(pygame.key.get_repeat())


		#definindo a fonte dos textos
		myfont = pygame.font.SysFont("arial", 15)

		#definindo a cor de fundo
		self.screen.fill([220,220,220])
		
		#Definindo tela atual (Start, Connected, Options)
		
		self.startSprites = StartSprites()
		self.connectedSprites = ConnectedSprites()
		self.optionSprites = OptionSprites()
				
		#atualizando as imagens
		pygame.display.update()

	def getAction(self, tela): #Gets if any key is pressed and what key
			
		clickedButton = ""
		
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				#TODO:
				#Sair do programa sem Error
				pygame.quit()
			
			elif tela == "Start":
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					for button in self.startSprites.buttons:
						if self.startSprites.buttons[button].collidepoint(pos):
							clickedButton = button						
			
			
			elif tela == "Connected":
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					for button in self.connectedSprites.buttons:
						if self.connectedSprites.buttons[button].collidepoint(pos):
							clickedButton = button							
			
			elif tela == "Options":
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					for button in self.connectedSprites.buttons:
						if self.connectedSprites.buttons[button].collidepoint(pos):
							clickedButton = button			

		keys = pygame.key.get_pressed()
		
		return (keys, clickedButton)								
		
	def update(self, tela, params={}):
			
		if tela == "Start":
			self.screen.fill([220,220,220])
			self.startSprites.update({'message': 'Test Message'})
			pygame.display.update()
		
		elif tela == "Connected":
			self.screen.fill([220,220,220])
			self.connectedSprites.update(params)
			pygame.display.update()
			
		elif tela == "Options":
		
			self.screen.fill([220,220,220])
			self.optionSprites.update(params)
			pygame.display.update()
			pass


