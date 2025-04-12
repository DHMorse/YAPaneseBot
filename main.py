import os
import dotenv 
import discord
from discord.ext import commands
from typing import Optional
import asyncio

from constants import LANGUAGE_ROLE_NAMES

dotenv.load_dotenv()

botToken: Optional[str] = os.getenv("BOT_TOKEN")

if not botToken:
    raise ValueError("BOT_TOKEN is not set in the environment variables")

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# On member update check what roles they have
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.roles != after.roles:
        # if the user has 3 or more roles from the LANGUAGE_ROLE_NAMES list, add the "Polyglot" role
        if len([role for role in after.roles if role.name in LANGUAGE_ROLE_NAMES]) >= 3:
            await after.add_roles(discord.utils.get(after.guild.roles, name="Polyglot"))
        else:
            await after.remove_roles(discord.utils.get(after.guild.roles, name="Polyglot"))


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")

if __name__ == "__main__":
    bot.run(botToken)