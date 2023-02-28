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

##### Command example:
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

##### Control who can interact: (`author_ids` param)
You can control which users can interact with the view by passing a `author_ids` list
```py
...

await Paginate(embeds = [embed1, embed2], author_ids = [#ID1, #ID2])
```
When anyone except the specified users try to interact, the paginator ignores that interaction
![]()

##### Adding a timeout: (`timeout` param)
By default, the view has a timeout of 90 seconds but this can be changed by passing a `timeout` parameter
```py
...

await Paginate(embeds = [embed1, embed2], timeout = 60)
```
The buttons get automatically disabled after timeout. You can also use `timeout = None` for no timeout
![]()
