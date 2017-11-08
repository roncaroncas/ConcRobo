'''
Esse objeto mantém o registro dos comandos inseridos pelo usuário.

Isto é:

-- Move é o que o usuário está pedindo para o arduino realizar
	Ou seja, qual tecla o usuário apertou.		

-- Id e Name são o identificador e o nome que o usuário escolheu para o percurso.

-- Flag é a mensagem que o usuário escreve para registrar em alguns pontos do percurso.

Obs: O Move que o usuário aperta não é necessariamente o mesmo que o Move do Zinho, visto que existem atrasos e/ou problemas de conexão

'''


class User:
	def __init__(self, id="0000", name=""):
		self.data = {
			'move': "STOP",
			'id':	id,
			'name': name,
			'flag': "",
			}

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			raise Exception ("There is no >>",key, "<< key!")
			

	def __str__ (self):
		s  = "\n-- User -- "
		s += "\nmove: " + self['move']
		s += "\nid:   " + self['id']
		s += "\nflag: " + self['flag']
		return (s)