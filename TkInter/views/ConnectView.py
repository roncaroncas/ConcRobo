import tkinter as tk
from tkinter import font  as tkfont
from PIL import Image, ImageTk
from os import listdir

class ConnectView(tk.Frame):

	def __init__(self, parent, controller, gui):
		#Importando configurações do parent
		tk.Frame.__init__(self, parent)

		#Setando Pointers
		self.controller = controller
		self.gui = gui

		#Ajustando colunas
		numColumns = 6
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		#CARREGANDO IMAGENS
		self.images = self.loadImages(["moves", "angles", "temperature", "pressure", "battery"])

		#Declarando as variáveis

		#String
		self.var_id			= tk.StringVar()
		self.var_ping		= tk.StringVar()
		self.var_x			= tk.StringVar()
		self.var_y			= tk.StringVar()
		self.var_z			= tk.StringVar()
		self.var_temp		= tk.StringVar()
		self.var_pres		= tk.StringVar()
		self.var_batV		= tk.StringVar()
		self.var_batA		= tk.StringVar()
		self.var_dist		= tk.StringVar()
		self.var_vel		= tk.StringVar()

		#Label
		self.varLb_move 	= None
		self.varLb_angleA 	= None
		self.varLb_angleB 	= None
		self.varLb_temp 	= None
		self.varLb_pres 	= None
		self.varLb_V 		= None
		self.varLb_A 		= None

		#ImageTk
		self.varIm_move 	= ImageTk.PhotoImage(self.images['moves']["STOP"])
		self.varIm_angleA 	= ImageTk.PhotoImage(self.images['angles']["angleA"])
		self.varIm_angleB 	= ImageTk.PhotoImage(self.images['angles']["angleB"])
		self.varIm_temp 	= ImageTk.PhotoImage(self.images['temperature']['temp-1'])
		self.varIm_pres 	= ImageTk.PhotoImage(self.images['pressure']['bar'])
		self.varIm_batV		= ImageTk.PhotoImage(self.images['battery']['bat-1'])
		self.varIm_batA		= ImageTk.PhotoImage(self.images['battery']['bat-1'])

		#CARREGANDO A PAGINA
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

		######TITULO 
		tk.Label(
			self, self.gui.border, text="Connected", font=self.gui.h1_font
			).grid(
			self.gui.h1_pad, column=1, columnspan=4, sticky="WENS")

		######ID
		tk.Label(
			self, self.gui.border, textvariable=self.var_id, font=self.gui.p_font
			).grid(
			self.gui.p_pad, column=1, columnspan=4, sticky="WENS")

		#######PING, MOVE & XYZ
		_, row = self.grid_size()

		#Ping
		tk.Label(
			self, self.gui.border, textvariable=self.var_ping, font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, column=1, columnspan=2, sticky="WENS")

		#Move
		self.varLb_move = tk.Label(self, self.gui.border, image=self.varIm_move)
		self.varLb_move.grid(self.gui.p_pad, column=1, columnspan=2, rowspan=2, sticky="WENS")

		#XYZ
		tk.Label(
			self, self.gui.border, text="X:", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=3, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_x, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=4, sticky="WENS")

		tk.Label(
			self, self.gui.border, text="Y:", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=3, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_y, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=4, sticky="WENS")

		tk.Label(
			self, self.gui.border, text="Z:", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+2, column=3, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_z, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+2, column=4, sticky="WENS")
		
		#ANGLES
		_, row = self.grid_size()

		self.varLb_angleA = tk.Label(self, self.gui.border, image=self.varIm_angleA)
		self.varLb_angleA.grid(self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		self.varLb_angleB = tk.Label(self, self.gui.border, image=self.varIm_angleB)
		self.varLb_angleB.grid(self.gui.p_pad, row=row, column=3, columnspan=2, sticky="WENS")

		#TEMP
		_, row = self.grid_size()

		tk.Label(
			self, self.gui.border, text="Temperature:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=1, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_temp, font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=2, sticky="WENS")

		self.varLb_temp = tk.Label(self, self.gui.border, image=self.varIm_temp)
		self.varLb_temp.grid(self.gui.p_pad, row=row, column=3, columnspan=2, sticky="WENS")

		#Pres
		_, row = self.grid_size()

		tk.Label(
			self, self.gui.border, text="Pressure:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=1, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_pres, font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=2, sticky="WENS")
		
		self.varLb_pres = tk.Label(self, self.gui.border, image=self.varIm_pres)
		self.varLb_pres.grid(self.gui.p_pad, row=row, column=3, columnspan=2, sticky="WENS")
		#Bateria - Tensao
		_, row = self.grid_size()
		
		tk.Label(
			self, self.gui.border, text="Tensão:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=1, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_batV, font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=2, sticky="WENS")
		
		self.varLb_batV = tk.Label(self, self.gui.border, image=self.varIm_batV)
		self.varLb_batV.grid(self.gui.p_pad, row=row, column=3, columnspan=2, sticky="WENS")
	

		#Bateria - Corrente
		_, row = self.grid_size()
		tk.Label(
			self, self.gui.border, text="Corrente:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=1, sticky="WENS")

		tk.Label(self, self.gui.border, textvariable=self.var_batA, font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=2, sticky="WENS")

		self.varLb_batA = tk.Label(self, self.gui.border, image=self.varIm_batA)
		self.varLb_batA.grid(self.gui.p_pad, row=row, column=3, columnspan=2, sticky="WENS")
	
		#Distancia Percorrida
		_, row = self.grid_size()
		tk.Label(
			self, self.gui.border, text="Distancia:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=1, sticky="WENS")

		tk.Label(self, self.gui.border, textvariable=self.var_dist, font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=2, sticky="WENS")

		#Velocidade
		_, row = self.grid_size()
		tk.Label(
			self, self.gui.border, text="Velocidade:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=1, sticky="WENS")

		tk.Label(
			self, self.gui.border, textvariable=self.var_vel, font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row, column=2, sticky="WENS")

		#BOTOES
		_, row = self.grid_size()
		button = tk.Button(self, text="Voltar",
						   command=lambda: self.gui.show_frame("Start"))
		button.grid(self.gui.p_pad, row=row, column=1, columnspan=4, sticky="WENS")