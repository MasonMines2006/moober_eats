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
        "I'm working on a lot of things! sorry they take so long. "
        "\n Order Update: have orders actualy complete an order (rly hard)\n "
        "Better UI/UX: the bot is pretty uggo so make it look more pretty and user friendly. Like a better app.",
        ephemeral=True,
    )


@client.tree.command(description="a history of everything I worked on!")
async def changelog(interaction: discord.Interaction):
    working_gif = jinshi_gifs.get("working")
    await interaction.response.send_message(
        "I really like looking back on everything that it took to make this bot, so if your curious, I have the full changelog below. \n"
        "\n**Changelog**\n"
        "**Initial Testing:** I made whole other test bot you didnt see to test discord.ui and the discord developer api. Basically was me learning how to make a bot even exist. \n"
        "**Art Design:** I actually designed the logo for moober eats first before anything else. I basicaly took a screenshot of the Uber Eats logo, and found a "
        "image online (that was actually a gif I had to screenshot) of the word MOVE in the uber logo. I combined them together in google slides and boom: i had a logo. \n"
        "**First Commit:** The first time I pushed anything official to the github repo. Most of it was in a test folder I called 'messing around'. I had to "
        "get rid of everything I had learned about coding discord bots in typescript/javascript, because there was a much easier library called Discord.UI in python "
        "that the tool is built off of today. Most of it was me playing with the discord api and the little 'getting started' tutorial codes that they have. \n",
        ephemeral=True,
    )
    await interaction.followup.send(
        "**Getting Started:** This is where I started getting serious about making it a fully working app. I messaged my old RedHat friend Alex Oladele (who is the goat btw)"
        ", and he helped give me ideas on how to work on my bot. I remembered from a convo we had that he gave a whole conference talk on making discord bots, so "
        "I messaged him asking how the dice bot was going and how I could deploy mine. We had a great convo where he reccomended me Fly.io, a really cheap deployment platform "
        "that I currently use to deploy the bot. It also apparently wont charge you if your spending is below 5 dollars a month, which is aweomse cuz its going to be used very infrequently.  "
        "During this time, I was also leanring how to do simple things like send messages to servers and channels, learning what guilds and stuff were, etc. \n"
        "**Cleaning up:** This was a big one. I learned what modals were, which are basically like little views that pop up when you run a command. Everything is built "
        "off of these modals! At the time of writing this, my modals are lik 750+ lines of code that I had to learn how to make by hand. They run off of async events "
        "that are basically like this: you run the /command, the api awaits a response to the little popup that I coded to show up (usually used for like timeouts or bans and stuff), "
        "and then it does something on submit, like send additional info to a DM or channel. Was very proud once I got my first modal working, even tho most of it was taken from a tutorial in the discord api docs lol. \n",
        ephemeral=True,
    )
    await interaction.followup.send(
        "**Working Bot:** This was the tipping point, and the point at which I faced the biggest crossroads. I had finished the working bot, spent a butt load of time into this gift"
        ", and was still not happy with how it had turned out. It looked fine: it could send messages without crashing, the modals were a little uggy but had taken forever, so overall "
        "I thought I had put a monumental amount of time into it. However, while I was coding late at night with my roommates brainstorming different ideas, Eunji and Anna "
        "kept throwing ideas for things Uber Eats does that my bot couldn't do. Things that would save Joan a bunch of time. The only problem was they required the bot to be able to save "
        "order informaiton in order to do things like reorder common orders, reccomend trends, update delivery times, etc. For a non-cs major, this does not sound that bad. "
        "I think only CS people understand how unbelieveable difficult this is, because your turning your bot from a basic input -> output machine into a fully working full-stack app "
        "with a working database to hold information and a backend to relay frontend commands into changing a backend. At this point, I saw how difficult that would be to code by hand, and "
        "I gave up. But then I crashed out about it some more with Eunji, who was like 'She deserves the best mason!' and so I started coding again through the night \n",
        ephemeral=True,
    )
    await interaction.followup.send(
        "**Making a Database:** Databases are freakin hard. I go from ez pz land of modifying little parts of pre-written tutorials designed to be easy, all in python, to learning how to code in sequal, creating my own database "
        "and CRUD (create, read, update, delete) functions for everything, figure out how to put it into my spaghetti code like a kindergartner putting the square block into the circle hole over and over, "
        "redoing the entire thing because I learned fly.io isnt powerful enough to do anything in sequel and it could only do a much more limited language called sql lite, "
        "crashing out all night because I lowk suck at coding, quitting and coming back like 4 times, etc etc. My final commit message from that night is simply 'so tired and must sleep'. \n"
        "**Version 1.0**: Finally, finally, finally I had a working version 1.0. Not deployed mind you, it only worked on my computer, but my test discord channel and dms "
        "with the bot is a testament to how much work went into making this first version. One thing I was proud of was I scoured gify (giffy? idk the gif website) for gifs "
        "of maomao and jinshi, named them all things like 'jinshi_sparkle', seperated them by tags like 'jinshi_sucess', and then had each command (including errors!) return "
        "a random gif from their appropriate tag. I also had to learn how a discord client works to get my database hooked up and have commands available globablly. Aforementioned "
        "child with the square block and circle hole. I popped tf off when it worked though holyyy \n"
        "**More security things** I added a secrets folder so nobody can steal our information, fixed deploy informaiton, did a buttttt ton of debugging and feature adding which "
        "you can read about in /hello, and finally sent to Joan! She likes it. she really likes it. The long nights were worth it. i rly like this girl :))",
        ephemeral=True,
    )
    await interaction.followup.send(working_gif or "", ephemeral=True)


client.run(MOOBER_TOKEN)
