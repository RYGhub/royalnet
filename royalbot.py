# -*- coding: utf-8 -*-

import requests #Modulo per fare richieste su HTTP
import time #Modulo per mettere in pausa il programma

#Ultimo messaggio mandato dal bot.
lastmsg = ""

#Inizializzazione keys
token = ""
steamtoken = ""
osutoken = ""

#Elenco degli steamid e degli username di telegram.
steamids =  {
	'@steffo': 76561198034314260,
	'@evilbaluisevilt_t': 76561198071012695,
	'@fultz': 76561198035547490,
	'@ilgattopardo': 76561198111021344,
	'@frankfrankfrank': 76561198071099951,
	'@fedyal': 76561198109189938,
	'@acterryg': 76561198146704979,
	'@maxsensei': 76561198121094516,
	'@heisendoc': 76561198080377213,
	'@supermattemb': 76561198115852550,
	'@peraemela99': 76561198161867082,
	'@thevagginadestroyer': 76561198128738388,
	'fillo': 76561198103292029,
	'@cosimo03': 76561198062778224,
	'@albertino04': 76561198071383448,
	'@voltaggio': 76561198147601821,
	'alle2002': 76561198052996311,
	'jummi': 76561198169975999,
	'@tauei': 76561198104305298,
	'@saitorlock': 76561198089120441,
	'@iemax': 76561198149695151,
	'@alleanderl': 76561198154175301,
	'@boni3099': 76561198131868211,
	'@adry99': 76561198230034568,
	'@mrdima98': 76561198140863530,
}

#Elenco degli steamid e degli username di telegram.
osuids =  {
	'@steffo': 'SteffoRYG',
	'@evilbaluisevilt_t': 'NemesisRYG',
	'@fultz': 'ftz99',
	'@ilgattopardo': 'gattopardo',
	'@frankfrankfrank': 'FrankezRYG',
	'@fedyal': 'fedececco',
	'@acterryg': 'Acter1',
	'@maxsensei': 'MaxSensei',
	'@heisendoc': 'ImHeisenberg',
	'@thevagginadestroyer': 'barboll',
	'@cosimo03': 'Cosimo03',
	'@albertino04': 'Alby1',
	'@voltaggio': 'voltaggio',
	'@tauei': 'tauei',
	'@saitorlock': 'saitorlock',
	'@boni3099': 'boni3099',
	'@mrdima98': 'MRdima98',
}

#Leggi un file e rispondi con il contenuto
def readFile(name):
	file = open(name, 'r')
	content = file.read()
	file.close()
	return content

#Scrivi qualcosa su un file
def writeFile(name, content):
	file = open(name, 'w')
	file.write(content)
	file.close()
	
#Ricevi gli ultimi messaggi
def getUpdates():
	#Parametri della richiesta da fare
	parametri = {
		'offset': readFile("lastid.txt"), #Update ID del messaggio da leggere
		'limit': 1, #Numero di messaggi da ricevere alla volta, lasciare 1
		'timeout': 300, #Secondi da mantenere attiva la richiesta se non c'e' nessun messaggio
	}
	#Manda la richiesta ai server di Telegram e convertila in un dizionario
	r = requests.get("https://api.telegram.org/bot" + token + "/getUpdates", params=parametri).json()
	return r
	
#Manda un messaggio
def sendMessage(content, to, da):
	#Parametri del messaggio
	parametri = {
		'chat_id': to, #L'ID della chat a cui mandare il messaggio, Royal Games: -2141322
		'text': content, #Il messaggio da mandare
		'parse_mode': 'Markdown' #Formattare il messaggio?
	}
	#Antispam: manda il messaggio solo se l'ultimo messaggio è diverso da quello che deve mandare ora.
	global lastmsg
	if(lastmsg != content):
		#Manda il messaggio
		r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage", params=parametri)
		lastmsg = content
	else:
		#Manda il messaggio in chat privata
		parametri['chat_id'] = da
		#Manda il messaggio
		r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage", params=parametri)
		
#RoyalBot sta scrivendo...
def setTyping(type, to):
	#Parametri del messaggio
	parametri = {
		'chat_id': to,
		'action': type,
	}
	#Manda la richiesta ai server di Telegram.
	requests.get("https://api.telegram.org/bot" + token + "/sendChatAction", params=parametri)

def getSteamStatus(steamid):
	#Parametri della richiesta
	parametri = {
		'key': steamtoken,
		'steamids': steamid,
	}
	#Manda la richiesta ai server di Steam e convertila in un dizionario
	r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=parametri).json()
	return r
	
def getOsuStatus(osuid, mode):
	#Parametri della richiesta
	parametri = {
		'k': osutoken,
		'u': osuid,
		'm': mode,
	}
	#Manda la richiesta ai server di Osu e convertila in un dizionario
	r = requests.get("https://osu.ppy.sh/api/get_user", params=parametri).json()
	return r

#Caricamento delle API Keys
token = readFile('telegramapi.txt')
steamtoken = readFile('steamapi.txt')
osutoken = readFile('osuapi.txt')

#Il loop del bot
while(True):
	#Ricevi gli ultimi messaggi
	data = getUpdates()
	#Se c'e' un nuovo messaggio
	if(data['ok']):
		if(data['result'] != []):
			#Aggiorna l'update ID sul file
			writeFile("lastid.txt", str(data['result'][0]['update_id'] + 1))
			#...esiste il messaggio? telegram wtf
			if(data['result'][0]['message'] is not None):
				#Leggi i dati del messaggio
				msg = data['result'][0]['message']
				#Ah, non lo so io!
				if(msg['text'].startswith("/ahnonlosoio")):
					sendMessage("Ah non lo so nemmeno io ¯\_(ツ)_/¯", msg['chat']['id'], msg['from']['id'])
				if(msg['text'].startswith("/ehoh")):
					sendMessage("Eh oh cose che capitano ¯\_(ツ)_/¯", msg['chat']['id'], msg['from']['id'])
				#Controlla lo stato di una persona su Steam.
				if(msg['text'].startswith("/steam")):
					#Se non viene specificato un
					if(msg['text'] == "/steam"):
						sendMessage(chr(9888) + " Non hai specificato uno SteamID o un username!", msg['chat']['id'], msg['from']['id'])
					else:
						#Royalbot sta scrivendo...
						setTyping('typing', msg['chat']['id'])
						#Controlla se la selezione è un username di telegram.
						if(msg['text'][7:].lower() in steamids):
							selezione = steamids[msg['text'][7:].lower()]
						else:
							selezione = msg['text'][7:]
						steam = getSteamStatus(selezione)
						if(steam['response']['players']):
							online = steam['response']['players'][0]['personastate']
							name = steam['response']['players'][0]['personaname']
							#E' in gioco? Se non c'è nessuna informazione sul gioco, lascia perdere
							try:
								steam['response']['players'][0]['gameextrainfo']
							except KeyError:
								ingame = None
							else:
								ingame = steam['response']['players'][0]['gameextrainfo']
							#Stati di Steam
							text = ""
							if(online == 0):
								text = chr(9898) + " _Offline_"
							elif(online == 1):
								text = chr(128309) + " _Online_"
							elif(online == 2):
								text = chr(128308) + " _Occupato_"
							elif(online == 3):
								text = chr(9899) + " _Assente_"
							elif(online == 4):
								text = chr(9899) + " _Addormentato_"
							elif(online == 5):
								text = chr(128309) + " _Disponibile per scambiare_"
							elif(online == 6):
								text = chr(128309) + " _Disponibile per giocare_"
							if ingame is not None:
								sendMessage("*" + name + "* sta giocando a " + chr(128308) + " " + ingame + ".", msg['chat']['id'], msg['from']['id'])
							else:
								sendMessage("*" + name + "* e' " + text + ".", msg['chat']['id'], msg['from']['id'])
						else:
							sendMessage(chr(9888) + " Lo SteamID o l'username non esiste!", msg['chat']['id'], msg['from']['id'])
				#Trova i punteggi di una persona su osu!
				if(msg['text'].startswith("/osu")):
					if(msg['text'] == "/osu"):
						sendMessage(chr(9888) + " Non hai specificato un PlayerID o un username di osu! o Telegram!", msg['chat']['id'], msg['from']['id'])
					else:
						#Controlla se la selezione è un username di telegram.
						if(msg['text'][5:].lower() in osuids):
							selezione = osuids[msg['text'][5:].lower()]
						else:
							selezione = msg['text'][5:]
						#Ricevi i dati di Osu e visualizza lo stato nella chat.
						setTyping('typing', msg['chat']['id'])
						osu = getOsuStatus(selezione, 0)
						setTyping('typing', msg['chat']['id'])
						taiko = getOsuStatus(selezione, 1)
						setTyping('typing', msg['chat']['id'])
						ctb = getOsuStatus(selezione, 2)
						setTyping('typing', msg['chat']['id'])
						osumania = getOsuStatus(selezione, 3)
						#Trova l'username della persona.
						name = osu[0]['username']
						#Trova i pp in ogni modalità
						if(osu[0]['pp_raw'] is not None):
							osupp = float(osu[0]['pp_raw'])
						else: 
							osupp = 0
						if(taiko[0]['pp_raw'] is not None):
							taikopp = float(taiko[0]['pp_raw'])
						else:
							taikopp = 0
						if(ctb[0]['pp_raw'] is not None):
							ctbpp = float(ctb[0]['pp_raw'])
						else: 
							ctbpp = 0
						if(osumania[0]['pp_raw'] is not None):
							osumaniapp = float(osumania[0]['pp_raw'])
						else:
							osumaniapp = 0
						#Manda il messaggio
						sendMessage("*" + name + "* ha:" + chr(10) + "_" + str(int(osupp)) + "pp_ su Osu!" + chr(10) + "_" + str(int(taikopp)) + "pp_ su Taiko" + chr(10) + "_" + str(int(ctbpp)) + "pp_ su Catch the Beat" + chr(10) + "_" + str(int(osumaniapp)) + "pp_ su Osu!mania", msg['chat']['id'], msg['from']['id'])