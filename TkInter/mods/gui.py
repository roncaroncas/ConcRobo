import tkinter as tk
from tkinter import font  as tkfont
from .views import *


class GUI(tk.Tk):

	def __init__(self, server):
		tk.Tk.__init__(self)
		#Server
		self.server = server
		
		#Fonts
		self.h1_font = 		tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		self.h2_font = 		tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")
		self.p_font = 		tkfont.Font(family='Helvetica', size=10)
		self.button_font = 	tkfont.Font(family='Helvetica', size=10, weight="bold")

		self.h1_pad = 		{'padx':5, 'pady':10, 	'ipadx':5, 'ipady':10}
		self.h2_pad = 		{'padx':5, 'pady':5, 	'ipadx':2, 'ipady':2}
		self.p_pad = 		{'padx':5, 'pady':3, 	'ipadx':2, 'ipady':2}
		self.button_pad = 	{'padx':5, 'pady':5, 	'ipadx':2, 'ipady':2}


		#Frames
		container = tk.Frame()
		container.grid(sticky="nsew")
		self.frames = {}
		for F in (StartView, ConnectView, SetupConnectView, HelpView, AdvancedView):
			page_name = F.__name__
			frame = F(parent=container, controller=self.server, gui=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, sticky="nsew")
			
		self.show_frame("StartView")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()


	def refresh(self, state):
		for F in self.frames:
			self.frames[F].refreshFrame(state)



if __name__ == "__main__":
	zinho = Server()

	while True:
		zinho.g.refreshGUI(zinho.state)
		zinho.g.refresh_idletasks()
		zinho.g.refresh()