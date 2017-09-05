from config import *
from os import path, makedirs, listdir, system

import tkinter as tk
from tkinter import messagebox

class SetupConnectController:
	def __init__(self, server):
		self.server = server
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		frame = self.server.gui.frames[self.name]
		frame.focus_set()
		frame.tkraise()

	def key(self, event):
		print ("pressed", repr(event.char))

	def keyRelease(self, event):
		print ("unpressed", repr(event.char))

	def mouse(self, event):
		print ("clicked at", event.x, event.y)

	def refresh(self, state):
		frame = self.server.gui.frames[self.name]
		text = frame.varEn_id.get()
		if len(text) > 4:
			frame.varEn_id.delete(0,tk.END)
			frame.varEn_id.insert(0,text[:-1])
		if len(text)>0:
			if not(text[-1].isdigit()):
				frame.varEn_id.delete(0,tk.END)
				frame.varEn_id.insert(0,text[:-1])

		if frame.var_radio.get() == 3 and text.isdigit():
			frame.var_id.set("ID: {:04}".format(int(""+text)))

		elif frame.var_radio.get() == 3 and len(text) == 0:
			frame.var_id.set("ID: {:04}".format(0))

	def testConnection(self):

		names = ["Router", "Zinho ", "CAM1   ", "CAM2   "]
		IPs = [IP_ROUTER, IP_ZINHO, IP_CAM1, IP_CAM2]
		responses = []

		for i in range (4):
			if system("ping -n 1 -w 20 {}".format(IPs[i])) == 0:
				responses.append(("{}\t{}\tOK!").format(names[i], IPs[i]))
			else:
				responses.append(("{}\t{}\tFAIL").format(names[i], IPs[i]))

		self.server.gui.frames['SetupConnect'].var_router.set(responses[0])
		self.server.gui.frames['SetupConnect'].var_zinho.set(responses[1])
		self.server.gui.frames['SetupConnect'].var_cam1.set(responses[2])
		self.server.gui.frames['SetupConnect'].var_cam2.set(responses[3])


	def getLastID(self):
		''' Retorna o ultimo ID'''
		
		#TODO
		percursos = listdir('./percursos')
		ID = 0
		for p in percursos:
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) > ID):
					ID = int(p.split('.csv')[0])
		
		self.server.gui.frames['SetupConnect'].var_id.set("ID: {:04}".format(int(ID)))
		self.server.gui.frames['SetupConnect'].varEn_id['state'] = "disabled"
		
	def getNewID(self):
		'''Retorna o próximo ID livre'''
		
		#TODO
		percursos = listdir('./percursos')
		ID = 0
		for p in percursos:
			if (p != "backup.csv"):
				if (int(p.split('.csv')[0]) > ID):
					ID = int(p.split('.csv')[0])
		ID += 1

		self.server.gui.frames['SetupConnect'].var_id.set("ID: {:04}".format(int(ID)))
		self.server.gui.frames['SetupConnect'].varEn_id['state'] = "disabled"

	def customID(self):
		self.server.gui.frames['SetupConnect'].varEn_id['state'] = "normal"
		
	def connect(self):
		'''Tenta conectar com o Zinho e retorna True se conseguiu, False se não conseguiu
		Além disso, cria-se um database com o referido id
		'''

		#Validação:
		if self.server.gui.frames['SetupConnect'].var_radio.get() not in (1,2,3):
			tk.messagebox.showinfo("Erro", "Selecione um ID!")
			return

		if self.server.gui.frames['SetupConnect'].var_id.get()[-5:] == '10000':
			tk.messagebox.showinfo("Erro", "Esvazie a pasta dos percursos!\nDica: Copie e Salve em outro lugar!")
			return

		id = self.server.gui.frames['SetupConnect'].var_id.get()[-4:]
		self.server.models['User'].__init__()
		self.server.models['User']['id'] = id


		if id == '0000':
			tk.messagebox.showinfo("Erro", "O ID não pode ser 0000!")
			return

		self.server.gui.frames['SetupConnect'].var_connect.set('Conectando...')
		self.server.gui.refreshAll(self.server.models['Zinho'])
		
		#tenta conectar
		self.server.conex.connect()

		#Se conectou com sucesso
		if self.server.conex.connected:

			self.server.gui.frames['SetupConnect'].var_radio.set(1)
			self.server.gui.frames['SetupConnect'].var_connect.set('Conectar')


			#Tenta criar um novo db (podendo aproveitar um antigo se necessário)
			self.server.initDB()
			
			if not(self.server.db.csv['fail']):
				#Pega os parâmetros do Db criado
				self.server.initZinho()
				
				#Muda de tela
				self.server.gui.show_frame('Connect')
				
		#Se não conseguiu conectar
		else:
			#Mensagem de erro
			tk.messagebox.showinfo("Erro", "A Conexão Falhou!")
			self.server.gui.frames['SetupConnect'].var_connect.set('Conectar')
		
		ID = self.server.gui.frames['SetupConnect'].var_id.get()