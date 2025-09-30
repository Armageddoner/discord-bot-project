# imports

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import logging

load_dotenv()
# variables

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
handler = logging.FileHandler('discord.log', encoding='utf-8', mode='w')
# intents are the perms you set up within the app page
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='*', intents=intents)

# functions
#test lmao

if __name__ == "__main__": # bitch ass token wanna throw an error. IT IS a string
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG) # type: ignore