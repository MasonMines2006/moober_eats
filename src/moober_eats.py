import discord

from src.client import MyClient
from src.links import jinshi_gifs
from src.modals import (
    BobaOrderModal,
    CustomOrderModal,
    DeliveryModal,
    MunchieOrderModal,
    OnlineOrderModal,
    PastDeliveryModal,
)
from src.secret_imports import (
    MASON_DISCORD_ID,
    MOOBER_TOKEN,
)

intents = discord.Intents.default()
client = MyClient(intents=intents)

# Define a modal dialog for reporting issues or feedback


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.tree.command(description="Moober Eats, show me what you got!")
async def hello(interaction: discord.Interaction):
    """Show the user's five most recent orders."""
    await interaction.response.send_message(
        "**Hello!** This is Mason, through the discord bot Moober Eats! \n \n"
        + "You might be wondering what I can do. "
        + "In short, I saw that ordering boba is fast when Mason can pick it up, but it could be faster. You have to go to the boba website, "
        + "find the menu on the internet, place your order, message me about it, and plan for when its delivered. boooooo! \n"
        + "So I spent two weeks working on Moober Eats "
        + "in order to save you around 30 seconds when you ordering boba/munchies. Because I'm a CS major. And its what we do. \n \n"
        + "**First,** order online with /online_order. It will give you a link to common boba/munchie places, so you dont have to look them up!. \n \n"
        + "**Once your done,** update Mason with one of the other commands. \n"
        + "/order_boba: Orders boba! You can choose between shop, size, your common boba faves, etc. \n"
        + "/order_munchies: munchies! delicious munchies. You can choose between different types of munchies here. \n"
        + "/order_custom: Sometimes, the options I can think of just wont cut it. You can specify your own craving here. \n \n"
        + "**Once you've ordered once,** you can order recent orders really fast with /order_repeat. \n \n"
        + "**There are other things too!** These are mainly for me, but feel free to look through them. \n"
        + "/delivery: This one is for me! It's how I will update you on your moober eats delivery. \n"
        + "/recent_five_orders: You can look at your most recent orders here!. \n"
        + "/whats_next: see future updates I'm planning on adding for Moober Eats. \n \n"
        + "And that's it. .--. i love u and i hope that this saves at least a little time you can use to not tweak out",
        ephemeral=True,
    )
    gif = jinshi_gifs.get("super-sparkle")
    await interaction.followup.send(gif if gif else " ", ephemeral=True)


@client.tree.command(description="Order boba.")
async def order_boba(interaction: discord.Interaction):
    # Send the modal with an instance of our `BobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(BobaOrderModal())


@client.tree.command(description="Order munchie.")
async def munchies(interaction: discord.Interaction):
    # Send the modal with an instance of our `MunchieOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(MunchieOrderModal())


@client.tree.command(description="Order custom boba.")
async def order_custom(interaction: discord.Interaction):
    # Send the modal with an instance of our `CustomBobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    await interaction.response.send_modal(CustomOrderModal())
    # They can only be done as a response to either an application command or a button press.


@client.tree.command(description="Order a past order.")
async def re_order(interaction: discord.Interaction):
    client = interaction.client
    assert isinstance(client, MyClient)
    deliveries = await client.db.get_recent_orders(interaction.user.id, 5)
    if not deliveries:
        await interaction.response.send_message(
            "u need to order something first lol", ephemeral=True
        )
        return
    # Send the modal with an instance of our `CustomBobaOrderModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    await interaction.response.send_modal(PastDeliveryModal(deliveries=deliveries))
    # They can only be done as a response to either an application command or a button press.


@client.tree.command(description="Update delivery status.")
async def delivery(interaction: discord.Interaction):

    # Send the modal with an instance of our `DeliveryUpdateModal` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    if interaction.user.id != int(MASON_DISCORD_ID):
        await interaction.response.send_message(
            "sorry, only mason can be moober eats boy lol.", ephemeral=True
        )
        return
    client = interaction.client
    assert isinstance(client, MyClient)
    deliveries = await client.db.get_open_orders(5)
    if not deliveries:
        await interaction.response.send_message(
            "u need to order something first lol", ephemeral=True
        )
        return

    await interaction.response.send_modal(DeliveryModal(deliveries=deliveries))


@client.tree.command(description="Redirect to online order.")
async def online_order(interaction: discord.Interaction):
    await interaction.response.send_modal(OnlineOrderModal())


@client.tree.command(description="Get recent five orders.")
async def past_orders(interaction: discord.Interaction):
    """Show the user's five most recent orders."""
    recent_orders = await client.db.get_recent_orders(
        user_id=interaction.user.id, limit=5
    )

    if not recent_orders:
        await interaction.response.send_message(
            "u need to order something first lol", ephemeral=True
        )
        return
    lines = []
    for order in recent_orders:
        lines.append(
            f"#{order['id']}: {order['order_name']} ({order['size']}) from {order['shop']} [{order['status']}]"
        )
    await interaction.response.send_message("\n".join(lines), ephemeral=True)


@client.tree.command(description="Im working on a lot of stuff. What are they?")
async def whats_next(interaction: discord.Interaction):
    working_gif = jinshi_gifs.get("working")
    await interaction.response.send_message(working_gif, ephemeral=True)
    await interaction.followup.send(
        "I'm working on a lot of things! sorry they take so long. \n Order Update: have orders actualy complete an order (rly hard)\n Simple Order Update: redirect to link of where youre ordering",
        ephemeral=True,
    )


client.run(MOOBER_TOKEN)
