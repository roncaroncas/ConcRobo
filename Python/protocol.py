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
		
	def forceStop(self):
		self.data = b'\x08'

	def mapKeyToData(self,key):
		#Gets a key
		#Return a list of actions in protocol format

		map = {
		KEYS['UP_LEFT']: b'\x07', #Q
		KEYS['UP']: b'\x00', #W
		KEYS['UP_RIGHT']: b'\x01', #E
		KEYS['LEFT']:  b'\x06', #A
		KEYS['STOP']: b'\x08', #S
		KEYS['RIGHT']: b'\x02', #D
		KEYS['DOWN_LEFT']: b'\x05', #Z
		KEYS['DOWN']: b'\x04', #X
		KEYS['DOWN_RIGHT']:  b'\x03', #C

		KEYS['PLUS_LIGHT']: b'\x16', # O (or click)
		KEYS['MINUS_LIGHT']: b'\x17', # P (or click)
		}
		
		if key in map:
			self.data = map[key]
		else:
			self.data = b'\x30'
			
		#print(self.data)
			
	def anyInfo(self):
		self.data = ANYINFO

class Response(Protocol):
	
	def __init__(self):
		self.head = HEADCHAR + HEADCHAR
		self.data = b'\x00' + b'\x00' + b'\x00'
		self.end = ENDCHAR + ENDCHAR
		
	def setData(self, data):
		self.data = data
	
		