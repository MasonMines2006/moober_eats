import aiosqlite
import discord
from discord import app_commands

from database import DatabaseManager
from src.secret_imports import DB_PATH, schema_path



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
        # Initialize our database
        self.db_connection = await aiosqlite.connect(DB_PATH)
        self.db_connection.row_factory = aiosqlite.Row
        with open(schema_path) as f: 
            schema_sql = f.read()
        await self.db_connection.executescript(schema_sql)
        self.db = DatabaseManager(connection=self.db_connection)

    async def close(self):
        await self.db_connection.close()
        await super().close()

