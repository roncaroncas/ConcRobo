from PIL import Image, ImageTk
import tkinter as tk

class ConnectController:
	def __init__(self, server):
		self.server = server
		self.name = self.__class__.__name__.split("Controller")[0]
		
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
			self.server.models['User']['move'] = KeysToMove[event.char]
		else:
			print ("pressed", repr(event.char))
			pass


	def keyRelease(self, event):
		self.server.models['User']['move'] = 'STOP'
		#print ("unpressed", repr(event.char))

	def mouse(self, event):
		print ("clicked at", event.x, event.y)
		self.server.gui.frames[self.name].focus_set()


	def b_Voltar(self):
		self.server.gui.show_frame("Start")
		self.server.conex.disconnect()

	def b_Warn(self):

		user = self.server.models['User']
		frame = self.server.gui.frames[self.name]

		flag = frame.varEn_warn.get()

		if flag != "":
			user['flag'] = frame.varEn_warn.get()
			frame.varEn_warn.delete(0, tk.END)
			frame.var_lastWarn.set(user['flag'])
		
		self.server.gui.frames[self.name].focus_set()
		print(user['flag'])

	def refresh(self, models):

		zinho = models['Zinho']
		user = models['User']

		frame = self.server.gui.frames[self.name]
		
		# w, h = frame.winfo_width(), frame.winfo_height()
		# print(w,h)

		#Atualiza ID/NOME
		if frame.var_id.get() != "ID " + str(user['id']):
			frame.var_id.set("ID " + str(user['id']))

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
		frame.var_temp.set("{:.1f}  ºC ".format(zinho['temperature']))
		#TODO: ATUALIZAR IMAGEMs

		#Atualiza Pressao
		frame.var_pres.set("{:.1f}  Pa ".format(zinho['pressure']))
		#TODO: ATUALIZAR IMAGEM

		#Atualiza BatV BatA

		frame.var_batV.set("{:.1f}   V ".format(zinho['batteryV']))
		frame.var_batA.set("{:.1f}   A ".format(zinho['batteryA']))

		#TODO: ATUALIZAR IMAGEM
		
		#Atualiza Dist
		frame.var_dist.set("{:.3f}   m ".format(zinho['distance']))
		#TODO: ATUALIZAR IMAGEM

		#Atualiza Vel
		frame.var_vel.set("{:.3f} m/s ".format(zinho['velocity']))