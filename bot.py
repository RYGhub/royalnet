# -*- coding: utf-8 -*-
import time
import filemanager
import telegram
import steam
import random
import osu
import hearthstone
import sys
import mumbleboxes
import lol


# Check per la modalità votazione del bot, corrisponde al numero della chat in cui è attiva la votazione
# 0 per disattivare la votazione
class Votazione:
    chat = int()
    domanda = str()
    # 0: non votato
    # 1: sì
    # 2: no
    # 3: astenuto
    voto = {
        'steffo': int(0),
        'alby1': int(0),
        'boni3099': int(0),
        'maxsensei': int(0),
        'cosimo03': int(0),
        'frankrekt': int(0),
        'doctorkawaii': int(0),
        'acterryg': int(0),
        'adry99': int(0),
        'alleanderl': int(0),
        'thevagginadestroyer': int(0),
        'tiztiztiz': int(0),
        'fultz': int(0),
        'gotob': int(0),
        'enribenassati': int(0),
        'iemax': int(0),
        'peraemela99': int(0),
        'ilgattopardo': int(0),
        'mrdima98': int(0),
        'ruozir': int(0),
        'supersmurf': int(0),
        'tauei': int(0),
        'voltaggio': int(0),
        'gibait': int(0),
    }

    def __init__(self, question, askin):
        self.domanda = question
        self.chat = askin

    def ask(self):
        telegram.sendmessage(self.domanda, self.chat)

    def register(self, utente, voto):
        self.voto[utente] = voto

    def showresults(self):
        lista = str()
        si = 0
        no = 0
        astenuti = 0
        for membro in self.voto:
            if self.voto[membro] == 0:
                lista += chr(9898)
            elif self.voto[membro] == 1:
                si += 1
                lista += chr(128309)
            elif self.voto[membro] == 2:
                no += 1
                lista += chr(128308)
            elif self.voto[membro] == 3:
                astenuti += 1
                lista += chr(9899)
            lista += " @" + membro + "\n"
        telegram.sendmessage(self.domanda + "\n"
                             "*Risultati:*\n"
                             "Sì: " + str(si) + " (" + str(round(si / (si + no + astenuti) * 100, 2)) + "%)\n"
                             "No: " + str(no) + " (" + str(round(no / (si + no + astenuti) * 100, 2)) + "%)\n"
                             "Astenuti: " + str(astenuti) + "\n\n" + lista, self.chat)


# Votazione in corso
incorso = None

# Playlist di /rage, si riempie quando è vuota
rage = []

# TODO: Rimettere gli audio di Wololo
# wololo = []

audiolist = {
    'madinuovo': 'BQADAgADMwIAAh8GgAFQaq1JNk1ZtwI',
    'sallati': 'BQADAgADrAIAAh8GgAHTdcu8cG-LbAI',
    'giummipersempre': 'BQADAgADEAIAAh8GgAE4O2578G1EagI',
    'nonewallhack': 'BQADAgAD3wEAAh8GgAEUqoKiAaPP9wI',
    'crystalmaiden': 'BQADAgADqwIAAh8GgAE62csQVNai8QI',
    'apeggia': 'BQADAgAD6wEAAh8GgAGe6IDqRVSAhwI',
    'johncena': 'BQADAgAD4AEAAh8GgAFRi-UD1VvyLwI',
    'tre': 'BQADAgADEwIAAh8GgAE-iNm-4V6pZAI',
    'cinqueanni': 'BQADAgADrgIAAh8GgAGKOIASQZevMwI',
    'infilatevi': 'BQADAgAD5gEAAh8GgAFsphnhj_xOnAI',
    'invidiosi': 'BQADAgADqAIAAh8GgAEDx7kiV1MdAwI',
    'salitipo': 'BQADAgADqQIAAh8GgAHhGzfuq1LGXAI',
    'mammadimari': 'BQADAgADpgIAAh8GgAFoIX9f88R-vAI',
    'plug': 'BQADAgADrwIAAh8GgAGdfZO0w1wAAYYC',
    'spari': 'BQADAgADEQIAAh8GgAHaG4P-MmuJKAI',
    'bastagarf': 'BQADAgAD6QEAAh8GgAF0xIIbFxW6NQI',
    'omiodio': 'BQADAgADMgIAAh8GgAFe9-lVwzdFzAI',
}

# Dizionario con i nomi utenti di osu!
# Se qualcuno cambia nome utente di Telegram, lo cambi anche QUI.
osuplayers = {
    'steffo': 'SteffoRYG',
    'evilbalu': 'NemesisRYG',
    'fultz': 'ftz99',
    'ilgattopardo': 'gattopardo',
    'frankrekt': 'FrankezRYG',
    'tiztiztiz': 'fedececco',
    'acterryg': 'Acter1',
    'maxsensei': 'MaxSensei',
    'doctorkawaii': 'ImHeisenberg',
    'thevagginadestroyer': 'barboll',
    'cosimo03': 'Cosimo03',
    'albertino04': 'Alby1',
    'voltaggio': 'voltaggio',
    'tauei': 'tauei',
    'boni3099': 'boni3099',
    'mrdima98': 'MRdima98',
}

# Elenco di username dei membri della RYG
royalgames = ['steffo', 'alby1', 'boni3099', 'maxsensei', 'cosimo03', 'frankrekt', 'doctorkawaii', 'acterryg', 'adry99',
              'alleanderl', 'thevagginadestroyer', 'tiztiztiz', 'fultz', 'gotob', 'enribenassati', 'iemax',
              'peraemela99', 'ilgattopardo', 'mrdima98', 'ruozir', 'supersmurf', 'tauei', 'voltaggio', 'gibait', 'evilbalu', 'generalapathy', 'paltri', 'doom_darth_vader']

# Dizionario con gli steamID
# Vedi sopra
rygsteamids = {
    'steffo': 76561198034314260,
    'alby1': 76561198071383448,
    'boni3099': 76561198131868211,
    'maxsensei': 76561198121094516,
    'cosimo03': 76561198062778224,
    'frankrekt': 76561198071099951,
    'doctorkawaii': 76561198080377213,
    'acterryg': 76561198146704979,
    'adry99': 76561198230034568,
    'alleanderl': 76561198154175301,
    'thevagginadestroyer': 76561198128738388,
    'tiztiztiz': 76561198109189938,
    'fultz': 76561198035547490,
    'gattino02': 76561198071069550,
    'gotob': 76561198096658890,
    'enribenassati': 76561198123018368,
    'iemax': 76561198149695151,
    'peraemela99': 76561198161867082,
    'ilgattopardo': 76561198111021344,
    'mrdima98': 76561198140863530,
    'ruozir': 76561198117708290,
    'supersmurf': 76561198115852550,
    'tauei': 76561198104305298,
    'voltaggio': 76561198147601821,
    'gibait': 76561198157721704,
}

# TODO: magari fare scadere questi dati quando cambiano sui server della rito
lolfreestring = None

random.seed()

# Ciclo principale del bot
print("Bot avviato!")
while True:
    try:
        # Guarda il comando ricevuto.
        msg = telegram.getupdates()
        # Se il messaggio non è una notifica di servizio...
        if 'text' in msg:
            # Salvatelo in una stringa
            text = msg['text']
            # Guarda l'ID della chat in cui è stato inviato
            sentin = msg['chat']['id']
            # ID del messaggio ricevuto
            source = msg['message_id']
            # Nome da visualizzare nella console per capire chi accidenti è che invia messaggi strani
            if 'username' in msg['from']:
                # Salva l'username se esiste
                username = msg['from']['username']
            else:
                # Altrimenti, salva l'userID
                username = str(msg['from']['id'])
            # Se sei un membro della Royal Games
            if username.lower() in royalgames:
                # Riconosci il comando.
                # Viene usato startswith perchè il comando potrebbe anche essere inviato in forma /ciao@RoyalBot.
                if text.startswith('/ahnonlosoio'):
                    print("@" + username + ": /ahnonlosoio")
                    # Rispondi con Ah, non lo so nemmeno io.
                    telegram.sendmessage("Ah, non lo so nemmeno io!", sentin, source)
                elif text.startswith('/ehoh'):
                    print("@" + username + ": /ehoh")
                    # Rispondi con Eh, oh. Sono cose che capitano.
                    telegram.sendmessage("Eh, oh. Sono cose che capitano.", sentin, source)
                elif text.startswith('/playing'):
                    print("@" + username + ": /playing")
                    # Informa Telegram che il messaggio è stato ricevuto e visualizza Royal Bot sta scrivendo.
                    telegram.sendchataction(sentin)
                    cmd = text.split(" ")
                    # Se è stato specificato un AppID...
                    if len(cmd) >= 2:
                        n = steam.getnumberofcurrentplayers(cmd[1])
                        # Se viene ricevuta una risposta...
                        if n is None:
                            telegram.sendmessage(chr(9888) + " L'app specificata non esiste!", sentin, source)
                        else:
                            telegram.sendmessage('In questo momento, ' + str(n) + ' persone stanno giocando a [' + cmd[1] +
                                                 '](https://steamdb.info/app/' + cmd[1] + '/graphs/)', sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) + ' Non hai specificato un AppID!\n'
                                                         'La sintassi corretta è /playing <AppID>.', sentin, source)
                elif text.startswith('/saldi'):
                    print("@" + username + ": /saldi")
                    # Visualizza il link di isthereanydeal con i saldi di un gioco.
                    # Informa Telegram che il messaggio è stato ricevuto e visualizza Royal Bot sta scrivendo.
                    telegram.sendchataction(sentin)
                    cmd = text.split(" ", 1)
                    if len(cmd) == 2:
                        telegram.sendmessage(
                            'Visualizza le offerte di '
                            '[' + cmd[1] + '](https://isthereanydeal.com/#/search:' + cmd[1].replace(' ', '%20') +
                            ";/scroll:%23gamelist).", sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) +
                                             " Non hai specificato un gioco!"
                                             "[Visualizza tutte le offerte]"
                                             "(https://isthereanydeal.com/#/search:.;/scroll:%23gamelist).",
                                             sentin, source)
                elif text.startswith('/audio'):
                    print("@" + username + ": /audio")
                    cmd = text.split(" ", 1)
                    if cmd[1] in audiolist:
                        sendme = audiolist[cmd[1]]
                        telegram.senddocument(sendme, sentin, source)
                    else:
                        sendme = chr(9888) + " L'audio richiesto non esiste!\n*Audio disponibili*:\n"
                        for audio in audiolist:
                            sendme += audio + "\n"
                        telegram.sendmessage(sendme, sentin, source)
                elif text.startswith('/sbam'):
                    print("@" + username + ": /sbam")
                    # Manda l'audio contenente gli sbam di tutti i membri Royal Games.
                    telegram.senddocument('BQADAgADBwMAAh8GgAGSsR4rwmk_LwI', sentin)
                elif text.startswith('/osu'):
                    print("@" + username + ": /osu")
                    # Visualizza il punteggio più recente di osu!
                    # Informa Telegram che il messaggio è stato ricevuto.
                    telegram.sendchataction(sentin)
                    # Trova il nome utente specificato
                    cmd = text.split(' ', 1)
                    # Se è stato specificato un nome utente
                    if len(cmd) >= 2:
                        # Trova la modalità
                        # 0 = osu!
                        # 1 = osu!taiko
                        # 2 = osu!catch
                        # 3 = osu!mania
                        cmd = text.split(' ', 2)
                        # Se è stata specificata una modalità
                        if len(cmd) >= 3:
                            # Modalità specificata
                            mode = int(cmd[2])
                        else:
                            # Imposta la modalità a osu!
                            mode = 0
                        # Prova a mandare una richiesta ai server di osu per l'ultima canzone giocata
                        try:
                            r = osu.getuserrecent(cmd[1], mode)
                        # Se la funzione restituisce un errore, riferisci su Telegram l'errore e previeni il crash.
                        except NameError:
                            telegram.sendmessage(chr(9888) + " Errore nella richiesta ai server di Osu!", sentin, source)
                        # Se tutto va bene, continua!
                        else:
                            # Se ci sono delle mod attive...
                            if "enabled_mods" in r:
                                mods = osu.listmods(r['enabled_mods'])
                            else:
                                mods = ""
                            # Specifica cosa vuole dire il grado F e il grado X
                            if r['rank'] == 'F':
                                r['rank'] = 'Failed'
                            elif r['rank'] == 'X':
                                r['rank'] = 'Unranked'
                            if mode == 0:
                                # Visualizza le informazioni relative alla modalità osu!
                                telegram.sendmessage("*osu!*\n"
                                                     "[Beatmap {0}](https://osu.ppy.sh/b/{0})\n"
                                                     "*{1}*\n"
                                                     "{2}\n"
                                                     "*Punti*: {3}\n"
                                                     "*Combo* x{4}\n"
                                                     "*300*: {5}\n"
                                                     "*100*: {6}\n"
                                                     "*50*: {7}\n"
                                                     "*Awesome*: {8}\n"
                                                     "*Good*: {9}\n"
                                                     "*Miss*: {10}"
                                                     .format(r['beatmap_id'],
                                                             r['rank'],
                                                             mods,
                                                             r['score'],
                                                             r['maxcombo'],
                                                             r['count300'],
                                                             r['count100'],
                                                             r['count50'],
                                                             r['countkatu'],
                                                             r['countgeki'],
                                                             r['countmiss']), sentin, source)
                            elif mode == 1:
                                # Visualizza le informazioni relative alla modalità osu!taiko
                                telegram.sendmessage("*osu!taiko*\n"
                                                     "[Beatmap {0}](https://osu.ppy.sh/b/{0})\n"
                                                     "*{1}*\n"
                                                     "{2}\n"
                                                     "*Punti*: {3}\n"
                                                     "*Combo* x{4}\n"
                                                     "*Great*: {5}\n"
                                                     "*Good*: {6}\n"
                                                     "_Large_ *Great*: {7}\n"
                                                     "_Large_ *Good*: {8}\n"
                                                     "*Miss*: {9}"
                                                     .format(r['beatmap_id'],
                                                             r['rank'],
                                                             mods,
                                                             r['score'],
                                                             r['maxcombo'],
                                                             r['count300'],
                                                             r['count100'],
                                                             r['countkatu'],
                                                             r['countgeki'],
                                                             r['countmiss']), sentin, source)
                            elif mode == 2:
                                # Visualizza le informazioni relative alla modalità osu!catch
                                telegram.sendmessage("*osu!catch*\n"
                                                     "[Beatmap " + r['beatmap_id'] + "](" + 'https://osu.ppy.sh/b/' + r[
                                                         'beatmap_id'] +
                                                     ")\n*" + r['rank'] + "*\n" + mods +
                                                     "\n*Punti*: " + r['score'] + "\n"
                                                                                  "*Combo* x" + r['maxcombo'] + "\n"
                                                                                                                "*Fruit*: " +
                                                     r['count300'] + "\n"
                                                                     "*Droplet* _tick_: " + r['count100'] + "\n"
                                                                                                    "*Droplet* _trail_: " +
                                                     r['count50'] + "\n"
                                                                    "*Miss*: " + r['countmiss'], sentin, source)
                            elif mode == 3:
                                # Visualizza le informazioni relative alla modalità osu!mania
                                telegram.sendmessage("*osu!mania*\n" +
                                                     "[Beatmap " + r['beatmap_id'] + "](" + 'https://osu.ppy.sh/b/' + r[
                                                         'beatmap_id'] + ")\n*" + r['rank'] + "*\n" + mods +
                                                     "\n*Punti*: " + r['score'] + "\n"
                                                                                  "*Combo* x" + r['maxcombo'] + "\n"
                                                                                                    "_Rainbow_ *300*: " +
                                                     r['countgeki'] + "\n"
                                                                      "*300*: " + r['count300'] + "\n"
                                                                                                  "*100*: " + r[
                                                         'count100'] + "\n"
                                                                       "*200*: " + r['countkatu'] + "\n"
                                                                                                    "*50*: " + r[
                                                         'count50'] + "\n"
                                                                      "*Miss*: " + r['countmiss'], sentin, source)
                    else:
                        # TODO: Mettere a posto sto schifo.
                        if username.lower() in osuplayers:
                            r = osu.getuserrecent(osuplayers[username.lower()], 0)
                            if "enabled_mods" in r:
                                mods = osu.listmods(r['enabled_mods'])
                            else:
                                mods = ""
                            telegram.sendmessage("*osu!*\n"
                                                 "[Beatmap {0}](https://osu.ppy.sh/b/{0})\n"
                                                 "*{1}*\n"
                                                 "{2}\n"
                                                 "*Punti*: {3}\n"
                                                 "*Combo* x{4}\n"
                                                 "*300*: {5}\n"
                                                 "*100*: {6}\n"
                                                 "*50*: {7}\n"
                                                 "*Awesome*: {8}\n"
                                                 "*Good*: {9}\n"
                                                 "*Miss*: {10}"
                                                 .format(r['beatmap_id'],
                                                         r['rank'],
                                                         mods,
                                                         r['score'],
                                                         r['maxcombo'],
                                                         r['count300'],
                                                         r['count100'],
                                                         r['count50'],
                                                         r['countkatu'],
                                                         r['countgeki'],
                                                         r['countmiss']), sentin, source)
                elif text.startswith('/roll'):
                    print("@" + username + ": /roll")
                    cmd = text.split(' ', 1)
                    # Se è stato specificato un numero
                    if len(cmd) >= 2:
                        # Controlla che sia convertibile in un intero.
                        try:
                            m = int(cmd[1])
                        except ValueError:
                            telegram.sendmessage(chr(9888) + " Il numero specificato non è un intero.", sentin, source)
                    else:
                        # Imposta il numero massimo a 100.
                        m = 100
                    # Prova a generare un numero casuale.
                    if m == 34261891881215712181524122318242223183627453833:
                        telegram.sendmessage("Numero casuale da 1 a _get rekt_:\n*@FrankRekt è scarso*", sentin, source)
                    else:
                        try:
                            n = random.randrange(m) + 1
                        except ValueError:
                            telegram.sendmessage(chr(9888) + " Il numero specificato non è maggiore o uguale a 0.", sentin,
                                                 source)
                        # Se tutto va bene visualizza il numero generato
                        else:
                            telegram.sendmessage("Numero casuale da 1 a " + str(m) + ":\n*" + str(n) + "*", sentin, source)
                elif text.startswith('/automah'):
                    print("@" + username + ": /automah")
                    # Invia il messaggio.
                    telegram.sendmessage("Automaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa! Devi funzionare, cavolo!", sentin,
                                         source)
                elif text.startswith('/hs'):
                    print("@" + username + ": /hs")
                    # Informa Telegram che il messaggio è stato ricevuto.
                    telegram.sendchataction(sentin)
                    cmd = text.split(" ", 1)
                    # Se è stata specificata una carta...
                    if len(cmd) >= 2:
                        # Controlla che la carta specificata esista.
                        try:
                            r = hearthstone.card(cmd[1])
                            # Se ci sono più carte, prendine una a caso!
                            r = r[random.randrange(len(r))]
                        except ValueError:
                            telegram.sendmessage(chr(9888) + " La carta specificata non esiste!", sentin, source)
                        # Se tutto va bene, elabora e visualizza le informazioni sulla carta.
                        else:
                            # Si trova nelle bustine
                            if 'howToGet' not in r:
                                if 'cardSet' in r:
                                    r['howToGet'] = "Trovala in " + r['cardSet'] + "."
                                else:
                                    r['howToGet'] = "Inottenibile."
                            # Nessuna classe
                            if 'playerClass' not in r:
                                r['playerClass'] = "Neutral"
                            # Nessun effetto
                            if 'text' not in r:
                                r['text'] = ""
                            # Converti l'HTML nella descrizione in Markdown. Circa.
                            r['text'] = r['text'].replace("<b>", "*")
                            r['text'] = r['text'].replace("</b>", "*")
                            r['text'] = r['text'].replace("<i>", "_")
                            r['text'] = r['text'].replace("</i>", "_")
                            # Togli il $, che indica che il numero di danni può essere modificato dallo Spell Damage
                            r['text'] = r['text'].replace("$", "")
                            # Nessuna rarità
                            if 'rarity' not in r:
                                r['rarity'] = "None"
                            # Nessuna descrizione
                            if 'flavor' not in r:
                                r['flavor'] = ""
                            # Testo principale
                            # Magie
                            if r['type'] == "Spell":
                                text = str("[" + r['name'] + "](" + r['img'] + ") "
                                                                               "(" + r['rarity'] + ")\n" +
                                           r['playerClass'] + "\n" +
                                           str(r['cost']) + " mana\n" +
                                           r['text'] + "\n" +
                                           r['howToGet'] + "\n\n_" +
                                           r['flavor'] + "_\n")
                            # Servitori
                            elif r['type'] == "Minion":
                                text = str("[" + r['name'] + "](" + r['img'] + ") "
                                                                               "(" + r['rarity'] + ")\n" +
                                           r['playerClass'] + "\n" +
                                           str(r['cost']) + " mana\n" +
                                           str(r['attack']) + " attacco\n" +
                                           str(r['health']) + " salute\n" +
                                           r['text'] + "\n" +
                                           r['howToGet'] + "\n\n_" +
                                           r['flavor'] + "_\n")
                            # Armi
                            elif r['type'] == "Weapon":
                                text = str("[" + r['name'] + "](" + r['img'] + ") "
                                                                               "(" + r['rarity'] + ")\n" +
                                           r['playerClass'] + "\n" +
                                           str(r['cost']) + " mana\n" +
                                           str(r['attack']) + " attacco\n" +
                                           str(r['durability']) + " integrita'\n" +
                                           r['text'] + "\n" +
                                           r['howToGet'] + "\n\n_" +
                                           r['flavor'] + "_\n")
                            # Potere Eroe
                            elif r['type'] == "Hero Power":
                                text = str("[" + r['name'] + "](" + r['img'] + ")\n" +
                                           r['playerClass'] + "\n" +
                                           str(r['cost']) + " mana\n" +
                                           r['text'] + "\n")
                            # Eroe
                            elif r['type'] == "Hero":
                                text = str("[" + r['name'] + "](" + r['img'] + ")\n" +
                                           "*Eroe*\n" +
                                           str(r['health']) + " salute\n")
                            telegram.sendmessage(text, sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) + " Non hai specificato nessuna carta!\n"
                                                         "La sintassi corretta è _/hs nomecarta_ .", sentin, source)
                elif text.startswith('/online'):
                    # Elenco di tutte le persone online su Steam
                    print("@" + username + ": /online ")
                    # Informa Telegram che il messaggio è stato ricevuto.
                    telegram.sendchataction(sentin)
                    cmd = text.split(" ")
                    if len(cmd) >= 2:
                        if cmd[1].lower() == "help":
                            telegram.sendmessage(chr(128309) + " Online\n" +
                                                 chr(128308) + " In gioco | Occupato\n" +
                                                 chr(9899) + " Assente | Inattivo\n" +
                                                 chr(128310) + " Disponibile per scambiare\n" +
                                                 chr(128311) + " Disponibile per giocare", sentin, source)
                    else:
                        # Stringa utilizzata per ottenere informazioni su tutti gli utenti in una sola richiesta a steam
                        userids = str()
                        for nome in rygsteamids:
                            userids += str(rygsteamids[nome]) + ','
                        tosend = "*Online ora:*\n"
                        r = steam.getplayersummaries(userids)
                        for player in r:
                            # In gioco
                            if 'gameextrainfo' in player:
                                tosend += chr(128308) + " _" + player['gameextrainfo'] + "_ |"
                            elif 'gameid' in player:
                                tosend += chr(128308) + " _" + player['gameid'] + "_ |"
                            # Online
                            elif player['personastate'] == 1:
                                tosend += chr(128309)
                            # Occupato
                            elif player['personastate'] == 2:
                                tosend += chr(128308)
                            # Assente o Inattivo
                            elif player['personastate'] == 3 or player['personastate'] == 4:
                                tosend += chr(9899)
                            # Disponibile per scambiare
                            elif player['personastate'] == 5:
                                tosend += chr(128310)
                            # Disponibile per giocare
                            elif player['personastate'] == 6:
                                tosend += chr(128311)
                            if player['personastate'] != 0:
                                tosend += " " + player['personaname'] + "\n"
                        else:
                            telegram.sendmessage(tosend, sentin, source)
                elif text.startswith('/shrekt'):
                    # Manda l'audio So much to do, so much to see
                    print("@" + username + ": /shrekt ")
                    telegram.senddocument("BQADBAADsQADiBjiAqYN-EBXASyhAg", sentin)
                elif text.startswith('/restart'):
                    # Riavvia il bot
                    if username == "Steffo":
                        print("@" + username + ": /restart ")
                        telegram.sendmessage("Riavvio accettato.", sentin, source)
                        sys.exit(0)
                    else:
                        telegram.sendmessage(chr(9888) + " Non hai i permessi necessari per creare una nuova votazione.",
                                             sentin, source)
                elif text.startswith('/nuovavotazione'):
                    if username == "Steffo":
                        print("@" + username + ": /nuovavotazione ")
                        cmd = text.split(" ", 1)
                        incorso = Votazione(cmd[1], sentin)
                    else:
                        telegram.sendmessage(chr(9888) + " Non hai i permessi necessari per creare una nuova votazione.",
                                             sentin, source)
                elif text.startswith('/si'):
                    print("@" + username + ": /si ")
                    if incorso is not None:
                        if incorso.chat == sentin:
                            incorso.register(username.lower(), 1)
                            telegram.sendmessage("Votazione registrata!", sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) + " Non è in corso nessuna votazione!", sentin, source)
                elif text.startswith('/no'):
                    print("@" + username + ": /no ")
                    if incorso is not None:
                        if incorso.chat == sentin:
                            incorso.register(username.lower(), 2)
                            telegram.sendmessage("Votazione registrata!", sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) + " Non è in corso nessuna votazione!", sentin, source)
                elif text.startswith('/astieniti'):
                    print("@" + username + ": /astieniti ")
                    if incorso is not None:
                        if incorso.chat == sentin:
                            incorso.register(username.lower(), 3)
                            telegram.sendmessage("Votazione registrata!", sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) + " Non è in corso nessuna votazione!", sentin, source)
                elif text.startswith('/domanda'):
                    print("@" + username + ": /domanda ")
                    if incorso is not None:
                        if incorso.chat == sentin:
                            incorso.ask()
                    else:
                        telegram.sendmessage(chr(9888) + " Non è in corso nessuna votazione!", sentin, source)
                elif text.startswith('/risultati'):
                    print("@" + username + ": /risultati ")
                    if incorso is not None:
                        if incorso.chat == sentin:
                            incorso.showresults()
                    else:
                        telegram.sendmessage(chr(9888) + " Non è in corso nessuna votazione!", sentin, source)
                elif text.startswith('/cv'):
                    # Visualizza l'elenco di persone nella chat di Mumble
                    print("@" + username + ": /cv ")
                    # Informa Telegram che il messaggio è stato ricevuto.
                    telegram.sendchataction(sentin)
                    r = mumbleboxes.getserverstatus("https://www.mumbleboxes.com/servers/5454/cvp.json").json()
                    tosend = "*Utenti online:*\n"
                    for u in r['root']['users']:
                        if not u['mute']:
                            if u['selfDeaf']:
                                tosend += chr(128263) + " "
                            elif u['selfMute']:
                                tosend += chr(128264) + " "
                            else:
                                tosend += chr(128266) + " "
                            tosend += u['name'] + "\n"
                    for ch in r['root']['channels']:
                        for u in ch['users']:
                            if not u['mute']:
                                if u['selfDeaf']:
                                    tosend += chr(128263) + " "
                                elif u['selfMute']:
                                    tosend += chr(128264) + " "
                                else:
                                    tosend += chr(128266) + " "
                                tosend += u['name'] + " | _" + ch['name'] + "_\n"
                    telegram.sendmessage(tosend, sentin, source)
                elif text.startswith('/diario'):
                    # Aggiungi una riga al diario Royal Games
                    print("@" + username + ": /diario ")
                    cmd = text.split(" ", 1)
                    if len(cmd) > 1:
                        cmd[1] = cmd[1].replace("\n", " ")
                        diario = filemanager.readfile("diario.txt")
                        diario += str(int(time.time())) + "|" + cmd[1] + "\n"
                        filemanager.writefile("diario.txt", diario)
                        telegram.sendmessage("Aggiunto al diario RYG.", sentin, source)
                    else:
                        telegram.sendmessage(chr(9888) + " Non hai scritto niente sul diario!\n"
                                                         "Sintassi corretta: /diario _quello che vuoi scrivere_", sentin,
                                             source)
                elif text.startswith('/leggi'):
                    # Leggi dal diario Royal Games
                    print("@" + username + ": /leggi")
                    cmd = text.split(" ", 1)
                    diario = filemanager.readfile("diario.txt")
                    diario = diario.split('\n')
                    text = str()
                    # Se è incluso un numero dopo leggi, prendi quel numero di eventi più recenti.
                    if len(cmd) > 1:
                        if int(cmd[1]) < len(diario):
                            # L'ultimo numero è escluso.
                            for n in range(int(cmd[1]) + 1, 1, -1):
                                riga = diario[len(diario) - n]
                                riga = riga.split("|", 1)
                                ora = time.gmtime(int(riga[0]))
                                text += "`" + str(ora.tm_mday) + "/" + str(ora.tm_mon) + "/" + str(ora.tm_year) + "`: `" + \
                                        str(ora.tm_hour) + ":" + str(ora.tm_min) + "` " + riga[1] + "\n"
                        else:
                            telegram.sendmessage(chr(9888) + " Il numero massimo di stringhe visualizzabili è " +
                                                 str(len(diario) - 1), sentin, source)
                    # Altrimenti, prendi un evento a caso.
                    else:
                        riga = diario[random.randrange(0, len(diario))]
                        riga = riga.split("|", 1)
                        ora = time.gmtime(int(riga[0]))
                        text += "`" + str(ora.tm_mday) + "/" + str(ora.tm_mon) + "/" + str(ora.tm_year) + "`: `" + \
                                str(ora.tm_hour) + ":" + str(ora.tm_min) + "` " + riga[1] + "\n"
                    telegram.sendmessage(text, sentin, source)
                elif text.startswith('/lolfree'):
                    # Visualizza i campioni gratuiti di LoL di questa settimana
                    print("@" + username + ": /lolfree")
                    # Informa Telegram che il messaggio è stato ricevuto.
                    telegram.sendchataction(sentin)
                    ora = time.gmtime()
                    cmd = text.split(" ", 1)
                    if len(cmd) > 1:
                        if cmd[1].startswith("refresh"):
                            refresh = True
                        else:
                            refresh = False
                    else:
                        refresh = False
                    # Controlla se i dati sono già stati scaricati.
                    if lolfreestring is None or refresh:
                        # Crea un nuovo set di dati.
                        print("Aggiornamento champ gratuiti di League of Legends...")
                        lolfreestring = "Champion gratuiti del `" + str(ora.tm_mday) + "/" + str(ora.tm_mon) + "/" + \
                                        str(ora.tm_year) + " " + str(ora.tm_hour) + ":" + str(ora.tm_min) + "`\n"
                        r = lol.getfreerotation()
                        for champion in r:
                            staticdata = lol.getsinglestaticdata(champion['id'])
                            lolfreestring += "*" + staticdata['name'] + "* " + staticdata['title'] + '\n'
                        print("Completato.")
                    telegram.sendmessage(lolfreestring, sentin, source)
                elif text.startswith('/crash'):
                    # Crasha il bot. Mi sembra geniale.
                    if username == 'Steffo':
                        raise Exception("Ho appena fatto crashare tutto apposta. Sono un genio.")
            else:
                print("@" + username + " bloccato.")
    except Exception as e:
        telegram.sendmessage(chr(9762) + " *ERRORE CRITICO:\n*"
                             "{0}\n".format(repr(e.args)), -2141322)
        print("ERRORE CRITICO:\n"
              "{0}".format(repr(e)))
