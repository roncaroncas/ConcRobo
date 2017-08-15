import tkinter as tk
from tkinter import font  as tkfont
from tkinter import messagebox

#IMPORT ALL
from .StartView import StartView
from .AdvancedView import AdvancedView
from .HelpView import HelpView
from .ConnectView import ConnectView
from .SetupConnectView import SetupConnectView

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

		#Pads
		self.h1_pad = 		{'padx':5, 'pady':10, 	'ipadx':5, 'ipady':10}
		self.h2_pad = 		{'padx':5, 'pady':5, 	'ipadx':2, 'ipady':2}
		self.p_pad = 		{'padx':5, 'pady':3, 	'ipadx':2, 'ipady':2}
		self.p_pad_compact ={'padx':5, 'pady':1, 	'ipadx':2, 'ipady':1}
		self.button_pad = 	{'padx':5, 'pady':5, 	'ipadx':2, 'ipady':2}

		#Border
		self.border = {"borderwidth":2, "relief":"groove"}

		#Frames
		container = tk.Frame()
		container.grid(sticky="nsew")
		self.frames = {}
		for F in ("Start", "Connect", "SetupConnect", "Help", "Advanced"):
			page_name = F
			view = eval(page_name+"View")
			controller = eval("self.server.controller.controls['"+F+"']")
			frame = view(parent=container, controller=controller, gui=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.bind("<Key>", self.key)
			frame.bind("<Button-1>", self.mouse)
			frame.grid(row=0, sticky="nsew")
			
		self.show_frame("Start")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		self.nowFrame = page_name 
		frame = self.frames[page_name]
		frame.focus_set()
		frame.tkraise()

	def refreshAll(self, state):
		for F in self.frames:
			#self.frames[F].refreshFrame(state)
			self.frames[self.nowFrame].controller.refresh(state)
		
	def key(self, event):
		self.frames[self.nowFrame].controller.mouse(event)

	def mouse(self, event):
		self.frames[self.nowFrame].controller.key(event)

if __name__ == "__main__":
	zinho = Server()

	while True:
		zinho.g.refreshGUI(zinho.state)
		zinho.g.refresh_idletasks()
		zinho.g.refresh()