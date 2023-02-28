# Copyright (c) 2023 OnceYT
# Licensed under the MIT License

import discord

class ModalPage(discord.ui.Modal, title = "Jump to page"):
  def __init__(self, embeds: list, author_ids: list, timeout: int):
    super().__init__(timeout = timeout)
    self.embeds = embeds
    self.author_ids = author_ids
    self.input.label = f"Page number: (0-{len(self.embeds)})"

  input = discord.ui.TextInput(label = "placeholder", placeholder = "Enter the page number...")

  async def on_submit(self, interaction: discord.Interaction):
    response = int(self.input.value)-1
    if response > len(self.embeds):
      await interaction.response.defer()
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[int(response)], view = PaginateButtons(embeds = self.embeds, page = int(response), author_ids = self.author_ids, timeout = self.timeout, interaction = interaction))
    else:
      await interaction.message.edit(embed = self.embeds[int(response)], view = PaginateButtons(embeds = self.embeds, page = int(response), author_ids = self.author_ids, timeout = self.timeout, interaction = interaction))
      await interaction.response.defer()

class PaginateButtons(discord.ui.View):
  def __init__(self, embeds: list[discord.Embed], page: int, author_ids: list[int], timeout: int, interaction: discord.Interaction = None):
    super().__init__(timeout = timeout)
    self.embeds = embeds
    self.page = page
    self.author_ids = author_ids
    self.timeout = timeout 
    self.interaction = interaction 
    self.buttonModal.label = f"{page+1}/{len(self.embeds)}"
    #self.remove_item(self.buttonPaginateLeftmost)
     
    if len(self.embeds) < 4:
      self.buttonModal.disabled = True
    if self.page > 0:
      self.buttonPaginateLeftmost.disabled = False
      self.buttonPaginateLeft.disabled = False
    if self.page != len(self.embeds)-1:
      self.buttonPaginateRightmost.disabled = False
      self.buttonPaginateRight.disabled = False

  async def on_timeout(self):
    if self.interaction:
      for children in self.children:
        children.disabled = True
      if self.interaction.message.flags.ephemeral:
        await self.interaction.edit_original_response(view = self)
      else:
        await self.interaction.message.edit(view = self)

  @discord.ui.button(emoji = "⏪", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateLeftmost(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[0], view = PaginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = 0, timeout = self.timeout, interaction = interaction))    
    else:
      await interaction.message.edit(embed = self.embeds[0], view = PaginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = 0, timeout = self.timeout, interaction = interaction))
      await interaction.response.defer()

  @discord.ui.button(emoji = "⬅️", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[self.page-1], view = PaginateButtons(embeds = self.embeds, page = self.page-1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction))      
    else:
      await interaction.message.edit(embed = self.embeds[self.page-1], view = PaginateButtons(embeds = self.embeds, page = self.page-1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction))
      await interaction.response.defer() 

  @discord.ui.button(label = "1", style = discord.ButtonStyle.blurple)
  async def buttonModal(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    await interaction.response.send_modal(ModalPage(embeds = self.embeds, author_ids = self.author_ids, timeout = self.timeout))

  @discord.ui.button(emoji = "➡️", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateRight(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[self.page+1], view = PaginateButtons(embeds = self.embeds, page = self.page+1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction))      
    else:
      await interaction.message.edit(embed = self.embeds[self.page+1], view = PaginateButtons(embeds = self.embeds, page = self.page+1, author_ids = self.author_ids, timeout = self.timeout, interaction = interaction))      
      await interaction.response.defer() 

  @discord.ui.button(emoji = "⏩", style=discord.ButtonStyle.grey, disabled = True)
  async def buttonPaginateRightmost(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.author_ids and interaction.user.id not in self.author_ids:
      return
    if interaction.message.flags.ephemeral:
      await interaction.response.defer()
      await interaction.edit_original_response(embed = self.embeds[len(self.embeds)-1], view = PaginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = len(self.embeds)-1, timeout = self.timeout, interaction = interaction))
    else:
      await interaction.message.edit(embed = self.embeds[len(self.embeds)-1], view = PaginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = len(self.embeds)-1, timeout = self.timeout, interaction = interaction))
      await interaction.response.defer()

class Paginator():
  def __init__(self, embeds: list[discord.Embed], author_ids: list[int], timeout: int):
    self.embeds = embeds
    self.embed = self.embeds[0]
    self.author_ids = author_ids
    self.timeout = timeout
    self.view = PaginateButtons(embeds = self.embeds, author_ids = self.author_ids, page = 0, timeout = self.timeout)

async def Paginate(embeds: list[discord.Embed], author_ids: list[int] = None, timeout: int = 90) -> Paginator:
  return Paginator(embeds, author_ids, timeout)
