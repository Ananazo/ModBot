import discord
from discord.ext import commands, tasks
from discord.commands import Option
from itertools import cycle
import os
from dotenv import load_dotenv
import asyncio

status = cycle(['Moderating!'])

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

bot = commands.Bot(command_prefix="/", intents=intents)

cogs_list = [
    'util',
    'admin'
]

for cog in cogs_list:
    bot.load_extension(f'src.commands.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    change_status.start()  # Start the status change task when the bot is ready
    
@tasks.loop(minutes=30)
async def change_status():
    activity = discord.Activity(name=next(status), type=1)
    await bot.change_presence(activity=activity)

bot.run(os.getenv('TOKEN'))