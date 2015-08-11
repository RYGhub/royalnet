# -*- coding: utf-8 -*-

import requests #Modulo per fare richieste su HTTP
import time #Modulo per mettere in pausa il programma
import math #Matematica. u_u

#Ultimo messaggio mandato dal bot.
lastmsg = ""

#Inizializzazione keys
token = ""
steamtoken = ""
osutoken = ""

#Elenco degli steamid e degli username di telegram.
steamids =  {
	'@Steffo': 76561198034314260,
	'@EvilBaluIsEvilT_T': 76561198071012695,
	'@Fultz': 76561198035547490,
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
	print("Mando richiesta...")
	r = requests.get("https://osu.ppy.sh/api/get_user", params=parametri).json()
	print("Ricevuta!")
	print(r)
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
	if(data['ok'] and data['result']):
		#Aggiorna l'update ID sul file
		writeFile("lastid.txt", str(data['result'][0]['update_id'] + 1))
		#Leggi i dati del messaggio
		msg = data['result'][0]['message']
		#Ah, non lo so io!
		if(msg['text'].startswith("/ahnonlosoio")):
			sendMessage("Ah non lo so nemmeno io ¯\_(ツ)_/¯", msg['chat']['id'], msg['from']['id'])
		#Controlla lo stato di una persona su Steam.
		if(msg['text'].startswith("/steam")):
			#Se non viene specificato un
			if(msg['text'] == "/steam"):
				sendMessage(unichr(9888) + " Non hai specificato uno SteamID o un username!", msg['chat']['id'], msg['from']['id'])
			else:
				#Controlla se la selezione è un username di telegram.
				if(msg['text'][7:] in steamids ):
					selezione = steamids[msg['text'][7:]]
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
						text = unichr(9898) + " Offline"
					elif(online == 1):
						text = unichr(55357) + unichr(56629) + " Online"
					elif(online == 2):
						text = unichr(55357) + unichr(56628) + " Occupato"
					elif(online == 3):
						text = unichr(9899) + " Assente"
					elif(online == 4):
						text = unichr(9899) + " Inattivo"
					elif(online == 5):
						text = unichr(55357) + unichr(56629) + " Disponibile per scambiare"
					elif(online == 6):
						text = unichr(55357) + unichr(56629) + " Disponibile per giocare"
					if ingame is not None:
						sendMessage(name + " sta giocando a " + unichr(55357) + unichr(56628) + " " + ingame + ".", msg['chat']['id'], msg['from']['id'])
					else:
						sendMessage(name + " e' " + text + ".", msg['chat']['id'], msg['from']['id'])
				else:
					sendMessage(unichr(9888) + " Lo SteamID o l'username non esiste!", msg['chat']['id'], msg['from']['id'])
		#Trova i punteggi di una persona su osu!
		if(msg['text'].startswith("/osu")):
			if(msg['text'] == "/osu"):
				sendMessage(unichr(9888) + " Non hai specificato un PlayerID o un username di osu! o Telegram!", msg['chat']['id'], msg['from']['id'])
			else:
				#Persona selezionata
				selezione = msg['text'][5:]
				#Ricevi i dati di Osu
				osu = getOsuStatus(selezione, 0)
				taiko = getOsuStatus(selezione, 1)
				ctb = getOsuStatus(selezione, 2)
				osumania = getOsuStatus(selezione, 3)
				#Trova l'username della persona.
				name = osu[0]['username']
				#Trova i pp in ogni modalità
				osupp = math.floor(float(osu[0]['pp_raw']))
				taikopp = math.floor(float(taiko[0]['pp_raw']))
				ctbpp = math.floor(float(ctb[0]['pp_raw']))
				osumaniapp = math.floor(float(osumania[0]['pp_raw']))
				#Manda il messaggio
				sendMessage(name + " ha:" + unichr(10) + osupp + "pp su Osu!" + unichr(10) + taikopp + "pp su Taiko" + unichr(10) + ctbpp + "pp su Catch the Beat" + unichr(10) + osumaniapp + "pp su Osu!mania")