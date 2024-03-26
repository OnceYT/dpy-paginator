# dpy-paginator
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dpy-paginator)
![Downloads](https://static.pepy.tech/badge/dpy-paginator)

<details>
<summary><strong>Table of contents</strong></summary>

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
    - [Basic usage](#basic_usage)
    - [discord.ext.Commands usage](#commands_usage)
    - [discord.app_commands usage (ephemeral)](#appcommands_usage)
- [Options and Parameters](#options)
    - [Control who can interact](#author_ids)
    - [Adding a timeout](#timeout)
    - [Using custom emojis in buttons](#button_emojis)
</details>

##### <a name='overview'></a>Built and tested on [discord.py](https://github.com/Rapptz/discord.py) 2.3.2
A discord.py utility with no external dependencies that makes paginating embeds easier.

<details>
<summary><strong>Quick links</strong></summary>

- [Documentation](https://github.com/OnceYT/dpy-paginator/blob/v1.1.0/README.md)
- [Security Policy](https://github.com/OnceYT/dpy-paginator/blob/main/.github/SECURITY.md)
- [Source](https://github.com/OnceYT/dpy-paginator/tree/v1.1.0)
- [PyPi](https://pypi.org/project/dpy-paginator/)
- [Support/Contact](https://onceyt.github.io/)
</details>

<details>
<summary><strong>Changelog (v1.0.0 -> v1.1.0 and v1.1.1)</strong></summary>

- Added the ability to use [custom emojis in buttons](#button_emojis).
- Code optimizations.
- Code cleanup.
- v1.1.0 -> v1.1.1 contains only readme updates and pyproject.toml changes for metadata.
</details>

**Some of it's features include:**
- Easy to use.
- Supports both ephemeral and non-ephemeral responses.
- Buttons are enabled/disabled automatically depending on the current page number, number of embeds provided or at timeout.

**The paginator consists of 4 buttons - ⏪, ◀️, 'Jump To' modal, ▶️, ⏩**
- ⏪ - Shows the first embed. Disabled if there are less than 3 embeds or if already on the first embed.
- ◀️ - Shows the previous embed. Disabled if already on the first embed.
- 'Jump To' modal - Triggers a `discord.ui.Modal` that takes you to the page number you input. Disabled if there are less than 4 embeds.
- ▶️ - Shows the next embed. Disabled if already on the last embed.
- ⏩ - Shows the last embed. Disabled if there are less than 3 embeds or if already on the last page.

# <a name='installation'></a>Installation
```
pip install dpy-paginator
```
or
```
pip install git+https://github.com/onceyt/dpy-paginator.git@v1.1.0
```

# <a name='usage'></a>Usage
##### <a name='basic_usage'></a>Basic usage:
```py
import discord
from dpy_paginator import paginate

embed1 = discord.Embed(title = "This is embed#1")
embed2 = discord.Embed(title = "This is embed#2")
output = paginate(embeds = [embed1, embed2])

# output.embed gives you the first embed of the pagination
# output.view gives you the discord.ui.View that controls the pagination

await Messagable.send(embed = output.embed, view = output.view)

# you want to send both in your Messageable.send
```

##### <a name='commands_usage'></a>discord.ext.Commands Example:
```py
import discord
from discord.ext import commands
from dpy_paginator import paginate

bot = discord.Bot() # your discord.Bot object

@bot.command()
async def example(ctx: commands.Context):
  embed1 = discord.Embed(title = "This is Embed#1")
  embed2 = discord.Embed(title = "This is Embed#2")
  output = paginate(embeds = [embed1, embed2])
  await ctx.send(embed = output.embed, view = output.view)
```
**This command has the following output:**

![discord.ext.Commands example image](https://i.imgur.com/7aOIIpK.png)

##### <a name='appcommands_usage'></a>discord.app_commands Example: (ephemeral)
```py
from discord import app_commands
from dpy_paginator import paginate

@app_commands.command(name='example')
async def example_command(interaction: discord.Interaction):
  await interaction.response.defer(ephemeral = True, thinking = True)
  embed1 = discord.Embed(title = "This is Embed#1")
  embed2 = discord.Embed(title = "This is Embed#2")
  output = paginate(embeds = [embed1, embed2])
  await interaction.followup.send(embed = output.embed, view = output.view)  
```
**This command has the following output:**

![discord.app_commands (ephemeral) example image](https://i.imgur.com/tA78jy0.png)

# <a name='options'></a>Options and Parameters 

##### <a name='author_ids'></a>Control who can interact: (`author_ids: list[int]` param)

You can control which user(s) can interact with the view by passing a `author_ids` list.
```py
...

output = paginate(embeds = [embed1, embed2], author_ids = [#ID1, #ID2])
```
When anyone except the specified user(s) try to interact, **the paginator ignores that interaction:**

![author_ids error example image](https://i.imgur.com/QY7dTrw.png)

##### <a name='timeout'></a>Adding a timeout: (`timeout: int` param)


By default, the view has a timeout of 90 seconds but this can be changed by passing a `timeout` parameter.
```py
...

output = paginate(embeds = [embed1, embed2], timeout = 60)
```
The buttons get automatically disabled after timeout (except when no button is interacted with)[^1]. You can also use `timeout = None` for no timeout.

**Example of a timedout view:**

![timedout image](https://i.imgur.com/qzI9eax.png)

In the scenario that no button is interacted with and the view gets timedout, the buttons will not be automatically disabled resulting in the need of an extra step. `output.view.timedout` returns a boolean which we can use to check if the view has timedout.
```py
import asyncio
...
timeout = 60

output = paginate(embeds = [embed1, embed2], timeout = timeout)
message = await Messageable.send(embed = output.embed, view = output.view)

await asyncio.sleep(timeout + 0.5) # add 0.5 to the timeout to account for processing delays
if output.view.timedout: # check if the view is timedout
  await message.edit(view = output.view) # manually edit the buttons if the output is timedout

# the view will automatically timeout incase this check returns False
```
Note that incase of ephemeral responses (or scenarios where the output will be deleted before the timeout), this extra step is not worth it.

##### <a name='button_emojis'></a>Using custom emojis in buttons: (`button_emojis: List[discord.Emoji]` param)

You can use custom emojis in the buttons by passing a list of discord.Emoji objects or Unicode emoji strings. The list needs to have exactly 4 elements.
```py
...
output = paginate(embeds = [embed1, embed2, embed3, embed4], button_emojis = ['<:DarkerTan:945570099081920532>', '<:DazzlingRose:945561181467344977>', '<:FluorescentBlue:945561331547914280>', '😮'])

# you can use unicode emojis (😮) directly
# for discord.Emoji objects you can either use them directly in the <:name:id> format or fetch the object using guild.get_emoji(id) or some other functionality
```

**Example of a view using custom emojis:**

![custom emojis in button example image](https://i.imgur.com/h8cDhvZ.png)

Note that the package has no error handling for if you pass a non discord.Emoji object or a non Unicode emoji string in the list. This is because explicitly checking for a discord.Emoji object will not accomodate using an Unicode string. Make sure you are passing the right objects or strings otherwise you will be getting the `HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body` error.

[^1]: To explain this, the `paginateButtons` view class receives the `discord.Interaction` object only when one of the buttons is interacted with which is then used to edit the message with the disabled buttons upon timeout. Only running `paginate()` and sending the output does not give the class access to the message sent, thus resulting in the need of an extra step to satisfy this possibility.
