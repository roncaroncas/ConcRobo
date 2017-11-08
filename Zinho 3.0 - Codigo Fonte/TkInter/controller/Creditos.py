class CreditosController:
	def __init__(self, client):
		self.client = client
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		frame = self.client.gui.frames[self.name]
		frame.focus_set()
		frame.tkraise()

	def key(self, event):
		pass
		#print ("pressed", repr(event.char))

	def keyRelease(self, event):
		pass
		#print ("unpressed", repr(event.char))

	def mouse(self, event):
		pass
		#print ("clicked at", event.x, event.y)

	def refresh(self, state):
		pass