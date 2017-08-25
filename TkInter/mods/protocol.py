#import constants in config
from config import *

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

	def key2data(self,key):
		#Gets a key
		#Return a list of actions in protocol format
		self.data = {
		'UP_LEFT': b'\x07', #Q
		'UP': b'\x00', #W
		'UP_RIGHT': b'\x01', #E
		'LEFT':  b'\x06', #A
		'STOP': b'\x08', #S
		'RIGHT': b'\x02', #D
		'DOWN_LEFT': b'\x05', #Z
		'DOWN': b'\x04', #X
		'DOWN_RIGHT':  b'\x03', #C
		}.get(key, b'\x08')
					
		return (self.toProtocol())

	def askRead(self):
		#Gets a key
		#Return a list of actions in protocol format
		self.data = b'\x30'	
		return (self.toProtocol())

class Response(Protocol):
	
	def __init__(self):
		self.head = HEADCHAR + HEADCHAR
		self.data = b'\x00' + b'\x00' + b'\x00'
		self.end = ENDCHAR + ENDCHAR
		
	def setData(self, data):
		self.data = data		