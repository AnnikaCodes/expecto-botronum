# Expecto Botronum v3
### ![tests](https://github.com/AnnikaCodes/expecto-botronum/workflows/tests/badge.svg)
Expecto Botronum is a Pokémon Showdown bot written by Annika for the [Magic & Mayhem room](psim.us/mm).



## Commands
| Usage | Description |
|-------|-------------|
| `-superhero <superhero>` | Displays information about the given superhero. |
| `-ping` | Says `Pong!` in chat. |
| `-owo <text>` | Converts vowels to owo faces. |
| `-uwu <text>` | Converts to anime text. |
| `-timer <duration>, [optional message]` | Sets a timer. |
| `-timer <duration>, [optional message]` | Sets a timer. |
| `-do <room>, <message>` | Sends a message to a room. |
| `-timer <duration>, [optional message]` | Sets a timer. |
| `-logsearch <room>, [optional user], [optional keyword]` | Searches chatlogs. Requires % or higher in the room whose logs are being searched. |
| `-topusers <room>, [optional number of days]` | Provides a list of the top 50 users by linecount in a room. Requires % or higher in the room. |
| `-linecount <user>, <room>, [optional number of days]` | Gets a user's linecount in a room and a breakdown by day. Requires % or higher in the room. |
| `-fact` | Shows a random fact from the room's fact database. Specify a room in PMs. |
| `-addfact <fact>` | Adds the fact to the fact database. Specify a room in PMs. |
| `-deletefact <fact>` | Deletes the fact from the fact database. Specify a room in PMs. |
| `-countfacts` | Gives the number of facts in the fact database. Specify a room in PMs. |
| `-listfacts` | Provides a Pastebin link of the facts for that room. Specify a room in PMs. |
| `-topic` | Shows a random topic from the room's topic database. Specify a room in PMs. |
| `-addtopic <topic>` | Adds the topic to the topic database. Specify a room in PMs. |
| `-deletetopic <topic>` | Deletes the topic from the topic database. Specify a room in PMs. |
| `-counttopics` | Gives the number of topics in the topic database. Specify a room in PMs. |
| `-listtopics` | Provides a Pastebin link of the topics for that room. Specify a room in PMs. |
| `-quote` | Shows a random quote from the room's quote database. Specify a room in PMs. |
| `-addquote <quote>` | Adds the quote to the quote database. Specify a room in PMs. |
| `-deletequote <quote>` | Deletes the quote from the quote database. Specify a room in PMs. |
| `-countquotes` | Gives the number of quotes in the quote database. Specify a room in PMs. |
| `-listquotes` | Provides a Pastebin link of the quotes for that room. Specify a room in PMs. |
| `-uno` | Starts a game of UNO. |
| `-tour <format>` | Starts a single elimination tournament in the given `format`. |
| `-reverse` | Provides a random Reversio phrase from the room's database. Specify a room in PMs. |
| `-addreversioword <word>` | Adds a Reversio phrase to the room's database. Specify a room in PMs. |
| `-removereversioword <word>` | Removes a Reversio phrase from the room's database. Specify a room in PMs. |
| `-addpoints <user>, [n]` | Adds `n` points (or 1 if no `n` is given) to the given `user`'s minigame score for that room. |
| `-showlb` | Shows the minigame scoreboard. Specify a room in PMs. |
| `-addjoinphrase <user>, <phrase>` | Sets `<user>`'s joinphrase to `phrase`. This phrase will be said by the bot when the user joins the room. Specify a room in PMs. |
| `-removejoinphrase <user>` | Removes `<user>`'s joinphrase. Specify a room in PMs. |
| `-joinhouse <house>` | Joins a house. |
| `-checkhouse [user]` | Checks the house of a given user, or the sender if none is specified. |

## Technical
Expecto Botronum is written in Python 3.x (specifically, Python 3.6). If you would like to contribute, feel free to work on one of the issues. To propose a feature, PM me on Discord (Annika#1562) or mention the feature in the channel for that purpose in the Magic & Mayhem discord.

To run Expecto Botronum, simply clone the source code, install dependencies (with `pip install -r requirements.txt`), copy `config-example.json` to `config.json` and edit it as needed, and run `core.py`. You can also run the script `test.sh` (on Linux and Mac) to run the linter and tests, if you're so inclined.

Further technical documentation is available in [v3.md](https://github.com/AnnikaCodes/expecto-botronum/blob/master/v3.md).
