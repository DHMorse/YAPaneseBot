import os
import dotenv 
import discord
from discord.ext import commands
from typing import Optional
import random

from constants import (
    LANGUAGE_ROLE_NAMES,
    LIST_OF_ANIME,
    DOOM_GUY_ID,
    DOOM_GUY_BOOK_URL,
    ANIME_GIF_URL
)

dotenv.load_dotenv()

botToken: Optional[str] = os.getenv("BOT_TOKEN")

if not botToken:
    raise ValueError("BOT_TOKEN is not set in the environment variables")

bot: commands.Bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# On member update check what roles they have
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.roles != after.roles:
        # if the user has 3 or more roles from the LANGUAGE_ROLE_NAMES list, add the "Polyglot" role
        if len([role for role in after.roles if role.name in LANGUAGE_ROLE_NAMES]) >= 3:
            polyglotRole = discord.utils.get(after.guild.roles, name="Polyglot")
            if polyglotRole:
                await after.add_roles(polyglotRole)
        else:
            polyglotRole = discord.utils.get(after.guild.roles, name="Polyglot")
            if polyglotRole:
                await after.remove_roles(polyglotRole)

    # if before.timeout != after.timeout:
    #     if after.timeout:
    #         channel = discord.utils.get(after.guild.text_channels, name="yapatron")
    #         if channel:
    #             await channel.send(f"{after.mention} has been deported")

    #             async for message in channel.history(limit=7):
    #                 if message.author == after:
    #                     await message.delete()

@bot.event
async def on_member_timeout(member: discord.Member):
    channel: discord.TextChannel | None = discord.utils.get(member.guild.text_channels, name="yapatron")

    if not channel:
        print(f"Channel not found for yapatron")
        return

    if channel:
        await channel.send(f"{member.mention} has been deported")

        async for message in channel.history(limit=7):
            if message.author == member:
                await message.delete()

@bot.event
async def on_message(message: discord.Message):
    # Check if any anime term is in the message and only send one response
    if not message.author.bot:
        if any(anime in message.content.lower() for anime in LIST_OF_ANIME):
            await message.reply(f'{ANIME_GIF_URL}')
            return

    if 'gay' in message.content.lower():
        await message.add_reaction("🏳️‍🌈")

    if 'porn' in message.content.lower():
        await message.add_reaction("❌")

    if message.mentions:
        for mention in message.mentions:
            if mention.id == DOOM_GUY_ID:
                randInt: int = random.randint(0, 10)
                if randInt > 8:
                    await message.reply(f"Check out this super family friendly [book]({DOOM_GUY_BOOK_URL})")

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(botToken)