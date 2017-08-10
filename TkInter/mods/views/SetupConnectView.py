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
			

		title_label = tk.Label(self, text="Connection Setup", font=gui.h1_font, borderwidth=2, relief="groove")
		title_label.grid(self.gui.h1_pad, column=0, columnspan=4, sticky="WENS")


		#### TEST CONNECTION #####

		test_conn_label = tk.Label(self, text="Connection Test", font=gui.h2_font, borderwidth=2, relief="groove")
		test_conn_label.grid(self.gui.h2_pad, column=0, columnspan=4, sticky="WENS")
		
		self.t_p_router = tk.StringVar()
		self.t_p_router.set("Roteador	: -----")
		e = tk.Label(self, textvariable=self.t_p_router, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		self.t_p_zinho = tk.StringVar()
		self.t_p_zinho.set("Zinho 	: -----")
		e = tk.Label(self, textvariable=self.t_p_zinho, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		self.t_p_cam1 = tk.StringVar()
		self.t_p_cam1.set("CAM1 	: -----")
		e = tk.Label(self, textvariable=self.t_p_cam1, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		self.t_p_cam2 = tk.StringVar()
		self.t_p_cam2.set("CAM2 	: -----")
		e = tk.Label(self, textvariable=self.t_p_cam2, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(self.gui.p_pad, column=1, columnspan=2, sticky="WENS")

		b_ping = tk.Button(self, text="Test Connection",
						   command=self.controller.testConnection)
		b_ping.grid(self.gui.button_pad, column=1, columnspan=2, sticky="WENS")


		#### ID #####

		id_label = tk.Label(self, text="ID Selection", font=gui.h2_font, borderwidth=2, relief="groove")
		id_label.grid(self.gui.h2_pad, column=0, columnspan=4, sticky="WENS")

		
		self.id = tk.StringVar()
		self.id.set('ID ----')

		t_id = tk.Label(self, textvariable=self.id, font=gui.p_font, borderwidth=2, relief="groove")
		t_id.grid(self.gui.p_pad, rowspan=1, column=1, columnspan=2, sticky="WENS")
		
		_, row = self.grid_size()

		self.radio = tk.IntVar()

		b = tk.Radiobutton(self, text="Ultima Rota", variable=self.radio, value=1, font=gui.p_font, command=self.controller.getLastID)
		b.grid(self.gui.p_pad, column=1, columnspan=1, sticky="W")

		b = tk.Radiobutton(self, text="Nova Rota", variable=self.radio, value=2, font=gui.p_font, command=self.controller.getNewID)
		b.grid(self.gui.p_pad, column=1, columnspan=1, sticky="W")

		b = tk.Radiobutton(self, text="Escolher Rota", variable=self.radio, value=3, font=gui.p_font, command=self.controller.customID)
		b.grid(self.gui.p_pad, column=1, columnspan=1, sticky="W")

		# t_id = tk.Label(self, text="Custom ID", borderwidth=2, font=gui.p_font, relief="groove")
		# t_id.grid(column=1, sticky="WENS")
		
		self.e_id = tk.Entry(self, text="Custom ID", width=3, font=gui.p_font, borderwidth=2, relief="groove", state="disabled")
		self.e_id.grid(self.gui.p_pad, row=row+2,column=2, sticky="WENS")
		
		
		##################

		_, row = self.grid_size()

		b_connec = tk.Button(self, text="Conectar",
						   command=self.controller.connect)
		b_connec.grid(self.gui.button_pad, row=row, column=1, sticky="WENS")


		b_back = tk.Button(self, text="Voltar",
						   command=lambda: gui.show_frame("StartView"))
		b_back.grid(self.gui.button_pad, row=row, column=2, sticky="WENS")


	def refreshFrame(self, state):
		if self.radio.get() == 3:
			self.id.set("ID: {}".format(self.e_id.get()))