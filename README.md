# Expecto Botronum
Expecto Botronum is a Pokemon Showdown bot for the [Magic & Mayhem room](psim.us/mm).

## Commands
| Usage | Required Rank | Description |
|-------|---------------|-------------|
| `~superhero <superhero>` | None (+ to broadcast) | Displays information about the given superhero. |
| `~ping` | None (+ to broadcast) | Says `Pong!` in chat. |
| `~pong` | None (+ to broadcast) | Says `Ping!` in chat. |
| `~parse` | None (+ to broadcast) | Gives information about the chat message received. |
| `~scores` | None (+ to broadcast) | Displays the minigame scoreboard. |
| `~fact` | None (+ to broadcast) | Shows a random fact from the fact database. |
| `~countfacts` | None (+ to broadcast) | Gives the number of facts in the fact database. |
| `~owo <text>` | None (+ to broadcast) | Changes all vowels in `text` to owo faces. |
| `~reverse` OR `~wallrev` | None (+ to broadcast) | `/wall`s a random Reversio phrase from the bot's database. |
| `~uno` | + | Starts a game of UNO. |
| `~addfact <fact>` | + | Adds the fact to the fact database (no italics needed). |
| `~deletefact <fact>` | + | Deletes the fact from the fact database (no italics needed). |
| `~listfacts` | + | PMs the user a pastebin containing all the facts. |
| `~tour <format>` | + | Starts a single elimination tournament in the given `format`. |
| `~addto <user>, [n]` | + | Adds `n` points (or 1 if no `n` is given) to the given `user`'s minigame score. |
| `~clearscores` | + | Clears the minigame scoreboard. |
| `~do <room>,<message>` | # | Says the given message in the given room. |
| `~jp <user>,<phrase>` | # | Sets `<user>`'s joinphrase to `phrase`. This phrase will be said by the bot when the user logs in. |
