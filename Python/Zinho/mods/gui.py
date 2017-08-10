import pygame
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

from .utils import keysBool2key

pygame.init()

pygame.display.set_caption('Zinho')

#Initialize Surface
SCREEN = pygame.display.set_mode((300,680))

# Initialize font
FONT = pygame.font.SysFont("monospace", 15)

##################

class StartSprites(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		
		route = Route([150, 250])
		connect = ConnectButton([150,400])
		help = HelpButton([150,475])
		advanced = AdvancedButton([150,550])
	
		self.add(
			Title([150,80]),
			Message([150, 225]),
			route,
			connect,
			help,
			advanced
		)
		
		self.buttons = {
			'connect': connect.rect,
			'routeSwitch' : route.rect,
			'help': help.rect,
			'advanced': advanced.rect,
			
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
		label = font.render('Zinho 2.0', 1, (0,0,0))
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
		
class Route(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'yes', 'no']

		folderName = 'start'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}			
		
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['no']
		self.rect = img.get_rect(center=[self.pos[0], self.pos[1]+65])
		
	def update(self, params):
	
		arg = params['id']
		arg2 = params['newRoute']

		#GET AND BLIT TEXT
		text = [
			"Percurso Atual: " + str(arg+arg2),
			'',
			'Novo Percurso:',			
			]
		
		font = pygame.font.SysFont("monospace", 16)
		
		for i in range(len(text)):
			label = font.render(text[i], 1, (0,0,0))
			SCREEN.blit(label, label.get_rect(center=[self.pos[0], self.pos[1] +i*17]))	 
		
		
		#GET AND BLIT IMG
		if arg2:
			img = self.imgs['yes']
		else:
			img = self.imgs['no']
		SCREEN.blit(img, self.rect)
		
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
			
class HelpButton(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'Help']

		folderName = 'start'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['Help']
		self.rect = img.get_rect(center=[self.pos[0], self.pos[1]])
		
		
		
	def update(self, _):
		
		#GET AND BLIT IMG
		img = self.imgs['Help']
		SCREEN.blit(img, img.get_rect(center=[self.pos[0], self.pos[1]]))
		
class AdvancedButton(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'Advanced']

		folderName = 'start'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
				
		
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['Advanced']
		self.rect = img.get_rect(center=[self.pos[0], self.pos[1]])
		
		
		
	def update(self, _):
		
		#GET AND BLIT IMG
		img = self.imgs['Advanced']
		SCREEN.blit(img, img.get_rect(center=[self.pos[0], self.pos[1]]))
		
#########################
		
class ConnectedSprites (pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
			
		#light = Light([5,275])
		flag = Flag([85,50])
		plot = Plot([10,460])
			
		self.add(
		Ping([0,0]),
		Id([300,0]),
		Move([25,50]),
		XYZ([170,35]),
		AngleA([15,115]),
		AngleB([165,115]),
		Temperature([20,260]),
		Pressure([250,305]),
		BatteryV([250,340]),
		BatteryA([250,375]),
		Distance([250,405]),
		Velocity([250,445]),
		flag,
		plot,
		)
		
		self.buttons = {
		#	'lightMinus': light.rectMinus,
		#	'lightPlus': light.rectPlus,
		'flag' : flag.rect,
		'zPlus': plot.rectZPlus,
		'zMinus': plot.rectZMinus,
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
	
class Id(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		self.pos = pos
		
	def update(self, params):
		arg = params['id']
		#GET AND BLIT TEXT	
		label = FONT.render('Id: {} '.format(arg), 1, (0,0,0))
		SCREEN.blit(label, label.get_rect(topright=self.pos))		
	
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
	
class XYZ(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SET POSITION
		self.pos = pos
		
	def update(self, params):
	
		x = params['x0']
		y = params['y0']
		z = params['z0']
			
		#GET AND BLIT TEXT
		text = [
			'X: {:6.2f} m'.format(x),
			'Y: {:6.2f} m'.format(y),
			'Z: {:6.2f} m'.format(z),
			]
		for i in range(len(text)):
			label = FONT.render(text[i], 1, (0,0,0))
			SCREEN.blit(label, (self.pos[0], self.pos[1]+i*17))	 
				
class AngleA(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleA']

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
	
		arg = params['angleA']
	
		#GET AND BLIT BACKGROUND
		bg = self.imgs['AngleBG']
		SCREEN.blit(bg, bg.get_rect(topleft=self.pos))
		
		#GET AND BLIT ROTATED IMAGE
		img = pygame.transform.rotate(self.imgs['AngleA'],arg)
		SCREEN.blit(img, img.get_rect(center=[self.pos[0]+60,self.pos[1]+60]))
		
		#GET AND BLIT TEXT
		label = FONT.render('Angulo A: {:4.1f}º'.format(arg*1.0), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0], self.pos[1]+120))
				
class AngleB(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)

		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleB']

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
	
		arg = params['angleB']
		
		#GET AND BLIT BACKGROUND
		bg = self.imgs['AngleBG']
		SCREEN.blit(bg, bg.get_rect(topleft=self.pos))
		
		#GET AND BLIT ROTATED IMAGE
		img = pygame.transform.rotate(self.imgs['AngleB'],arg)
		SCREEN.blit(img, img.get_rect(center=[self.pos[0]+60,self.pos[1]+60]))
		
		#GET AND BLIT TEXT
		label = FONT.render('Angulo B: {:4.1f}º'.format(arg*1.0), 1, (0,0,0))
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
			label = FONT.render('Temperatura: ??.? ºC', 1, (0,0,0))
		else:
			label = FONT.render('Temperatura: {:4.1f} ºC'.format(arg), 1, (0,0,0))
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
			label = FONT.render('Pressão:  ?????.? Pa'.format(arg), 1, (0,0,0))
		else:
			label = FONT.render('Pressão:  {:5.1f} Pa'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
class BatteryV(pygame.sprite.Sprite):
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
		
		#SET AND BLIT DEFAULT IMAGE
		img = self.imgs['bat-1']		
		#SCREEN.blit(img, img.get_rect(center=self.pos))
		
	def update(self, params):
	
		arg = params['batteryV']
	
		#CHOOSING IMAGE:
		Bmin = 0
		Bmax = 100
		numImgs = len(self.imgs)-1
		
		if arg == -1:
			img = self.imgs['bat-1']
		elif arg <= Bmin:
			img = self.imgs['bat00']
		elif arg < Bmax:
			img = self.imgs['bat{:02}'.format(int((arg-Bmin)*numImgs/(Bmax-Bmin)))]
		else:
			img = self.imgs['bat{:02}'.format(numImgs-1)]
		
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
		#GET AND BLIT TEXT
		if arg == -1:
			label = FONT.render('Bateria:     ??.? %', 1, (0,0,0))
		else:
			#label = FONT.render('Bateria: {:3.0f}%'.format(arg), 1, (0,0,0))
			label = FONT.render('Bateria:   {:5.3f} V'.format(arg), 1, (0,0,0))
		
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))

class BatteryA(pygame.sprite.Sprite):
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
		
		#SET AND BLIT DEFAULT IMAGE
		img = self.imgs['bat-1']		
		#SCREEN.blit(img, img.get_rect(center=self.pos))
		
	def update(self, params):
	
		arg = params['batteryA']
	
		#CHOOSING IMAGE:
		Bmin = 0
		Bmax = 100
		numImgs = len(self.imgs)-1
		
		if arg == -1:
			img = self.imgs['bat-1']
		elif arg <= Bmin:
			img = self.imgs['bat00']
		elif arg < Bmax:
			img = self.imgs['bat{:02}'.format(int((arg-Bmin)*numImgs/(Bmax-Bmin)))]
		else:
			img = self.imgs['bat{:02}'.format(numImgs-1)]
		
		SCREEN.blit(img, img.get_rect(center=self.pos))
		
		#GET AND BLIT TEXT
		if arg == -1:
			label = FONT.render('Bateria:     ??.? %', 1, (0,0,0))
		else:
			#label = FONT.render('Bateria: {:3.0f}%'.format(arg), 1, (0,0,0))
			label = FONT.render('Bateria:   {:5.3f} V'.format(arg), 1, (0,0,0))
		
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
												
class Distance(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		#SET POSITION
		self.pos = pos
		
	def update(self, params):
	
		arg = params['distance']
	
		#GET AND BLIT TEXT
		label = FONT.render('Distância:   {:5.3f} m'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))
		
class Velocity(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		#SET IMAGES
		#TODO

		#SET POSITION
		self.pos = pos
		
	def update(self, params):
	
		arg = params['velocity']
	
		#GET AND BLIT TEXT
		label = FONT.render('Velocidade:  {:5.3f} m/s'.format(arg), 1, (0,0,0))
		SCREEN.blit(label, (self.pos[0]-230, self.pos[1]-15))				
	
class Flag(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		#SET IMAGES
		
		imgNames = ['flag']

		folderName = 'flag'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}
								
		#SET POSITION
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['flag']
		self.rect = img.get_rect(topleft=self.pos)
		
	def update(self, params):
	
		#GET AND BLIT IMG
		img = self.imgs['flag']
		SCREEN.blit(img, img.get_rect(topleft=self.pos))		
		
class Plot(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		self.zoom = 10

		#SET IMAGES
		
		imgNames = ['zoomPlus', 'zoomMinus']

		folderName = 'plot'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}		
	
		#SET POSITION
		self.pos = pos
		self.posZPlus = [pos[0]+36, pos[1]+25]
		self.posZMinus = [pos[0]+36, pos[1]+45] 
		
		#SET RECT TO USE AS BUTTON
		imgZPlus = self.imgs['zoomPlus']
		self.rectZPlus = imgZPlus.get_rect(topleft=self.posZPlus)
		
		imgZMinus = self.imgs['zoomMinus']
		self.rectZMinus = imgZMinus.get_rect(topleft=self.posZMinus)
		
		self.surface = None
		
		self.first = True
				
	def getSurface(self, zoom, arg1, arg2, arg3):
		
		fig = pylab.figure(figsize=[2.8, 2], # Inches
						   dpi=100,        	   # 100 dots per inch, so the resulting buffer is 400x400 pixels
						   )
		ax = fig.gca()
		
		lastX = arg1[-1]
		lastY = arg2[-1]
		
		ax.axis([-zoom+arg1[-1], zoom+arg1[-1], -zoom/1.4+arg2[-1], zoom/1.4+arg2[-1]])
		#print(arg1,arg2,arg3)
		ax.plot(arg1,arg2)
		i = len(arg3)-1
		
		while arg3[i] == "":
			i -= 1
		
		if arg3[i] == "init":
			ax.plot(arg1[i],arg2[i],'go')
		if arg3[i] == "flag":
			ax.plot(arg1[i],arg2[i],'ro')
	

		canvas = agg.FigureCanvasAgg(fig)
		canvas.draw()
		renderer = canvas.get_renderer()
		raw_data = renderer.tostring_rgb()

		size = canvas.get_width_height()

		#Create pygame surface from string
		surf = pygame.image.fromstring(raw_data, size, "RGB")
		
		pylab.close(fig)
		
		#SET TRANSPARENCY TO IMAGES
		surf.set_colorkey((255,255,255))
	
		return surf
		
	
	def update(self, params):
	
		arg = params['perc']
		zoom = params['zoom']
		
		arg1, arg2, arg3 = list(zip(*arg))
		
		if self.first:
			self.first = False
			self.lastX = arg1[-1]
			self.lastY = arg2[-1]
			self.surface = self.getSurface(zoom, arg1,arg2,arg3)
		
		lastX = arg1[-1]
		lastY = arg2[-1]
			
		#print('LASTXY:                  ', lastX, lastY)
		
		if not(lastX == self.lastX and lastY == self.lastY):
			self.lastX = lastX
			self.lastY = lastY
			
			self.surface = self.getSurface(zoom, arg1,arg2,arg3)
	
		SCREEN.blit(self.surface, self.pos)
		SCREEN.blit(self.imgs['zoomPlus'], self.posZPlus)
		SCREEN.blit(self.imgs['zoomMinus'], self.posZMinus)
		
		self.lastX = lastX
		self.lastY = lastY
		
#######################
	
class HelpSprites(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		
		self.add(
		MoveHelp([15,15]),
		EscapeHelp([15,130]),
		TextHelp([15,170]),
		)
			
class MoveHelp(pygame.sprite.Sprite):
	
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		self.pos = pos

	def update(self, params):
		#GET AND BLIT TEXT
		text = [
			'Para mover, use as teclas:',
			'',
			'          Q W E',
			'          A S D',
			'          Z X C',
			]
		for i in range(len(text)):
			label = FONT.render(text[i], 1, (0,0,0))
			SCREEN.blit(label, (self.pos[0], self.pos[1]+i*17))	

class EscapeHelp(pygame.sprite.Sprite):		

	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		self.pos = pos

	def update(self, params):
		#GET AND BLIT TEXT
		text = [
			'Para voltar, aperte ESC',
			]
		for i in range(len(text)):
			label = FONT.render(text[i], 1, (0,0,0))
			SCREEN.blit(label, (self.pos[0], self.pos[1]+i*17))	 

class TextHelp(pygame.sprite.Sprite):		

	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)	
		
		self.pos = pos
		
		#SETTING IMAGES
		imgNames = [
			'AngleBG', 'AngleA']

		folderName = 'angles'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}

		#SETTING TRANSPARENCY TO IMAGES
		for name in self.imgs:
			self.imgs[name].set_colorkey((255,0,255))

	def update(self, params):
	
		#GET AND BLIT TEXT
		text = [
			'Você deve monitorar o Zinho',
			'e garantir condições seguras!',
			'',			
			'Você tem acesso a:',
			' - Temperatura', 
			' - Pressao',
			' - Inclinação',
			' - Tensão da Bateria',
			' - Velocidade aproximada',
			' - Distancia percorrida ',
			'',
			'',
			'Em relação a posição inicial, ',
			'XYZ representam respectivamente:',
			' - esquerda (-) ~ direita (+) ',
			' - trás     (-) ~ frente  (+) ',
			' - baixo    (-) ~ cima    (+) ',
			
			]
		for i in range(len(text)):
			label = FONT.render(text[i], 1, (0,0,0))
			SCREEN.blit(label, (self.pos[0], self.pos[1]+i*17))	 
	
########################	
class AdvancedSprites(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		
		clearRoutes = ClearRoutes([150,625])
		
		self.add(
		clearRoutes,
		)
		
		self.buttons = {
			'clear': clearRoutes.rect,
		}
					
class ClearRoutes(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		
		#SETTING IMAGES
		imgNames = [
			'Clear']

		folderName = 'advanced'

		self.imgs      = {
				name: pygame.image.load("./img/"+folderName+"/{}.jpeg".format(name)).convert()
				for name in imgNames
				}			
		
		self.pos = pos
		
		#SET RECT TO USE AS BUTTON
		img = self.imgs['Clear']
		self.rect = img.get_rect(center=[self.pos[0], self.pos[1]])
		
	def update(self, params):
		SCREEN.blit(self.imgs['Clear'], self.rect)			
		
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
		self.helpSprites = HelpSprites()
		self.advancedSprites = AdvancedSprites()
				
		#atualizando as imagens
		pygame.display.update()

	def getAction(self, tela): #Gets if any key is pressed and what key
			
		clickedButton = None 
		flag = None
		
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				flag = 'quit'
				
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
			
			elif tela == "Help":
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					for button in self.connectedSprites.buttons:
						if self.connectedSprites.buttons[button].collidepoint(pos):
							clickedButton = button	

			elif tela == "Advanced":
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					for button in self.advancedSprites.buttons:
						if self.advancedSprites.buttons[button].collidepoint(pos):
							clickedButton = button									

		key = keysBool2key(pygame.key.get_pressed())		
		return (key, clickedButton, flag)								
		
	def update(self, tela, params={}):
			
		#print(params)
		
		if tela == "Start":
			self.screen.fill([220,220,220])
			self.startSprites.update(params)
			pygame.display.update()
		
		elif tela == "Connected":
			self.screen.fill([220,220,220])
			self.connectedSprites.update(params)
			pygame.display.update()
			
		elif tela == "Help":
			self.screen.fill([220,220,220])
			self.helpSprites.update(params)
			pygame.display.update()

		elif tela == "Advanced":
			self.screen.fill([220,220,220])
			self.advancedSprites.update(params)
			pygame.display.update()
