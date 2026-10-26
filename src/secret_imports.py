
import os

import discord
from dotenv import load_dotenv


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
DB_PATH = required_env('DB_PATH')

HERE = os.path.dirname(__file__)
schema_path = os.path.join(HERE, "../database", "schema.sql")

secret_imports = {
    "MOOBER_TOKEN": MOOBER_TOKEN,
    "SERVER_ID": SERVER_ID,
    "CHANNEL_ID": CHANNEL_ID,
    "MASON_DISCORD_ID": MASON_DISCORD_ID,
    "MY_GUILD": MY_GUILD,
    "MASON_DM": MASON_DM,
    "REPORTS_CHANNEL_ID": REPORTS_CHANNEL_ID,
    "DB_PATH": DB_PATH,
    "HERE": HERE,
    "schema_path": schema_path
}