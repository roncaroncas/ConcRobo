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

class ConfiguracoesView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		#Setando colunas
		self.columnconfigure(0, minsize=25)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, minsize=25)

		#Int
		self.var_offlineMode = tk.IntVar()

		#Str
		self.var_ipRouter = tk.StringVar()

		self.var_ipZinho = tk.StringVar()
		self.var_portZinho = tk.StringVar()

		self.var_ipCam1 = tk.StringVar()
		self.var_portCam1 = tk.StringVar()

		self.var_ipCam2 = tk.StringVar()
		self.var_portCam2 = tk.StringVar()
		
		self.var_Krv = tk.StringVar()
		self.var_Krw = tk.StringVar()

		self.var_Kdv = tk.StringVar()
		self.var_Kdw = tk.StringVar()
		
		self.var_Klv = tk.StringVar()
		self.var_Klw = tk.StringVar()

		self.draw()

		#Seta os inputs
		self.binder()

	def draw(self):

		tk.Label(
			self, self.gui.border, text="Configurações", font=self.gui.h1_font
			).grid(
			self.gui.h1_pad, column=1, sticky="WENS")

		###### CONFIGURACOES DE IP ########

		ipFrame = tk.Frame(self, self.gui.border)
		ipFrame.grid(self.gui.h2_pad, column=1, sticky="WENS")
		ipFrame.columnconfigure(0, weight=1)
		ipFrame.columnconfigure(1, minsize=50)
		ipFrame.columnconfigure(2, minsize=50)

		tk.Label(
			ipFrame, self.gui.border, text="Alterar IP", font=self.gui.h2_font
			).grid(
			self.gui.h2_pad_compact, columnspan=3, sticky="WENS")

		tk.Label(
			ipFrame, self.gui.border, text="Dispositivo", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=0, sticky="WENS")
		
		tk.Label(
			ipFrame, self.gui.border, text="IP", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=1, sticky="WENS")
		
		tk.Label(
			ipFrame, self.gui.border, text="Port", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=2, sticky="WENS")

		#### ROUTER

		tk.Label(
			ipFrame, self.gui.border, text="Roteador", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=2, column=0, sticky="WENS")

		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable= self.var_ipRouter, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=2, column=1, sticky="WENS")

		#### Zinho

		tk.Label(
			ipFrame, self.gui.border, text="Zinho", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=3, column=0, sticky="WENS")


		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable=self.var_ipZinho, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=3, column=1, sticky="WENS")

		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable=self.var_portZinho, width=8, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=3, column=2, sticky="WENS")

		#### CAM1

		tk.Label(
			ipFrame, self.gui.border, text="Camera 1", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=4, column=0, sticky="WENS")

		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable=self.var_ipCam1, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=4, column=1, sticky="WENS")

		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable=self.var_portCam1, width=8, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=4, column=2, sticky="WENS")


		#### CAM2

		tk.Label(
			ipFrame, self.gui.border, text="Camera 2", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=5, column=0, sticky="WENS")

		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable=self.var_ipCam2, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=5, column=1, sticky="WENS")

		tk.Entry(
			ipFrame, font=self.gui.p_font, textvariable=self.var_portCam2, width=8, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=5, column=2, sticky="WENS")


		tk.Checkbutton(
			ipFrame, text="Modo Offline", variable=self.var_offlineMode
			).grid(
			self.gui.p_pad, columnspan=3, row=6, sticky="WENS")

		### Botoes

		ipBtnFrame = tk.Frame(ipFrame)
		ipBtnFrame.grid(self.gui.p_pad_compact,columnspan=3, sticky="WENS")
		ipBtnFrame.columnconfigure(0, weight=1)
		ipBtnFrame.columnconfigure(1, weight=1)
		ipBtnFrame.columnconfigure(2, weight=1)

		tk.Button(
			ipBtnFrame, text="Salvar", command=self.controller.saveIP
			).grid(
			self.gui.button_pad, row=7, column=0, sticky="WENS")
		tk.Button(
			ipBtnFrame, text="Restaurar\nPadrão", command=self.controller.defaultIP
			).grid(
			self.gui.button_pad, row=7, column=1, sticky="WENS")
		tk.Button(
			ipBtnFrame, text="Cancelar", command=self.controller.cancelIP
			).grid(
			self.gui.button_pad, row=7, column=2, sticky="WENS")


		#### CALIBRAR VELOCIDADE


		calibFrame = tk.Frame(self, self.gui.border)
		calibFrame.grid(self.gui.h2_pad, column=1, sticky="WENS")
		calibFrame.columnconfigure(0, weight=1)
		calibFrame.columnconfigure(1, minsize=50)
		calibFrame.columnconfigure(2, minsize=50)

		tk.Label(
			calibFrame, self.gui.border, text="Calibrar", font=self.gui.h2_font
			).grid(
			self.gui.h2_pad_compact, columnspan=3, sticky="WENS")

		tk.Label(
			calibFrame, self.gui.border, text="Direção", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=0, sticky="WENS")
		
		tk.Label(
			calibFrame, self.gui.border, text="Velocidade Linear\nm/s", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=1, sticky="WENS")
		
		tk.Label(
			calibFrame, self.gui.border, text="Velocidade Angular\nvoltas/s", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=2, sticky="WENS")

		#### Frente

		tk.Label(
			calibFrame, self.gui.border, text="Frente", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=2, column=0, sticky="WENS")

		tk.Entry(
			calibFrame, font=self.gui.p_font, textvariable= self.var_Krv, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=2, column=1, sticky="WENS")

		
		#### Diagonal

		tk.Label(
			calibFrame, self.gui.border, text="Diagonal", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=3, column=0, sticky="WENS")

		tk.Entry(
			calibFrame, font=self.gui.p_font, textvariable= self.var_Kdv, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=3, column=1, sticky="WENS")

		tk.Entry(
			calibFrame, font=self.gui.p_font, textvariable= self.var_Kdw, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=3, column=2, sticky="WENS")

		#### Lado

		tk.Label(
			calibFrame, self.gui.border, text="Lado", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=4, column=0, sticky="WENS")

		tk.Entry(
			calibFrame, font=self.gui.p_font, textvariable= self.var_Klw, width=15, borderwidth=2, relief="groove"
			).grid(self.gui.p_pad_compact, row=4, column=2, sticky="WENS")

		### Botoes

		calibBtnFrame = tk.Frame(calibFrame)
		calibBtnFrame.grid(self.gui.p_pad_compact,columnspan=3, sticky="WENS")
		calibBtnFrame.columnconfigure(0, weight=1)
		calibBtnFrame.columnconfigure(1, weight=1)
		calibBtnFrame.columnconfigure(2, weight=1)

		tk.Button(
			calibBtnFrame, text="Salvar", command=self.controller.saveCalib
			).grid(
			self.gui.button_pad, row=7, column=0, sticky="WENS")
		tk.Button(
			calibBtnFrame, text="Restaurar\nPadrão", command=self.controller.defaultCalib
			).grid(
			self.gui.button_pad, row=7, column=1, sticky="WENS")
		tk.Button(
			calibBtnFrame, text="Cancelar", command=self.controller.cancelCalib
			).grid(
			self.gui.button_pad, row=7, column=2, sticky="WENS")



		tk.Button(
			self, text="Voltar", command=lambda: self.gui.show_frame("Menu")
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