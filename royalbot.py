# -*- coding: utf-8 -*-

import requests #Modulo per fare richieste su HTTP
import time #Modulo per mettere in pausa il programma

#Token del bot, non diffondere
token = "120621161:AAHeVgQhlfGx36KT9NyGemauZBPEbe9Xfv0"

#Token di Steam, per /steam
steamtoken = "042E26965C7AA24487FEBA6205017315"

#Ultimo messaggio mandato dal bot.
lastmsg = ""

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
def sendMessage(content, to):
	#Parametri del messaggio
	parametri = {
		'chat_id': to, #L'ID della chat a cui mandare il messaggio, Royal Games: -2141322
		'text': content, #Il messaggio da mandare
	}
	#Antispam: manda il messaggio solo se l'ultimo messaggio è diverso da quello che deve mandare ora.
	global lastmsg
	if(lastmsg != content):
		#Manda il messaggio
		r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage", params=parametri)
		lastmsg = content
	else:
		print("Tentativo di spam rilevato.")

def getSteamStatus(steamid):
	#Parametri della richiesta
	parametri = {
		'key': steamtoken,
		'steamids': steamid,
	}
	#Manda la richiesta ai server di Telegram e convertila in un dizionario
	r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=parametri).json()
	return r
	
#Il loop del bot
while(True):
	#Ricevi gli ultimi messaggi
	data = getUpdates()
	#Se c'e' un nuovo messaggio
	if(data['ok'] and data['result']):
		#Aggiorna l'update ID sul file
		writeFile("lastid.txt", str(data['result'][0]['update_id'] + 1))
		#Leggi i dati del messaggio
		msg = data['result'][0]['message']
		#Ah, non lo so io!
		if(msg['text'].startswith("/ahnonlosoio")):
			sendMessage("Ah non lo so nemmeno io ¯\_(?)_/¯", msg['chat']['id'])
		#Controlla lo stato di una persona su Steam.
		if(msg['text'].startswith("/steam")):
			#Se non viene specificato un
			if(msg['text'] == "/steam"):
				sendMessage("\u26A0 Non hai specificato uno steamid!", msg['chat']['id'])
			else:
				#Elenco degli steamid e degli username di telegram.
				steamids = {
					'@Steffo': 76561198034314260,
					'@EvilBaluIsEvilT_T': 76561198071012695,
					'@Fulz': 76561198035547490,
					'@IlGattopardo': 76561198111021344,
					'@FrankFrankFrank': 76561198071099951,
					'@fedYal': 76561198109189938,
					'@ActerRYG': 76561198146704979,
					'@YouTouchMyTralala': 76561198121094516,
					'@Heisenberg_TheMadDoctor': 76561198080377213,
					'@SuperMattemb': 76561198115852550,
					'@Peraemela99': 76561198161867082,
					'@thevagginadestroyer': 76561198128738388,
					'Fillo': 76561198103292029,
					'@Cosimo03': 76561198062778224,
					'Alby': 76561198071383448,
					'@Voltaggio': 76561198147601821,
					'Alle2002': 76561198052996311,
					'Jummi': 76561198169975999,
					'@Tauei': 76561198104305298,
					'@Saitorlock': 76561198089120441,
					'@iEmax': 76561198149695151,
					'@Alleanderl': 76561198154175301,
					'@Boni3099': 76561198131868211,
				}
				#Controlla se la selezione è un username di telegram.
				if(steamids[msg['text'][7:]]):
					selezione = steamids[msg['text'][7:]]
				else:
					selezione = msg['text'][7:]
				steam = getSteamStatus(selezione)
				if(steam['response']['players']):
					online = steam['response']['players'][0]['personastate']
					name = steam['response']['players'][0]['personaname']
					text = ""
					if(online == 0):
						text = "\u26AA Offline"
					elif(online == 1):
						text = "\U1F535 Online"
					elif(online == 2):
						text = "\U1F534 Occupato"
					elif(online == 3):
						text = "\u26AB Assente"
					elif(online == 4):
						text = "\u26AB Inattivo"
					elif(online == 5):
						text = "\U1F535 Disponibile per scambiare"
					elif(online == 6):
						text = "\U1F535 Disponibile per giocare"
					sendMessage(name + " e' " + text + ".", msg['chat']['id'])
				else:
					sendMessage("Lo steamid non esiste!", msg['chat']['id'])