# -*- coding: latin-1 -*-

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
	r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=parametri).json().decode('utf-8')
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
		if(msg['text'] == "/ahnonlosoio"):
			sendMessage("Ah non lo so nemmeno io ¯\_(ツ)_/¯", msg['chat']['id'])
		if(msg['text'].startswith("/steam")):
			if(msg['text'] == "/steam"):
				sendMessage("Specifica lo steamid della persona di cui vuoi specificare lo stato. Tag di telegram coming soon!", msg['chat']['id'])
			else:
				steam = getSteamStatus(msg['text'][7:])
				if(steam['response']['players']):
					online = steam['response']['players'][0]['personastate']
					name = steam['response']['players'][0]['personaname']
					text = ""
					if(online == 0):
						text = "Offline"
					elif(online == 1):
						text = "Online"
					elif(online == 2):
						text = "Occupato"
					elif(online == 3):
						text = "Assente"
					elif(online == 4):
						text = "Inattivo"
					elif(online == 5):
						text = "Disponibile per scambiare"
					elif(online == 6):
						text = "Disponibile per giocare"
					sendMessage(name + " è " + text + ".", msg['chat']['id'])
				else:
					sendMessage("Lo steamid non esiste!", msg['chat']['id'])