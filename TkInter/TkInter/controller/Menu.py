class MenuController():
	def __init__(self, client):
		self.client = client
		self.name = self.__class__.__name__.split("Controller")[0]

	def show_frame(self):
		frame = self.client.gui.frames[self.name]
		frame.focus_set()
		frame.tkraise()

	def key(self, event):
		#print ("pressed", repr(event.char))
		pass
		
	def keyRelease(self, event):
		#print ("unpressed", repr(event.char))
		pass
		
	def mouse(self, event):
		#print ("clicked at", event.x, event.y)
		pass
		
	def refresh(self, state):
		pass
