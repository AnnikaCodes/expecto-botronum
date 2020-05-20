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

superheroes = {'abomb': 1, 'abesapien': 2, 'abinsur': 3, 'abomination': 4, 'abraxas': 5, 'absorbingman': 6, 'adammonroe': 7, 'adamstrange': 8, 'agent13': 9, 'agentbob': 10, 'agentzero': 11, 'airwalker': 12, 'ajax': 13, 'alanscott': 14, 'alexmercer': 15, 'alexwoolsly': 16, 'alfredpennyworth': 17, 'alien': 18, 'allanquatermain': 19, 'amazo': 20, 'ammo': 21, 'andomasahashi': 22, 'angel': 24, 'angeldust': 25, 'angelsalvadore': 26, 'angela': 27, 'animalman': 28, 'annihilus': 29, 'antman': 30, 'antmanii': 31, 'antimonitor': 32, 'antispawn': 33, 'antivenom': 34, 'apocalypse': 35, 'aquababy': 36, 'aqualad': 37, 'aquaman': 38, 'arachne': 39, 'archangel': 40, 'arclight': 41, 'ardina': 42, 'ares': 43, 'ariel': 44, 'armor': 45, 'arsenal': 46, 'astroboy': 47, 'atlas': 49, 'atom': 51, 'atomgirl': 52, 'atomii': 53, 'atomiii': 54, 'atomiv': 55, 'aurora': 56, 'azazel': 57, 'azrael': 58, 'aztar': 59, 'bane': 60, 'banshee': 61, 'bantam': 62, 'batgirl': 64, 'batgirliii': 65, 'batgirliv': 66, 'batgirlv': 67, 'batgirlvi': 68, 'batman': 70, 'batmanii': 71, 'battlestar': 72, 'batwomanv': 73, 'beak': 74, 'beast': 75, 'beastboy': 76, 'beetle': 77, 'ben10': 78, 'betaraybill': 79, 'beyonder': 80, 'bigbarda': 81, 'bigdaddy': 82, 'bigman': 83, 'billharken': 84, 'billykincaid': 85, 'binary': 86, 'bionicwoman': 87, 'birdbrain': 88, 'birdman': 91, 'birdmanii': 90, 'bishop': 92, 'bizarro': 93, 'blackabbott': 94, 'blackadam': 95, 'blackbolt': 96, 'blackcanary': 98, 'blackcat': 99, 'blackflash': 100, 'blackgoliath': 101, 'blackknightiii': 102, 'blacklightning': 103, 'blackmamba': 104, 'blackmanta': 105, 'blackpanther': 106, 'blackwidow': 107, 'blackwidowii': 108, 'blackout': 109, 'blackwing': 110, 'blackwulf': 111, 'blade': 112, 'blaquesmith': 113, 'bling': 114, 'blink': 115, 'blizzard': 117, 'blizzardii': 118, 'blob': 119, 'bloodaxe': 120, 'bloodhawk': 121, 'bloodwraith': 122, 'bluebeetle': 124, 'bluebeetleii': 125, 'bluebeetleiii': 126, 'bobafett': 127, 'bolt': 128, 'bombqueen': 129, 'boomboom': 130, 'boomer': 131, 'boostergold': 132, 'box': 133, 'boxiii': 134, 'boxiv': 135, 'brainiac': 136, 'brainiac5': 137, 'brothervoodoo': 138, 'brundlefly': 139, 'buffy': 140, 'bullseye': 141, 'bumblebee': 142, 'bumbleboy': 143, 'bushido': 144, 'cable': 145, 'callisto': 146, 'cameronhicks': 147, 'cannonball': 148, 'captainamerica': 149, 'captainatom': 150, 'captainbritain': 151, 'captaincold': 152, 'captainepic': 153, 'captainhindsight': 154, 'captainmarvell': 155, 'captainmarvel': 157, 'captainmarvelii': 158, 'captainmidnight': 159, 'captainplanet': 160, 'captainuniverse': 161, 'carnage': 162, 'cat': 163, 'catii': 164, 'catwoman': 165, 'ceciliareyes': 166, 'century': 167, 'cerebra': 168, 'chamber': 169, 'chameleon': 170, 'changeling': 171, 'cheetah': 172, 'cheetahii': 173, 'cheetahiii': 174, 'chromos': 175, 'chucknorris': 176, 'citizensteel': 177, 'clairebennet': 178, 'clea': 179, 'cloak': 180, 'clockking': 181, 'cogliostro': 182, 'colinwagner': 183, 'colossalboy': 184, 'colossus': 185, 'copycat': 186, 'corsair': 187, 'cottonmouth': 188, 'crimsoncrusader': 189, 'crimsondynamo': 190, 'crystal': 191, 'curse': 192, 'cygor': 193, 'cyborg': 194, 'cyborgsuperman': 195, 'cyclops': 196, 'cypher': 197, 'dagger': 198, 'dannycooper': 199, 'daphnepowell': 200, 'daredevil': 201, 'darkhawk': 202, 'darkman': 203, 'darkseid': 204, 'darkside': 205, 'darkstar': 206, 'darthmaul': 207, 'darthvader': 208, 'dash': 209, 'data': 210, 'dazzler': 211, 'deadman': 212, 'deadpool': 213, 'deadshot': 214, 'deathlok': 215, 'deathstroke': 216, 'demogoblin': 217, 'destroyer': 218, 'diamondback': 219, 'dlhawkins': 220, 'docsamson': 221, 'doctordoom': 222, 'doctordoomii': 223, 'doctorfate': 224, 'doctoroctopus': 225, 'doctorstrange': 226, 'domino': 227, 'donatello': 228, 'donnatroy': 229, 'doomsday': 230, 'doppelganger': 231, 'dormammu': 232, 'drmanhattan': 233, 'draxthedestroyer': 234, 'ego': 235, 'elastigirl': 236, 'electro': 237, 'elektra': 238, 'ellebishop': 239, 'elongatedman': 240, 'emmafrost': 241, 'enchantress': 242, 'energy': 243, 'erg1': 244, 'ethanhunt': 245, 'etrigan': 246, 'evildeadpool': 247, 'evilhawk': 248, 'exodus': 249, 'fabiancortez': 250, 'falcon': 251, 'fallenoneii': 252, 'faora': 253, 'feral': 254, 'fightingspirit': 255, 'finfangfoom': 256, 'firebird': 257, 'firelord': 258, 'firestar': 259, 'firestorm': 261, 'fixer': 262, 'flash': 263, 'flashgordon': 264, 'flashii': 265, 'flashiii': 266, 'flashiv': 267, 'forge': 268, 'franklinrichards': 269, 'franklinstorm': 270, 'frenzy': 271, 'frigga': 272, 'galactus': 273, 'gambit': 274, 'gamora': 275, 'garbageman': 276, 'garybell': 277, 'generalzod': 278, 'genesis': 279, 'ghostrider': 280, 'ghostriderii': 281, 'giantman': 282, 'giantmanii': 283, 'giganta': 284, 'gladiator': 285, 'goblinqueen': 286, 'godzilla': 287, 'gog': 288, 'goku': 289, 'goliath': 292, 'goliathiv': 293, 'gorillagrodd': 294, 'grannygoodness': 295, 'gravity': 296, 'greedo': 297, 'greenarrow': 298, 'greengoblin': 299, 'greengoblinii': 300, 'greengobliniii': 301, 'greengobliniv': 302, 'groot': 303, 'guardian': 304, 'guygardner': 305, 'haljordan': 306, 'hansolo': 307, 'hancock': 308, 'harleyquinn': 309, 'harrypotter': 310, 'havok': 311, 'hawk': 312, 'hawkeye': 313, 'hawkeyeii': 314, 'hawkgirl': 315, 'hawkman': 316, 'hawkwoman': 317, 'hawkwomanii': 318, 'hawkwomaniii': 319, 'heatwave': 320, 'hela': 321, 'hellboy': 322, 'hellcat': 323, 'hellstorm': 324, 'hercules': 325, 'hironakamura': 326, 'hitgirl': 327, 'hobgoblin': 328, 'hollow': 329, 'hopesummers': 330, 'howardtheduck': 331, 'hulk': 332, 'humantorch': 333, 'huntress': 334, 'husk': 335, 'hybrid': 336, 'hydroman': 337, 'hyperion': 338, 'iceman': 339, 'impulse': 340, 'indianajones': 341, 'indigo': 342, 'ink': 343, 'invisiblewoman': 344, 'ironfist': 345, 'ironman': 346, 'ironmonger': 347, 'isis': 348, 'jackbauer': 349, 'jackofhearts': 350, 'jackjack': 351, 'jamesbond': 352, 'jamestkirk': 353, 'jarjarbinks': 354, 'jasonbourne': 355, 'jeangrey': 356, 'jeanlucpicard': 357, 'jenniferkale': 358, 'jessequick': 359, 'jessicacruz': 360, 'jessicajones': 361, 'jessicasanders': 362, 'jigsaw': 363, 'jimpowell': 364, 'jjpowell': 365, 'johannkrauss': 366, 'johnconstantine': 367, 'johnstewart': 368, 'johnwraith': 369, 'joker': 370, 'jolt': 371, 'jubilee': 372, 'judgedredd': 373, 'juggernaut': 374, 'junkpile': 375, 'justice': 376, 'jynerso': 377, 'k2so': 378, 'kang': 379, 'kathrynjaneway': 380, 'katnisseverdeen': 381, 'kevin11': 382, 'kickass': 383, 'kidflash': 384, 'kidflashii': 385, 'killercroc': 386, 'killerfrost': 387, 'kilowog': 388, 'kingkong': 389, 'kingshark': 390, 'kingpin': 391, 'klaw': 392, 'koolaidman': 393, 'kravenii': 394, 'kraventhehunter': 395, 'krypto': 396, 'kylerayner': 397, 'kyloren': 398, 'ladybullseye': 399, 'ladydeathstrike': 400, 'leader': 401, 'leech': 402, 'legion': 403, 'leonardo': 404, 'lexluthor': 405, 'lightlass': 406, 'lightninglad': 407, 'lightninglord': 408, 'livingbrain': 409, 'livingtribunal': 410, 'lizsherman': 411, 'lizard': 412, 'lobo': 413, 'loki': 414, 'longshot': 415, 'lukecage': 416, 'lukecampbell': 417, 'lukeskywalker': 418, 'luna': 419, 'lyja': 420, 'machiv': 421, 'machineman': 422, 'magneto': 423, 'magog': 424, 'magus': 425, 'manofmiracles': 426, 'manbat': 427, 'manthing': 428, 'manwolf': 429, 'mandarin': 430, 'mantis': 431, 'martianmanhunter': 432, 'marvelgirl': 433, 'masterbrood': 434, 'masterchief': 435, 'match': 436, 'mattparkman': 437, 'maverick': 438, 'maxima': 439, 'mayaherrera': 440, 'medusa': 441, 'meltdown': 442, 'mephisto': 443, 'mera': 444, 'metallo': 445, 'metamorpho': 446, 'meteorite': 447, 'metron': 448, 'micahsanders': 449, 'michelangelo': 450, 'microlad': 451, 'mimic': 452, 'minnamurray': 453, 'misfit': 454, 'missmartian': 455, 'misterfantastic': 456, 'misterfreeze': 457, 'misterknife': 458, 'mistermxyzptlk': 459, 'mistersinister': 460, 'misterzsasz': 461, 'mockingbird': 462, 'modok': 463, 'mogo': 464, 'mohindersuresh': 465, 'moloch': 466, 'moltenman': 467, 'monarch': 468, 'monicadawson': 469, 'moonknight': 470, 'moonstone': 471, 'morlun': 472, 'morph': 473, 'mosesmagnum': 474, 'mrimmortal': 475, 'mrincredible': 476, 'msmarvelii': 477, 'multipleman': 478, 'mysterio': 479, 'mystique': 480, 'namor': 482, 'namora': 483, 'namorita': 484, 'narutouzumaki': 485, 'nathanpetrelli': 486, 'nebula': 487, 'negasonicteenagewarhead': 488, 'nickfury': 489, 'nightcrawler': 490, 'nightwing': 491, 'nikisanders': 492, 'ninatheroux': 493, 'niteowlii': 494, 'northstar': 495, 'nova': 497, 'odin': 498, 'offspring': 499, 'omegared': 500, 'omniscient': 501, 'onepunchman': 502, 'oneaboveall': 503, 'onslaught': 504, 'oracle': 505, 'osiris': 506, 'overtkill': 507, 'ozymandias': 508, 'parademon': 509, 'paulblart': 510, 'penance': 511, 'penancei': 512, 'penanceii': 513, 'penguin': 514, 'phantom': 515, 'phantomgirl': 516, 'phoenix': 517, 'plantman': 518, 'plasticlad': 519, 'plasticman': 520, 'plastique': 521, 'poisonivy': 522, 'polaris': 523, 'powergirl': 524, 'powerman': 525, 'predator': 526, 'professorx': 527, 'professorzoom': 528, 'psylocke': 529, 'punisher': 530, 'purpleman': 531, 'pyro': 532, 'q': 533, 'quantum': 534, 'question': 535, 'quicksilver': 536, 'quill': 537, 'rasalghul': 538, 'rachelpirzad': 539, 'rambo': 540, 'raphael': 541, 'raven': 542, 'ray': 543, 'razorfistii': 544, 'redarrow': 545, 'redhood': 546, 'redhulk': 547, 'redmist': 548, 'redrobin': 549, 'redskull': 550, 'redtornado': 551, 'redeemerii': 552, 'redeemeriii': 553, 'renatasoliz': 554, 'rey': 555, 'rhino': 556, 'rickflag': 557, 'riddler': 558, 'riphunter': 559, 'ripcord': 560, 'robin': 561, 'robinii': 562, 'robiniii': 563, 'robinv': 564, 'robinvi': 565, 'rocketraccoon': 566, 'rogue': 567, 'ronin': 568, 'rorschach': 569, 'sabretooth': 570, 'sage': 571, 'sandman': 572, 'sasquatch': 573, 'sauron': 574, 'savagedragon': 575, 'scarecrow': 576, 'scarletspider': 577, 'scarletspiderii': 578, 'scarletwitch': 579, 'scorpia': 580, 'scorpion': 581, 'sebastianshaw': 582, 'sentry': 583, 'shadowking': 584, 'shadowlass': 585, 'shadowcat': 586, 'shangchi': 587, 'shatterstar': 588, 'shehulk': 589, 'shething': 590, 'shocker': 591, 'shriek': 592, 'shrinkingviolet': 593, 'sif': 594, 'silk': 595, 'silkspectre': 596, 'silkspectreii': 597, 'silversurfer': 598, 'silverclaw': 599, 'simonbaz': 600, 'sinestro': 601, 'siren': 602, 'sirenii': 603, 'siryn': 604, 'skaar': 605, 'snakeeyes': 606, 'snowbird': 607, 'sobek': 608, 'solomongrundy': 609, 'songbird': 610, 'spaceghost': 611, 'spawn': 612, 'spectre': 613, 'speedball': 614, 'speedy': 616, 'spidercarnage': 617, 'spidergirl': 618, 'spidergwen': 619, 'spiderman': 622, 'spiderwoman': 623, 'spiderwomanii': 624, 'spiderwomaniii': 625, 'spiderwomaniv': 626, 'spock': 627, 'spyke': 628, 'stacyx': 629, 'starlord': 630, 'stardust': 631, 'starfire': 632, 'stargirl': 633, 'static': 634, 'steel': 635, 'stephaniepowell': 636, 'steppenwolf': 637, 'storm': 638, 'stormtrooper': 639, 'sunspot': 640, 'superboy': 641, 'superboyprime': 642, 'supergirl': 643, 'superman': 644, 'swampthing': 645, 'swarm': 646, 'sylar': 647, 'synch': 648, 't1000': 649, 't800': 650, 't850': 651, 'tx': 652, 'taskmaster': 653, 'tempest': 654, 'thanos': 655, 'thecape': 656, 'thecomedian': 657, 'thing': 658, 'thor': 659, 'thorgirl': 660, 'thunderbird': 661, 'thunderbirdii': 662, 'thunderbirdiii': 663, 'thunderstrike': 664, 'thundra': 665, 'tigershark': 666, 'tigra': 667, 'tinkerer': 668, 'titan': 669, 'toad': 670, 'toxin': 672, 'tracystrauss': 673, 'trickster': 674, 'trigon': 675, 'triplicategirl': 676, 'triton': 677, 'twoface': 678, 'ultragirl': 679, 'ultron': 680, 'utgardloki': 681, 'vagabond': 682, 'valeriehart': 683, 'valkyrie': 684, 'vanisher': 685, 'vegeta': 686, 'venom': 687, 'venomii': 688, 'venomiii': 689, 'venompool': 690, 'vertigoii': 691, 'vibe': 692, 'vindicator': 694, 'violator': 695, 'violetparr': 696, 'vision': 697, 'visionii': 698, 'vixen': 699, 'vulcan': 700, 'vulture': 701, 'walrus': 702, 'warmachine': 703, 'warbird': 704, 'warlock': 705, 'warp': 706, 'warpath': 707, 'wasp': 708, 'watcher': 709, 'weaponxi': 710, 'whitecanary': 711, 'whitequeen': 712, 'wildfire': 713, 'wintersoldier': 714, 'wizkid': 715, 'wolfsbane': 716, 'wolverine': 717, 'wondergirl': 718, 'wonderman': 719, 'wonderwoman': 720, 'wondra': 721, 'wyattwingfoot': 722, 'x23': 723, 'xman': 724, 'yellowclaw': 725, 'yellowjacket': 726, 'yellowjacketii': 727, 'ymir': 728, 'yoda': 729, 'zatanna': 730, 'zoom': 731}

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

###################
## Superhero API ##
###################

def superhero(parsed):
	argument = parsed['message'].split(' ',1)[1].strip()
	id = re.sub(r'[^a-zA-Z0-9]', '', argument).lower() # remove non alphanumeric stuff
	# convert to int
	if id in superheroes:
		id = superheroes[id]
	elif id.isdigit():
		id = int(id)

	if type(id) is str or id not in range(1,732): # not a valid id
		ws.send(parsed['replyPrefix'] + "{hero} is not a valid superhero.".format(hero=argument))
		return

	request = requests.get("https://superheroapi.com/api/{key}/{id}".format(key=config.superheroAPIKey, id=id)).content
	data = json.loads(request)

	if data['response'] != 'success': # oops! let's drop stuff for debugging
		ws.send(parsed['replyPrefix'] + "The API request for {hero} (ID: {id}) failed with response {response}. Please try again.".format(hero=hero, id=id, response=data['response']))

	# Giant string of HTML that's then formatted.
	# This is hacky but it's the simplest way I found to do it
	# And since we're not doing this conversion from dictionaries to HTML <details> elements much I think it's OK.
	html = """<img src="{image}" width="1" height="1" style='height: 15%; width: 15%; object-fit: scale-down; padding-right: 15px; float: left'>
	<details><summary>{name}</summary><details><summary>Stats</summary>
	<b>Intelligence:</b> {int}<br/><b>Strength:</b> {str}<br/><b>Speed:</b> {spe}<br/>
	<b>Durability:</b> {dur}<br/><b>Power:</b> {pow}<br/><b>Combat:</b> {com}<br/>
	</details><details><summary>Biography</summary>
	<b>Full Name:</b> {fullname}<br/><b>Alter Egos:</b> {altergos}<br/><b>Aliases:</b> {aliases}<br/>
	<b>Birthplace:</b> {birthplace}<br/><b>Debut:</b> {debut}<br/><b>Publisher:</b> {publisher}<br/>
	<b>Alignment:</b> {alignment}<br/>
	</details><details><summary>Appearance</summary>
	<b>Gender:</b> {gender}<br/><b>Race:</b> {race}<br/><b>Height:</b> {height}<br/><b>Weight:</b> {weight}<br/>
	<b>Eye Color:</b> {eye}<br/><b>Hair Color:</b> {hair}<br/>
	</details><details><summary>Work</summary>
	<b>Occupation:</b> {occupation}<br/><b>Base:</b> {base}<br/>
	</details><details><summary>Connections</summary>
	<b>Group Affiliation:</b> {group}<br/><b>Relatives:</b> {relatives}<br/>
	</details></details>
	"""

	# the API may return lists of aliases and relatives, so we can't use that data directly.
	aliases = data['biography']['aliases']
	relatives = data['connections']['relatives']
	if type(aliases) is list:
		aliases = ", ".join(aliases)
	if type(relatives) is list:
		relatives = ", ".join(relatives)

	# To whomever needs to read this code, I'm sorry.
	html = html.format(name = data['name'], image = data['image']['url'], int = data['powerstats']['intelligence'],
		str = data['powerstats']['strength'], spe = data['powerstats']['speed'], dur = data['powerstats']['durability'],
		pow = data['powerstats']['power'], com = data['powerstats']['combat'], fullname = data['biography']['full-name'],
		altergos = data['biography']['alter-egos'], aliases = aliases, birthplace = data['biography']['place-of-birth'],
		debut = data['biography']['first-appearance'], publisher = data['biography']['publisher'], alignment = data['biography']['alignment'],
		gender = data['appearance']['gender'], race = data['appearance']['race'], height = data['appearance']['height'][1],
		weight = data['appearance']['weight'][1], eye = data['appearance']['eye-color'], hair = data['appearance']['hair-color'],
		occupation = data['work']['occupation'], base = data['work']['base'], group = data['connections']['group-affiliation'], relatives = relatives)
	if parsed['type'] == 'pm':
		# super hacky + you need to be in M&M for it to work
		ws.send(parsed['replyPrefix'] + "``~superhero`` only works in PMs if you are in <<" + config.rooms[0] + ">>.")
		ws.send(config.rooms[0] + "|/pminfobox {user},{html}".format(user=parsed['user'],html=html.replace('\n','').replace('15','40')))
	else:
		ws.send(parsed['replyPrefix'] + '/adduhtml superhero,' + html)


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
