import random
import traceback

import discord
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()

# Variables
def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} is not set")
    return value


MOOBER_TOKEN = required_env('MOOBER_TOKEN')
SERVER_ID = required_env('TEST_SERVER_ID')
CHANNEL_ID = required_env('CHANNEL_ID')
MASON_DISCORD_ID = required_env('MASON_DISCORD_ID')
MY_GUILD = discord.Object(id=int(SERVER_ID)) 
MASON_DM = discord.Object(id=int(MASON_DISCORD_ID))
REPORTS_CHANNEL_ID = required_env('CHANNEL_ID')


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
        self.tree = app_commands.CommandTree(self, allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True), allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True))

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        await self.tree.sync()



intents = discord.Intents.default()
client = MyClient(intents=intents)

maomao_gifs = {"hehehe": "https://tenor.com/gg023IrsKv5.gif", "ugh": "https://tenor.com/n2Slykonyhs.gif", "eating":"https://tenor.com/oyy00ODeRzU.gif", "bored munching": "https://tenor.com/iHRldzpmWO2.gif", "autism jump":"https://tenor.com/iBtRd6qJxAl.gif", "bruh disgust": "https://tenor.com/hIFctTvu0LM.gif", "cat grr": "https://tenor.com/iM8BVbMFSQj.gif", "scowl":"https://tenor.com/frAA0BZemKC.gif", "hard-work":"https://tenor.com/k15Z78dpf2c.gif",  "deflated":"https://tenor.com/fYN4LHjrSVT.gif", "headhit": "https://tenor.com/dEOzoNyoxZx.gif", "working-hug":"https://tenor.com/bweeGhgoO77.gif"}
jinshi_gifs = {"headbang":"https://tenor.com/j3xuAYm6cOy.gif", "working-hug":"https://tenor.com/bweeGhgoO77.gif", "close-sparkle":"https://tenor.com/pxKgwbITPs5.gif", "moody":"https://tenor.com/ewwfTeKWIPs.gif", "super-sparkle":"https://tenor.com/bHG6FgKBAcQ.gif"}

# Define a modal dialog for reporting issues or feedback
class BobaOrderModal(discord.ui.Modal, title='Boba Order'):
    shop = discord.ui.Label(
        text='Boba Shop Location',
        description='Select yummiest boba place',
        component=discord.ui.Select(
            placeholder='Where is Mason going to get boba?',
            required=False,
            options=[
                discord.SelectOption(label='Tea Hill CH'),
                discord.SelectOption(label='Moge Tea CH'),
                discord.SelectOption(label='Bobo Baba Cary'),
                discord.SelectOption(label='Moge Tea Raleigh'),
                discord.SelectOption(label='Other'),
            ],
        ),
    )
    boba_type = discord.ui.Label(
            text='Boba Type',
            description='Select the type of boba you want',
        
            component=discord.ui.Select(
                placeholder='what boba type are u getting?',
                required=False,
                options=[
                    discord.SelectOption(label='Passion Fruit Green Tea'),
                    discord.SelectOption(label='Yuzu Oolong'),
                    discord.SelectOption(label='Superfruit Green Tea'),
                    discord.SelectOption(label='Lemon Tea'),
                    discord.SelectOption(label='Other'),
                ],
            ),
        )
    toppings = discord.ui.Label(
        text='Toppings',
        description='Select the toppings you want on your boba',
        component=discord.ui.Select(
            placeholder='What toppings do you want on your boba?',
            required=False,
            options=[
                discord.SelectOption(label='Normal Boba'),
                discord.SelectOption(label='Golden Bubble'),
                discord.SelectOption(label='None'),
    
            ],
        ),
    )
    size = discord.ui.Label(
                text='Size',
                description='Select the size of your boba',
                component=discord.ui.Select(
                    placeholder='What size do you want your boba?',
                    required=False,
                    options=[
                        discord.SelectOption(label='Large'),
                        discord.SelectOption(label='Medium'),
                        discord.SelectOption(label='Small'),
                    ],
                ),
            )
    footer = discord.ui.TextDisplay(
        'thank you for ordering with moober eats :)))'
    )

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.shop.component, discord.ui.Select)
        assert isinstance(self.boba_type.component, discord.ui.Select)
        assert isinstance(self.toppings.component, discord.ui.Select)
        assert isinstance(self.size.component, discord.ui.Select)
        assert isinstance(self.footer, discord.ui.TextDisplay)



        shop = self.shop.component.values[0] if self.shop.component.values else "custom"
        boba_type = self.boba_type.component.values[0] if self.boba_type.component.values else "custom"
        toppings = self.toppings.component.values[0] if self.toppings.component.values else "custom"
        size = self.size.component.values[0] if self.size.component.values else "custom"



        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay('-# New Boba Order'))

        timestamp = discord.utils.format_dt(interaction.created_at, 'F')
        footer = discord.ui.TextDisplay(f'-# Reported by {interaction.user} (ID: {interaction.user.id}) | {timestamp}')

        if shop:
            container.add_item(discord.ui.TextDisplay(f'Shop: {shop}'))
        if boba_type:
            container.add_item(discord.ui.TextDisplay(f'### Boba Type: {boba_type}'))
        if toppings:
            container.add_item(discord.ui.TextDisplay(f'### Toppings: {toppings}'))
        if size:
            container.add_item(discord.ui.TextDisplay(f'### Size: {size}'))


        container.add_item(footer)
        return view
        

    async def on_submit(self, interaction: discord.Interaction):
        view = self.to_view(interaction)
    
        # Send the order to the Mason's dm's
        member = await interaction.client.fetch_user(int(MASON_DISCORD_ID))
        channel = await member.create_dm()
        await channel.send(view=view)
        await interaction.response.send_message('Thank you for ordering with Moober Eats, your order got sent to Mason and he is getting your food', ephemeral=True)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Mason coded something wrong T-T sorry you have to order manually', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

class CustomBobaOrderModal(discord.ui.Modal, title='Custom Boba Order'):
    custom_order = discord.ui.Label(
        text='Custom Order',
        description='A detailed description of your custom order.',
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            placeholder='Describe your custom order here.',
            max_length=2000,
        ),
    )
    footer = discord.ui.TextDisplay(
        'thank you for ordering with moober eats :)))'
    )

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.custom_order.component, discord.ui.TextInput)

        custom_order = self.custom_order.component.value

        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay('-# New Boba Order}'))

        timestamp = discord.utils.format_dt(interaction.created_at, 'F')
        footer = discord.ui.TextDisplay(f'-# Reported by {interaction.user} (ID: {interaction.user.id}) | {timestamp}')

        container.add_item(discord.ui.TextDisplay(f'### Custom Order: {custom_order}'))

        container.add_item(footer)
        return view

    async def on_submit(self, interaction: discord.Interaction):
        view = self.to_view(interaction)

        # Send the order to the Mason's dm's
        member = await interaction.client.fetch_user(int(MASON_DISCORD_ID))
        channel = await member.create_dm()
        await channel.send(view=view)
        await interaction.response.send_message('Thank you for ordering with Moober Eats, your order got sent to Mason and he is getting your food', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Mason coded something wrong T-T sorry you have to order manually', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

# Define a modal dialog for reporting issues or feedback
class DeliveryModal(discord.ui.Modal, title='Delivery Update'):
    delivery = discord.ui.Label(
            text='Delivery Name',
            description='Name of Deliver',
            component=discord.ui.TextInput(
                style=discord.TextStyle.paragraph,
                placeholder='What is being delivered',
                max_length=2000,
            ),
        )
    duration = discord.ui.Label(
            text='Duration',
            description='How long to timeout the member for.',
            component=discord.ui.Select(
                options=[
                    discord.SelectOption(label='Here!'),
                    discord.SelectOption(label='1 minute'),
                    discord.SelectOption(label='3 minutes'),
                    discord.SelectOption(label='5 minutes'),
                    discord.SelectOption(label='10 minutes'),
                    discord.SelectOption(label='15 minutes'),
                    discord.SelectOption(label='30 minutes'),
                    discord.SelectOption(label='45 minutes'),
                    discord.SelectOption(label='1+ hours'),
                ],
            ),
        )
    description = discord.ui.Label(
        text='Description',
        description='Notes to add to the delivery',
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            placeholder='When I use /ping, the bot does not respond at all. There are no error messages.',
            max_length=2000,
            required=False
        ),
    )
    images = discord.ui.Label(
        text='Images',
        description='Upload any relevant images for your report (optional).',
        component=discord.ui.FileUpload(
            max_values=10,
            custom_id='report_images',
            required=False,
        ),
    )
    footer = discord.ui.TextDisplay(
        'Thanks for getting joans food lol'
    )

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.delivery.component, discord.ui.TextInput)
        assert isinstance(self.duration.component, discord.ui.Select)
        assert isinstance(self.description.component, discord.ui.TextInput)
        assert isinstance(self.images.component, discord.ui.FileUpload)

        delivery = self.delivery.component.value
        duration = self.duration.component.values[0]
        description = self.description.component.value
        files = self.images.component.values

     
        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay(f'-# User Report\n## {delivery}'))

        timestamp = discord.utils.format_dt(interaction.created_at, 'F')
        footer = discord.ui.TextDisplay(f'-# Reported by {interaction.user} (ID: {interaction.user.id}) | {timestamp}')

        container.add_item(discord.ui.TextDisplay(f'### {duration}'))

        if description: 
            container.add_item(discord.ui.TextDisplay(f'>>> {description}'))
    

        if files:
            gallery = discord.ui.MediaGallery()
            gallery.items = [discord.MediaGalleryItem(media=attachment.url) for attachment in files]
            container.add_item(gallery)

        container.add_item(footer)
        return view

    async def on_submit(self, interaction: discord.Interaction):
        view = self.to_view(interaction)

        # Send the order to the discord
        channel = client.get_channel(int(CHANNEL_ID))  #  Gets channel from internal cache Sends message to channel
        if not isinstance(channel, discord.TextChannel):
            raise RuntimeError("It has to be text channel")

        await channel.send(view=view)
        await interaction.response.send_message('Thank you for updating Joan!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Mason coded something wrong T-T sorry you have to just tell her manually', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


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

@client.tree.command(description='Order boba.')
async def order_boba(interaction: discord.Interaction):
    # Send the modal with an instance of our `BobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(BobaOrderModal())

@client.tree.command(description='Order custom boba.')
async def order_custom_boba(interaction: discord.Interaction):
    # Send the modal with an instance of our `CustomBobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(CustomBobaOrderModal())

@client.tree.command(description='Update delivery status.')
async def delivery(interaction: discord.Interaction):
    # Send the modal with an instance of our `DeliveryUpdateModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(DeliveryModal())


client.run(MOOBER_TOKEN)