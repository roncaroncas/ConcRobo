### PROTOCOLO (HEADCHAR, ENDCHAR)
HEADCHAR = b'\xfd'
ENDCHAR = b'\xfe'
BYTES_IN_MSG = 3
BYTES_IN_RESP = 8

class Protocol:
	
	def __str__(self):
		return str(self.head + self.data + self.end)

	def toProtocol(self):
		return (self.head + self.data + self.end)

class Message(Protocol):

	def __init__(self):
		self.head = HEADCHAR
		self.data = b'\x08'
		self.end = ENDCHAR
		self.infoCycle = [
			b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15'] #GARANTIR QUE InfoCycle Segue o protocolo para as informações dos dados analogicos
		self.iInfo = 0
		
	def forceStop(self):
		self.data = b'\x08'

	def fromKey(self,key):
		#Gets a key
		#Return a list of actions in protocol format

		#Q - UP_LEFT
		if key == 113:
			self.data = b'\x07'

		#W - UP
		elif key == 119:
			self.data = b'\x00'

		#E - UP_RIGHT
		elif key == 101:
			self.data = b'\x01'

		#A - LEFT
		elif key == 97:
			self.data = b'\x06'

		#S - STOP
		elif key == 115:
			self.data = b'\x08'

		#D - RIGHT
		elif key == 100:
			self.data = b'\x02'

		#Z - DOWN_LEFT
		elif key == 122:
			self.data = b'\x05'

		#X - DOWN
		elif key == 120:
			self.data = b'\x04'

		#C - DOWN_RIGHT
		elif key == 99:
			self.data = b'\x03'

		else:
			self.data = b'\x20'

	def nextInfo(self):
		self.data = self.infoCycle[self.iInfo]
		self.iInfo = (self.iInfo + 1)%len(self.infoCycle)

class Response(Protocol):
	
	def __init__(self):
		self.head = HEADCHAR + HEADCHAR
		self.data = b'\x00' + b'\x00'
		self.end = ENDCHAR + ENDCHAR
		
	def setData(self, data):
		self.data = data
	
		