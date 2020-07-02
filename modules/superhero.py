"""superhero.py
    contains commands for interacting with the Superhero API
    by Annika"""

import requests
import psclient

import config
import data

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {"superhero": self.superhero, "hero": self.superhero}

    def superhero(self, message):
        """Gets information on a superhero from the Superhero API

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        superheroIDDictionary = data.get("superheroIDDictionary") or _initializeData()
        superhero = psclient.toID(config.separator.join(message.arguments[1:]))
        if superhero not in superheroIDDictionary:
            return message.respond(f"{superhero} isn't a superhero that can be looked up with the API.")
        superheroID = superheroIDDictionary[superhero]

        APIResponse = requests.get(f"https://superheroapi.com/api/{config.superheroAPIKey}/{superheroID}").json()
        if APIResponse['response'] != 'success':
            return message.respond(
                f"The API request for {superhero} (ID: {superheroID}) failed with response {APIResponse['response']}."
            )

        # Aliases and relatives can be lists
        aliases = APIResponse['biography']['aliases']
        relatives = APIResponse['connections']['relatives']
        aliases = aliases if isinstance(aliases, str) else ", ".join(aliases)
        relatives = relatives  if isinstance(relatives, str) else ", ".join(relatives)

        html = f"""
            <img src="{APIResponse['image']['url']}" width="1" height="1" style='height: 15%; width: 15%; object-fit: scale-down; padding-right: 15px; float: left'>

            <details><summary>{APIResponse['name']}</summary><details><summary>Stats</summary>
            <b>Intelligence:</b> {APIResponse['powerstats']['intelligence']}<br>
            <b>Strength:</b> {APIResponse['powerstats']['strength']}<br>
            <b>Speed:</b> {APIResponse['powerstats']['speed']}<br>
            <b>Durability:</b> {APIResponse['powerstats']['durability']}<br>
            <b>Power:</b> {APIResponse['powerstats']['power']}<br>
            <b>Combat:</b> {APIResponse['powerstats']['combat']}<br>

            </details><details><summary>Biography</summary>
            <b>Full Name:</b> {APIResponse['biography']['full-name']}<br>
            <b>Alter Egos:</b> {APIResponse['biography']['alter-egos']}<br>
            <b>Aliases:</b> {aliases}<br>
            <b>Birthplace:</b> {APIResponse['biography']['place-of-birth']}<br>
            <b>Debut:</b> {APIResponse['biography']['first-appearance']}<br>
            <b>Publisher:</b> {APIResponse['biography']['publisher']}<br>
            <b>Alignment:</b> {APIResponse['biography']['alignment']}<br>

            </details><details><summary>Appearance</summary>
            <b>Gender:</b> {APIResponse['appearance']['gender']}<br>
            <b>Race:</b> {APIResponse['appearance']['race']}<br>
            <b>Height:</b> {APIResponse['appearance']['height'][1]}<br>
            <b>Weight:</b> {APIResponse['appearance']['weight'][1]}<br>
            <b>Eye Color:</b> {APIResponse['appearance']['eye-color']}<br>
            <b>Hair Color:</b> {APIResponse['appearance']['hair-color']}<br>

            </details><details><summary>Work</summary>
            <b>Occupation:</b> {APIResponse['work']['occupation']}<br>
            <b>Base:</b> {APIResponse['work']['base']}<br>

            </details><details><summary>Connections</summary>
            <b>Group Affiliation:</b> {APIResponse['connections']['group-affiliation']}<br>
            <b>Relatives:</b> {relatives}<br>
            </details></details>
        """

        return message.respondHTML(html)

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Superhero module: interacts with the Superhero API. Commands: {', '.join(self.commands.keys())}"

def _initializeData():
    """Initializes (or updates) the "superheroIDDictionary" data variable

    Returns:
        dictionary -- the superhero ID dictionary
    """
    superheroIDDictionary = {
        'abomb': 1, 'abesapien': 2, 'abinsur': 3, 'abomination': 4, 'abraxas': 5, 'absorbingman': 6, 'adammonroe': 7,
        'adamstrange': 8, 'agent13': 9, 'agentbob': 10, 'agentzero': 11, 'airwalker': 12, 'ajax': 13, 'alanscott': 14,
        'alexmercer': 15, 'alexwoolsly': 16, 'alfredpennyworth': 17, 'alien': 18, 'allanquatermain': 19, 'amazo': 20,
        'ammo': 21, 'andomasahashi': 22, 'angel': 24, 'angeldust': 25, 'angelsalvadore': 26, 'angela': 27, 'animalman': 28,
        'annihilus': 29, 'antman': 30, 'antmanii': 31, 'antimonitor': 32, 'antispawn': 33, 'antivenom': 34, 'apocalypse': 35,
        'aquababy': 36, 'aqualad': 37, 'aquaman': 38, 'arachne': 39, 'archangel': 40, 'arclight': 41, 'ardina': 42,
        'ares': 43, 'ariel': 44, 'armor': 45, 'arsenal': 46, 'astroboy': 47, 'atlas': 49, 'atom': 51, 'atomgirl': 52,
        'atomii': 53, 'atomiii': 54, 'atomiv': 55, 'aurora': 56, 'azazel': 57, 'azrael': 58, 'aztar': 59, 'bane': 60,
        'banshee': 61, 'bantam': 62, 'batgirl': 64, 'batgirliii': 65, 'batgirliv': 66, 'batgirlv': 67, 'batgirlvi': 68,
        'batman': 70, 'batmanii': 71, 'battlestar': 72, 'batwomanv': 73, 'beak': 74, 'beast': 75, 'beastboy': 76,
        'beetle': 77, 'ben10': 78, 'betaraybill': 79, 'beyonder': 80, 'bigbarda': 81, 'bigdaddy': 82, 'bigman': 83,
        'billharken': 84, 'billykincaid': 85, 'binary': 86, 'bionicwoman': 87, 'birdbrain': 88, 'birdman': 91,
        'birdmanii': 90, 'bishop': 92, 'bizarro': 93, 'blackabbott': 94, 'blackadam': 95, 'blackbolt': 96, 'blackcanary': 98,
        'blackcat': 99, 'blackflash': 100, 'blackgoliath': 101, 'blackknightiii': 102, 'blacklightning': 103,
        'blackmamba': 104, 'blackmanta': 105, 'blackpanther': 106, 'blackwidow': 107, 'blackwidowii': 108, 'blackout': 109,
        'blackwing': 110, 'blackwulf': 111, 'blade': 112, 'blaquesmith': 113, 'bling': 114, 'blink': 115, 'blizzard': 117,
        'blizzardii': 118, 'blob': 119, 'bloodaxe': 120, 'bloodhawk': 121, 'bloodwraith': 122, 'bluebeetle': 124,
        'bluebeetleii': 125, 'bluebeetleiii': 126, 'bobafett': 127, 'bolt': 128, 'bombqueen': 129, 'boomboom': 130,
        'boomer': 131, 'boostergold': 132, 'box': 133, 'boxiii': 134, 'boxiv': 135, 'brainiac': 136, 'brainiac5': 137,
        'brothervoodoo': 138, 'brundlefly': 139, 'buffy': 140, 'bullseye': 141, 'bumblebee': 142, 'bumbleboy': 143,
        'bushido': 144, 'cable': 145, 'callisto': 146, 'cameronhicks': 147, 'cannonball': 148, 'captainamerica': 149,
        'captainatom': 150, 'captainbritain': 151, 'captaincold': 152, 'captainepic': 153, 'captainhindsight': 154,
        'captainmarvell': 155, 'captainmarvel': 157, 'captainmarvelii': 158, 'captainmidnight': 159, 'captainplanet': 160,
        'captainuniverse': 161, 'carnage': 162, 'cat': 163, 'catii': 164, 'catwoman': 165, 'ceciliareyes': 166,
        'century': 167, 'cerebra': 168, 'chamber': 169, 'chameleon': 170, 'changeling': 171, 'cheetah': 172, 'cheetahii': 173,
        'cheetahiii': 174, 'chromos': 175, 'chucknorris': 176, 'citizensteel': 177, 'clairebennet': 178, 'clea': 179,
        'cloak': 180, 'clockking': 181, 'cogliostro': 182, 'colinwagner': 183, 'colossalboy': 184, 'colossus': 185,
        'copycat': 186, 'corsair': 187, 'cottonmouth': 188, 'crimsoncrusader': 189, 'crimsondynamo': 190, 'crystal': 191,
        'curse': 192, 'cygor': 193, 'cyborg': 194, 'cyborgsuperman': 195, 'cyclops': 196, 'cypher': 197, 'dagger': 198,
        'dannycooper': 199, 'daphnepowell': 200, 'daredevil': 201, 'darkhawk': 202, 'darkman': 203, 'darkseid': 204,
        'darkside': 205, 'darkstar': 206, 'darthmaul': 207, 'darthvader': 208, 'dash': 209, 'data': 210, 'dazzler': 211,
        'deadman': 212, 'deadpool': 213, 'deadshot': 214, 'deathlok': 215, 'deathstroke': 216, 'demogoblin': 217,
        'destroyer': 218, 'diamondback': 219, 'dlhawkins': 220, 'docsamson': 221, 'doctordoom': 222, 'doctordoomii': 223,
        'doctorfate': 224, 'doctoroctopus': 225, 'doctorstrange': 226, 'domino': 227, 'donatello': 228, 'donnatroy': 229,
        'doomsday': 230, 'doppelganger': 231, 'dormammu': 232, 'drmanhattan': 233, 'draxthedestroyer': 234, 'ego': 235,
        'elastigirl': 236, 'electro': 237, 'elektra': 238, 'ellebishop': 239, 'elongatedman': 240, 'emmafrost': 241,
        'enchantress': 242, 'energy': 243, 'erg1': 244, 'ethanhunt': 245, 'etrigan': 246, 'evildeadpool': 247,
        'evilhawk': 248, 'exodus': 249, 'fabiancortez': 250, 'falcon': 251, 'fallenoneii': 252, 'faora': 253, 'feral': 254,
        'fightingspirit': 255, 'finfangfoom': 256, 'firebird': 257, 'firelord': 258, 'firestar': 259, 'firestorm': 261,
        'fixer': 262, 'flash': 263, 'flashgordon': 264, 'flashii': 265, 'flashiii': 266, 'flashiv': 267, 'forge': 268,
        'franklinrichards': 269, 'franklinstorm': 270, 'frenzy': 271, 'frigga': 272, 'galactus': 273, 'gambit': 274,
        'gamora': 275, 'garbageman': 276, 'garybell': 277, 'generalzod': 278, 'genesis': 279, 'ghostrider': 280,
        'ghostriderii': 281, 'giantman': 282, 'giantmanii': 283, 'giganta': 284, 'gladiator': 285, 'goblinqueen': 286,
        'godzilla': 287, 'gog': 288, 'goku': 289, 'goliath': 292, 'goliathiv': 293, 'gorillagrodd': 294,
        'grannygoodness': 295, 'gravity': 296, 'greedo': 297, 'greenarrow': 298, 'greengoblin': 299, 'greengoblinii': 300,
        'greengobliniii': 301, 'greengobliniv': 302, 'groot': 303, 'guardian': 304, 'guygardner': 305, 'haljordan': 306,
        'hansolo': 307, 'hancock': 308, 'harleyquinn': 309, 'harrypotter': 310, 'havok': 311, 'hawk': 312, 'hawkeye': 313,
        'hawkeyeii': 314, 'hawkgirl': 315, 'hawkman': 316, 'hawkwoman': 317, 'hawkwomanii': 318, 'hawkwomaniii': 319,
        'heatwave': 320, 'hela': 321, 'hellboy': 322, 'hellcat': 323, 'hellstorm': 324, 'hercules': 325, 'hironakamura': 326,
        'hitgirl': 327, 'hobgoblin': 328, 'hollow': 329, 'hopesummers': 330, 'howardtheduck': 331, 'hulk': 332,
        'humantorch': 333, 'huntress': 334, 'husk': 335, 'hybrid': 336, 'hydroman': 337, 'hyperion': 338, 'iceman': 339,
        'impulse': 340, 'indianajones': 341, 'indigo': 342, 'ink': 343, 'invisiblewoman': 344, 'ironfist': 345,
        'ironman': 346, 'ironmonger': 347, 'isis': 348, 'jackbauer': 349, 'jackofhearts': 350, 'jackjack': 351,
        'jamesbond': 352, 'jamestkirk': 353, 'jarjarbinks': 354, 'jasonbourne': 355, 'jeangrey': 356, 'jeanlucpicard': 357,
        'jenniferkale': 358, 'jessequick': 359, 'jessicacruz': 360, 'jessicajones': 361, 'jessicasanders': 362, 'jigsaw': 363,
        'jimpowell': 364, 'jjpowell': 365, 'johannkrauss': 366, 'johnconstantine': 367, 'johnstewart': 368, 'johnwraith': 369,
        'joker': 370, 'jolt': 371, 'jubilee': 372, 'judgedredd': 373, 'juggernaut': 374, 'junkpile': 375, 'justice': 376,
        'jynerso': 377, 'k2so': 378, 'kang': 379, 'kathrynjaneway': 380, 'katnisseverdeen': 381, 'kevin11': 382,
        'kickass': 383, 'kidflash': 384, 'kidflashii': 385, 'killercroc': 386, 'killerfrost': 387, 'kilowog': 388,
        'kingkong': 389, 'kingshark': 390, 'kingpin': 391, 'klaw': 392, 'koolaidman': 393, 'kravenii': 394,
        'kraventhehunter': 395, 'krypto': 396, 'kylerayner': 397, 'kyloren': 398, 'ladybullseye': 399, 'ladydeathstrike': 400,
        'leader': 401, 'leech': 402, 'legion': 403, 'leonardo': 404, 'lexluthor': 405, 'lightlass': 406, 'lightninglad': 407,
        'lightninglord': 408, 'livingbrain': 409, 'livingtribunal': 410, 'lizsherman': 411, 'lizard': 412, 'lobo': 413,
        'loki': 414, 'longshot': 415, 'lukecage': 416, 'lukecampbell': 417, 'lukeskywalker': 418, 'luna': 419, 'lyja': 420,
        'machiv': 421, 'machineman': 422, 'magneto': 423, 'magog': 424, 'magus': 425, 'manofmiracles': 426, 'manbat': 427,
        'manthing': 428, 'manwolf': 429, 'mandarin': 430, 'mantis': 431, 'martianmanhunter': 432, 'marvelgirl': 433,
        'masterbrood': 434, 'masterchief': 435, 'match': 436, 'mattparkman': 437, 'maverick': 438, 'maxima': 439,
        'mayaherrera': 440, 'medusa': 441, 'meltdown': 442, 'mephisto': 443, 'mera': 444, 'metallo': 445, 'metamorpho': 446,
        'meteorite': 447, 'metron': 448, 'micahsanders': 449, 'michelangelo': 450, 'microlad': 451, 'mimic': 452,
        'minnamurray': 453, 'misfit': 454, 'missmartian': 455, 'misterfantastic': 456, 'misterfreeze': 457,
        'misterknife': 458, 'mistermxyzptlk': 459, 'mistersinister': 460, 'misterzsasz': 461, 'mockingbird': 462,
        'modok': 463, 'mogo': 464, 'mohindersuresh': 465, 'moloch': 466, 'moltenman': 467, 'monarch': 468,
        'monicadawson': 469, 'moonknight': 470, 'moonstone': 471, 'morlun': 472, 'morph': 473, 'mosesmagnum': 474,
        'mrimmortal': 475, 'mrincredible': 476, 'msmarvelii': 477, 'multipleman': 478, 'mysterio': 479, 'mystique': 480,
        'namor': 482, 'namora': 483, 'namorita': 484, 'narutouzumaki': 485, 'nathanpetrelli': 486, 'nebula': 487,
        'negasonicteenagewarhead': 488, 'nickfury': 489, 'nightcrawler': 490, 'nightwing': 491, 'nikisanders': 492,
        'ninatheroux': 493, 'niteowlii': 494, 'northstar': 495, 'nova': 497, 'odin': 498, 'offspring': 499, 'omegared': 500,
        'omniscient': 501, 'onepunchman': 502, 'oneaboveall': 503, 'onslaught': 504, 'oracle': 505, 'osiris': 506,
        'overtkill': 507, 'ozymandias': 508, 'parademon': 509, 'paulblart': 510, 'penance': 511, 'penancei': 512,
        'penanceii': 513, 'penguin': 514, 'phantom': 515, 'phantomgirl': 516, 'phoenix': 517, 'plantman': 518,
        'plasticlad': 519, 'plasticman': 520, 'plastique': 521, 'poisonivy': 522, 'polaris': 523, 'powergirl': 524,
        'powerman': 525, 'predator': 526, 'professorx': 527, 'professorzoom': 528, 'psylocke': 529, 'punisher': 530,
        'purpleman': 531, 'pyro': 532, 'q': 533, 'quantum': 534, 'question': 535, 'quicksilver': 536, 'quill': 537,
        'rasalghul': 538, 'rachelpirzad': 539, 'rambo': 540, 'raphael': 541, 'raven': 542, 'ray': 543, 'razorfistii': 544,
        'redarrow': 545, 'redhood': 546, 'redhulk': 547, 'redmist': 548, 'redrobin': 549, 'redskull': 550, 'redtornado': 551,
        'redeemerii': 552, 'redeemeriii': 553, 'renatasoliz': 554, 'rey': 555, 'rhino': 556, 'rickflag': 557, 'riddler': 558,
        'riphunter': 559, 'ripcord': 560, 'robin': 561, 'robinii': 562, 'robiniii': 563, 'robinv': 564, 'robinvi': 565,
        'rocketraccoon': 566, 'rogue': 567, 'ronin': 568, 'rorschach': 569, 'sabretooth': 570, 'sage': 571, 'sandman': 572,
        'sasquatch': 573, 'sauron': 574, 'savagedragon': 575, 'scarecrow': 576, 'scarletspider': 577, 'scarletspiderii': 578,
        'scarletwitch': 579, 'scorpia': 580, 'scorpion': 581, 'sebastianshaw': 582, 'sentry': 583, 'shadowking': 584,
        'shadowlass': 585, 'shadowcat': 586, 'shangchi': 587, 'shatterstar': 588, 'shehulk': 589, 'shething': 590,
        'shocker': 591, 'shriek': 592, 'shrinkingviolet': 593, 'sif': 594, 'silk': 595, 'silkspectre': 596,
        'silkspectreii': 597, 'silversurfer': 598, 'silverclaw': 599, 'simonbaz': 600, 'sinestro': 601, 'siren': 602,
        'sirenii': 603, 'siryn': 604, 'skaar': 605, 'snakeeyes': 606, 'snowbird': 607, 'sobek': 608, 'solomongrundy': 609,
        'songbird': 610, 'spaceghost': 611, 'spawn': 612, 'spectre': 613, 'speedball': 614, 'speedy': 616,
        'spidercarnage': 617, 'spidergirl': 618, 'spidergwen': 619, 'spiderman': 622, 'spiderwoman': 623,
        'spiderwomanii': 624, 'spiderwomaniii': 625, 'spiderwomaniv': 626, 'spock': 627, 'spyke': 628, 'stacyx': 629,
        'starlord': 630, 'stardust': 631, 'starfire': 632, 'stargirl': 633, 'static': 634, 'steel': 635,
        'stephaniepowell': 636, 'steppenwolf': 637, 'storm': 638, 'stormtrooper': 639, 'sunspot': 640, 'superboy': 641,
        'superboyprime': 642, 'supergirl': 643, 'superman': 644, 'swampthing': 645, 'swarm': 646, 'sylar': 647, 'synch': 648,
        't1000': 649, 't800': 650, 't850': 651, 'tx': 652, 'taskmaster': 653, 'tempest': 654, 'thanos': 655, 'thecape': 656,
        'thecomedian': 657, 'thing': 658, 'thor': 659, 'thorgirl': 660, 'thunderbird': 661, 'thunderbirdii': 662,
        'thunderbirdiii': 663, 'thunderstrike': 664, 'thundra': 665, 'tigershark': 666, 'tigra': 667, 'tinkerer': 668,
        'titan': 669, 'toad': 670, 'toxin': 672, 'tracystrauss': 673, 'trickster': 674, 'trigon': 675, 'triplicategirl': 676,
        'triton': 677, 'twoface': 678, 'ultragirl': 679, 'ultron': 680, 'utgardloki': 681, 'vagabond': 682,
        'valeriehart': 683, 'valkyrie': 684, 'vanisher': 685, 'vegeta': 686, 'venom': 687, 'venomii': 688, 'venomiii': 689,
        'venompool': 690, 'vertigoii': 691, 'vibe': 692, 'vindicator': 694, 'violator': 695, 'violetparr': 696, 'vision': 697,
        'visionii': 698, 'vixen': 699, 'vulcan': 700, 'vulture': 701, 'walrus': 702, 'warmachine': 703, 'warbird': 704,
        'warlock': 705, 'warp': 706, 'warpath': 707, 'wasp': 708, 'watcher': 709, 'weaponxi': 710, 'whitecanary': 711,
        'whitequeen': 712, 'wildfire': 713, 'wintersoldier': 714, 'wizkid': 715, 'wolfsbane': 716, 'wolverine': 717,
        'wondergirl': 718, 'wonderman': 719, 'wonderwoman': 720, 'wondra': 721, 'wyattwingfoot': 722, 'x23': 723, 'xman': 724,
        'yellowclaw': 725, 'yellowjacket': 726, 'yellowjacketii': 727, 'ymir': 728, 'yoda': 729, 'zatanna': 730, 'zoom': 731
    }
    data.store("superheroIDDictionary", superheroIDDictionary)
    return superheroIDDictionary
