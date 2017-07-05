# CONFIGURACOES GERAIS
# Faz a "tradução" do .json para variáveis do python
# Possui variáveis que não precisam ser alteradas pelo usuário


import json

with open('../config.json') as jfile:
            config = json.load(jfile)

IP = config['IP']
PORT = config['PORT']

KEYS = config['KEYS']
			
CONEX = config['CONEX'] #MUST BE: OFFLINE, ETHERNET OR SERIAL

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



