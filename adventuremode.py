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
target_group = -13164589

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
			if(data['result'][0]['message']['text'] is not None):
				return data['result'][0]['message']
			else:
				raise KeyError("Qualcosa nel messaggio di Telegram è andato storto. Molto storto.")

#############################################
## Qui inizia la roba che serve a te, max! ##
#############################################

#Vita iniziale!
hp = 100

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
	sendMessage(chr(10067) + "Cosa vuoi fare?\n1: " + puno + "\n2: " + pdue + "\n3: " + ptre, json.dumps(tastiera))
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
			
#Modifica la vita. Mettere valori negativi per ridurla, positivi per aumentarla.
def vita(var):
	hp = hp + var

#############################
## Qui inizia la storia... ##
#############################
#Copyright @MaxSensei 2015
sendMessage("Benvenuto a Royal Bot Adventures!\nVERSIONE ALPHA QUINDI PIENA DI BUG\nStoria scritta da @MaxSensei")
racconto("Vi svegliate in un luogo del tutto buio, sentite un flebile respiro da qualche parte nel buio. Tastate la vostra fedelissima spada. Cercate di ricordare qualcosa ma con scarso successo (originale eh?). ")
while(True):
	s = treScelte("Brandite la spada verso i respiri nel buio", "Chiedete chi è ad alta voce", "State zitti e immobili")
	if(s == 1):
		racconto("Ahia! Tu e la tua compagnia vi colpite a vicenda con le spade.")
	elif(s == 2):
		racconto("Riconoscete i vostri amici e vi ritenete fortunati di non aver ferito nessuno.")
		break
	elif(s == 3):
		racconto("Che codardi, tanto non succede nulla...")
		break
racconto("Siete in un luogo del tutto buio, ma vedete della luce molto lontano.")
while(True):
	s = treScelte("Esaminate il luogo circostante", "Muovetevi nella direzione della luce", "Ispezionatevi")
	if(s == 1):
		racconto("Sembrate constatare che il pavimento sia fatto di dura roccia e le parenti intorno non si sentono, tastate per terra quello che sembra una candela spenta (utile eh?).\nDecidete di lasciarla per terra visto che non avete tasche e le mani vi servono ad orientarvi.")
	elif(s == 2):
		racconto("Brancolate nel buio nella direzione della luce, inciampate in qualcosa e vi spaccate il naso per terra.")
	elif(s == 3):
		racconto("Vi ritrovate in dei vestiti pesanti e grossi, pieni di tasche.")
		break
racconto("Ad una accurata ispezione trovate un barattolo contenente qualcosa che sembra liquido.")
while(True):
	s = treScelte("Bevete il liquido", "Vi spalmate addosso il liquido", "Introducete nella cavità anale")
	if(s == 1):
		racconto("Ha un sapore orribile!\nVi sentite male...")
	elif(s == 2):
		racconto("Congratulazioni, ora siete coperti di feci di origini sconosciute!")
	elif(s == 3):
		racconto("Sentite all'improvviso una forza sconosciuta pervadervi tutto il corpo;\n vi concentrate, e riuscite a far splendere le vostre splendide chiappe più del sole in estate.")
		break
racconto("The End?")
