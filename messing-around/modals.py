import random

import discord
from discord import app_commands

import traceback

from dotenv import load_dotenv
import os

load_dotenv()
SERVER_ID = os.getenv('TEST_SERVER_ID') or "none"
MOOBER_TOKEN = os.getenv('MOOBER_TOKEN') or "none"


MY_GUILD = discord.Object(id=SERVER_ID)  # replace with your guild id
# The guild in which this slash command will be registered.
# It is recommended to have a test guild to separate from your "production" bot
TEST_GUILD = discord.Object(id=SERVER_ID)


class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser # type: ignore

    def __init__(self) -> None:
        # Just default intents and a `discord.Client` instance
        # We don't need a `commands.Bot` instance because we are not
        # creating text-based commands.
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        # We need an `discord.app_commands.CommandTree` instance
        # to register application commands (slash commands in this case)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        # Sync the application command with Discord.
        await self.tree.sync(guild=TEST_GUILD)


class Feedback(discord.ui.Modal, title='Feedback'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label='What do you think of this new feature?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

        


client = MyClient()


@client.tree.command(guild=TEST_GUILD, description='Submit feedback')
async def feedback(interaction: discord.Interaction):
    # Send the modal with an instance of our `Feedback` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(Feedback())

# Source - https://stackoverflow.com/a/57340966
# Posted by Iain Shelvington, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-21, License - CC BY-SA 4.0
@client.tree.command()
async def send_dm(interaction: discord.Interaction, member: discord.Member, *, content: str):
    channel = await member.create_dm()
    await channel.send(content)
    await interaction.response.send_message("You did it!")

# Source - https://stackoverflow.com/a/78879538
# Posted by Lia Milenakos
# Retrieved 2026-10-21, License - CC BY-SA 4.0


@client.event
async def on_ready():
    await client.tree.sync()

@client.tree.command(name="randomness_number",description="used to giveaway thing")
async def qr(interaction:discord.Interaction,amount:int):
    await interaction.response.send_message(f"result is: {random.randint(1,amount)}")


client.run(MOOBER_TOKEN)