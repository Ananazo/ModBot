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

cogs_list = ['util', 'admin']

for cog in cogs_list:
    bot.load_extension(f'src.commands.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    change_status.start()

@bot.event
async def on_guild_join(guild: discord.Guild):
    category = await guild.create_category("ModBot")
    role = guild.get_role(1162821285592703056) 
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
        role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
    }
    await category.edit(overwrites=overwrites)
    await guild.create_text_channel("ModBot", category=category, overwrites=overwrites)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        channel_name = str(message.author.id)
        guild = bot.get_guild(1158488964085321738)
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel:
            await channel.send(message.content)
    else:
        try:
            user_id = int(message.channel.name)
            user = bot.get_user(user_id)
            if user:
                await user.send(message.content)
        except ValueError:
            return

@tasks.loop(minutes=30)
async def change_status():
    activity = discord.Activity(name=next(status), type=1)
    await bot.change_presence(activity=activity)

bot.run(os.getenv('TOKEN'))