"""sampleteams.py
    provides sample teams to the Portuguese room
    by Annika"""

from typing import Dict, Any, Union, List

import psclient # type: ignore
import core

htmlboxes: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {
    "gen7uu": [
        {
            "tier": "[Gen 7] UU",
            "name": "Reuniclus Bulky Offense",
            "pokemon": ["infernape", "klefki", "reuniclus", "hydreigon", "aerodactyl-mega", "tentacruel"],
            "pokepasteURL": "https://pokepast.es/734acc955fc2fa62",
            "username": "Amane Misa",
        },
        {
            "tier": "[Gen 7] UU",
            "name": "Hazards Stacking HO",
            "pokemon": ["sharpedo-mega", "latias", "froslass", "cobalion", "mimikyu", "mamoswine"],
            "pokepasteURL": "https://pokepast.es/415c42ba45bfce3f",
            "username": "Adaam",
        },
        {
            "tier": "[Gen 7] UU",
            "name": "Screens HO",
            "pokemon": ["xatu", "krookodile", "latias", "linoone", "scizor", "feraligatr"],
            "pokepasteURL": "https://pokepast.es/17d63170ca804d6e",
            "username": "Amane Misa",
        },
        {
            "tier": "[Gen 7] UU",
            "name": "Sand BO",
            "pokemon": ["tentacruel", "aerodactyl-mega", "celebi", "hippowdon", "cobalion", "doublade"],
            "pokepasteURL": "https://pokepast.es/dff49306fe0f0c10",
            "username": "Sage",
        },
        {
            "tier": "[Gen 7] UU",
            "name": "Semi-Stall",
            "pokemon": ["altaria-mega", "magneton", "alomomola", "blissey", "gligar", "scizor"],
            "pokepasteURL": "https://pokepast.es/ca4946eeb84bc044",
            "username": "Christo",
        },
        {
            "tier": "[Gen 7] UU",
            "name": "Bulky Offense",
            "pokemon": ["rotom-heat", "altaria-mega", "tentacruel", "krookodile", "necrozma", "scizor"],
            "pokepasteURL": "https://pokepast.es/33c1f022384b761d",
            "username": "vivalospride",
        },
        {
            "tier": "[Gen 7] UU",
            "name": "Spikes Stall",
            "pokemon": ["umbreon", "alomomola", "blissey", "klefki", "tentacruel", "quagsire"],
            "pokepasteURL": "https://pokepast.es/6502caa9ade216a3",
            "username": "pokeisfun",
        },
    ],
    "gen7ou": [
        {
            "tier": "[Gen 7] OU",
            "name": "Conkeldurr Trick Room",
            "pokemon": ["magearna", "mesprit", "cresselia", "mawile-mega", "marowak-alola", "conkeldurr"],
            "pokepasteURL": "https://pokepast.es/22d6df9005c25f13",
            "username": "Hyperion1233",
        },
        {
            "tier": "[Gen 7] OU",
            "name": "Adrenaline Kartana",
            "pokemon": ["kartana", "mew", "scizor-mega", "rotom-wash", "kyurem", "magearna"],
            "pokepasteURL": "https://pokepast.es/17a5eabc048548e0",
            "username": "ManjoojII",
        },
        {
            "tier": "[Gen 7] OU",
            "name": "Mega Diancie Balanced",
            "pokemon": ["diancie-mega", "ferrothorn", "tapu-lele", "heatran", "greninja-ash", "zapdos"],
            "pokepasteURL": "https://pokepast.es/04b8ccebd1f39869",
            "username": "ORASSS",
        },
        {
            "tier": "[Gen 7] OU",
            "name": "Medicham Dual Punch",
            "pokemon": ["tapu-koko", "medicham-mega", "ferrothorn", "zapdos", "ditto", "greninja"],
            "pokepasteURL": "https://pokepast.es/df4cedf025e5f1cf",
            "username": "Imagine Fairies",
        },
        {
            "tier": "[Gen 7] OU",
            "name": "MScizor Bulky Offense",
            "pokemon": ["slowbro", "kommo-o", "tapu-fini", "scizor-mega", "heatran", "landorus-therian"],
            "pokepasteURL": "https://pokepast.es/22f3b9f0c8617986",
            "username": "Skiry",
        },
        {
            "tier": "[Gen 7] OU",
            "name": "Kommo-o BO",
            "pokemon": ["kommo-o", "clefable", "tapu-koko", "magnezone", "latias-mega", "tapu-fini"],
            "pokepasteURL": "https://pokepast.es/3d50e5c476efc26b",
            "username": "Skiry",
        },
    ],
    "gen8rps": [
        {
            "tier": "[Gen 8] Rock, Paper, Scissors",
            "name": "Rock, Paper, Scissors",
            "pokemon": ["golem", "leafeon", "swellow"],
            "pokepasteURL": "https://pokepast.es/81714a0f5c3ad6c0",
            "username": "MyPearl",
        },
    ],
    "gen8shedinjamb": [
        {
            "tier": "[Gen 8] Shedinja Metronome Battle",
            "name": "Shedinja Metronome Battle",
            "pokemon": ["shedinja", "shedinja", "shedinja", "shedinja", "shedinja", "shedinja"],
            "pokepasteURL": "https://pokepast.es/4d779bd467a94029",
            "username": "MyPearl",
        },
    ],
    "gen8birdpresentbattle": [
        {
            "tier": "[Gen 8] Delibird Hustle Present Battle",
            "name": "Delibird Hustle Present Battle",
            "pokemon": ["delibird", "delibird", "delibird", "delibird", "delibird", "delibird"],
            "pokepasteURL": "https://pokepast.es/00a6873514d574e7",
            "username": "MyPearl",
        },
    ],
    "gen7monotype": [
        {
            "tier": "[Gen 7] Monotype",
            "name": "Mega Pinsir Hyper Offense Bug",
            "pokemon": ["volcarona", "pinsir-mega", "heracross", "scizor", "galvantula", "armaldo"],
            "pokepasteURL": "https://pokepast.es/29ba0818f219c0f1",
            "username": "GoldenTorkoal",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Mega Sharpedo Balance Water",
            "pokemon": ["swampert", "toxapex", "rotom-wash", "keldeo", "greninja", "sharpedo-mega"],
            "pokepasteURL": "https://pokepast.es/9f7f89a624d29937",
            "username": "Tico 21",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Sticky Webs Fairy",
            "pokemon": ["ribombee", "klefki", "diancie-mega", "tapu-koko", "azumarill", "tapu-bulu"],
            "pokepasteURL": "https://pokepast.es/e80d35100f5cbf88",
            "username": "Harpp",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Offensive Dragon",
            "pokemon": ["dragonite", "latios", "kommo-o", "garchomp", "altaria-mega", "kyurem-black"],
            "pokepasteURL": "https://pokepast.es/f950a52accdb3b92",
            "username": "Eien",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Sticky Webs HO Rock",
            "pokemon": ["shuckle", "golem-alola", "terrakion", "nihilego", "diancie-mega", "tyranitar"],
            "pokepasteURL": "https://pokepast.es/e0e764ccf08f0b8c",
            "username": "Tico 21",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Balance Flying",
            "pokemon": ["landorus-therian", "charizard-mega-y", "skarmory", "zapdos", "mantine", "gliscor"],
            "pokepasteURL": "https://pokepast.es/3ebf7571a55753d3",
            "username": "Izaya",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Balance Ghost",
            "pokemon": ["gengar", "jellicent", "gourgeist-super", "marowak-alola", "mimikyu", "sableye-mega"],
            "pokepasteURL": "https://pokepast.es/f787ed43aafe4d37",
            "username": "Decem",
        },
    ],
    "gen7ubers": [
        {
            "tier": "[Gen 7] Ubers",
            "name": "Dual Primal + Extremekiller Arceus HO",
            "pokemon": ["salamence-mega", "kyogre-primal", "groudon-primal", "arceus", "xerneas", "necrozma-dusk-mane"],
            "pokepasteURL": "https://pokepast.es/0adb04027d87a8d6",
            "username": "Mysterious M & Zesty43",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "Dual Primal Bulky Offense",
            "pokemon": ["kyogre-primal", "groudon-primal", "arceus-fairy", "yveltal", "necrozma-dusk-mane", "salamence-mega"],
            "pokepasteURL": "https://pokepast.es/1cc156c3bfed4d34",
            "username": "obii",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "Calm Mind Mega Mewtwo-Y Bulky Offense",
            "pokemon": ["mewtwo-mega-y", "arceus-fairy", "yveltal", "groudon-primal", "necrozma-dusk-mane", "marshadow"],
            "pokepasteURL": "https://pokepast.es/2e4b7e6cf3050984",
            "username": "Garay oak",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "U-turn Mega Scizor Bulky Offense",
            "pokemon": ["scizor-mega", "groudon-primal", "giratina-origin", "kyogre-primal", "arceus-fairy", "yveltal"],
            "pokepasteURL": "https://pokepast.es/66aaa33563ad4474",
            "username": "The Dovahneer",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "DD Zygarde Bulky Offense",
            "pokemon": ["gengar-mega", "arceus-water", "yveltal", "zygarde-complete", "groudon-primal", "necrozma-dusk-mane"],
            "pokepasteURL": "https://pokepast.es/7bd47ad6a6568011",
            "username": "Ubers Council",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "Mega Mewtwo Y + Ho-Oh Balance",
            "pokemon": ["ho-oh", "mewtwo-mega-y", "arceus-dark", "groudon-primal", "ferrothorn", "zygarde-complete"],
            "pokepasteURL": "https://pokepast.es/1ec4406061330e65",
            "username": "PurpleGatorade",
        },
    ],
    "gen7ru": [
        {
            "tier": "[Gen 7] RU",
            "name": "Dragalge HO",
            "pokemon": ["bruxish", "yanmega", "dragalge", "blastoise-mega", "salazzle", "donphan"],
            "pokepasteURL": "https://pokepast.es/924422ba0ce15e37",
            "username": "M3m3kyu45",
        },
        {
            "tier": "[Gen 7] RU",
            "name": "Bulky Necrozma + Vaporeon Balance",
            "pokemon": ["registeel", "mandibuzz", "vaporeon", "necrozma", "ditto", "nidoqueen"],
            "pokepasteURL": "https://pokepast.es/91164ef044ffac94",
            "username": "eifo",
        },
        {
            "tier": "[Gen 7] RU",
            "name": "Special Toxicroak Sticky Web",
            "pokemon": ["araquanid", "toxicroak", "gardevoir", "honchkrow", "nidoqueen", "blastoise-mega"],
            "pokepasteURL": "https://pokepast.es/3a46551a06a7f674",
            "username": "RyLon",
        },
        {
            "tier": "[Gen 7] RU",
            "name": "Zygarde-10% Balance",
            "pokemon": ["zygarde-10", "bronzong", "mantine", "necrozma", "abomasnow-mega", "florges"],
            "pokepasteURL": "https://pokepast.es/65115fc2d998837b",
            "username": "Datsplashtho",
        },
        {
            "tier": "[Gen 7] RU",
            "name": "Barbaracle Bulky Offense",
            "pokemon": ["donphan", "metagross", "virizion", "barbaracle", "noivern", "goodra"],
            "pokepasteURL": "https://pokepast.es/b4759b4a9ffaa2a5",
            "username": "roman",
        },
        {
            "tier": "[Gen 7] RU",
            "name": "Bulky Offense",
            "pokemon": ["raikou", "uxie", "machamp", "mismagius", "abomasnow-mega", "forretress"],
            "pokepasteURL": "https://pokepast.es/fdce26d70a97ed26",
            "username": "Leoshad",
        },
    ],
    "gen7nu": [
        {
            "tier": "[Gen 7] NU",
            "name": "Specs Samurott",
            "pokemon": ["samurott", "torterra", "incineroar", "garbodor", "rotom", "klinklang"],
            "pokepasteURL": "https://pokepast.es/92a752d5b91b3826",
            "username": "Davon",
        },
        {
            "tier": "[Gen 7] NU",
            "name": "Absol and CM Comfey",
            "pokemon": ["absol", "comfey", "xatu", "togedemaru", "palossand", "vaporeon"],
            "pokepasteURL": "https://pokepast.es/3cffc58b51daf8cd",
            "username": "Jisoo",
        },
        {
            "tier": "[Gen 7] NU",
            "name": "Sticky Web HO",
            "pokemon": ["smeargle", "sigilyph", "braviary", "incineroar", "mismagius", "medicham"],
            "pokepasteURL": "https://pokepast.es/2e4b7e6cf3050984",
            "username": "Davon",
        },
        {
            "tier": "[Gen 7] NU",
            "name": "Stall",
            "pokemon": ["xatu", "audino-mega", "palossand", "pyukumuku", "delphox", "golbat"],
            "pokepasteURL": "https://pokepast.es/384828e7d8c5b1ae",
            "username": "Funbot28",
        },
        {
            "tier": "[Gen 7] NU",
            "name": "Specs TL Sigilyph + Spikes",
            "pokemon": ["ferroseed", "sigilyph", "golbat", "blastoise", "incineroar", "passimian"],
            "pokepasteURL": "https://pokepast.es/723a6c350a0581d7",
            "username": "SANJAY",
        },
        {
            "tier": "[Gen 7] NU",
            "name": "Pangoro Scarf Bulky Offense",
            "pokemon": ["pangoro", "comfey", "heliolisk", "glalie-mega", "xatu", "rhydon"],
            "pokepasteURL": "https://pokepast.es/623eb7e649006de7",
            "username": "Fragmented",
        },
    ],
    "gen7pu": [
        {
            "tier": "[Gen 7] PU",
            "name": "Simisear Balance",
            "pokemon": ["eelektross", "mudsdale", "musharna", "cryogonal", "simisear", "gurdurr"],
            "pokepasteURL": "https://pokepast.es/57c1922d48f686d5",
            "username": "LordST",
        },
        {
            "tier": "[Gen 7] PU",
            "name": "Carracosta Offense",
            "pokemon": ["carracosta", "victreebel", "mudsdale", "dodrio", "hitmonchan", "rotom-frost"],
            "pokepasteURL": "https://pokepast.es/4d2d30856bdca3c9",
            "username": "Squash17",
        },
        {
            "tier": "[Gen 7] PU",
            "name": "Hail + Parting Shot",
            "pokemon": ["abomasnow", "sandslash-alola", "mudsdale", "silvally-fairy", "oricorio-pom-pom", "persian-alola"],
            "pokepasteURL": "https://pokepast.es/87a7c1ef3d42842d",
            "username": "UberSkitty",
        },
        {
            "tier": "[Gen 7] PU",
            "name": "Torterra Balance",
            "pokemon": ["torterra", "jellicent", "primeape", "altaria", "sandslash-alola", "eelektross"],
            "pokepasteURL": "https://pokepast.es/2cd85c76717644a1",
            "username": "Ktütverde",
        },
        {
            "tier": "[Gen 7] PU",
            "name": "Leafeon Offense",
            "pokemon": ["leafeon", "ferroseed", "dodrio", "lanturn", "silvally-poison", "musharna"],
            "pokepasteURL": "https://pokepast.es/0de6e967c293d98a",
            "username": "Megazard",
        },
        {
            "tier": "[Gen 7] PU",
            "name": "U-turn Offense",
            "pokemon": ["drampa", "oricorio-sensu", "primeape", "silvally-fairy", "regirock", "simisear"],
            "pokepasteURL": "https://pokepast.es/d9ced767daf37f7d",
            "username": "tlenit",
        },
    ],
}

def generateHTML(teams: List[dict]) -> str:
    """Generates HTML from sample team info

    Args:
        info (dict): data about the team

    Returns:
        str: [description]
    """
    html = ''.join(['<center>• Sample teams <strong>', teams[0]["tier"], '</strong> •</center>'])
    for info in teams:
        html += ''.join([
            ''.join([f'<img src="https://www.smogon.com/forums/media/minisprites/{pokemon}.png" alt="" width="40" height="30">' for pokemon in info["pokemon"]]), # pylint: disable=line-too-long
            ' - <a title="Pokepast" href="', info["pokepasteURL"], '">',
            '<strong>', info["name"], '</strong></a> made by <strong>', info["username"], '</strong><br>'
        ])
    return html

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands: Dict[str, Any] = {"samples": self.showSampleTeams}

    def showSampleTeams(self, message: core.BotMessage) -> None:
        """Displays sample teams

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        formatid = psclient.toID(','.join(message.arguments[1:]) if len(message.arguments) > 1 else '')
        if not formatid or formatid not in htmlboxes:
            return message.respond(f"You must specify a format that I have sample teams for: {', '.join(list(htmlboxes.keys()))}")

        return message.respondHTML(generateHTML(htmlboxes[formatid]))

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Sample teams module: provides sample teams. Commands: {', '.join(self.commands.keys())}"
