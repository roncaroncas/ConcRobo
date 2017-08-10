# CONFIGURACOES GERAIS
# Faz a "tradução" do .json para variáveis do python
# Possui variáveis que não precisam ser alteradas pelo usuário


import json

with open('../config.json') as jfile:
            config = json.load(jfile)

IP_ROUTER = config['IP_ROUTER']

IP_ZINHO = config['IP_ZINHO']
PORT_ZINHO = config['PORT_ZINHO']

IP_CAM1 = config['IP_CAM1']
PORT_CAM1 = config['PORT_CAM1']

IP_CAM2 = config['IP_CAM2']
PORT_CAM2 = config['PORT_CAM2']

KEYS = config['KEYS']
			
CONEX = config['CONEX'] #MUST BE: OFFLINE OR ETHERNET

##### PROTOCOLO (HEADCHAR, ENDCHAR)
HEADCHAR = b'\xfd'
ENDCHAR = b'\xfe'
BYTES_IN_MSG = 3
BYTES_IN_RESP = 8
ANYINFO = b'\x30'

#MOVEMENT CONSTANTS:
## Movimento Reto:
Krv = 	config['Krv']	#m/s
Krw = 	config['Krw']	#voltas/s
## Movimento Diagonal 
Kdv = 	config['Kdv'] 	# m/s
Kdw = 	config['Kdw'] 	# voltas/s
## Movimento Lado
Klv = 	config['Klv']		# m/s
Klw = 	config['Klw'] 	# voltas/s



