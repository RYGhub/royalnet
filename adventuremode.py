# -*- coding: utf-8 -*-
import requests
import json

#Inizializza la API Key di Telegram
token = ""

#Ultimo messaggio mandato dal bot.
lastmsg = ""

#Nascondi la tastiera.
no_keyboard = {
	'hide_keyboard': True,
}
json.dumps(no_keyboard)

#Gruppo di destinazione
target_group = -2141322

#Manda un messaggio.
def sendMessage(content, tastiera=no_keyboard, to=target_group):
	#Parametri del messaggio
	parametri = {
		'chat_id': to, #L'ID della chat a cui mandare il messaggio, Royal Games: -2141322
		'text': content, #Il messaggio da mandare
		'reply_markup': tastiera
	}
	#Manda il messaggio
	r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage", params=parametri)
	
#Leggi un file e rispondi con il contenuto!
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
	
#Caricamento delle API Keys...
token = readFile('telegramapi.txt')

def getUpdates():
	#Parametri della richiesta da fare
	parametri = {
		'offset': readFile("lastid.txt"), #Update ID del messaggio da leggere
		'limit': 1, #Numero di messaggi da ricevere alla volta, lasciare 1
		'timeout': 300, #Secondi da mantenere attiva la richiesta se non c'e' nessun messaggio
	}
	#Manda la richiesta ai server di Telegram e convertila in un dizionario
	data = requests.get("https://api.telegram.org/bot" + token + "/getUpdates", params=parametri).json()
	if(data['ok']):
		if(data['result'] != []):
			#Aggiorna l'update ID sul file
			writeFile("lastid.txt", str(data['result'][0]['update_id'] + 1))
			#...esiste il messaggio? telegram wtf
			if(data['result'][0]['message'] is not None):
				return data['result'][0]['message']

#############################################
## Qui inizia la roba che serve a te, max! ##
#############################################

#Scrivi la storia!
def racconto(testo):
	print(testo)
	sendMessage(testo)

#Apri una tastiera con due scelte
def treScelte(puno, pdue, ptre):
	tastiera = {
		'keyboard':	[[puno, pdue, ptre]],
		'one_time_keyboard': True,
	}
	print("Cosa vuoi fare?\n1: " + puno + "\n2: " + pdue + "\n3: " + ptre)
	sendMessage("Cosa vuoi fare?\n1: " + puno + "\n2: " + pdue + "\n3: " + ptre, json.dumps(tastiera))
	#Aspetta una risposta...
	waiting = True
	while(waiting):
		msg = getUpdates()
		if(msg['text'] == puno):
			return 1
		elif(msg['text'] == pdue):
			return 2
		elif(msg['text'] == ptre):
			return 3
	
r = treScelte("Banana", "Fragola", "Frankez")
if(r == 1):
	racconto("Ottima scelta, una banana fresca, proprio come Frank!")
elif(r == 2):
	racconto("Bah, secondo me era molto meglio una banana...")
elif(r == 3):
	racconto("Frankez è una banana, quindi perchè non hai scelto direttamente quella?")
racconto("Fine dello script")