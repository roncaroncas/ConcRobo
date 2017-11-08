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

class ConectarView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		#Setando as colunas
		self.columnconfigure(0, minsize=25)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, minsize=25)
			
		#Declarando Variáveis
		#String e Ints
		self.var_router = tk.StringVar()
		self.var_zinho = tk.StringVar()
		self.var_cam1 = tk.StringVar()
		self.var_cam2 = tk.StringVar()
		self.var_id = tk.StringVar()
		self.var_radio = tk.IntVar()
		self.var_id2 = tk.StringVar()
		self.var_name = tk.StringVar()
		self.var_connect = tk.StringVar()

		#Setando valores Default
		self.var_id.set('ID: 0000')
		self.var_connect.set('Conectar')

		#Entry
		self.varEn_id = None
		self.varEn_name = None

		#Carregando a página
		self.draw()


		#Seta os inputs
		self.binder()



	def draw(self):

		tk.Label(
			self, text="Conectar", font=self.gui.h1_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.h1_pad_compact, column=1, sticky="WENS")

		###### CONFIGURACOES DE IP ########

		testFrame = tk.Frame(self, self.gui.border)
		testFrame.grid(self.gui.h2_pad_compact, column=1, sticky="WENS")
		testFrame.columnconfigure(0, weight=1)
		testFrame.columnconfigure(1, weight=1)

		tk.Label(
			testFrame, self.gui.border, text="Teste de Conexão", font=self.gui.h2_font
			).grid(
			self.gui.h2_pad_compact, columnspan=2, sticky="WENS")

		tk.Label(
			testFrame, self.gui.border, text="Dispositivo", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=0, sticky="WENS")
		
		tk.Label(
			testFrame, self.gui.border, text="Funcionando", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=1, column=1, sticky="WENS")

		#### ROUTER

		tk.Label(
			testFrame, self.gui.border, text="Roteador", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=2, column=0, sticky="WENS")

		tk.Label(
			testFrame, self.gui.border, font=self.gui.p_font, textvariable=self.var_router,
			).grid(self.gui.p_pad_compact, row=2, column=1, sticky="WENS")


		#### Zinho

		tk.Label(
			testFrame, self.gui.border, text="Zinho", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=3, column=0, sticky="WENS")

		tk.Label(
			testFrame, self.gui.border, font=self.gui.p_font, textvariable=self.var_zinho,
			).grid(self.gui.p_pad_compact, row=3, column=1, sticky="WENS")


		#### Cam 1

		tk.Label(
			testFrame, self.gui.border, text="Camera 1", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=4, column=0, sticky="WENS")

		tk.Label(
			testFrame, self.gui.border, font=self.gui.p_font, textvariable=self.var_cam1,
			).grid(self.gui.p_pad_compact, row=4, column=1, sticky="WENS")


		#### Cam 2

		tk.Label(
			testFrame, self.gui.border, text="Camera 2", font=self.gui.p_font
			).grid(
			self.gui.p_pad_compact, row=5, column=0, sticky="WENS")

		tk.Label(
			testFrame, self.gui.border, font=self.gui.p_font, textvariable=self.var_cam2,
			).grid(self.gui.p_pad_compact, row=5, column=1, sticky="WENS")


		tk.Button(
			testFrame, text="Testar", command=self.controller.testConnection
			).grid(
			self.gui.button_pad, columnspan=2, sticky="WENS")



		#### ID #####

		idFrame = tk.Frame(self, self.gui.border)
		idFrame.grid(self.gui.p_pad_compact, column=1, sticky="WENS")
		idFrame.columnconfigure(0, weight=1)
		idFrame.columnconfigure(1, weight=1)

		tk.Label(
			idFrame, text="Selecionar CSV", font=self.gui.h2_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.h2_pad, column=0, columnspan=2, sticky="WENS")

		tk.Label(
			idFrame, textvariable=self.var_id, font=self.gui.p_font, width=1, borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad, column=0, columnspan=2, sticky="WENS")

		_, row = self.grid_size()

		tk.Radiobutton(
			idFrame, text="Ultima Rota", variable=self.var_radio, value=1, font=self.gui.p_font, command=self.controller.getLastID
			).grid(
			self.gui.p_pad, column=0, columnspan=1, sticky="W")

		tk.Radiobutton(
			idFrame, text="Nova Rota", variable=self.var_radio, value=2, font=self.gui.p_font, command=self.controller.getNewID
			).grid(
			self.gui.p_pad, column=0, columnspan=1, sticky="W")

		tk.Radiobutton(
			idFrame, text="Escolher Rota", variable=self.var_radio, value=3, font=self.gui.p_font, command=self.controller.customID
			).grid(
			self.gui.p_pad, column=0, columnspan=1, sticky="W")
		
		self.varEn_id = tk.Entry(idFrame, width=4, font=self.gui.p_font, borderwidth=2, relief="groove", state="disabled")
		self.varEn_id.grid(self.gui.p_pad, row=row+1,column=1, sticky="WENS")

		tk.Label(
			idFrame, text="Nome (opcional):", font=self.gui.p_font
			).grid(
			self.gui.p_pad, row=row+2, column=0, sticky="WENS")

		self.varEn_name = tk.Entry(
			idFrame, textvariable=self.var_name, font=self.gui.p_font, borderwidth=2, relief="groove", state="disabled"
			)

		self.varEn_name.grid(
			self.gui.p_pad, row=row+2, column=1, sticky="WENS")
		

		tk.Button(
			idFrame, textvariable=self.var_connect, command=self.controller.connect
			).grid(
			self.gui.button_pad, column=0, columnspan=2, sticky="WENS")
		
		##################

		tk.Button(
			self, text="Voltar", command=lambda: self.gui.show_frame("Menu")
			).grid(self.gui.button_pad, column=1, sticky="WENS")


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