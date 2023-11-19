import discord
from discord.ext import commands, tasks
from discord.commands import Option
from itertools import cycle
import os
from dotenv import load_dotenv

status = cycle(['Moderating!'])

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

load_dotenv()

bot = discord.Bot(intents=intents)

cogs_list = ['util', 'admin', 'events']

for cog in cogs_list:
    bot.load_extension(f'commands.{cog}')

@tasks.loop(minutes=30)
async def change_status():
    activity = discord.Activity(name=next(status), type=1)
    await bot.change_presence(activity=activity)

bot.run(os.getenv('TOKEN'))