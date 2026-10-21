import random
from typing import Optional

import discord
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()
MOOBER_TOKEN = os.getenv('MOOBER_TOKEN') or "none"
SERVER_ID = os.getenv('TEST_SERVER_ID') or "none"
MASON_DISCORD_ID = os.getenv('MASON_DISCORD_ID') or "none"


MY_GUILD = discord.Object(id=SERVER_ID)  # replace with your guild id


class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser # pyright: ignore[reportIncompatibleMethodOverride]

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

maomao_gifs = {"hehehe": "https://tenor.com/gg023IrsKv5.gif", "ugh": "https://tenor.com/n2Slykonyhs.gif", "eating":"https://tenor.com/oyy00ODeRzU.gif", "bored munching": "https://tenor.com/iHRldzpmWO2.gif", "autism jump":"https://tenor.com/iBtRd6qJxAl.gif", "bruh disgust": "https://tenor.com/hIFctTvu0LM.gif", "cat grr": "https://tenor.com/iM8BVbMFSQj.gif", "scowl":"https://tenor.com/frAA0BZemKC.gif", "hard-work":"https://tenor.com/k15Z78dpf2c.gif",  "deflated":"https://tenor.com/fYN4LHjrSVT.gif", "headhit": "https://tenor.com/dEOzoNyoxZx.gif", "working-hug":"https://tenor.com/bweeGhgoO77.gif"}
jinshi_gifs = {"headbang":"https://tenor.com/j3xuAYm6cOy.gif", "working-hug":"https://tenor.com/bweeGhgoO77.gif", "close-sparkle":"https://tenor.com/pxKgwbITPs5.gif", "moody":"https://tenor.com/ewwfTeKWIPs.gif", "super-sparkle":"https://tenor.com/bHG6FgKBAcQ.gif"}



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
async def bobaaaa_0_0_(interaction: discord.Interaction):
    """Place to order boba"""
    await interaction.response.send_message(f'{interaction.user.mention} wants to order boba. Alert <@{MASON_DISCORD_ID}>!')

@client.tree.command()
async def munchies(interaction: discord.Interaction):
    """Place to order munchies"""
    await interaction.response.send_message(f'{interaction.user.mention} wants to order munchies. Alert <@{MASON_DISCORD_ID}>!')

@client.tree.command()
async def maomao(interaction: discord.Interaction):
    """Send a random gif"""
    gif = random.choice(list(maomao_gifs.values()))
    await interaction.response.send_message(gif)

@client.tree.command()
async def jinshi(interaction: discord.Interaction):
    """Send a random gif"""
    gif = random.choice(list(jinshi_gifs.values()))
    await interaction.response.send_message(gif)



client.run(MOOBER_TOKEN)