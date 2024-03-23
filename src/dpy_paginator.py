# Copyright (c) 2024 OnceYT
# Licensed under the MIT License

import discord

class modal(discord.ui.Modal, title = "Jump to page"):
  def __init__(self, embeds: list, author_ids: list, timeout: int, button_emojis: list[discord.Emoji] = None):
    super().__init__(timeout = timeout)
    self.embeds = embeds
    self.author_ids = author_ids
    self.button_emojis = button_emojis
    self.input.label = f"Page number: (1-{len(self.embeds)})"

  input = discord.ui.TextInput(label = "placeholder", placeholder = "Enter the page number to jump to...")

  async def on_submit(self, interaction: discord.Interaction):
    response = int(self.input.value)-1
    if response not in range(len(self.embeds)):
      await interaction.response.defer()
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[int(response)], view = paginateButtons(embeds = self.embeds, page = int(response), author_ids = self.author_ids, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))
    else:
      await interaction.message.edit(embed = self.embeds[int(response)], view = paginateButtons(embeds = self.embeds, page = int(response), author_ids = self.author_ids, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))
      await interaction.response.defer()

class paginateButtons(discord.ui.View):
  def __init__(self, embeds: list[discord.Embed], page: int, author_ids: list[int], timeout: int, button_emojis: list[discord.Emoji] = None, interaction: discord.Interaction = None, timedout: bool = False):
    super().__init__(timeout = timeout)
    self.embeds, self.page, self.author_ids, self.timeout, self.button_emojis, self.interaction, self.timedout = embeds, page, author_ids, timeout, button_emojis, interaction, timedout
    self.buttonModal.label = f"{page+1}/{len(self.embeds)}"
    if self.button_emojis:
      self.buttonPaginateLeftmost.emoji, self.buttonPaginateLeft.emoji, self.buttonPaginateRight.emoji, self.buttonPaginateRightmost.emoji = self.button_emojis[0], self.button_emojis[1], self.button_emojis[2], self.button_emojis[3]
    if len(self.embeds) < 4:
      self.buttonModal.disabled = True
    if len(self.embeds) < 3:
      self.remove_item(self.buttonPaginateLeftmost)
      self.remove_item(self.buttonPaginateRightmost)     
    if self.page > 0:
      self.buttonPaginateLeftmost.disabled = False
      self.buttonPaginateLeft.disabled = False
    if self.page != len(self.embeds)-1:
      self.buttonPaginateRightmost.disabled = False
      self.buttonPaginateRight.disabled = False
  
  async def on_timeout(self):
    for children in self.children:
      children.disabled = True
    self.timedout = True
    if self.interaction:
      if self.interaction.message.flags.ephemeral:
        await self.interaction.edit_original_response(view = self)
      else:
        await self.interaction.message.edit(view = self)

  @discord.ui.button(emoji = '⏪', style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateLeftmost(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[0], view = paginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = 0, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))    
    else:
      await interaction.message.edit(embed = self.embeds[0], view = paginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = 0, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))
      await interaction.response.defer()

  @discord.ui.button(emoji = "⬅️", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[self.page-1], view = paginateButtons(embeds = self.embeds, page = self.page-1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))      
    else:
      await interaction.message.edit(embed = self.embeds[self.page-1], view = paginateButtons(embeds = self.embeds, page = self.page-1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))
      await interaction.response.defer() 

  @discord.ui.button(label = "1", style = discord.ButtonStyle.blurple)
  async def buttonModal(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    await interaction.response.send_modal(modal(embeds = self.embeds, author_ids = self.author_ids, timeout = self.timeout, button_emojis = self.button_emojis))

  @discord.ui.button(emoji = "➡️", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateRight(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[self.page+1], view = paginateButtons(embeds = self.embeds, page = self.page+1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))      
    else:
      await interaction.message.edit(embed = self.embeds[self.page+1], view = paginateButtons(embeds = self.embeds, page = self.page+1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))      
      await interaction.response.defer() 

  @discord.ui.button(emoji = "⏩", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateRightmost(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[len(self.embeds)-1], view = paginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = len(self.embeds)-1, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))
    else:
      await interaction.message.edit(embed = self.embeds[len(self.embeds)-1], view = paginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = len(self.embeds)-1, timeout = self.timeout, interaction = interaction, button_emojis = self.button_emojis))
      await interaction.response.defer()

class paginator():
  def __init__(self, embeds: list[discord.Embed], author_ids: list[int], timeout: int, button_emojis: list[discord.Emoji] = None, interaction: discord.Interaction = None):
    self.embeds = embeds
    self.embed = self.embeds[0]
    self.author_ids = author_ids
    self.timeout = timeout
    self.button_emojis = button_emojis
    self.view = paginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = 0, timeout = self.timeout, button_emojis = self.button_emojis)

def paginate(embeds: list[discord.Embed], author_ids: list[int] = None, timeout: int = 90, button_emojis: list[discord.Emoji] = None) -> paginator:
  """
  Returns a dpy_paginator.paginator object that contains the first embed
  and the view associated with it.

  Parameters
  ----------
  embeds: List[:class:`discord.Embed`]
      A list of embeds to paginate.
  author_ids: List[:class:`int`] (optional)
      An optional list of author IDs who can interact with the view.
      Anyone can interact with the buttons if left blank.
  timeout: :class:`int` (optional)
      An optional integer for specifying the timeout (in seconds).
      Defaults to 90.
  button_emojis: List[:class:`discord.Emoji`] (optional)
      An optional list of discord.Emoji objects to be used in the buttons.
      Must have exactly 4 objects.
  """
  if not isinstance(embeds, list):
    raise TypeError(f'embeds: Expected a list of discord.Embed objects, got {type(embeds).__name__} instead.')

  for embed in embeds:
    if not isinstance(embed, discord.Embed):
      raise TypeError(f'embeds: Expected discord.Embed objects, got {type(embed).__name__} instead.')

  if author_ids:
    if not isinstance(author_ids, list):
      raise TypeError(f'author_ids: Expected a list of ints, got {type(author_ids).__name__} instead.')
    for author_id in author_ids:
      if not isinstance(author_id, int):
        raise TypeError(f'author_ids: Expected int objects, got {type(author_id).__name__} instead.')

  if timeout and not isinstance(timeout, int):
    raise TypeError(f'timeout: Expected an int, got {type(timeout).__name__} instead.')

  if button_emojis:
    if not isinstance(button_emojis, list):
      raise TypeError(f'button_emojis: Expected a list of discord.Embed objects or Unicode strings, got {type(button_emojis).__name__} instead.')
    if len(button_emojis) != 4:
      raise ValueError(f'button_emojis: List must contain 4 discord.Emoji objects or Unicode strings, got {len(button_emojis)} instead.')

  return paginator(embeds = embeds, author_ids = author_ids, timeout = timeout, button_emojis = button_emojis)
