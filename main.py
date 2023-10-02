import discord
import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

cogs_list = [
    'util',
    'moderation',
    'fun',
    'owner'
]

for cog in cogs_list:
    bot.load_extension(f'commands.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

bot.run(os.getenv('TOKEN')) # run the bot with the toke