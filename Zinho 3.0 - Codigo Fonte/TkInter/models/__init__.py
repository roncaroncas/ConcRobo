'''
Os models são a estrura que mantém armazena os dados do Zinho, do usuário e do percurso.
De maneira simples, são as estruturas onde ficam as variáveis que o programa precisa para funcionar.

As explicações de cada um dos 3 Models estão em cada um dos arquivos.

'''

from .zinho import Zinho
from .user import User
from .route import Route

class Models:

	def __init__(self, client):

		self.models={}

		self.models['Zinho'] = Zinho()	#Passar os params
		self.models['User'] = User()	
		self.models['Route'] = Route()

	def __getitem__(self, key):
		return(self.models[key])

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			raise("There is no >>",key, "<< key!")

