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
            "name": "Sticky Webs HO Rock",
            "pokemon": ["shuckle", "golem-alola", "terrakion", "nihilego", "diancie-mega", "tyranitar"],
            "pokepasteURL": "https://pokepast.es/e0e764ccf08f0b8c",
            "username": "Tico 21",
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
            "name": "Balance Flying",
            "pokemon": ["landorus-therian", "charizard-mega-y", "skarmory", "zapdos", "mantine", "gliscor"],
            "pokepasteURL": "https://pokepast.es/3ebf7571a55753d3",
            "username": "Izaya",
        },
        {
            "tier": "[Gen 7] Monotype",
            "name": "Balance Ghost",
            "pokemon": ["gengar", "jellicent", "gourgeist", "marowak-alola", "mimikyu", "sableye-mega"],
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
            "pokepasteURL": "https://pokepast.es/fe4fdada370db6ff",
            "username": "The Dovahneer",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "DD Zygarde Bulky Offense",
            "pokemon": ["gengar-mega", "arceus-water", "yveltal", "zygarde-complete", "groudon-primal", "necrozma-dusk-mane"],
            "pokepasteURL": "https://pokepast.es/6432889c487e7201",
            "username": "Ubers Council",
        },
        {
            "tier": "[Gen 7] Ubers",
            "name": "Mega Mewtwo Y + Ho-Oh Balance",
            "pokemon": ["ho-oh", "mewtwo-mega-y", "arceus-dark", "groudon-primal", "ferrothorn", "zygarde-complete"],
            "pokepasteURL": "https://pokepast.es/b4311fa71bbdbc10",
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
    "gen8sspte": [
        {
            "tier": "[Gen 8] SSPTE",
            "name": "Volt Turn Offense",
            "pokemon": ["alakazam", "lopunny-mega", "magearna-original", "cyndaquil", "noivern", "oshawott"],
            "pokepasteURL": "https://pokepast.es/d5a469cafa55cc73",
            "username": "Imagine Fairies",
        },
        {
            "tier": "[Gen 8] SSPTE",
            "name": "GS Cross Offense",
            "pokemon": ["genesect", "staraptor", "chatot", "scizor-mega", "sylveon", "vaporeon"],
            "pokepasteURL": "https://pokepast.es/b877c3f9eac18fcd",
            "username": "Piloswine Gripado",
        },
        {
            "tier": "[Gen 8] SSPTE",
            "name": "Scizor1914 Core",
            "pokemon": ["zygarde", "scizor-mega", "yveltal", "magearna-original", "jigglypuff", "buizel"],
            "pokepasteURL": "https://pokepast.es/753da8343f71df39",
            "username": "Scizor Boladão",
        },
        {
            "tier": "[Gen 8] SSPTE",
            "name": "Bulky Offense",
            "pokemon": ["golisopod", "magearna-original", "shaymin", "yveltal", "zygarde", "alakazam"],
            "pokepasteURL": "https://pokepast.es/8aae440e058f5248",
            "username": "Lockjaw",
        },
        {
            "tier": "[Gen 8] SSPTE",
            "name": "Hazard Stack Balance",
            "pokemon": ["gastrodon", "serperior", "genesect", "misdreavus", "rapidash-galar", "scorbunny"],
            "pokepasteURL": "https://pokepast.es/78899067814af2fb",
            "username": "Imagine Fairies",
        },
        {
            "tier": "[Gen 8] SSPTE",
            "name": "Stall",
            "pokemon": ["audino-mega", "toxapex", "slowbro-mega", "hippowdon", "sandshrew", "bulbasaur"],
            "pokepasteURL": "https://pokepast.es/d1e81274c96d65b1",
            "username": "Imagine Fairies",
        },
        {
            "tier": "[Gen 8] SSPTE",
            "name": "Aurora Veil HO",
            "pokemon": ["gallade-mega", "meowth-alola", "lycanroc-dusk", "archeops", "alakazam", "genesect"],
            "pokepasteURL": "https://pokepast.es/59132eb1809013a9",
            "username": "Imagine Fairies",
        },
    ],
    "gen8nfe": [
        {
            "tier": "[Gen 8] NFE",
            "name": "Stall",
            "pokemon": ["lickitung", "corsola-galar", "carkol", "machoke", "duosion", "tangela"],
            "pokepasteURL": "https://pokepast.es/5d35e01bda1da493",
            "username": "xHys",
        },
        {
            "tier": "[Gen 8] NFE",
            "name": "Dual Hazards HO",
            "pokemon": ["krokorok", "roselia", "wartortle", "thwackey", "lampent", "klang"],
            "pokepasteURL": "https://pokepast.es/d4c5892beb9aec53",
            "username": "Hon3nConfirm3d",
        },
        {
            "tier": "[Gen 8] NFE",
            "name": "Webs Bulky Offense",
            "pokemon": ["raboot", "thwackey", "charjabug", "clefairy", "machoke", "hattrem"],
            "pokepasteURL": "https://pokepast.es/4664d5912c73a970",
            "username": "Jett x~x",
        },
        {
            "tier": "[Gen 8] NFE",
            "name": "Pivot Offense",
            "pokemon": ["raboot", "thwackey", "vullaby", "corsola-galar", "kadrabra", "mareanie"],
            "pokepasteURL": "https://pokepast.es/f6cf8e17674b142a",
            "username": "Hon3nConfirm3d",
        },
    ],
    "natdex": [
        {
            "tier": "National Dex",
            "name": "Mega Lopunny BO",
            "pokemon": ["kyurem", "lopunny-mega", "zapdos", "magearna", "kartana", "seismitoad"],
            "pokepasteURL": "https://pokepast.es/fc324b0d09bdb691",
            "username": "Some God Plays",
        },
        {
            "tier": "National Dex",
            "name": "Mega Medicham Pivot Balance",
            "pokemon": ["medicham-mega", "garchomp", "blissey", "zapdos", "slowbro", "weavile"],
            "pokepasteURL": "https://pokepast.es/612e55bf9f23fe80",
            "username": "Jordy and Guardsweeper",
        },
        {
            "tier": "National Dex",
            "name": "Rip Rain",
            "pokemon": ["pelipper", "swampert-mega", "ferrothorn", "kingdra", "manaphy", "zapdos"],
            "pokepasteURL": "https://pokepast.es/a46a04a2660c72d1",
            "username": "Some God Plays",
        },
        {
            "tier": "National Dex",
            "name": "SM with Rillaboom",
            "pokemon": ["kartana", "rillaboom", "magearna", "rotom-wash", "landorus-therian", "magnezone"],
            "pokepasteURL": "https://pokepast.es/ac32a2646facebfb",
            "username": "Some God Plays",
        },
        {
            "tier": "National Dex",
            "name": "M-Lopunny Hydreigon Balance",
            "pokemon": ["hydreigon", "hippowdon", "toxapex", "lopunny-mega", "clefable", "corviknight"],
            "pokepasteURL": "https://pokepast.es/7ce274ca1c9c69d2",
            "username": "SputnikGT and faded love",
        },
        {
            "tier": "National Dex",
            "name": "Gliscor Balance",
            "pokemon": ["gliscor", "latias-mega", "ferrothorn", "toxapex", "clefable", "cinderace"],
            "pokepasteURL": "https://pokepast.es/31bb8d80fbea789c",
            "username": "Some God Plays",
        },
    ],
    "gen7dou": [
        {
            "tier": "[Gen 7] Doubles OU",
            "name": "Camerupt Trick Room",
            "pokemon": ["camerupt-mega", "stakataka", "scrafty", "tapu-bulu", "diancie", "porygon-2"],
            "pokepasteURL": "https://pokepast.es/8f61b0c7d3fcf584",
            "username": "miltankmilk",
        },
        {
            "tier": "[Gen 7] Doubles OU",
            "name": "Mega Charizard Y Offense",
            "pokemon": ["charizard-mega-y", "kommo-o", "kartana", "tapu-koko", "porygon-2", "landorus-therian"],
            "pokepasteURL": "https://pokepast.es/bb59785e1a8b170b",
            "username": "emforbes",
        },
        {
            "tier": "[Gen 7] Doubles OU",
            "name": "Scizor Balance",
            "pokemon": ["kyurem-black", "tapu-koko", "gothitelle", "landorus-therian", "volcanion", "scizor-mega"],
            "pokepasteURL": "https://pokepast.es/55eeb0e725c421e8",
            "username": "MajorBowman",
        },
        {
            "tier": "[Gen 7] Doubles OU",
            "name": "Metagross Tailwind Offense",
            "pokemon": ["incineroar", "tapu-fini", "metagross", "zapdos", "amoonguss", "landorus-therian"],
            "pokepasteURL": "https://pokepast.es/fd47331c4023a0d7",
            "username": "EmbCPT",
        },
        {
            "tier": "[Gen 7] Doubles OU",
            "name": "Zeraora is fun",
            "pokemon": ["scizor-mega", "zeraora", "kyurem-black", "volcanion", "landorus-therian", "gothitelle"],
            "pokepasteURL": "https://pokepast.es/e3ba5d81b401404e",
            "username": "Givrix",
        },
    ],
    "gen8metronomebattle": [
        {
            "tier": "[Gen 8] Metronome Battle",
            "name": "Extreme Strength",
            "pokemon": ["heracross-mega", "heracross-mega"],
            "pokepasteURL": "https://pokepast.es/050cf831db6da72b",
            "username": "Ivy",
        },
        {
            "tier": "[Gen 8] Metronome Battle",
            "name": "Bonk Stall",
            "pokemon": ["type-null", "dusclops"],
            "pokepasteURL": "https://pokepast.es/d3ecf52b738a103a",
            "username": "Bonk",
        },
        {
            "tier": "[Gen 8] Metronome Battle",
            "name": "Imposter Blisseys",
            "pokemon": ["blissey", "blissey"],
            "pokepasteURL": "https://pokepast.es/a92bb32e96d695c3",
            "username": "Ivy",
        },
        {
            "tier": "[Gen 8] Metronome Battle",
            "name": "Balanced Flower Veil",
            "pokemon": ["venusaur-mega", "necturna"],
            "pokepasteURL": "https://pokepast.es/66411402d3abf217",
            "username": "Ivy",
        },
    ],
    "gen8ou": [
        {
            "tier": "[Gen 8] OU",
            "name": "BO Zarude + Choice Scarf Magearna",
            "pokemon": ["zarude", "slowking-galar", "magearna", "zapdos", "gastrodon", "heatran"],
            "pokepasteURL": "https://pokepast.es/df5a12017d1eb6fe",
            "username": "Storm Zone",
        },
        {
            "tier": "[Gen 8] OU",
            "name": "SD Garchomp + Specs Magnezone Balance",
            "pokemon": ["pheromosa", "garchomp", "magnezone", "slowbro", "clefable", "mandibuzz"],
            "pokepasteURL": "https://pokepast.es/fefeb5ec41d76d8a",
            "username": "Finchinator",
        },
        {
            "tier": "[Gen 8] OU",
            "name": "NP Spectrier + SD Kartana Sand Balance",
            "pokemon": ["spectrier", "tyranitar", "toxapex", "kartana", "excadrill", "moltres"],
            "pokepasteURL": "https://pokepast.es/806cb7e04547acd1",
            "username": "Finchinator",
        },
        {
            "tier": "[Gen 8] OU",
            "name": "Rain Offense",
            "pokemon": ["pelipper", "barraskewda", "ferrothorn", "clefable", "swampert", "urshifu-rapid-strike"],
            "pokepasteURL": "https://pokepast.es/bd354abd34c2fc79",
            "username": "Steez Ibanez",
        },
        {
            "tier": "[Gen 8] OU",
            "name": "Choice Band Urshifu + Choice Specs Magearna VoltTurn",
            "pokemon": ["urshifu", "magearna", "mandibuzz", "slowking", "toxapex", "landorus-therian"],
            "pokepasteURL": "https://pokepast.es/391c5b474d2ee3c4",
            "username": "Ruft",
        },
        {
            "tier": "[Gen 8] OU",
            "name": "Pivot Cinderace + Future Sight Slowbro Balance",
            "pokemon": ["cinderace", "slowbro", "dragapult", "excadrill", "clefable", "mandibuzz"],
            "pokepasteURL": "https://pokepast.es/1c2d1429e3afd88f",
            "username": "TPP",
        },
        {
            "tier": "[Gen 8] OU",
            "name": "NP Tornadus-T + Choice Band Barraskewda Rain Offense",
            "pokemon": ["pelipper", "tornadus-therian", "barraskewda", "ferrothorn", "garchomp", "urshifu"],
            "pokepasteURL": "https://pokepast.es/f71063f07af87a03",
            "username": "Finchinator",
        },
    ],
    "gen8uu": [
        {
            "tier": "[Gen 8] UU",
            "name": "Specs Kyurem",
            "pokemon": ["zeraora", "kyurem", "slowking", "jirachi", "terrakion", "rotom-heat"],
            "pokepasteURL": "https://pokepast.es/0a32da9b04b1b16a",
            "username": "Moutemoute",
        },
        {
            "tier": "[Gen 8] UU",
            "name": "Chansey Bulky Offense",
            "pokemon": ["victini", "zeraora", "kommo-o", "skarmory", "tentacruel", "chansey"],
            "pokepasteURL": "https://pokepast.es/f3f9e0c69e4eaf4a",
            "username": "Estarossa",
        },
        {
            "tier": "[Gen 8] UU",
            "name": "Veil Haxorus",
            "pokemon": ["ninetales-alola", "celesteela", "azumarill", "blaziken", "krookodile", "haxorus"],
            "pokepasteURL": "https://pokepast.es/975cca2352cab4a8",
            "username": "navi",
        },
        {
            "tier": "[Gen 8] UU",
            "name": "Blaziken Webs",
            "pokemon": ["blaziken", "thundurus-therian", "shuckle", "mimikyu", "bisharp", "latias"],
            "pokepasteURL": "https://pokepast.es/16569e8ee1c0dda5",
            "username": "Avarice",
        },
        {
            "tier": "[Gen 8] UU",
            "name": "Bulky Offense",
            "pokemon": ["victini", "zeraora", "krookodile", "celesteela", "tangrowth", "tentacruel"],
            "pokepasteURL": "https://pokepast.es/665ea777d97a6294",
            "username": "Sickist",
        },
        {
            "tier": "[Gen 8] UU",
            "name": "Belly Drum Kommo-o HO",
            "pokemon": ["mew", "gyarados", "kommo-o", "mimikyu", "scizor", "toxtricity"],
            "pokepasteURL": "https://pokepast.es/81518555c790cc51",
            "username": "Twilight",
        },
        {
            "tier": "[Gen 8] UU",
            "name": "Heliolisk VoltTurn BO",
            "pokemon": ["heliolisk", "cobalion", "slowbro-galar", "sylveon", "incineroar", "golisopod"],
            "pokepasteURL": "https://pokepast.es/96e700f952d7bac9",
            "username": "Ramolost",
        },
    ],
    "gen8ubers": [
        {
            "tier": "[Gen 8] Ubers",
            "name": "Dialga lead + Geneshift Screen",
            "pokemon": ["genesect", "dialga", "ho-oh", "regieleki", "xerneas", "zygarde"],
            "pokepasteURL": "https://pokepast.es/35fa9785b57e0684",
            "username": "Kabilapok",
        },
        {
            "tier": "[Gen 8] Ubers",
            "name": "Specs Calyrex-S Yveltal Balance",
            "pokemon": ["necrozma-dusk-mane", "ho-oh", "eternatus", "yveltal", "zygarde", "calyrex-shadow"],
            "pokepasteURL": "https://pokepast.es/508587e35dbbba40",
            "username": "Icemaster",
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
    html = ''.join(['<center><details><summary>Sample teams <strong>', teams[0]["tier"], '</strong></summary>'])
    for info in teams:
        html += ''.join([
            ''.join([f'<img src="https://www.smogon.com/forums/media/minisprites/{pokemon}.png" alt="" width="40" height="30">' for pokemon in info["pokemon"]]), # pylint: disable=line-too-long
            ' - <a title="Pokepast" href="', info["pokepasteURL"], '">',
            '<strong>', info["name"], '</strong></a> made by <strong>', info["username"], '</strong><br>'
        ])
    html += '</details></center>'
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
