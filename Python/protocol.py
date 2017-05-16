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
		self.infoCycle = INFOCYCLE #GARANTIR QUE InfoCycle Segue o protocolo para as informações dos dados analogicos
		self.iInfo = 0
		
	def forceStop(self):
		self.data = b'\x08'

	def fromKey(self,key):
		#Gets a key
		#Return a list of actions in protocol format

		map = {
		UP_LEFT_KEY: b'\x07', #Q
		UP_KEY: b'\x00', #W
		UP_RIGHT_KEY: b'\x01', #E
		LEFT_KEY:  b'\x06', #A
		STOP_KEY: b'\x08', #S
		RIGHT_KEY: b'\x02', #D
		DOWN_LEFT_KEY: b'\x05', #Z
		DOWN_KEY: b'\x04', #X
		DOWN_RIGHT_KEY:  b'\x03', #C

		PLUS_LIGHT_KEY: b'\x16', # O (or click)
		MINUS_LIGHT_KEY: b'\x17', # P (or click)
		}
		
		if key in map:
			self.data = map[key]
		else:
			self.data = b'\x20'
			
		print(self.data)
			
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
	
		