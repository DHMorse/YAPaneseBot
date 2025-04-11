import os
import dotenv 
import discord
from discord.ext import commands

dotenv.load_dotenv()

botToken = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")

if __name__ == "__main__":
    bot.run(botToken)