import json
import re

import tkinter as tk
from tkinter import messagebox

class AdvancedController:
	def __init__(self, server):
		self.server = server
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		frame = self.server.gui.frames[self.name]
		frame.focus_set()
		frame.tkraise()

		with open('config.json', 'r') as f:
			data = json.load(f)

		frame.var_ipRouter.set(data['IP_ROUTER'])
		
		frame.var_ipZinho.set(data['IP_ZINHO'])
		frame.var_portZinho.set(data['PORT_ZINHO'])
		
		frame.var_ipCam1.set(data['IP_CAM1'])
		frame.var_portCam1.set(data['PORT_CAM1'])

		frame.var_ipCam2.set(data['IP_CAM2'])
		frame.var_portCam2.set(data['PORT_CAM2'])

		frame.var_offlineMode.set(data['CONEX']=="OFFLINE")

		print(data)

		frame.var_Krv.set(data['Krv']) 
		frame.var_Kdv.set(data['Kdv'])
		frame.var_Kdw.set(data['Kdw'])
		frame.var_Klw.set(data['Klw'])


	def key(self, event):
		print ("pressed", repr(event.char))

	def keyRelease(self, event):
		print ("unpressed", repr(event.char))

	def mouse(self, event):
		print ("clicked at", event.x, event.y)

	def refresh(self, state):
		pass

	def saveIP(self):
		print("saveIP")

		frame = self.server.gui.frames[self.name]

		IpPattern = re.compile('^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$')
		PortPattern = re.compile('^[0-9]{1,5}$')

		IP_ROUTER = frame.var_ipRouter.get()
		
		IP_ZINHO = frame.var_ipZinho.get()
		PORT_ZINHO = frame.var_portZinho.get()
		
		IP_CAM1 = frame.var_ipCam1.get()
		PORT_CAM1 = frame.var_portCam1.get()

		IP_CAM2 = frame.var_ipCam2.get()
		PORT_CAM2 = frame.var_portCam2.get()


		#VALIDAR DATA

		if not(
			IpPattern.match(IP_ROUTER) and
			IpPattern.match(IP_ZINHO) and
			IpPattern.match(IP_CAM1) and
			IpPattern.match(IP_CAM2)
			):

			tk.messagebox.showinfo("Erro", "Coloque o IP no formato correto: XXX.XXX.XXX.XXX\nExemplo: 192.168.0.1")
			return

		if not(
			PortPattern.match(PORT_ZINHO) and
			PortPattern.match(PORT_CAM1) and
			PortPattern.match(PORT_CAM2)
			):

			tk.messagebox.showinfo("Erro", "Coloque a Porta no formato correto: XXXXX\nExemplo: 34567")
			return


		modoOffline = frame.var_offlineMode.get()	

		with open('config.json', 'r') as f:
			data = json.load(f)

		data['IP_ROUTER'] = IP_ROUTER

		data['IP_ZINHO'] = IP_ZINHO
		data['IP_ZINHO'] = IP_ZINHO

		data['IP_CAM1'] = IP_CAM1
		data['PORT_CAM1'] = PORT_CAM1

		data['IP_CAM2'] = IP_CAM2
		data['PORT_CAM2'] = PORT_CAM2

		if modoOffline == 1:
			data['CONEX'] = "OFFLINE"
		else:	
			data['CONEX'] = "ETHERNET"

		with open('config.json', 'w') as f:
			json.dump(data, f)

		tk.messagebox.showinfo("Aviso", "Reinicie o programa para aplicar as alterações")

	def defaultIP(self):
		print("defaultIP")

		with open('config.json', 'r') as f:
			data = json.load(f)

		data['IP_ROUTER'] = '192.168.0.1'

		data['IP_ZINHO'] = '192.168.0.120'
		data['PORT_ZINHO'] = '23'

		data['IP_CAM1'] = '192.168.0.10'
		data['PORT_CAM1'] = '34567'

		data['IP_CAM2'] = '192.168.0.110'
		data['PORT_CAM2'] = '34568'

		data['CONEX'] = "ETHERNET"

		with open('config.json', 'w') as f:
			json.dump(data, f)

		tk.messagebox.showinfo("Aviso", "Reinicie o programa para aplicar as alterações")

	def cancelIP(self):
		print("cancelIP")

		frame = self.server.gui.frames[self.name]

		with open('config.json', 'r') as f:
			data = json.load(f)

		frame.var_ipRouter.set(data['IP_ROUTER'])
		
		frame.var_ipZinho.set(data['IP_ZINHO'])
		frame.var_portZinho.set(data['PORT_ZINHO'])
		
		frame.var_ipCam1.set(data['IP_CAM1'])
		frame.var_portCam1.set(data['PORT_CAM1'])

		frame.var_ipCam2.set(data['IP_CAM2'])
		frame.var_portCam2.set(data['PORT_CAM2'])

		frame.var_offlineMode.set(data['CONEX'])

	def saveCalib(self):
		print("saveCalib")

		frame = self.server.gui.frames[self.name]

		try:
			Krv = frame.var_Krv.get()
			Kdv = float(frame.var_Kdv.get())
			Kdw = float(frame.var_Kdw.get())
			Klw = float(frame.var_Klw.get())

		except:
			tk.messagebox.showinfo("Erro", "Os valores devem ser numéricos\n(Utilize . para separar os decimais)")
			return

		with open('config.json', 'r') as f:
			data = json.load(f)

		data["Krv"] = Krv 
		data["Kdv"] = Kdv
		data["Kdw"] = Kdw
		data["Klw"] = Klw

		with open('config.json', 'w') as f:
			json.dump(data, f)

		tk.messagebox.showinfo("Aviso", "Reinicie o programa para aplicar as alterações")


	def defaultCalib(self):

		with open('config.json', 'r') as f:
			data = json.load(f)

		data["Krv"] = 0.1125
		data["Krw"] = 0
		data["Kdv"] = 0.06081
		data["Kdw"] = 0.03226
		data["Klv"] = 0
		data["Klw"] = 0.06427	

		print(data["Krv"])

		with open('config.json', 'w') as f:
			json.dump(data, f)

		tk.messagebox.showinfo("Aviso", "Reinicie o programa para aplicar as alterações")
	def cancelCalib(self):

		frame = self.server.gui.frames[self.name]

		with open('config.json', 'r') as f:
			data = json.load(f)

		frame.var_Krv.set(data['Krv']) 
		frame.var_Kdv.set(data['Kdv'])
		frame.var_Kdw.set(data['Kdw'])
		frame.var_Klw.set(data['Klw'])
