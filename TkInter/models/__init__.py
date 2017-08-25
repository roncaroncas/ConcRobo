from .zinho import Zinho
from .user import User

class Models:

	def __init__(self, server):

		self.models={}

		self.models['Zinho'] = Zinho()	#Passar os params
		self.models['User'] = User()	

	def __getitem__(self, key):
		return(self.models[key])

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			print("!!!!!!!!!!!!!!!!There is no >>",key, "<< key!")
			1/0