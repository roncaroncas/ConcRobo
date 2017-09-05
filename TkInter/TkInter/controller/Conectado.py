from PIL import Image, ImageTk
import tkinter as tk

class ConectadoController:
	def __init__(self, client):
		self.client = client
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		frame = self.client.gui.frames[self.name]
		frame.focus_set()
		frame.tkraise()
		
	def key(self, event):

		KeysToMove = {
		'q':'UP_LEFT',
		'w':'UP',
		'e':'UP_RIGHT',
		'a':'LEFT',
		's':'STOP',
		'd':'RIGHT',
		'z':'DOWN_LEFT',
		'x':'DOWN',
		'c':'DOWN_RIGHT',
		}

		if event.char in (list(KeysToMove.keys())):
			#print("pressed", KeysToMove[event.char])
			self.client.models['User']['move'] = KeysToMove[event.char]
		else:
			print ("pressed", repr(event.char))
			pass


	def keyRelease(self, event):
		self.client.models['User']['move'] = 'STOP'
		#print ("unpressed", repr(event.char))

	def mouse(self, event):
		#print ("clicked at", event.x, event.y)
		self.client.gui.frames[self.name].focus_set()


	def b_Voltar(self):
		self.client.gui.show_frame("Menu")
		self.client.conex.disconnect()
		self.client.models['Route'].close()

	def b_Warn(self):

		user = self.client.models['User']
		frame = self.client.gui.frames[self.name]

		flag = frame.varEn_warn.get()

		if flag != "":
			user['flag'] = frame.varEn_warn.get()
			frame.varEn_warn.delete(0, tk.END)
			frame.var_lastWarn.set(user['flag'])
		
		self.client.gui.frames[self.name].focus_set()
		#print(user['flag'])

	def refresh(self, models):


		######### CONFIG DE MIN E MAX DAS IMAGENS ######
		minTemp = 20
		maxTemp = 30

		minPres =  80000
		maxPres = 150000

		minBatV = 10
		maxBatV = 13.5

		minBatA = 0
		maxBatA = 10

		#################################################


		zinho = models['Zinho']
		user = models['User']

		frame = self.client.gui.frames[self.name]
		
		# w, h = frame.winfo_width(), frame.winfo_height()
		# print(w,h)

		#print(frame.var_id.get() != "ID " + str(user['id']))

		#Atualiza ID/NOME
		if frame.var_id.get() != "ID {}\n{}".format(user['id'], user['name']):
			frame.var_id.set("ID {}\n{}".format(user['id'], user['name']))

		#Atualiza Ping
		
		if frame.var_ping.get() != "Ping: " + str(zinho['ping']):
			frame.var_ping.set("Ping: " + str(zinho['ping']))

		#Atualiza Move
		frame.varIm_move = ImageTk.PhotoImage(frame.images['moves'][zinho['lastMove']])
		frame.varLb_move.configure(image=frame.varIm_move)

		#Atualiza X, Y e Z
		if frame.var_x.get() != "{:.1f} m ".format(zinho['x']):
			frame.var_x.set("{:.1f} m ".format(zinho['x']))
		if frame.var_y.get() != "{:.1f} m ".format(zinho['y']):
			frame.var_y.set("{:.1f} m ".format(zinho['y']))
		if frame.var_z.get() != "{:.1f} m ".format(zinho['z']):
			frame.var_z.set("{:.1f} m ".format(zinho['z']))

		#Atualiza Angle A e B
		bg = frame.images['angles']['angleBG']

		if frame.var_angleA.get() != "{:04.1f}°".format(zinho['angleA']):
			frame.var_angleA.set("{:04.1f}°".format(zinho['angleA']))
			angleA = frame.images['angles']['angleA'].rotate(zinho['angleA'])
			frame.varIm_angleA = ImageTk.PhotoImage(Image.alpha_composite(bg, angleA))
			frame.varLb_angleA.configure(image=frame.varIm_angleA)

		if frame.var_angleB.get() != "{:04.1f}°".format(zinho['angleB']):		
			frame.var_angleB.set("{:04.1f}°".format(zinho['angleB']))
			angleB = frame.images['angles']['angleB'].rotate(zinho['angleB'])
			frame.varIm_angleB = ImageTk.PhotoImage(Image.alpha_composite(bg, angleB))
			frame.varLb_angleB.configure(image=frame.varIm_angleB)

		#Atualiza Temp
		
		self._tempImgNum = -1

		minVal = minTemp
		maxVal = maxTemp

		images = frame.images['temperature']
		numImgs = len(images)

		value = int(zinho['temperature'])

		if value == -1:
			ind = -1
		elif value <= minVal:
			ind = 0
		elif value <= maxVal:
			ind = int((value-minVal)*numImgs/(maxVal-minVal))
		else:
			ind = numImgs - 2
		
		if self._tempImgNum != ind:
			self._tempImgNum = ind
			frame.varIm_temp = ImageTk.PhotoImage(images['temp{:02}'.format(ind)])
			frame.varLb_temp.configure(image=frame.varIm_temp)
		
		frame.var_temp.set("{:.1f}  ºC ".format(value))



		#Atualiza Pressao
		self._presImgNum = -1

		minVal = minPres
		maxVal = maxPres

		images = frame.images['pressure']
		numImgs = len(images)

		value = int(zinho['pressure'])

		if value == -1:
			ind = -1
		elif value <= minVal:
			ind = 0
		elif value <= maxVal:
			ind = int((value-minVal)*numImgs/(maxVal-minVal))
		else:
			ind = numImgs - 2
		
		if self._presImgNum != ind:
			self._presImgNum = ind
			frame.varIm_pres = ImageTk.PhotoImage(images['bar{:02}'.format(ind)])
			frame.varLb_pres.configure(image=frame.varIm_pres)

		frame.var_pres.set("{:.1f}  Pa ".format(zinho['pressure']))



		#Atualiza BatV
		
		self._batVImgNum = -1

		minVal = minBatV
		maxVal = maxBatV

		images = frame.images['battery']
		numImgs = len(images)

		value = int(zinho['batteryV'])

		if value == -1:
			ind = -1
		elif value <= minVal:
			ind = 0
		elif value <= maxVal:
			ind = int((value-minVal)*numImgs/(maxVal-minVal))
		else:
			ind = numImgs - 2
		
		if self._batVImgNum != ind:
			self._batVImgNum = ind
			frame.varIm_batV = ImageTk.PhotoImage(images['bat{:02}'.format(ind)])
			frame.varLb_batV.configure(image=frame.varIm_batV)
		
		frame.var_batV.set("{:.1f}   V ".format(zinho['batteryV']))



		#Atualiza BatA
		
		self._batAImgNum = -1

		minVal = minBatA
		maxVal = maxBatA

		images = frame.images['battery']
		numImgs = len(images)

		value = int(zinho['batteryA'])

		if value == -1:
			ind = -1
		elif value <= minVal:
			ind = 0
		elif value <= maxVal:
			ind = int((value-minVal)*numImgs/(maxVal-minVal))
		else:
			ind = numImgs - 2
		
		if self._batAImgNum != ind:
			self._batAImgNum = ind
			frame.varIm_batA = ImageTk.PhotoImage(images['bat{:02}'.format(ind)])
			frame.varLb_batA.configure(image=frame.varIm_batA)
		
		frame.var_batA.set("{:.1f}   A ".format(zinho['batteryA']))



		#Atualiza Dist
		frame.var_dist.set("{:.3f}   m ".format(zinho['distance']))


		#Atualiza Vel
		frame.var_vel.set("{:.3f} m/s ".format(zinho['velocity']))