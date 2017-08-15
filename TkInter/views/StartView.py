import tkinter as tk
from tkinter import font  as tkfont
from PIL import Image, ImageTk
from os import listdir

class StartView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		numColumns = 3
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		#Carregando Imagens
		self.images = self.loadImages(['start'])

		#Setando as variaveis


		#Label
		self.varLb_logo = None
	
		#ImageTk
		self.varIm_logo = ImageTk.PhotoImage(self.images['start']["logo"])
		

		#Carregando a página
		self.draw()

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
			column=1, sticky="WENS", padx=5, pady=10, ipadx=5, ipady=10)
		
		tk.Button(
			self, text="Conectar", font=self.gui.button_font, command=lambda: self.gui.show_frame("SetupConnect")
			).grid(column=1, sticky="WENS", padx=5, pady=5)

		tk.Button(
			self, text="Instruções", font=self.gui.button_font, command=lambda: self.gui.show_frame("Help")
			).grid(column=1, sticky="WENS", padx=5, pady=5)

		tk.Button(
			self, text="Configurações", font=self.gui.button_font, command=lambda: self.gui.show_frame("Advanced")
			).grid(column=1, sticky="WENS", padx=5, pady=5)

	def refreshFrame(self, state):
		pass