class User:
	def __init__(self):
		self.data = {
			'move': "STOP",
			'id':	"0000",
			'flag': "",
			}

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		if key in list(self.data.keys()):
			self.data[key] = value
		else:
			print("!!!!!!!!!!!!!!!!There is no >>",key, "<< key!")
			1/0

	def __str__ (self):
		s  = "\n-- User -- "
		s += "\nmove: " + self['move']
		s += "\nid:   " + self['id']
		s += "\nflag: " + self['flag']
		return (s)