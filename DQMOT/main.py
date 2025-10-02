# imports

import discord
# from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import logging
from keepAlive import keepAlive

load_dotenv()
# variables

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
handler = logging.FileHandler('discord.log', encoding='utf-8', mode='w')
# intents are the perms you set up within the app page
intents.message_content = True
intents.members = True
intents.messages = True

g_id = 262069922060959744

class QuoteBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.quotes_file = "quotes.json"
        self.quotes = self.load_quotes()

    def load_quotes(self):
        if os.path.exists(self.quotes_file):
            with open(self.quotes_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_quotes(self):
        with open(self.quotes_file, 'w') as f:
            json.dump(self.quotes, f, indent=1)

    def get_guild_quotes(self, guild_id):
        return self.quotes.setdefault(str(guild_id), []) # thanks chat

    async def setup_hook(self):
        
        # guild = discord.Object(id=g_id)
        # self.tree.clear_commands(guild=guild)
        # self.tree.copy_global_to(guild=guild)
        await self.tree.sync()
        print("We have synced cmds.")

bot = QuoteBot()
# functions
# @bot.tree.command(name="get_quotes", description="Returns all quotes made in this guild")
# async def get_quotes(interaction: discord.Interaction):
#     if interaction.user.id:
#         await interaction.response.send_message("sybau")

@bot.tree.command(name="get_quotes_from_user", description="Gets the list of quotes from a provided user")
async def get_quotes_from_user(interaction: discord.Interaction, user: discord.User):
    guild_id = str(interaction.guild_id)
    guild_quotes = bot.get_guild_quotes(guild_id)

    user_quotes = [quote for quote in guild_quotes if quote['user_id'] == user.id]

    if not user_quotes:
        await interaction.response.send_message(f"Failed to get quotes from {user.name}")

    string = ""
    for quote in user_quotes:
        string = string + f'"*{quote['quote']}*" - {quote['user_name']} (id: {quote['id']})\n'
    await interaction.response.send_message(string)

@bot.tree.command(name="quote_user", description="Stores a quote and the author")
async def quote_user(interaction: discord.Interaction, user: discord.User, text: str):
    guild_id = str(interaction.guild_id)
    guild_quotes = bot.get_guild_quotes(guild_id)
    quote_id = quote_id = max([q["id"] for q in guild_quotes], default=0) + 1

    guild_quotes.append(
        {
            "id": quote_id,
            "user_id": user.id,
            "user_name": user.name,
            "quote": text
        }
    )
    bot.save_quotes()
    await interaction.response.send_message(f"Quote added for {user.mention} (ID: {quote_id})")

async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="get_guild_quotes", description="Gets all the quotes from this guild")
async def get_guild_quotes(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    guild_quotes = bot.get_guild_quotes(guild_id)

    if len(guild_quotes) == 0:
        await interaction.response.send_message("This guild has no quotes.")
        return

    string = ""

    for quote in guild_quotes:
        string = string + f'"*{quote['quote']}*" - {quote['user_name']} (id: {quote['id']})\n'

    await interaction.response.send_message(f'{string}')


@bot.tree.command(name="delete_quote", description="Delete a quote by ID (mod only)")
async def delete_quote(interaction: discord.Interaction, quote_id: int):
    if not interaction.user.guild_permissions.manage_messages: # type: ignore
        await interaction.response.send_message(
            "❌ You don’t have permission to delete quotes.", ephemeral=True
        )
        return

    guild_id = str(interaction.guild_id)
    guild_quotes = bot.get_guild_quotes(guild_id)

    for q in guild_quotes:
        if q["id"] == quote_id:
            guild_quotes.remove(q)
            bot.save_quotes()
            await interaction.response.send_message(f"🗑️ Deleted quote ID {quote_id}.")
            return

    await interaction.response.send_message("❌ Quote not found.")

if __name__ == "__main__": # bitch ass token wanna throw an error. IT IS a string
    keepAlive()
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG) # type: ignore