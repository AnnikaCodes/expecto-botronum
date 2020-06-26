# Expecto Botronum v3
Expecto Botronum is a Pokémon Showdown bot written by Annika for the [Magic & Mayhem room](psim.us/mm).

## Commands
| Usage | Description |
|-------|-------------|
| `~superhero <superhero>` | Displays information about the given superhero. |
| `~ping` | Says `Pong!` in chat. |
| `~owo <text>` | Converts vowels to owo faces. |
| `~uwu <text>` | Converts to anime text. |
| `~timer <duration>, [optional message]` | Sets a timer. |
| `~timer <duration>, [optional message]` | Sets a timer. |
| `~do <room>, <message>` | Sends a message to a room. |
| `~timer <duration>, [optional message]` | Sets a timer. |
| `~logsearch <room>, [optional user], [optional keyword]` | Searches chatlogs. Requires % or higher in the room whose logs are being searched. |
| `~fact` | Shows a random fact from the room's fact database. Specify a room in PMs. |
| `~addfact <fact>` | Adds the fact to the fact database. Specify a room in PMs. |
| `~deletefact <fact>` | Deletes the fact from the fact database. Specify a room in PMs. |
| `~countfacts` | Gives the number of facts in the fact database. Specify a room in PMs. |
| `~listfacts` | Provides a Pastebin link of the facts for that room. Specify a room in PMs. |
| `~topic` | Shows a random topic from the room's topic database. Specify a room in PMs. |
| `~addtopic <topic>` | Adds the topic to the topic database. Specify a room in PMs. |
| `~deletetopic <topic>` | Deletes the topic from the topic database. Specify a room in PMs. |
| `~counttopics` | Gives the number of topics in the topic database. Specify a room in PMs. |
| `~listtopics` | Provides a Pastebin link of the topics for that room. Specify a room in PMs. |
| `~uno` | Starts a game of UNO. |
| `~tour <format>` | Starts a single elimination tournament in the given `format`. |
| `~reverse` | Provides a random Reversio phrase from the room's database. Specify a room in PMs. |
| `~addreversioword <word>` | Adds a Reversio phrase to the room's database. Specify a room in PMs. |
| `~removereversioword <word>` | Removes a Reversio phrase from the room's database. Specify a room in PMs. |
| `~addpoints <user>, [n]` | Adds `n` points (or 1 if no `n` is given) to the given `user`'s minigame score for that room. |
| `~showlb` | Shows the minigame scoreboard. Specify a room in PMs. |
| `~addjoinphrase <user>, <phrase>` | Sets `<user>`'s joinphrase to `phrase`. This phrase will be said by the bot when the user joins the room. Specify a room in PMs. |
| `~removejoinphrase <user>` | Removes `<user>`'s joinphrase. Specify a room in PMs. |
| `~superhero <superhero>` | Shows information about a superhero from the Superhero API. |

## Technical 
Expecto Botronum is written in Python 3.x (specifically, Python 3.5). If you would like to contribute, feel free to work on one of the issues. To propose a feature, PM me on Discord (Annika#1562) or mention the feature in the channel for that purpose in the Magic & Mayhem discord.

Further technical documentation is available in [v3.md](https://github.com/AnnikaCodes/expecto-botronum/blob/master/v3.md). 
