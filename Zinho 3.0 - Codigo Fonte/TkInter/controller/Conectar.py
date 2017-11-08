from os import path, makedirs, listdir, system

import tkinter as tk
from tkinter import messagebox

import subprocess as sp

import config

class ConectarController:
	def __init__(self, client):
		self.client = client
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		self.frame = self.client.gui.frames[self.name]
		self.frame.focus_set()
		self.frame.tkraise()
		self.frame.var_name.set("")

		self.frame.varEn_name['state'] = "disabled"
		self.frame.varEn_name.delete(0,tk.END)

	def key(self, event):
		pass
		#print ("pressed", repr(event.char))

	def keyRelease(self, event):
		pass
		#print ("unpressed", repr(event.char))

	def mouse(self, event):
		#print ("clicked at", event.x, event.y)
		pass

	def refresh(self, state):
		
		#Controla o que o usuario escreve no campo de ID
		text = self.frame.varEn_id.get()
		if len(text) > 4:
			self.frame.varEn_id.delete(0,tk.END)
			self.frame.varEn_id.insert(0,text[:-1])
		if len(text)>0:
			if not(text[-1].isdigit()):
				self.frame.varEn_id.delete(0,tk.END)
				self.frame.varEn_id.insert(0,text[:-1])

		if self.frame.var_radio.get() == 3 and text.isdigit():
			self.frame.var_id.set("ID: {:04}".format(int(""+text)))

		elif self.frame.var_radio.get() == 3 and len(text) == 0:
			self.frame.var_id.set("ID: {:04}".format(0))

		#Pega o ID do ultimo valor setado
		ID = self.frame.var_id.get()[4:8]

		#Define o name de acordo com o radiobutton
		if self.frame.var_radio.get() == 1:
			name = self.frame.var_id.get()[11:]
		else:
			name = self.frame.varEn_name.get()

		#Escreve no campo de nome
		if name:
			self.frame.var_id.set("ID: {:04} - {}".format(int(ID), name))
		else:
			self.frame.var_id.set("ID: {:04}".format(int(ID)))



	def testConnection(self):

		names = ["Router", "Zinho ", "CAM1   ", "CAM2   "]
		IPs = [config.IP_ROUTER, config.IP_ZINHO, config.IP_CAM1, config.IP_CAM2]
		responses = []

		for i in range (4): 
			if sp.call(['ping', '-n', '1', '-w', '20', IPs[i]], stdout=sp.DEVNULL, shell=True) == 0:
				responses.append("Sim")
			else:
				responses.append("Não")

		self.frame.var_router.set(responses[0])
		self.frame.var_zinho.set(responses[1])
		self.frame.var_cam1.set(responses[2])
		self.frame.var_cam2.set(responses[3])


	def getLastID(self):
		''' Retorna o ultimo ID'''
		
		percursos = listdir('../percursos')
		ID = 0
		name = ""
		for p in percursos:
			try:
				ID = int(p[:4])
				if len(p) > 9: 		#4 digitos do ID + 4 digitos do ".csv"
					name = p[7:-4]	#4 digitos do ID + 3 digitos " - "
			except:
				pass
		if name:
			self.frame.var_id.set("ID: {:04} - {}".format(ID, name))
		else:
			self.frame.var_id.set("ID: {:04}".format(ID))

		self.frame.varEn_id['state'] = "disabled"
		self.frame.varEn_name['state'] = "disabled"
		
	def getNewID(self):
		'''Retorna o próximo ID livre'''
		
		percursos = listdir('../percursos')
		ID = 0
		name =self.frame.var_name.get()
		for p in percursos:
			try:
				ID = int(p[:4])
			except:
				pass
		ID += 1

		self.frame.var_id.set("ID: {:04}".format(int(ID)))
		
		self.frame.varEn_id['state'] = "disabled"
		self.frame.varEn_name['state'] = "normal"

	def customID(self):
		self.frame.varEn_id['state'] = "normal"
		self.frame.varEn_name['state'] = "normal"
		
	def connect(self):
		'''Tenta conectar com o Zinho e retorna True se conseguiu, False se não conseguiu
		Além disso, cria-se um database com o referido id
		'''

		#Validação:
		if self.frame.var_radio.get() not in (1,2,3):
			tk.messagebox.showinfo("Erro", "Selecione um ID!")
			return

		if self.frame.var_id.get()[-5:] == '10000':
			tk.messagebox.showinfo("Erro", "Esvazie a pasta dos percursos!\nDica: Copie e Salve em outro lugar!")
			return

		id = self.frame.var_id.get()[4:8]

		if id == '0000':
			tk.messagebox.showinfo("Erro", "O ID não pode ser 0000!")
			return

		#Pegando o nome
		name = ""

		if self.frame.var_radio.get() == 1:
			name = self.frame.var_id.get()[11:]
		elif self.frame.var_radio.get() == 2:
			name = self.frame.var_name.get()
		else:
			percursos = listdir('../percursos')
			for p in percursos:
				try: 
					int(p[:4])
					if id == p[:4]:
						if len(p) > 8:
							name = p[7:-4]
				except:
					pass


		self.client.models['User'].__init__(id, name)

		self.frame.var_connect.set('Conectando...')
		#self.client.gui.refreshAll(self.client.models['Zinho'])
		self.client.gui.refreshAll(self.client.models)
		
		#tenta conectar
		self.client.conex.connect()

		#Se conectou com sucesso
		if self.client.conex.connected:

			self.frame.var_radio.set(1)
			self.frame.var_connect.set('Conectar')

			#Tenta criar um novo db
			self.client.controller.initDB()

			
			if not(self.client.models['Route'].csv['fail']):
				#Pega os parâmetros do Db criado
				self.client.controller.initZinho()
				
				#Muda de tela
				self.client.gui.show_frame('Conectado')
				
		#Se não conseguiu conectar
		else:
			#Mensagem de erro
			tk.messagebox.showinfo("Erro", "A Conexão Falhou!")
			self.frame.var_connect.set('Conectar')
		
		ID = self.frame.var_id.get()