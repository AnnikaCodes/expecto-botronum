#!/usr/bin/python3

# Basic code from https://pypi.org/project/websocket_client/
import websocket
import requests
import time
import json
import numpy
import wsaccel
import re
import pickle
from pprint import pprint
import config
import random
from pbwrap import Pastebin
from threading import Timer
from datetime import date

pastebin = Pastebin(config.pastebinKey)
def numRank(char):
	return (config.authSymbols.index(char) + 1)
##########################
## Miscellaneous Arrays ##
##########################

unoCommands = [
	'/uno create 500',
	'/uno timer 45',
	'/uno autostart 150',
]

tourCommands = [
	'/tour create {format}, elimination',
	'/tour autostart 5',
	'/tour autodq 2',
	'/tour forcetimer on'
]

battleFormats = ['gen7randombattle', 'gen7unratedrandombattle', 'gen7ou', 'gen7ubers', 'gen7uu', 'gen7ru', 'gen7nu', 'gen7pu', 'gen7lc', 'gen7monotype', 'gen7anythinggoes', 'gen71v1', 'gen7zu', 'gen7cap', 'gen7caplc', 'gen7battlespotsingles', 'gen7battlespotspecial15', 'gen7customgame', 'gen7randomdoublesbattle', 'gen7doublesou', 'gen7doublesubers', 'gen7doublesuu', 'gen7vgc2019sunseries', 'gen7vgc2019moonseries', 'gen7vgc2019ultraseries', 'gen7vgc2018', 'gen7vgc2017', 'gen7battlespotdoubles', 'gen72v2doubles', 'gen7metronomebattle', 'gen7doublescustomgame', 'gen7trademarked', 'gen7ultimatez', 'gen7balancedhackmons', 'gen7mixandmega', 'gen7almostanyability', 'gen7camomons', 'gen7stabmons', 'gen7tiershift', 'gen7partnersincrime', 'gen6gen-nextou', "gen7let'sgorandombattle", "gen7let'sgoou", "gen7let'sgosinglesnorestrictions", "gen7let'sgodoublesou", "gen7let'sgodoublesnorestrictions", 'gen7battlefactory', 'gen7bssfactory', 'gen7monotyperandombattle', 'gen7superstaffbrosbrawl', 'gen7challengecup1v1', 'gen7challengecup2v2', 'gen7hackmonscup', 'gen7doubleshackmonscup', 'gen6randombattle', 'gen6battlefactory', 'gen5randombattle', 'gen4randombattle', 'gen3randombattle', 'gen2randombattle', 'gen1randombattle', 'gen1challengecup', 'gen6uu', 'gen51v1', 'gen5balancedhackmons', 'gen6ou', 'gen5ou', 'gen4ou', 'gen3ou', 'gen2ou', 'gen1ou', 'gen6ubers', 'gen6ru', 'gen6nu', 'gen6pu', 'gen6lc', 'gen6monotype', 'gen6anythinggoes', 'gen61v1', 'gen6cap', 'gen6battlespotsingles', 'gen6customgame', 'gen6doublesou', 'gen6vgc2016', 'gen6battlespotdoubles', 'gen6doublescustomgame', 'gen6battlespottriples', 'gen6triplescustomgame', 'gen5ubers', 'gen5uu', 'gen5ru', 'gen5nu', 'gen5lc', 'gen5monotype', 'gen5gbusingles', 'gen5customgame', 'gen5doublesou', 'gen5gbudoubles', 'gen5doublescustomgame', 'gen4ubers', 'gen4uu', 'gen4nu', 'gen4lc', 'gen4anythinggoes', 'gen4customgame', 'gen4doublesou', 'gen4doublescustomgame', 'gen3ubers', 'gen3uu', 'gen3nu', 'gen3customgame', 'gen3doublescustomgame', 'gen2ubers', 'gen2uu', 'gen2nu', 'gen2customgame', 'gen1ubers', 'gen1uu', 'gen1ou(tradeback)', 'gen1stadiumou', 'gen1customgame']

#######################
## WebSocket logging ##
## Command handling  ##
#######################
possibles = ['J', 'j', "join"]
pointsDB = {}

def onMessage(ws, message):
	if message[1] + message[2] == 'pm': # It's a pm, so log it.
		path = "logs/{date}-pm.log".format(date = date.today().strftime("%b-%d-%Y"))
	else:
                path = "logs/{date}-chat.log".format(date = date.today().strftime("%b-%d-%Y"))
	toLog = str(message.encode('utf-8'))[2:-1] # remove b'' part
	if "\n" in toLog:
		toLog = toLog.split("\n")[1] # remove >harrypotter part
	f = open(path, 'a+')
	f.write(toLog + str('\n'))
	f.close()
	if 'challstr' in message and parseMessage(message)['type'] == 'challstr':
		challstrHandler(message)
	if 'j' in message or 'join' in message or 'J' in message and message.split('|')[1] in possibles:
		s = message.split('|')
		print(str(s).encode('ascii', 'ignore').decode('utf-8'))
		user = re.sub(r'[^a-zA-Z0-9]', '',s[2].encode('ascii', 'ignore').decode('utf-8').lower())
		if user in joinDB and 'harrypotter' in s[0]:
			ws.send( 'harrypotter' + '|' + joinDB[user])
	if '~ping' in message  and parseMessage(message)['message'][:5] == '~ping':
		ws.send(parseMessage(message)['replyPrefix'] + "Pong!")
	if '~pong' in message and parseMessage(message)['message'][:5] == '~pong':
		ws.send(parseMessage(message)['replyPrefix'] + "Ping!")
	if '~parse' in message and parseMessage(message)['message'][:6] == '~parse':
		ws.send(parseMessage(message)['replyPrefix'] + "Parsed data: ``" + str(parseMessage(message)) + "``")
	if '~do' in message and parseMessage(message)['message'][:4] == '~do ':
		doCommand(parseMessage(message))
#	if '~check' in message and parseMessage(message)['message'][:7] == '~check ':
#		checkPoints(parseMessage(message))
#	if '~houses' in message and parseMessage(message)['message'][:7] == '~houses':
#		showHouses(parseMessage(message))
#	if '~lb' in message and parseMessage(message)['message'][:4] == '~lb ':
#		lb(parseMessage(message)) '''
#	if '~join' in message and parseMessage(message)['message'][:6] == '~join ':
#		joinHouse(parseMessage(message))
#	if '~house' in message and parseMessage(message)['message'][:7] == '~house ':
#		checkHouse(parseMessage(message))
#	if '~give' in message and parseMessage(message)['message'][:6] == '~give ':
#		givePoints(parseMessage(message))'''
	if '~eval' in message and parseMessage(message)['message'][:6] == '~eval ' and parseMessage(message)['user'].lower() in config.goodUsers:
		data = str(eval(parseMessage(message)['message'][6:]))
		if '\n' in data:
			split = data.split('\n')
			j = "!code "
			for word in split:
				j += word
				j += '\n'
			ws.send(parseMessage(message)['room'] + j)
		else:
			ws.send(parseMessage(message)['replyPrefix'] + '``' + data + '``')
	if '~jp ' in message and parseMessage(message)['message'][:4] == '~jp ':
		addPhrase(parseMessage(message))
	if '~owo ' in message and parseMessage(message)['message'][:5] == '~owo ':
		owoify(parseMessage(message))
	if '~reverse' in message and parseMessage(message)['message'][:8] == '~reverse':
		wallreverse(parseMessage(message))
	if '~wallrev' in message and parseMessage(message)['message'][:8] == '~wallrev':
		wallreverse(parseMessage(message))
	if '~uno' in message and parseMessage(message)['message'][:4] == '~uno':
		uno(parseMessage(message))
	if '~tour ' in message and parseMessage(message)['message'][:6] == '~tour ':
		startTour(parseMessage(message))
	if '~scores' in message and parseMessage(message)['message'][:8] == '~scores':
		showScores(parseMessage(message))
	if '~addto' in message and parseMessage(message)['message'][:7] == '~addto ':
		addScore(parseMessage(message))
	if '~clearscores' in message and parseMessage(message)['message'][:13] == '~clearscores' and parseMessage(message)['numrank'] >= numRank('+'):
		pointsDB.clear()
		ws.send(parseMessage(message)['replyPrefix'] + "Scores cleared!")
	if '~fact' in message and parseMessage(message)['message'][:5] == '~fact':
		showFact(parseMessage(message))
	if '~addfact' in message and parseMessage(message)['message'][:9] == '~addfact ':
		addFact(parseMessage(message))
	if '~deletefact' in message and parseMessage(message)['message'][:12] == '~deletefact ':
		removeFact(parseMessage(message))
	if '~countfacts' in message and parseMessage(message)['message'][:11] == '~countfacts':
		numFacts(parseMessage(message))
	if '~listfacts' in message and parseMessage(message)['message'][:10] == '~listfacts':
		listFacts(parseMessage(message))
#	if '~triwizard' in message and parseMessage(message)['message'][:10] == '~triwizard':
#		showTriwizardLB(parseMessage(message))
	if '~timer ' in message and parseMessage(message)['message'][:len('~timer ')] == '~timer ':
		timer(parseMessage(message))
	if '~topic' in message and parseMessage(message)['message'][:6] == '~topic':
		showTopic(parseMessage(message))
	if '~addtopic' in message and parseMessage(message)['message'][:10] == '~addtopic ':
		addTopic(parseMessage(message))
	if '~deletetopic' in message and parseMessage(message)['message'][:13] == '~deletetopic ':
		removeTopic(parseMessage(message))
	if '~counttopics' in message and parseMessage(message)['message'][:12] == '~counttopics':
		numTopics(parseMessage(message))
	if '~listtopics' in message and parseMessage(message)['message'][:11] == '~listtopics':
		listTopics(parseMessage(message))
	if '~superhero ' in message and parseMessage(message)['message'][:len('~superhero ')] == '~superhero ':
			superhero(parseMessage(message))
#if '~triwizard' in message and parseMessage(message)['message'][:10] == '~triwizard':
#		showTriwizardLB(parseMessage(message))







def onError(ws, error):
    print("Error.")

def onClose(ws):
    websocket.enableTrace(True)

def onOpen(ws):
	print(config.initString)

def challstrHandler(message):
	print("Challstr received!")
	challstr = message[len('|challstr|'):]
	r = requests.post('http://play.pokemonshowdown.com/action.php', data = {'act': 'login', 'name': config.username, 'pass': config.password, 'challstr': challstr})
	assertion = json.loads(r.content[1:].decode('utf-8'))['assertion']
	ws.send('|/trn {name},0,{magic}'.format(name = config.username, magic = assertion))
	for room in config.rooms:
		ws.send('|/j {r}'.format(r = room))
	ws.send(config.rooms[0] + '|/status {status}'.format(status = config.status))
	print("Success!")

#####################
## Message Parsing ##
#####################

def parseMessage(message):
	# Returns a dictionary with the following parts: `room`, `rank`, `numrank` `type`, `time`, `user`, `replyPrefix`, and `message`
	params = message.split('|')
	data = {}
	data['room'] = params[0].replace('>', '').strip() # > is never in a room name

	# PM Handling
	if data['room'] == '' and 'pm' in params[1]:
		data['room'] = params[1].strip()
		data['user'] = re.sub(r'[^a-zA-Z0-9]', '',params[2].strip().encode("ascii", "ignore").decode("utf-8"))
		data['rank'] = ''
		data['numrank'] = 0
		if params[2].strip()[0] in config.authSymbols:
			data['rank'] = params[2].strip()[0]
			data['numrank'] = (config.authSymbols.index(data['rank']) + 1)
		try:
			data['message'] = params[4].strip().strip('\n')
		except Exception as e:
			print('Error: ' + str(e))
		data['replyPrefix'] = '|/w {to},'.format(to = data['user'])
		# Deal with null values
		data['type'] = 'pm'
		data['time'] = -1
		if data['user'].lower() in config.goodUsers:
			data['numrank'] = len(config.authSymbols)
		return data
	# End PM Handling

	data['type'] = params[1].replace(':', '').strip()
	try:
		data['time'] = int(params[2].strip())
	except Exception as e:
		data['time'] = -1
		print('Error parsing time: ' + str(e))
	data['user'] =  re.sub(r'[^a-zA-Z0-9]', '', params[3].strip().encode("ascii", "ignore").decode("utf-8"))
	data['rank'] = ''
	data['numrank'] = 0
	if params[3].strip().encode("ascii", "ignore").decode("utf-8")[0] in config.authSymbols:
		data['rank'] =  params[3].strip().encode("ascii", "ignore").decode("utf-8")[0]
		data['numrank'] = (numRank(data['rank']))
	try:
		data['message'] = params[4].strip().strip('\n')
	except Exception as e:
		print('Error: ' + str(e))
	if data['numrank'] >= config.authSymbols.index(config.broadcastRank) + 1 or data['user'].lower() in config.goodUsers:
		# We can broadcast!
		data['replyPrefix'] = (data['room'] + '|')
	else:
		# We should fail
		data['replyPrefix'] = '|/w {to}, Permission denied: use the command in PMs for a result.\n'.format(to = data['user'])

	if data['user'].lower() in config.goodUsers:
		data['numrank'] = len(config.authSymbols)
	return data

##############
## Commands ##
##############
def doCommand(parsed):
	if parsed['numrank'] >= numRank('#') or parsed['user'] in config.goodUsers:
		toDo = parsed['message'][4:].split(',')
		ws.send(toDo[0] + '|' + toDo[1])
	else:
		ws.send(parsed['replyPrefix'] + "Permission denied.")


def saveJoins():
    f = open('data/joins.json', 'w')
    json.dump(joinDB, f)
    print("Joinphrases saved.")

def loadJoins():
    f = open('data/joins.json', 'r')
    j = json.load(f)
    return j

joinDB = loadJoins()

def addPhrase(parsed):
   if parsed['room'] != 'harrypotter':
       ws.send(parsed['replyPrefix'] + "That functionality is only available in the <<harrypotter>> room.")
       return
   elif parsed['numrank'] < numRank('#'):
       ws.send(parsed['replyPrefix'] + "Only Room Owners can add joinphrases.")
       return
   args = parsed['message'].split(' ', 1)[1].split(',')
   user = re.sub(r'[^a-zA-Z0-9]', '',args[0].encode('ascii', 'ignore').decode('utf-8').lower())
   phrase = args[1]
   joinDB[user] = phrase
   saveJoins()
   ws.send(parsed['replyPrefix'] + "Joinphrase added!")

def owoify(parsed):
   ws.send(parsed['replyPrefix'] + parsed['message'].split(' ', 1)[1].replace('a', 'awa').replace('e','ewe').replace('i', 'iwi').replace('o', 'owo').replace('u', 'uwu').replace('A', 'Awa').replace('E', "Ewe").replace("I", "Iwi").replace("O", "Owo").replace("U", "Uwu"))

def reverse(parsed):
	ws.send(parsed['replyPrefix'] + random.choice(config.words).lower()[::-1])
def wallreverse(parsed):
        ws.send(parsed['replyPrefix'] + '/wall ' + random.choice(config.words).lower()[::-1])

def uno(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + 'Your rank is not high enough to start a game of UNO.')
		return
	else:
		for command in unoCommands:
			ws.send(parsed['room'] + '|' + command)
			ws.send(parsed['room'] + '|' + '/mn UNO started by ' + parsed['user'])

def startTour(parsed):
	format = parsed['message'].split(' ', 1)[1]
	if format not in battleFormats:
		ws.send(parsed['replyPrefix'] + "Warning: ``" + format + "`` may not be a valid format.")
	for command in tourCommands:
		ws.send(parsed['replyPrefix'] + command.format(format = format))

def showScores(parsed):
	m = parsed['replyPrefix'] + "/wall "
	for user in reversed(sorted(pointsDB, key=pointsDB.__getitem__)):
		m = m + "**{u}** ({n}), ".format(u = user, n = pointsDB[user])
	m = m.strip(' ').strip(',')
	if pointsDB == {}:
		m = parsed['replyPrefix'] + "There are no scores."
	ws.send(m)

def addScore(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	user = parsed['message'].split(' ', 1)[1]
	n = 1
	if ',' in user:
		try:
			n = int(user.split(',')[1])
		except:
			ws.send(parsed['replyPrefix'] + "An error occurred.")
		user = user.split(',')[0]
	if user in pointsDB:
		pointsDB[user] += n
	else:
		pointsDB[user] = n
	ws.send(parsed['replyPrefix'] + "Point(s) added!")

def timer(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	args = parsed['message'].split(' ', 1)[1].split(',')
	duration = int(args[0]) # Duration in seconds
	if len(args) > 1: # There's a custom message
		message = parsed['replyPrefix'] + '/wall Timer: ' + args[1]
	else: # no custom message.
		user = parsed['user']
		if user == 'annika0':
			user = 'Annika'
		message = parsed['replyPrefix'] + "/wall Timer set by {user} is up.".format(user=user)
	timer = Timer(duration, ws.send, args = [message])
	timer.start()

def superhero(parsed):
	id = parsed['message'].split(' ',1)[1].strip()
	print(f"id: {id}")
	# TODO: actually support stuff like `~superhero Iron Man`
	if (not id.isdigit()) or int(id) not in range(1,732): #not a valid id... yet
		ws.send(parsed['replyPrefix'] + "{id} is not a valid superhero.".format(id=id))
		return
	request = requests.get("https://superheroapi.com/api/{key}/{id}".format(key=config.superheroAPIKey, id=id)).content
	data = json.loads(request)
	ws.send(parsed['replyPrefix'] + data['name'])

###################
## Fact Handling ##
###################

def loadFactList():
	'''Returns fact list'''
	f = open('data/facts.pickle', 'rb')
	return pickle.load(f)

def saveFactList():
	'''Saves fact list'''
	f = open('data/facts.pickle', 'wb')
	pickle.dump(factList, f)

factList = loadFactList()

def addFact(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	fact = parsed['message'].split(' ', 1)[1] # Remove everything before the first space/
	factList.append(fact)
	saveFactList()
	ws.send(parsed['replyPrefix'] + "Fact added.")

def removeFact(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	fact = parsed['message'].split(' ', 1)[1] # Remove everything before the first space/
	if fact in factList:
		factList.remove(fact)
		saveFactList()
		ws.send(parsed['replyPrefix'] + "Fact deleted.")
	else:
		ws.send(parsed['replyPrefix'] + "Fact not found.")

def showFact(parsed):
	if len(factList) == 0:
		ws.send(parsed['replyPrefix'] + "There are no facts.")
	else:
		ws.send(parsed['replyPrefix'] + '__{fact}__'.format(fact = random.choice(factList)))

def listFacts(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	factString = ""
	for fact in factList:
		factString += fact
		factString += '\n'
	ws.send("|/w {user}, Fact list: {url}".format(user = parsed['user'], url = pastebin.create_paste(factString, 1)))
def numFacts(parsed):
	ws.send(parsed['replyPrefix'] + "There are {n} facts in the fact database.".format(n=len(factList)))



####################
## Topic Handling ##
####################

def loadTopicList():
	'''Returns topic list'''
	f = open('data/topics.pickle', 'rb')
	return pickle.load(f)

def saveTopicList():
	'''Saves topic list'''
	f = open('data/topics.pickle', 'wb')
	pickle.dump(topicList, f)

topicList = loadTopicList()

def addTopic(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	topic = parsed['message'].split(' ', 1)[1] # Remove everything before the first space
	topicList.append(topic)
	saveTopicList()
	ws.send(parsed['replyPrefix'] + "Topic added.")

def removeTopic(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	topic = parsed['message'].split(' ', 1)[1] # Remove everything before the first space/
	if topic in topicList:
		topicList.remove(topic)
		saveTopicList()
		ws.send(parsed['replyPrefix'] + "Topic deleted.")
	else:
		ws.send(parsed['replyPrefix'] + "Topic not found.")

def showTopic(parsed):
	if len(topicList) == 0:
		ws.send(parsed['replyPrefix'] + "There are no topics.")
	else:
		ws.send(parsed['replyPrefix'] + '__{topic}__'.format(topic = random.choice(topicList)))

def listTopics(parsed):
	if parsed['numrank'] < numRank('+'):
		ws.send(parsed['replyPrefix'] + "Permission denied.")
		return
	topicString = ""
	for topic in topicList:
		topicString += topic
		topicString += '\n'
	ws.send("|/w {user}, Topic list: {url}".format(user = parsed['user'], url = pastebin.create_paste(topicString, 1)))

def numTopics(parsed):
	ws.send(parsed['replyPrefix'] + "There are {n} topics in the topic database.".format(n=len(topicList)))

###########################
## House Points Tracking ##
###########################


# def loadPoints():
#     file = open('data/points.json', 'r')
#     print("Points loaded.")
#     return json.load(file)
#
# def loadHouses():
#     r = open('data/ravenclaw.json', 'rb')
#     h = open('data/hufflepuff.json', 'rb')
#     s = open('data/slytherin.json', 'rb')
#     g = open('data/gryffindor.json', 'rb')
#     print("Points loaded.")
#     ravenclaw = pickle.load(r)
#     hufflepuff = pickle.load(h)
#     slytherin = pickle.load(s)
#     gryffindor = pickle.load(g)
#     return ravenclaw,hufflepuff,slytherin,gryffindor
#
# def loadHouseLBs():
#     r = open('data/ravenclawLB.json', 'r')
#     h = open('data/hufflepuffLB.json', 'r')
#     s = open('data/slytherinLB.json', 'r')
#     g = open('data/gryffindorLB.json', 'r')
#     print("Points loaded.")
#     ravenclaw = json.load(r)
#     hufflepuff = json.load(h)
#     slytherin = json.load(s)
#     gryffindor = json.load(g)
#
#     print("House Members loaded")
#     return ravenclaw,hufflepuff,slytherin,gryffindor
#
# pointsTracker = loadPoints()
# ravenclaw, hufflepuff, slytherin, gryffindor = loadHouses()
# ravenclawLB, hufflepuffLB, slytherinLB, gryffindorLB = loadHouseLBs()


# def savePoints():
#     file = open('data/points.json', 'w')
#     json.dump(pointsTracker, file)
#     print("Points saved.")
#
# def saveHouses():
#     r = open('data/ravenclaw.json', 'wb')
#     h = open('data/hufflepuff.json', 'wb')
#     s = open('data/slytherin.json', 'wb')
#     g = open('data/gryffindor.json', 'wb')
#     pickle.dump(ravenclaw, r)
#     pickle.dump(hufflepuff, h)
#     pickle.dump(slytherin, s)
#     pickle.dump(gryffindor, g)
#     print("House Members saved")
#
# def saveHouseLBs():
#     r = open('data/ravenclawLB.json', 'w')
#     h = open('data/hufflepuffLB.json', 'w')
#     s = open('data/slytherinLB.json', 'w')
#     g = open('data/gryffindorLB.json', 'w')
#     json.dump(ravenclawLB, r)
#     json.dump(hufflepuffLB, h)
#     json.dump(slytherinLB, s)
#     json.dump(gryffindorLB, g)
#     print("House Leaderboards saved")
#
# def checkPoints(parsed):
#     key = parsed['message'].split(' ')[1].lower()
#     ws.send(parsed['replyPrefix'] + '{house} has {points} points.'.format(house = parsed['message'].split(' ')[1], points = pointsTracker[key]))
#
# def showHouses(parsed):
#     retString = ''
#     for house in ['Gryffindor', 'Ravenclaw', 'Slytherin', 'Hufflepuff']:
#         key = house.lower()
#         retString += '{house} has {points} points. '.format(house = house, points = pointsTracker[key])
#     ws.send(parsed['replyPrefix'] + retString)
#
# def showTriwizardLB(parsed):
# 	'''Shows the Triwizard LB - no auth and no houses.'''
# 	allUsersPoints = {}
# 	allUsersPoints.update(gryffindorLB)
# 	allUsersPoints.update(ravenclawLB)
# 	allUsersPoints.update(slytherinLB)
# 	allUsersPoints.update(hufflepuffLB)
# 	# We've updated allUsersPoints with all the LBs from the houses.
# 	output = "**Triwizard Tournament Leaderboard:** "
# 	outputTwo = ""
# 	# All the users sorted by how many points they have.
# 	users = list(reversed(sorted(allUsersPoints, key=allUsersPoints.__getitem__)))
# 	AUTH = ['annika0', 'birdy', 'dandaman99', 'profspalding', 'gwynt', 'tonixy', 'imsoapy', 'ravioliqueen', 'tonixy', 'awanderingcaelum','dawnofares', 'madeinsaudi']
# 	# This is a magic variable btw
# 	for user in [p for p in users if p not in AUTH][:16]: # First sixteen non-auth
# 		if len(output) < 260:
# 			output += '__{usern}__: {points}, '.format(usern = user, points = allUsersPoints[user])
# 		else:
# 			outputTwo += '__{usern}__: {points}, '.format(usern = user, points = allUsersPoints[user])
# 	ws.send(parsed['replyPrefix'] + output[:-2])
# 	ws.send(parsed['replyPrefix'] + outputTwo[:-2])
#
#
#
# def lb(parsed):
#     house = parsed['message'].split(' ', 1)[1].split(',')[0].strip()
#     try:
#         n = (-1) * int(parsed['message'].split(' ', 1)[1].split(',')[1])
#     except:
#         n = -5
#     reply = ''
#     if house.lower() == 'gryffindor':
#         for user in reversed(sorted(gryffindorLB, key=gryffindorLB.__getitem__)[n:]):
#             reply += '__{usern}__: {points}, '.format(usern = user, points = gryffindorLB[user])
#     if house.lower() == 'ravenclaw':
#         for user in reversed(sorted(ravenclawLB, key=ravenclawLB.__getitem__)[n:]):
#             reply += '__{usern}__: {points}, '.format(usern = user, points = ravenclawLB[user])
#     if house.lower() == 'slytherin':
#         for user in reversed(sorted(slytherinLB, key=slytherinLB.__getitem__)[n:]):
#             reply += '__{usern}__: {points}, '.format(usern = user, points = slytherinLB[user])
#     if house.lower() == 'hufflepuff':
#         for user in reversed(sorted(hufflepuffLB, key=hufflepuffLB.__getitem__)[n:]):
#             reply += '__{usern}__: {points}, '.format(usern = user, points = hufflepuffLB[user])
#     if reply == '':
#         reply = "{houses} isn't a valid houseaa".format(houses = house)
#     reply = reply[:-2]
#     reply += '.'
#     ws.send(parsed['replyPrefix'] + reply)
#
# def joinHouse(parsed):
#     if 'use the command in PMs for a result.' in parsed['replyPrefix']:
#         ws.send(parsed['replyPrefix'])
#         return
#     house = parsed['message'].split(' ', 1)[1].split(',')[0].strip().lower()
#     print(house)
#     if parsed['user'].lower() not in ravenclaw and parsed['user'].lower() not in hufflepuff and parsed['user'].lower() not in slytherin and parsed['user'].lower() not in gryffindor:
#         if house == 'gryffindor':
#             gryffindor.append(parsed['user'].lower())
#             saveHouses()
#             ws.send(parsed['replyPrefix'] + "You joined Gryffindor!")
#             return
#         if house == 'ravenclaw':
#             ravenclaw.append(parsed['user'].lower())
#             saveHouses()
#             ws.send(parsed['replyPrefix'] + "You joined Ravenclaw!")
#             return
#         if house == 'hufflepuff':
#             hufflepuff.append(parsed['user'].lower())
#             saveHouses()
#             ws.send(parsed['replyPrefix'] + "You joined Hufflepuff!")
#             return
#         if house == 'slytherin':
#             slytherin.append(parsed['user'].lower())
#             saveHouses()
#             ws.send(parsed['replyPrefix'] + "You joined Slytherin!")
#             return
#         else:
#             ws.send(parsed['replyPrefix'] + "{h} isn't a valid house.".format(h = house))
#             return
#     ws.send(parsed['replyPrefix'] + "You're already in a house! Ask Annika0 to change your house.")
#     return
# def checkHouse(parsed):
#     try:
#        	username =  re.sub(r'[^a-zA-Z0-9]', '' ,parsed['message'].split(' ', 1)[1].strip().lower().encode('ascii', 'ignore').decode('utf-8'))
#     except Exception as e:
#         ws.send(parsed['replyPrefix'] + str(e))
#         return
#     if username in gryffindor:
#         ws.send(parsed['replyPrefix'] + 'That user is a Gryffindor.')
#     elif username in slytherin:
#         ws.send(parsed['replyPrefix'] + 'That user is a Slytherin.')
#     elif username in hufflepuff:
#         ws.send(parsed['replyPrefix'] + 'That user is a Hufflepuff.')
#     elif username in ravenclaw:
#         ws.send(parsed['replyPrefix'] + 'That user is a Ravenclaw.')
#     else:
#         ws.send(parsed['replyPrefix'] + "That user isn't in any house.")
#
# def givePoints(parsed):
#     if parsed['numrank'] < numRank('+') and parsed['user'] not in config.goodUsers:
#         ws.send(parsed['replyPrefix'] + "Your rank is not high enough to give points.")
#         return
#     if parsed['type'] == 'pm':
#         ws.send(parsed['replyPrefix'] + "For transparency, please don't give points in PMs.")
#         return
#     loadPoints()
#     args = parsed['message'].split(' ', 1)[1].split(',')
#     house = args[0].lower()
#     user = re.sub(r'[^a-zA-Z0-9]','',args[0].lower().strip().encode("ascii", "ignore").decode("utf-8"))
#     if user in gryffindor:
#         house = 'gryffindor'
#         try:
#             gryffindorLB[user] += int(args[1])
#         except:
#             gryffindorLB[user] = int(args[1])
#     if user in slytherin:
#         house = 'slytherin'
#         try:
#             slytherinLB[user] += int(args[1])
#         except:
#             slytherinLB[user] = int(args[1])
#     if user in hufflepuff:
#         house = 'hufflepuff'
#         try:
#             hufflepuffLB[user] += int(args[1])
#         except:
#             hufflepuffLB[user] = int(args[1])
#     if user in ravenclaw:
#         house = 'ravenclaw'
#         try:
#             ravenclawLB[user] += int(args[1])
#         except:
#             ravenclawLB[user] = int(args[1])
#     if house not in pointsTracker:
#        return
#     try:
#         pointsTracker[house] += int(args[1])
#         saveHouseLBs()
#         savePoints()
#         ws.send("harrypotter|/mn {points} points given to {user} [{hus}] by {giver}".format( points = int(args[1]), user = user, hus=house, giver = parsed['user'])) # * ( len(house) / averageHouse))))
#         ws.send(parsed['replyPrefix'] + '{house} was given {points} points.'.format(house = args[0].encode("ascii","ignore").decode(), points = int(args[1])))
#     except Exception as e:
#         ws.send(parsed['replyPrefix'] + 'There was an error: {msg}. Ask Annika0 for details.'.format(msg=str(e)))

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(config.url,
                              on_message = onMessage,
                              on_error = onError,
                              on_close = onClose)
    ws.on_open = onOpen
    ws.run_forever()
