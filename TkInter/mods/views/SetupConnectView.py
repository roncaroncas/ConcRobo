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
			self.columnconfigure(i, minsize=25)


		title_label = tk.Label(self, text="Connection Setup", font=gui.h1_font, borderwidth=2, relief="groove")
		title_label.grid(column=0, columnspan=4, sticky="WENS", padx=5, pady=10, ipadx=5, ipady=10)


		#### TEST CONNECTION #####

		test_conn_label = tk.Label(self, text="Connection Test", font=gui.h2_font, borderwidth=2, relief="groove")
		test_conn_label.grid(column=0, columnspan=4, sticky="WENS", padx=5, pady=5)
		
		self.t_p_router = tk.StringVar()
		self.t_p_router.set("Roteador	: -----")
		e = tk.Label(self, textvariable=self.t_p_router, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(column=1, columnspan=2, sticky="WENS", padx=5, pady=3)

		self.t_p_zinho = tk.StringVar()
		self.t_p_zinho.set("Zinho 	: -----")
		e = tk.Label(self, textvariable=self.t_p_zinho, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(column=1, columnspan=2, sticky="WENS", padx=5, pady=3)

		self.t_p_cam1 = tk.StringVar()
		self.t_p_cam1.set("CAM1 	: -----")
		e = tk.Label(self, textvariable=self.t_p_cam1, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(column=1, columnspan=2, sticky="WENS", padx=5, pady=3)

		self.t_p_cam2 = tk.StringVar()
		self.t_p_cam2.set("CAM2 	: -----")
		e = tk.Label(self, textvariable=self.t_p_cam2, font=gui.p_font, borderwidth=2, relief="groove")
		e.grid(column=1, columnspan=2, sticky="WENS", padx=5, pady=3)

		b_ping = tk.Button(self, text="Test Connection",
						   command=self.testConnection)
		b_ping.grid(column=1, columnspan=2, sticky="WENS", padx=5, pady=5)


		#### ID #####

		id_label = tk.Label(self, text="ID Selection", font=gui.h2_font, borderwidth=2, relief="groove")
		id_label.grid(column=0, columnspan=4, sticky="WENS", padx=5, pady=5)
		
		_, row = self.grid_size()

		self.radio = tk.IntVar()
		b = tk.Radiobutton(self, text="Nova Rota", variable=self.radio, value=1, font=gui.p_font, command=self.getNewID)
		b.grid(column=1, columnspan=1, sticky="W", padx=5, pady=5)

		b = tk.Radiobutton(self, text="Ultima Rota", variable=self.radio, value=2, font=gui.p_font, command=self.getLastID)
		b.grid(column=1, columnspan=1, sticky="W", padx=5, pady=5)

		b = tk.Radiobutton(self, text="Escolher Rota", variable=self.radio, value=3, font=gui.p_font, command=self.customID)
		b.grid(column=1, columnspan=1, sticky="W", padx=5, pady=5)

		# t_id = tk.Label(self, text="Custom ID", borderwidth=2, font=gui.p_font, relief="groove")
		# t_id.grid(column=1, sticky="WENS", padx=5, pady=5)
		
		self.e_id = tk.Entry(self, text="Custom ID", width=3, font=gui.p_font, borderwidth=2, relief="groove", state="disabled")
		self.e_id.grid(row=row+2,column=2, sticky="WENS", padx=5, pady=5)
		

		self.id = tk.StringVar()
		self.id.set('ID ???')

		t_id = tk.Label(self, textvariable=self.id, font=gui.p_font, borderwidth=2, relief="groove")
		t_id.grid(row=row, rowspan=2, column=2, sticky="WENS", padx=5, pady=5)
		
		##################

		_, row = self.grid_size()

		b_connec = tk.Button(self, text="Conectar",
						   command=self.connect)
		b_connec.grid(row=row, column=1, sticky="WENS", padx=5, pady=5)


		b_back = tk.Button(self, text="Voltar",
						   command=lambda: gui.show_frame("StartView"))
		b_back.grid(row=row, column=2, sticky="WENS", padx=5, pady=5)

	def testConnection(self):
		a, b, c, d = self.controller.testConnection()
		self.t_p_router.set(a)
		self.t_p_zinho.set(b)
		self.t_p_cam1.set(c)
		self.t_p_cam2.set(d)

	def getLastID(self):
		self.id.set("ID: {}".format(self.controller.getLastID()))
		self.e_id['state'] = "disabled"

	def getNewID(self):
		self.id.set("ID: {}".format(self.controller.getNewID()))
		self.e_id['state'] = "disabled"
		
	def customID(self):
		self.e_id['state'] = "normal"

	def connect(self):

		ID = self.id.get()
		success = self.controller.connect(ID)
		if success:
			self.gui.show_frame("ConnectView")
		else:
			self.gui.show_frame("StartView")


	def refreshFrame(self, state):
		if self.radio.get() == 3:
			self.id.set("ID: {}".format(self.e_id.get()))