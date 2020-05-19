# Expecto Botronum
Expecto Botronum is a Pokemon Showdown bot for the [Magic & Mayhem room](psim.us/mm).

## Commands
| Usage | Required Rank | Description |
|-------|---------------|-------------|
| `~join <house>` | None | Adds the user to the given house. |
| `~ping` | None (+ to broadcast) | Says `Pong!` in chat. |
| `~pong` | None (+ to broadcast) | Says `Ping!` in chat. |
| `~parse` | None (+ to broadcast) | Gives information about the chat message received. |
| `~check <house>` | None (+ to broadcast) | Gives the number of points the given house has. |
| `~houses` | None (+ to broadcast) | Gives the scores of each house. |
| `~scores` | None (+ to broadcast) | Displays the minigame scoreboard. |
| `~fact` | None (+ to broadcast) | Shows a random fact from the fact database. |
| `~countfacts` | None (+ to broadcast) | Gives the number of facts in the fact database. |
| `~lb <house>, [n]` | None (+ to broadcast) | Gives the scores of the top `n` users in the given house. If no `n` is provided, the default is 5. |
| `~house <username>` | None (+ to broadcast) | Tells what house `username` is in. |
| `~owo <text>` | None (+ to broadcast) | Changes all vowels in `text` to owo faces. |
| `~reverse` OR `~wallrev` | None (+ to broadcast) | `/wall`s a random Reversio phrase from the bot's database. |
| `~uno` | + | Starts a game of UNO. |
| `~addfact <fact>` | + | Adds the fact to the fact database (no italics needed). |
| `~deletefact <fact>` | + | Deletes the fact from the fact database (no italics needed). |
| `~listfacts` | + | PMs the user a pastebin containing all the facts. |
| `~tour <format>` | + | Starts a single elimination tournament in the given `format`. |
| `~addto <user>, [n]` | + | Adds `n` points (or 1 if no `n` is given) to the given `user`'s minigame score. |
| `~clearscores` | + | Clears the minigame scoreboard. |
| `~give <user>, <points>` OR `~give <house>, <points>` | + | Awards the given `user` or house `points` points. |
| `~do <room>,<message>` | # | Says the given message in the given room. |
| `~jp <user>,<phrase>` | # | Sets `<user>`'s joinphrase to `phrase`. This phrase will be said by the bot when the user logs in. |
