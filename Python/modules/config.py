# CONFIGURACOES GERAIS
PRINT = False

CONEX = "OFFLINE" #MUST BE: OFFLINE, ETHERNET OR SERIAL
DELAY = False

##KEYS
KEYS = {
'UP_LEFT' : 113,
'UP' : 119,
'UP_RIGHT' : 101,
'LEFT' : 97,
'STOP' : 115, 
'RIGHT' : 100,
'DOWN_LEFT' : 122,
'DOWN' : 120,
'DOWN_RIGHT' : 99,

'PLUS_LIGHT' : 111,
'MINUS_LIGHT' : 112,	

'ESCAPE': 27,	
}


##### PROTOCOLO (HEADCHAR, ENDCHAR)
HEADCHAR = b'\xfd'
ENDCHAR = b'\xfe'
BYTES_IN_MSG = 3
BYTES_IN_RESP = 8
#INFOCYCLE = [b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15']
ANYINFO = b'\x30'

#NETWORK
###ETHERNET: (IP, PORT)
######ARDUINO:
IP = "192.168.0.120"
PORT = 23

#SERIAL:
COM_PORT = "com3"

#MOVEMENT CONSTANTS:
## Movimento Reto:
Krv = 	0.1125 			#m/s
Krw = 	0				#voltas/s
## Movimento Diagonal 
Kdv = 	0.06081 		# m/s
Kdw = 	0.03226 		# voltas/s
## Movimento Lado
Klv = 	0 				# m/s
Klw = 	0.06427 		# voltas/s



