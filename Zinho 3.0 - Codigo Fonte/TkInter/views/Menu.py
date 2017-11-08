'''
Cada View é um objeto do tipo tk.Frame

Possui 3 ponteiros:
- gui, para o pai de todos os gráficos
- controller, para ao objeto equivalente que possui os controles desse view
- parent, para o pai direto desse objeto 

Se necessário, importam-se as imagens

Declara-se todas as variáveis necessárias com objetivo de organizar o código.
Vale notar padrões estabelecidos na nomeação:
Str ou Int: 	var_NOME
Label:			valLb_NOME
Entry:			varEn_NOME
Image:			varIm_NOME

Faz-se o desenho de toda a página com a função draw()
	Primeiro, define-se o tamanho das colunas do frame através da função columnconfigure(column, regra)
	A função draw chama widgets do tipo Label, Entry, Button, Frame... e desenham em uma linha e uma coluna,
	Vale notar que quando-se chama um Frame, deve-se setar as colunas e criar seus próprios widgets Label, Entry, Button, Frame...
	Os parâmetros para cada tipo de widget variam e podem ser explorador melhor no site: http://effbot.org/tkinterbook/
	Apenas os widgets que precisam ser chamados pelo controller ficam guardados em uma variável

A função binder() relaciona os inputs do usuário (mouse/teclado) de todos os widgets a função equivalente em controller

'''

import tkinter as tk
from tkinter import font  as tkfont
from PIL import Image, ImageTk
from os import listdir

class MenuView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		#Setando as colunas
		self.columnconfigure(0, minsize=25)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, minsize=25)

		#Carregando Imagens
		self.images = self.loadImages(['start'])

		#Setando as variaveis
		#Label
		self.varLb_logo = None
	
		#ImageTk
		self.varIm_logo = ImageTk.PhotoImage(self.images['start']["logo"])
		
		#Carregando a página
		self.draw()

		#Seta os inputs
		self.binder()

	def loadImages(self, folders):

		#folders deve ser uma lista de strings

		images = {}

		image_format = ".jpeg"

		for folder in folders:
			pathroot = 'img/'+folder
			image_list = listdir(pathroot)
			images[folder] ={}
			for image_name in image_list:
				name = image_name.split(image_format)[0]
				img = Image.open(pathroot+"/"+image_name)

				#SETTING TRASNPARENCY PARA 255 0 255 (rosa)
				img = img.convert("RGBA")
				datas = img.getdata()
				newData = []
				for item in datas:
					if item[0] == 255 and item[1] == 0 and item[2] == 255:
						newData.append((255, 255, 255, 0))
					else:
						newData.append(item)
				img.putdata(newData)
				images[folder][name] = img
		
		return(images)


	def draw(self):

		tk.Label(self, text="Concremat\nZinho", font=self.gui.h1_font, borderwidth=2, relief="groove"
			).grid(
			column=1, sticky="WENS", padx=5, pady=10, ipadx=5, ipady=10)

		self.varLb_logo = tk.Label(self, self.gui.border, image=self.varIm_logo)
		self.varLb_logo.grid(self.gui.p_pad, column=1, rowspan=2, sticky="WENS")

		tk.Label(self, text="Versão 3.0", font=self.gui.h2_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.h1_pad, column=1, sticky="WENS")
		
		tk.Button(
			self, text="Conectar", font=self.gui.button_font, command=lambda: self.gui.show_frame("Conectar")
			).grid(
			self.gui.button_pad, column=1, sticky="WENS")

		tk.Button(
			self, text="Instruções", font=self.gui.button_font, command=lambda: self.gui.show_frame("Instrucoes")
			).grid(
			self.gui.button_pad, column=1, sticky="WENS")

		tk.Button(
			self, text="Configurações", font=self.gui.button_font, command=lambda: self.gui.show_frame("Configuracoes")
			).grid(
			self.gui.button_pad, column=1, sticky="WENS")

		tk.Button(
			self, text="Créditos", font=self.gui.button_font, command=lambda: self.gui.show_frame("Creditos")
			).grid(
			self.gui.button_pad, column=1, sticky="WENS")


	def binder(self):

		self.bind("<Key>", self.controller.key)
		self.bind("<KeyRelease>", self.controller.keyRelease)
		self.bind("<Button-1>", self.controller.mouse)

		for wid in self.winfo_children():
			wid.bind("<Key>", self.controller.key)
			wid.bind("<KeyRelease>", self.controller.keyRelease)
			wid.bind("<Button-1>", self.controller.mouse)
		
			for wid2 in wid.winfo_children():
				wid2.bind("<Key>", self.controller.key)
				wid2.bind("<KeyRelease>", self.controller.keyRelease)
				wid2.bind("<Button-1>", self.controller.mouse)