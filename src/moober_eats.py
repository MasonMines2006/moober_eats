import discord
from src.secret_imports import MOOBER_TOKEN, SERVER_ID, CHANNEL_ID, MASON_DISCORD_ID, MY_GUILD, MASON_DM, REPORTS_CHANNEL_ID, DB_PATH, schema_path
from src.modals import BobaOrderModal, MunchieOrderModal, CustomOrderModal, DeliveryModal
from src.client import MyClient

intents = discord.Intents.default()
client = MyClient(intents=intents)

# Define a modal dialog for reporting issues or feedback

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command(description='Get recent five orders.')
async def recent_five_orders(interaction: discord.Interaction):
    """Show the user's five most recent orders."""
    recent_orders = await client.db.get_recent_orders(
        user_id=interaction.user.id,
        limit=5
    )

    if not recent_orders:
        await interaction.response.send_message("u need to order something first lol", ephemeral=True)
        return
    lines = []
    for order in recent_orders:
        lines.append(
            f"#{order['id']}: {order['order_name']} ({order['size']}) from {order['shop']} [{order['status']}]"
        )
    await interaction.response.send_message("\n".join(lines), ephemeral=True)

@client.tree.command(description='Order boba.')
async def order_boba(interaction: discord.Interaction):
    # Send the modal with an instance of our `BobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(BobaOrderModal())

@client.tree.command(description='Order munchie.')
async def munchies(interaction: discord.Interaction):
    # Send the modal with an instance of our `MunchieOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(MunchieOrderModal())

@client.tree.command(description='Order custom boba.')
async def order_custom(interaction: discord.Interaction):
    # Send the modal with an instance of our `CustomBobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    await interaction.response.send_modal(CustomOrderModal())
    # They can only be done as a response to either an application command or a button press.

@client.tree.command(description='Update delivery status.')
async def delivery(interaction: discord.Interaction):
    # Send the modal with an instance of our `DeliveryUpdateModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(DeliveryModal())
   





client.run(MOOBER_TOKEN)