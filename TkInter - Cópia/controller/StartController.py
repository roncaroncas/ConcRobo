class StartController():
	def __init__(self, server):
		self.server = server
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		frame = self.server.gui.frames[self.name]
		frame.focus_set()
		frame.tkraise()

	def key(self, event):
		print ("pressed", repr(event.char))

	def keyRelease(self, event):
		print ("unpressed", repr(event.char))

	def mouse(self, event):
		print ("clicked at", event.x, event.y)

	def refresh(self, state):
		pass
