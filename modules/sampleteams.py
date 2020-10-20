"""sampleteams.py
    provides sample teams to the Portuguese room
    by Annika"""

from typing import Dict, Any, Union, List

import psclient
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
