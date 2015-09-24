# -*- coding: utf-8 -*-
import requests
import json
import sys
import random

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
		'chat_id': to, #L'ID della chat a cui mandare il messaggio, Royal Games: -2141322 Royal Bot Testing Group: -13164589
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
	while(True):	
		data = requests.get("https://api.telegram.org/bot" + token + "/getUpdates", params=parametri).json()
		if(data['ok'] == True):
			if(data['result'] != []):
				#Aggiorna l'update ID sul file
				writeFile("lastid.txt", str(data['result'][0]['update_id'] + 1))
				#...esiste il messaggio? telegram wtf
				if(data['result'][0]['message'] != None):
					if(data['result'][0]['message']['text'] != ""):
						return data['result'][0]['message']
					else:
						raise KeyError("Qualcosa nel messaggio di Telegram è andato storto. Molto storto.")
				else:
					raise KeyError("Qualcosa nel messaggio di Telegram è andato storto. Molto storto.")

#############################################
## Qui inizia la roba che serve a te, max! ##
#############################################

#Vita iniziale!
hp = 100

#La candela!
candela = False

#Scrivi la storia!
def racconto(testo):
	sendMessage(testo)

#Apri una tastiera con due scelte
def treScelte(puno, pdue, ptre):
	tastiera = {
		'keyboard':	[[puno, pdue, ptre]],
		'one_time_keyboard': True,
	}
	sendMessage(chr(10067) + "Cosa volete fare?\n1: " + puno + "\n2: " + pdue + "\n3: " + ptre, json.dumps(tastiera))
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
	global hp
	hp = hp + var
	sendMessage(chr(10084) + ' ' + str(var) + "\n" + "Ora avete " + str(hp) + " punti vita.")
	if(hp <= 0):
		sendMessage("Hai finito la vita! Game over!")
		sys.exit()

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
		vita(-15)
	elif(s == 2):
		racconto("Riconoscete i vostri amici e vi ritenete fortunati di non aver ferito nessuno.")
		break
	elif(s == 3):
		racconto("Che codardi, tanto non succede nulla...")
		break
racconto("Siete in un luogo del tutto buio, ma vedete della luce molto lontano.")
while(True):
	s = treScelte("Esaminate il luogo circostante", "Muovetevi nella direzione della luce", "Controllate i vostri vestiti")
	if(s == 1):
		racconto("Sembrate constatare che il pavimento sia fatto di dura roccia e le parenti intorno non si sentono, tastate per terra quello che sembra una candela spenta (utile eh?).")
		candela = True
	elif(s == 2):
		if(candela == False):
			racconto("Brancolate nel buio nella direzione della luce, inciampate in qualcosa e vi spaccate il naso per terra.")
			vita(-10)
			racconto("Scavando nella dura roccia. Scoprite di essere incastrati in un qualcosa simile a una radice, ma grossa e semovente.")
			c = treScelte("Proseguite verso la luce con cautela", "Correte verso la luce", "Tornate indietro")
		elif(candela == True):
			racconto("Vi dirigete verso la luce, ma scoprite che un enorme pianta vi intralcia la strada. Si sentono soffocati fruscii nel terreno in cui penetra la radice.")
			racconto("La candela per fortuna si é rivelata essere elettrica per mancanza di fantasia dell'autore, e premendo un pulsantino sul lato illumina l'area circostante. La luce non é abbastanza da illuminare del tutto la caverna, ma potete almeno vedere ciò su cui camminate.")
			c = treScelte("Proseguite verso la luce sicuri di voi stessi", "Correte verso la luce", "Esaminate la pianta")
		if(c == 1) and (candela == True):
			racconto("Vi addentrate nella caverna, dove la sala si estende nelle profondità della terra. Ad un certo punto del cammino siete costretti a interrompere il viaggio a causa di un bivio. Alla luce della vostra candela qualcosa risplende sulla sinistra, ma allo stesso momento qualcosa emana una luce rossa di suo sulla destra...")
			while(True):
				v = treScelte("Controllate a sinistra", "Procedete spavaldi verso destra", "Inventate il primo *facewall*")
				if(v == 1):
					racconto("Svoltate a sinistra verso lo scintillio. Trovate un ascia, circondata da rune naniche, per terra. Mentre la pulite dall'enorme quantità di ragnatele, vi accorgete di essere a vostra volta avvolti da fili duri e sottili. Un ragno mostruoso vi spunta davanti.")
					r = treScelte("Affrontate il ragno usando l'ascia", "Scappate urlando come ragazzine", "Vi pisciate addosso molto forte")
					if(r == 1):
						racconto("Il piccolo ragnetto impaurito esplode sotto l'enorme peso della vostra ascia. Quest'ultima però si rompe in mille schegge a causa dell'urto.")
						racconto("Congratulazioni, vi siete salvati!")
						sendMessage("Conclusione #3! Rigiocate per scoprire le altre.")
						break
					elif(r == 2):
						racconto("Cercate di scappare, ma inciampate nelle ragnatele. Cadete di faccia sul povero ragnetto, spiaccicandolo. Svenite. (Molto anticlimatico, lo so, ma siete voi che fate scelte da imbranati)")
						sendMessage("Continua...")
						break
					elif(r == 3):
						racconto("La piscia cola dai vostri pantaloni, inondando la caverna e lasciandovi senza ossigeno. Il ragnetto vi osserva stupito e si nasconde nelle ragnatele.")
						vita(-100)
				elif(v == 2):
					#Non succede nulla. Per ora.
					sendMessage("Qui non c'è nulla, per ora... Max mandami quel coso")
				elif(v == 3):
					racconto("Ahi, che male! La vostra intelligenza aumenta di " + str(random.randint(1, 7)) + " punti.")
					vita(-10)
			#Coso buttato lì perchè non mi viene in mente un modo migliore. Eh, vabbè.
			break
		elif(c == 1):
			racconto("Osservate da vicino quello che pare essere un'enorme radice che inizia dai meandri oscuri del soffitto e scende giù, perforando con facilità il duro granito. Il tentacolo affonda sempre più giù e potete sentire come rompe e sgretola la terra sottostante...")
			vita(-2)
		elif(c == 2):
			racconto("Avanzate correndo verso la luce, e inciampate in altri tentacoli, subendo solo un po' di danni. Quello che all'inizio sembrava essere un alone di luce si rivelò essere un piccolo varco nella parete. I vostri occhi, ormai abituati al buio, non distinguono chiaramente quello che c'è oltre.")
			vita(-10)
		elif(c == 3) and (candela == True):
			racconto("Vedete crepe ovunque, e la pianta che penetra nel terreno creandone altre...")
		if(c == 1) or (c == 2) or ((c == 3) and (candela == True)):
			racconto("La terra inizia a tremare e grosse crepe iniziano a comprarire nel terreno, le grosse radici vengono rapidamente rissuchiate nel soffito immenso, e un orribile ruggito vi spacca le orecchie. Siete assordati, e non potete sentire nulla.")
			racconto("Avete il presentimento che qualcosa di terribile stia per accadere.")
			b = treScelte("Scappate via dalla zona crepata", "Rimanete come idioti a guardare l'avvenimento", "Vi buttate al centro del buco")
			if(b == 1):
				racconto("Vi buttate fuori dal buco appena in tempo, e sentite una forta esplosione alle vostre spalle... Con una forza possente venite spinti giù dalla montagna. Cadete facendo un'incredibile fracasso e sentite un male allucinante. Siete sull'orlo di svenire. Con le ultime forze vi girate ad osservare la scena. Un enorme creatura grande come il picco della montagna si stava levando in cielo, una mastodontica isola composta da tentacoli e occhi gialli. Un enorme tentacolo continua ad essere attaccato nel centro di quello che una volta era un gigantesco picco, finchè non crollò su se stesso ed implose. La grossa nube volò lentamente emettendo il suo ruggito di trionfo sopra di voi, e in quel preciso istante le palpebre divennero troppo pesanti e cedettero.")
				sendMessage("Conclusione #1! Rigiocate per scoprire le altre.")
				break
			elif(b == 2):
				racconto("Ottima scelta! Il soffito all'improvviso si stacca con un forte boato, inondando la caverna di luce. Grossi tentacoli si ritraggono da sotto il suolo, e la terra inizia a sgretolarsi sotto i vostri piedi. Fate in tempo a vedere un enorme tentacolo al centro del pavimento. Improvvisamente, il tentacolo iniziò a gonfiarsi e tutto il mondo intorno implose. Svenite.")
				sendMessage("Conclusione #2! Rigiocate per scoprire le altre.")
				break
			elif(b == 3):
				racconto("Siete proprio pirla... La montagna si avvolge su sè stessa e, avvolti da lava e roccia, spiaccicati con una forza enorme, perite.")
				vita(-100)
	elif(s == 3):
		racconto("Vi ritrovate in dei vestiti pesanti e grossi, pieni di tasche.")
		racconto("Ad una accurata ispezione trovate un barattolo contenente qualcosa che sembra liquido.")
		while(True):
			s = treScelte("Bevete il liquido", "Vi spalmate addosso il liquido", "Introducete nella cavità anale")
			if(s == 1):
				racconto("Ha un sapore orribile!\nVi sentite male...")
				vita(-10)
			elif(s == 2):
				racconto("Congratulazioni, ora siete coperti di feci di origini sconosciute!")
				vita(-2)
			elif(s == 3):
				racconto("Sentite all'improvviso una forza sconosciuta pervadervi tutto il corpo;\n vi concentrate, e riuscite a far splendere le vostre splendide chiappe più del sole in estate.")
				break
		#Coso buttato lì perchè non mi viene in mente un modo migliore. Eh, vabbè.
		break
racconto("THE END!")