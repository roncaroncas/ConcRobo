import tkinter as tk
from tkinter import font  as tkfont

class SetupConnectView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		numColumns = 4
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		self.columnconfigure(1,minsize=120)
		self.columnconfigure(2,minsize=120)
			
		#Declarando Variáveis
		#String e Ints
		self.var_router = tk.StringVar()
		self.var_zinho = tk.StringVar()
		self.var_cam1 = tk.StringVar()
		self.var_cam2 = tk.StringVar()
		self.var_id = tk.StringVar()
		self.var_radio = tk.IntVar()
		self.var_connect = tk.StringVar()

		#Setando valores Default
		self.var_router.set("Roteador	: -----")
		self.var_zinho.set("Zinho 	: -----")
		self.var_cam1.set("CAM1 	: -----")
		self.var_cam2.set("CAM2 	: -----")
		self.var_id.set('ID: 0000')
		self.var_connect.set('Conectar')

		#Entry
		self.varEn_id = tk.Entry(self, width=0, font=self.gui.p_font, borderwidth=2, relief="groove", state="disabled")

		

		#Carregando a página
		self.draw()



	def draw(self):

		tk.Label(
			self, text="Connection Setup", font=self.gui.h1_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.h1_pad, column=0, columnspan=4, sticky="WENS")

		#### TEST CONNECTION #####

		tk.Label(
			self, text="Connection Test", font=self.gui.h2_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.h2_pad, column=0, columnspan=4, sticky="WENS")
		
		tk.Label(self, textvariable=self.var_router, font=self.gui.p_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		tk.Label(self, textvariable=self.var_zinho, font=self.gui.p_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		tk.Label(self, textvariable=self.var_cam1, font=self.gui.p_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		tk.Label(self, textvariable=self.var_cam2, font=self.gui.p_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		tk.Button(self, text="Test Connection", command=self.controller.testConnection
			).grid(
			self.gui.button_pad, column=1, columnspan=2, sticky="WENS")


		#### ID #####

		tk.Label(
			self, text="ID Selection", font=self.gui.h2_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.h2_pad, column=0, columnspan=4, sticky="WENS")

		tk.Label(
			self, textvariable=self.var_id, font=self.gui.p_font, borderwidth=2, relief="groove"
			).grid(
			self.gui.p_pad, rowspan=1, column=1, columnspan=2, sticky="WENS")
		

		_, row = self.grid_size()

		tk.Radiobutton(
			self, text="Ultima Rota", variable=self.var_radio, value=1, font=self.gui.p_font, command=self.controller.getLastID
			).grid(
			self.gui.p_pad, column=1, columnspan=1, sticky="W")

		tk.Radiobutton(
			self, text="Nova Rota", variable=self.var_radio, value=2, font=self.gui.p_font, command=self.controller.getNewID
			).grid(
			self.gui.p_pad, column=1, columnspan=1, sticky="W")

		tk.Radiobutton(
			self, text="Escolher Rota", variable=self.var_radio, value=3, font=self.gui.p_font, command=self.controller.customID
			).grid(
			self.gui.p_pad, column=1, columnspan=1, sticky="W")
		
		self.varEn_id.grid(self.gui.p_pad, row=row+2,column=2, sticky="WENS")
		
		##################

		_, row = self.grid_size()

		tk.Button(
			self, textvariable=self.var_connect, command=self.controller.connect
			).grid(
			self.gui.button_pad, row=row, column=1, sticky="WENS")

		tk.Button(
			self, text="Voltar", command=lambda: self.gui.show_frame("Start")
			).grid(self.gui.button_pad, row=row, column=2, sticky="WENS")
