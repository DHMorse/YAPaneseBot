import os
import random
import dotenv 
import discord
from discord.ext import commands
from typing import Optional

from constants import (
    LANGUAGE_ROLE_NAMES,
    LIST_OF_ANIME,
    YAPATRON_CHANNEL_ID,
    DOOM_GUY_ID
)

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

@bot.event
async def on_message(message: discord.Message):
    # Check if any anime term is in the message and only send one response
    if not message.author.bot:
        if any(anime in message.content.lower() for anime in LIST_OF_ANIME):
            await message.channel.send("https://tenor.com/view/anime-gif-7279870884587886608")
            return

    if 'gay' in message.content.lower():
        await message.add_reaction("🏳️‍🌈")

    if 'porn' in message.content.lower():
        await message.add_reaction("❌")

    if message.mentions:
        for mention in message.mentions:
            if mention.id == DOOM_GUY_ID:
                await message.reply("Check out this super family friendly [book](https://www.wattpad.com/story/392586616-the-hollow-born)")

    await bot.process_commands(message)

# Send custom message on timeout
@bot.event
async def on_member_update(before, after) -> None:
    if before.timeout != after.timeout:
        if after.timeout:
            channel: discord.TextChannel = bot.get_channel(YAPATRON_CHANNEL_ID)
            await channel.send(f"{after.mention} has been deported")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")

if __name__ == "__main__":
    bot.run(botToken)