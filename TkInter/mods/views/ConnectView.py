import tkinter as tk
from tkinter import font  as tkfont

class ConnectView(tk.Frame):

	def __init__(self, parent, controller, gui):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.gui = gui

		numColumns = 4
		for i in range(numColumns):
			self.columnconfigure(i, weight=1)

		#TITULO 

		title_label = tk.Label(self, text="Connected", font=gui.h1_font, borderwidth=2, relief="groove")
		title_label.grid(self.gui.h1_pad, column=1, columnspan=2, sticky="WENS")

		
		#ID & NOME

		self.t_ping = tk.StringVar()
		self.t_ping.set("ID 0001 - Nome: Tubo asdfgqwer")
		e = tk.Label(self, textvariable=self.t_ping, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, columnspan=2, sticky="WENS")


		
		#PING

		self.t_ping = tk.StringVar()
		self.t_ping.set("Ping:")
		e = tk.Label(self, textvariable=self.t_ping, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, sticky="WENS")

		
		#MOVE & XYZ

		_, row = self.grid_size()
		self.t_move = tk.StringVar()
		self.t_move.set("Move: ")
		e = tk.Label(self, textvariable=self.t_move, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, rowspan=3, sticky="WENS")

		self.t_x = tk.StringVar()
		self.t_x.set("X:")
		e = tk.Label(self, textvariable=self.t_x, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=2, sticky="WENS")

		self.t_y = tk.StringVar()
		self.t_y.set("Y:")
		e = tk.Label(self, textvariable=self.t_y, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row+1, column=2, sticky="WENS")

		self.t_z = tk.StringVar()
		self.t_z.set("Z:")
		e = tk.Label(self, textvariable=self.t_z, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row+2, column=2, sticky="WENS")

		
		#ANGLES

		_, row = self.grid_size()
		self.t_angleA = tk.StringVar()
		self.t_angleA.set("AngleA: ")
		e = tk.Label(self, textvariable=self.t_angleA, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, sticky="WENS")

		self.t_angleB = tk.StringVar()
		self.t_angleB.set("AngleB: ")
		e = tk.Label(self, textvariable=self.t_angleB, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=2, sticky="WENS")


		#TEMP
		_, row = self.grid_size()
		self.t_temp = tk.StringVar()
		self.t_temp.set("Temp:")
		e = tk.Label(self, textvariable=self.t_temp, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, sticky="WENS")
		
		#Pres
		_, row = self.grid_size()
		self.t_pres = tk.StringVar()
		self.t_pres.set("Pres:")
		e = tk.Label(self, textvariable=self.t_pres, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, sticky="WENS")

		
		#Bateria - Tensao
		_, row = self.grid_size()
		self.t_bat = tk.StringVar()
		self.t_bat.set("Bat:")
		e = tk.Label(self, textvariable=self.t_bat, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, sticky="WENS")

		#Bateria - Corrente
		_, row = self.grid_size()
		self.t_bat = tk.StringVar()
		self.t_bat.set("Bat:")
		e = tk.Label(self, textvariable=self.t_bat, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, sticky="WENS")

		#Distancia Percorrida
		_, row = self.grid_size()
		self.t_dist = tk.StringVar()
		self.t_dist.set("Dist:")
		e = tk.Label(self, textvariable=self.t_dist, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, sticky="WENS")

		#Velocidade
		_, row = self.grid_size()
		self.t_vel = tk.StringVar()
		self.t_vel.set("Vel:")
		e = tk.Label(self, textvariable=self.t_vel, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, sticky="WENS")

		#GRAFICO
		_, row = self.grid_size()
		self.t_graph = tk.StringVar()
		self.t_graph.set("~GRAFICO~")
		e = tk.Label(self, textvariable=self.t_graph, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, row=row, column=1, columnspan=2, sticky="WENS")

		#BOTOES
		_, row = self.grid_size()
		button = tk.Button(self, text="Voltar",
						   command=lambda: gui.show_frame("StartView"))
		button.grid(self.gui.p_pad, row=row, column=1, columnspan=2, sticky="WENS")


	def refreshFrame(self, state):
		pass