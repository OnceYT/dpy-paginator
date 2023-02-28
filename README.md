# dpy-paginator
##### Built and tested on [discord.py](https://github.com/Rapptz/discord.py) 2.1.1
A discord.py utility with no external dependencies that makes paginating embeds easier.

Some of it's features are -
- Easy to use.
- Supports both ephemeral and non-ephemeral responses.
- Buttons are enabled/disabled automatically depending on the current page number, number of embeds provided or at timeout.

The paginator consists of 4 buttons - ⏪, ◀️, 'Jump To' modal, ▶️, ⏩
- ⏪ - Shows the first embed. Disabled if there are less than 3 embeds or if already on the first embed.
- ◀️ - Shows the previous embed. Disabled if already on the first embed.
- 'Jump To' modal - Triggers a `discord.ui.Modal` that takes you to the page number you input. Disabled if there are less than 3 embeds.
- ▶️ - Shows the next embed. Disabled if already on the last embed.
- ⏩ - Shows the last embed. Disabled if there are less than 3 embeds or if already on the last page.

# Installation
```
pip install git+https://github.com/onceyt/dpy-paginator.git
```

# Usage
##### Basic usage:
```py
import discord
from dpy-paginator import Paginate

embed1 = discord.Embed(title = "This is embed#1")
embed2 = discord.Embed(title = "This is embed#2")
output = await Paginate(embeds = [embed1, embed2])

# output.embed gives you the first embed of the pagination
# output.view gives you the discord.ui.View that controls the pagination

await Messagable.send(embed = output.embed, view = output.view)

# you want to send both in your Messageable.send
```

##### discord.ext.Commands example:
```py
import discord
from discord.ext import commands
from dpy-paginator import Paginate

bot = discord.Bot() # your discord.Bot object

@bot.command()
async def example(ctx):
  embed1 = discord.Embed(title = "This is Embed#1")
  embed2 = discord.Embed(title = "This is Embed#2")
  output = await Paginate(embeds = [embed1, embed2])
  await ctx.send(embed = output.embed, view = output.view)
```
This command has the following output - 
![]()

<details>
<summary><h5>Control who can interact: (<code>author_ids</code> param)</h5></summary>


You can control which users can interact with the view by passing a `author_ids` list
```py
...

await Paginate(embeds = [embed1, embed2], author_ids = [#ID1, #ID2])
```
When anyone except the specified users try to interact, the paginator ignores that interaction
![]()
</details>

<details>
<summary><h5>Adding a timeout: (<code>timeout</code> param)</h5></summary>


By default, the view has a timeout of 90 seconds but this can be changed by passing a `timeout` parameter.
```py
...

await Paginate(embeds = [embed1, embed2], timeout = 60)
```
The buttons get automatically disabled after timeout (except when no button is interacted with)[^1]. You can also use `timeout = None` for no timeout.

In the scenario that no button is interacted with and the view timesout, the buttons will not be automatically disabled resulting in the need of an extra step.
```py
import asyncio
...
timeout = 60

output = await Paginate(embeds = [embed1, embed2], timeout = timeout)
message = await Messageable.send(embed = output.embed, view = output.view)

await asyncio.sleep(timeout)
if output.timedout: # check if the view is timedout
  await message.edit(view = output.view) # manually edit the buttons if the output is timedout
```
Note that incase of ephemeral responses (or scenarios where the output will be deleted before the timeout), this extra step is probably not worth it.
![]()
</details>

[^1]: To explain this, the `PaginateButtons` view class receives the `discord.Interaction` object only when one of the buttons is interacted with which is then used to edit the message with the disabled buttons upon timeout. Only running `Paginate()` and sending the output does not give the class access to the message sent, thus resulting in the need of an extra step to satisfy this possibility.
