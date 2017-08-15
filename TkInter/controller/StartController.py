class StartController():
	def __init__(self, server):
		self.server = server
		self.name = self.__class__.__name__.split("Controller")[0]

	def key(self, event):
		print ("clicked at", event.x, event.y)

	def mouse(self, event):
		print ("pressed", repr(event.char))

	def refresh(self, state):
		pass
