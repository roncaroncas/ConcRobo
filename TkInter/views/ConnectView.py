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
		numColumns = 4
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		self.columnconfigure(0,minsize=20)

		self.columnconfigure(1,minsize=160)
		self.columnconfigure(2,minsize=160)

		self.columnconfigure(3,minsize=20)

		#CARREGANDO IMAGENS
		self.images = self.loadImages(["moves", "angles", "temperature", "pressure", "battery"])

		#Declarando as variáveis

		#String
		self.var_id			= tk.StringVar()
		self.var_ping		= tk.StringVar()
		self.var_x			= tk.StringVar()
		self.var_y			= tk.StringVar()
		self.var_z			= tk.StringVar()
		self.var_angleA		= tk.StringVar()
		self.var_angleB		= tk.StringVar()
		self.var_temp		= tk.StringVar()
		self.var_pres		= tk.StringVar()
		self.var_batV		= tk.StringVar()
		self.var_batA		= tk.StringVar()
		self.var_dist		= tk.StringVar()
		self.var_vel		= tk.StringVar()
		self.var_lastWarn	= tk.StringVar()

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

		#Entry
		self.varEn_warn = None #Só para avisar que essa variável existe

		#CARREGANDO A PAGINA
		self.draw()

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

		######TITULO 
		tk.Label(
			self, self.gui.border, text="Conectado", font=self.gui.h1_font
			).grid(
			self.gui.h1_pad_compact, column=1, columnspan=2, sticky="WENS")

		######ID
		tk.Label(
			self, self.gui.border, textvariable=self.var_id, font=self.gui.h2_font
			).grid(
			self.gui.h2_pad_compact, column=1, columnspan=2, sticky="WENS")

		#######PING, MOVE & XYZ
		_, row = self.grid_size()

		pingFrame = tk.Frame(self, self.gui.border)
		pingFrame.grid(self.gui.p_pad_compact, row=row, column=1, sticky="WENS")
		pingFrame.columnconfigure(0, minsize=160)

		#Ping
		tk.Label(
			pingFrame, self.gui.border, textvariable=self.var_ping, font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, column=0, sticky="WENS")

		#Move
		self.varLb_move = tk.Label(pingFrame, self.gui.border, image=self.varIm_move)
		self.varLb_move.grid(self.gui.p_pad_compact, column=0, sticky="WENS")

		#XYZ
		xyzFrame = tk.Frame(self, self.gui.border)
		xyzFrame.grid(self.gui.p_pad_compact, row=row, column=2, sticky="WENS")
		xyzFrame.columnconfigure(0,minsize=60)
		xyzFrame.columnconfigure(1,minsize=100)

		tk.Label(
			xyzFrame, self.gui.border, text="X:", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")

		tk.Label(
			xyzFrame, self.gui.border, textvariable=self.var_x, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=1, sticky="WENS")

		tk.Label(
			xyzFrame, self.gui.border, text="Y:", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=0, sticky="WENS")

		tk.Label(
			xyzFrame, self.gui.border, textvariable=self.var_y, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=1, sticky="WENS")

		tk.Label(
			xyzFrame, self.gui.border, text="Z:", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+2, column=0, sticky="WENS")

		tk.Label(
			xyzFrame, self.gui.border, textvariable=self.var_z, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+2, column=1, sticky="WENS")
		
		#ANGLES FRAME

		angleFrame = tk.Frame(self, self.gui.border)
		angleFrame.grid(self.gui.p_pad_compact, column=1, columnspan=2, sticky="WENS")
		for i in range (2):
			angleFrame.columnconfigure(i,weight=1)
		
	
		_, row = angleFrame.grid_size()

		self.varLb_angleA = tk.Label(angleFrame, self.gui.border, image=self.varIm_angleA)
		self.varLb_angleA.grid(self.gui.p_pad_compact, column=0, sticky="WENS")
		tk.Label(
			angleFrame, self.gui.border, textvariable=self.var_angleA, font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=0, sticky="WENS")

		self.varLb_angleB = tk.Label(angleFrame, self.gui.border, image=self.varIm_angleB)
		self.varLb_angleB.grid(self.gui.p_pad_compact, row=row, column=1, sticky="WENS")
		tk.Label(
			angleFrame, self.gui.border, textvariable=self.var_angleB, font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=1, sticky="WENS")


		####### MEASURES FRAME ##########
		measureFrame = tk.Frame(self, self.gui.border)
		measureFrame.grid(self.gui.p_pad_compact, column=1, columnspan=2, sticky="WENS")

		measureFrame.columnconfigure(0,minsize=90)
		measureFrame.columnconfigure(1,minsize=120)
		measureFrame.columnconfigure(2,minsize=120)
			
			
		#TEMP
		_, row = measureFrame.grid_size()

		tk.Label(
			measureFrame, self.gui.border, text="Temperatura:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")

		tk.Label(
			measureFrame, self.gui.border, textvariable=self.var_temp, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=1, sticky="WENS")

		self.varLb_temp = tk.Label(measureFrame, self.gui.border, image=self.varIm_temp)
		self.varLb_temp.grid(self.gui.p_pad_compact, row=row, column=2, sticky="WENS")

		#Pres
		_, row = measureFrame.grid_size()

		tk.Label(
			measureFrame, self.gui.border, text="Pressão:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")

		tk.Label(
			measureFrame, self.gui.border, textvariable=self.var_pres, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=1, sticky="WENS")
		
		self.varLb_pres = tk.Label(measureFrame, self.gui.border, image=self.varIm_pres)
		self.varLb_pres.grid(self.gui.p_pad_compact, row=row, column=2, sticky="WENS")
		#Bateria - Tensao
		_, row = measureFrame.grid_size()
		
		tk.Label(
			measureFrame, self.gui.border, text="Tensão:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")

		tk.Label(
			measureFrame, self.gui.border, textvariable=self.var_batV, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=1, sticky="WENS")
		
		self.varLb_batV = tk.Label(measureFrame, self.gui.border, image=self.varIm_batV)
		self.varLb_batV.grid(self.gui.p_pad_compact, row=row, column=2, sticky="WENS")
	

		#Bateria - Corrente
		_, row = measureFrame.grid_size()
		tk.Label(
			measureFrame, self.gui.border, text="Corrente:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")

		tk.Label(
			measureFrame, self.gui.border, textvariable=self.var_batA, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=1, sticky="WENS")

		self.varLb_batA = tk.Label(measureFrame, self.gui.border, image=self.varIm_batA)
		self.varLb_batA.grid(self.gui.p_pad_compact, row=row, column=2, sticky="WENS")
	
		#Distancia Percorrida
		_, row = measureFrame.grid_size()
		tk.Label(
			measureFrame, self.gui.border, text="Distância:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")

		tk.Label(
			measureFrame, self.gui.border, textvariable=self.var_dist, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=1, sticky="WENS")

		#Velocidade
		tk.Label(
			measureFrame, self.gui.border, text="Velocidade:", anchor="w", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=0, sticky="WENS")

		tk.Label(
			measureFrame, self.gui.border, textvariable=self.var_vel, anchor="e", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=1, sticky="WENS")


		#Aviso
		warnFrame = tk.Frame(self, self.gui.border)
		warnFrame.grid(self.gui.p_pad_compact, column=1, columnspan=2, sticky="WENS")

		warnFrame.columnconfigure(0, minsize=90)
		warnFrame.columnconfigure(1, minsize=180)
		warnFrame.columnconfigure(2, minsize=60)

		# tk.Label(
		# 	warnFrame, self.gui.border, text="Criar Aviso", font=self.gui.h2_font
		# 	).grid(
		# 	self.gui.h2_pad_compact, column=0, columnspan=3, sticky="WENS")

		_, row = warnFrame.grid_size()
		tk.Label(
			warnFrame, self.gui.border, text="Criar Aviso:", anchor='w', font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row, column=0, sticky="WENS")
	
		self.varEn_warn = tk.Entry(warnFrame, width=20, font=self.gui.p_font, borderwidth=2, relief="groove")
		self.varEn_warn.grid(self.gui.p_pad_compact, row=row, column=1, sticky="WENS")

		tk.Label(
			warnFrame, self.gui.border, text="Ultimo Aviso:", anchor='w', font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=row+1, column=0, sticky="WENS")
	
		tk.Label(
			warnFrame, width=20, font=self.gui.p_font,textvariable=self.var_lastWarn, anchor='w', borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad_compact, row=row+1, column=1, sticky="WENS")

		tk.Button(
			warnFrame, text="Enviar", command=self.controller.b_Warn,
			).grid(self.gui.p_pad_compact, row=row, column=2, rowspan=2, sticky="WENS")

		#BOTOES
		_, row = self.grid_size()
		tk.Button(
			self, text="Voltar", command=self.controller.b_Voltar,
			).grid(self.gui.button_pad_compact, row=row, column=1, columnspan=2, sticky="WENS")



	def binder(self):
		
		for wid in self.winfo_children():
			wid.bind("<Key>", self.controller.key)
			wid.bind("<KeyRelease>", self.controller.keyRelease)
			wid.bind("<Button-1>", self.controller.mouse)
		
			for wid2 in wid.winfo_children():
				wid2.bind("<Key>", self.controller.key)
				wid2.bind("<KeyRelease>", self.controller.keyRelease)
				wid2.bind("<Button-1>", self.controller.mouse)

		#exceptions
		self.varEn_warn.unbind("<Key>")
		self.varEn_warn.unbind("<KeyRelease>")
		self.varEn_warn.unbind("<Button-1>")

