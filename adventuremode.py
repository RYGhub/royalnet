# -*- coding: utf-8 -*-
import requests
import json
import sys
import random
import time

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
def sendMessage(content, tastiera="", to=target_group):
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
						print(str(data['result'][0]['update_id']) + ": " + data['result'][0]['message']['text'])
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
	sendMessage(chr(128172) + " " + testo, no_keyboard)

#Apri una tastiera con due scelte
def treScelte(puno, pdue, ptre):
	tastiera = {
		'keyboard':	[[puno, pdue, ptre]],
		'one_time_keyboard': True,
	}
	time.sleep(4)
	sendMessage(chr(10067) + " Cosa volete fare?\n1: " + puno + "\n2: " + pdue + "\n3: " + ptre, json.dumps(tastiera))
	#Aspetta una risposta...
	while(True):
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
sendMessage("Benvenuto a Royal Bot Adventures !\nStoria scritta da @MaxSensei")
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
			racconto("Notate che nel pavimento c'è qualcosa di simile a una radice, ma grossa e sembra quasi che si stia muovendo.")
			c = treScelte("Proseguite verso la luce con cautela", "Correte in direzione opposta", "Tornate indietro")
		elif(candela == True):
			racconto("La candela per fortuna si é rivelata essere elettrica per mancanza di fantasia dell'autore, e premendo un pulsantino sul lato illumina l'area circostante. \nLa luce non é abbastanza da illuminare del tutto la caverna, ma potete almeno vedere ciò su cui camminate.")
			racconto("Vi dirigete verso la luce, ma scoprite che un enorme pianta vi intralcia la strada. \nSi sentono soffocati fruscii nel terreno in cui penetrano le radici.")
			c = treScelte("Proseguite verso la luce sicuri di non inciampare", "Correte in direzione opposta", "Esaminate la pianta")
		if(c == 1) and (candela == True):
			racconto("Vi addentrate nella caverna, dove una sala si estende nelle profondità della terra. \nAd un certo punto del cammino siete costretti a interrompere il viaggio a causa di un bivio. La luce che stavate seguendo prima risplende sulla sinistra, ma allo stesso momento qualcosa emana una luce rossa di suo sulla destra...")
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
						sendMessage("Conclusione #4! Rigiocate per scoprire le altre.")
						break
					elif(r == 3):
						racconto("La piscia cola dai vostri pantaloni, inondando la caverna e lasciandovi senza ossigeno. Il ragnetto vi osserva stupito e si nasconde nelle ragnatele.")
						vita(-100)
				elif(v == 2):
					racconto("Man mano che vi addentrate sempre di più nelle profondità del tunnel, una luce rossa pervade le pareti, sempre più luminosa, finchè non svoltate. Ai vostri occhi si rivela un gigantesco portone nanico, ornato da una moltitudine di rune e circondato da un ruscello di lava.")
					racconto("All'improvviso sentite la terra tremare e udite un ruggito potentissimo echeggiare. Pochi secondi dopo un corno risuona nelle vicinanze, e i portoni iniziano lentamente a chiudersi (Sto pensando a te, portale nero di Mordor)")
					p = treScelte("Correte più veloce che potete attraverso le porte", "Vi nascondete e cercate un riparo nella caverna", "Vi grattate le palle")
					if(p == 1):
						racconto("Più veloce che potete correte verso gli enormi portoni che si stanno lentamente chiudendo di fronte a voi. Col cuore a mille vedete crollare stalattiti ovunque, una delle quali vi colpisce forte sulla spalla, ma riuscite a saltare un secondo prima di venire schiacciati.")
						vita(-35)
						racconto("Di fronte a voi si estende una delle più grandi città naniche del mondo, ma storditi e feriti, non riuscite a coglierne tutta la sua bellezza. Le case più fragili crollano intorno e piccoli ma robusti omini nel panico cercano un rifugio in un grande castello. Sentite un altro ruggito, e il mondo si trasforma in zolfo ed esplosioni. L'ultima cosa che ricordate sono dolori atroci ovunque...")
						sendMessage("Conclusione #5! Rigiocate per scoprire le altre.")
						break
					elif(p == 2):
						racconto("Rinunciate ad attraversare i portoni, siete infatti dubbiosi dell'ospitalità dei nani. \nPiuttosto decidete di cercare riparo nella caverna. \nVi nascondete dentro una cavità nella parete dall'aspetto solido. \nSentite suoni di esplosioni e roccia sgretolarsi ovunque, e dalla paura vi viene un infarto.")
						vita(-100)
					elif(p == 3):
						racconto("Mmmmh, che bello grattarsi! Ora però sentite prurito al culo...")
						treScelte("Grattatevi", "Grattatevi", "Grattatevi")
						racconto("Aaaaah, che piacere! Ma vi viene prurito al pancino...")
						treScelte("Grattatevi", "Grattatevi", "Grattatevi")
						racconto("Una stalattite enorme cade molto vicino a voi, e sentite diffondersi un prurito incredibile nelle ascelle...")
						treScelte("Grattatevi", "Grattatevi", "Grattatevi")
						racconto("Una stalattite vi arriva in testa, vi buca il cervello e morite. Il tutto mentre avevate prurito al naso...")
						vita(-100)
				elif(v == 3):
					x = str(random.randint(1, 10))
					racconto("Ahi, che male! La vostra intelligenza aumenta di " + x + " punti.")
					vita(-10)
			#Coso buttato lì perchè non mi viene in mente un modo migliore per fare the end. Eh, vabbè.
			break
		elif(c == 1):
			racconto("Osservate da vicino quella che pare essere un'enorme radice che inizia dai meandri oscuri del soffitto e scende giù, perforando con facilità il duro granito. La radice affonda sempre più giù e potete sentire come rompe e sgretola la terra sottostante...")
			vita(-2)
		elif(c == 2):
			racconto("Avanzate correndo verso la parete opposta, ma inciampate in altre radici, subendo solo dei danni. Notate un piccolo varco nella parete. I vostri occhi, ormai abituati al buio, non distinguono chiaramente quello che c'è oltre.")
			vita(-10)
		elif(c == 3) and (candela == True):
			racconto("Vedete crepe ovunque, e la pianta che penetra nel terreno creandone altre...")
		if(c == 1) or (c == 2) or ((c == 3) and (candela == True)):
			racconto("La terra inizia a tremare e grosse crepe iniziano a comprarire nel terreno. \nGrosse radici, ora illuminate dalla luce del sole, vengono rapidamente rissuchiate nel soffito immenso. \nUn orribile ruggito vi spacca le orecchie. Siete assordati, e non potete sentire nulla.")
			racconto("Avete il presentimento che qualcosa di terribile stia per accadere.")
			b = treScelte("Buttatevi fuori dalla zona crepata", "Rimanete come idioti a guardare l'avvenimento", "Correte in direzione dello scintillio che si vede in lontananza")
			if(b == 1):
				racconto("Vi buttate fuori dal buco appena in tempo, e sentite una forte esplosione alle vostre spalle... Con una forza possente venite spinti giù dalla montagna. Cadete facendo un'incredibile fracasso e sentite un male allucinante. Siete sull'orlo di svenire. Con le ultime forze vi girate ad osservare la scena. Un enorme creatura grande come il picco della montagna si stava levando in cielo, una mastodontica isola composta da tentacoli e occhi gialli. Un enorme tentacolo continuava ad essere attaccato nel centro di quello che una volta era un gigantesco picco, finchè non crollò su se stesso ed implose. La grossa nube volava lentamente, emettendo il suo ruggito di trionfo sopra di voi, e in quel preciso istante le palpebre divennero troppo pesanti e cedettero.")
				sendMessage("Conclusione #1! Rigiocate per scoprire le altre.")
				break
			elif(b == 2):
				racconto("Il soffito all'improvviso si stacca con un forte boato, inondando la caverna di luce. Grossi tentacoli si ritraggono da sotto il suolo, e la terra inizia a sgretolarsi sotto i vostri piedi. Fate in tempo a vedere un enorme tentacolo al centro del pavimento. Improvvisamente, il tentacolo inizia a gonfiarsi e tutto il mondo intorno implode. Svenite.")
				sendMessage("Conclusione #2! Rigiocate per scoprire le altre.")
				break
			elif(b == 3):
				racconto("Siete proprio pirla... Intravedete qualcosa a forma di ascia, ma non fate in tempo a raggiungerla che la montagna si avvolge su sè stessa e, avvolti da lava e roccia, spiaccicati con una forza enorme, perite.")
				vita(-100)
	elif(s == 3):
		racconto("Vi ritrovate in dei vestiti pesanti e grossi, pieni di tasche.")
		racconto("Ad una accurata ispezione trovate una bottiglia contenente qualcosa che sembra liquido. Sull'etichetta vi è raffigurata una lucciola.")
		while(True):
			s = treScelte("Bevete il liquido", "Vi spalmate addosso il liquido", "Introducete nella cavità anale")
			if(s == 1):
				racconto("Ha un sapore orribile!\nVi sentite male...")
				vita(-10)
			elif(s == 2):
				racconto("Congratulazioni, ora siete coperti di merda di origini sconosciute!")
				vita(-2)
			elif(s == 3):
				racconto("Sentite all'improvviso una forza sconosciuta pervadervi tutto il corpo; vi concentrate, e riuscite a far splendere le vostre splendide chiappe più del sole in estate.")
				racconto("Le vostre chiappe risplendono più del sole, e illuminano tutta la caverna. Vi stupite dalla sua immensità: sembra il picco di una montagna, ma avvolto da una specie di enorme pianta, le cui radici entrano qua e là nel terreno. \nOsservate anche tante sfere gialle alle estremità della caverna. Esattamente al centro, c'é una specie di enorme pilastro...")
				while(True):
					h = treScelte("Lodate la bellezza delle vostre chiappe", "Esaminate le radici", "Esaminate il grosso pilastro")
					if(h == 1):
						racconto("Lodate la bellezza del vostro culo e ammirate il modo in cui non succede niente!")
					elif(h == 2):
						racconto("Quelle che a prima vista sembravano radici in realtà sono grossi tentacoli verdognoli che penetrano dal soffito verso il terreno, scavandolo in profondità. \nNotate alla chiara luce dei vostri glutei che sono semitrasparenti, e potete vedere un liquido rossastro e luminoso scorrere al loro interno.")
						break
					elif(h == 3):
						racconto("Esaminate l'enorme pilastro al centro della caverna per scoprire che in realtà é un enorme tentacolo! Dentro potete vedete confluire altri tentacoli. \nNotate che é semitrasparente, e potete vedere come pietra incandescente e lava scorrono al suo interno. \nNotate anche un luccichio che sembra provenire da gemme all'interno.")
						break
				racconto("All'improvviso la terra inizia a tremare e i tentacoli uno ad uno vengono risucchiati nel soffito, mentre il tentacolo madre inizia a gonfiarsi, raggiungendo dimensioni enormi...")
				racconto("In una parete notate una crepa che potrebbe condurvi all'uscita della caverna.")
				b = treScelte("Andate verso la crepa", "Aggrappatevi ad un tentacolo", "Abbracciate il grosso tentacolo centrale, magari ha solo bisogno di amore")
				if(b == 1):
					racconto("Raggiungete la crepa e cercate di attraversarla, ma notate che il vostro culo oltre a illuminarsi si é anche ingrandito! \nRimanete incastrati nella fessura. All'improvviso sentite un fortissimo ruggito, e le vostre chiappe, in preda alla paura, si contraggono, esplodendo e rilasciando tutta la luminescenza in forma di propulsione. \nSchizzate alla velocità della luce fuori dalla montagna, e fuori dai confini della città nanica al suo esterno. L'ultima cosa che vedete é una casetta sull'albero in un bosco. La attraversate come un proiettile e svenite.")
					sendMessage("Conclusione #5! Rigiocate per scoprire le altre.")
				elif(b == 2):
					racconto("Vi aggrappate al tentacolo più vicino, e appena lo toccate questo schizza verso alto, entrando nel soffito e portandovi dietro. \nAll'improvviso l'intera pianta si stacca dalla montagna e inizia a volare sempre più in alto nel cielo. \nGuardate sotto e vedete come l'enorme tentacolo madre sia ancora attaccato alla montagna. \nNon aveste mai pensato che esso si rimpicciolisse all'istante, rilasciando sotto forma di vapore la roccia incandescente, facendo esplodere la montagna e dando un'ulteriore spinta all'isola pianta volante... \nIl tentacolo a cui pensavate di essere aggrappati invece si aggrappa a sua volta a voi e vi risucchia all'interno di una strana membrana... Svenite e sognate unicorni che sparano arcobaleni e bagni nello spazio profondo.")
					sendMessage("Conclusione #6! Rigiocate per scoprire le altre.")
				elif(b == 3):
					racconto("Abbracciate il tentacolo madre con un sorriso stampato sulle labbra. Vi divertite tantissimo a raccontare in paradiso di come siete esploso e di come i vostri pezzettini siano stati ritrovati nei 5 continenti.")
					vita(-100)
				break
		#Coso buttato lì perchè non mi viene in mente un modo migliore per fare the end. Eh, vabbè.
		break
sendMessage("THE END!")