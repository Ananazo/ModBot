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

@bot.slash_command(description="Gets some feedback.")
async def feedback(ctx: discord.ApplicationContext):
    try:
        await ctx.respond(f"Hey, {ctx.author}! Send your feedback within the next 30 seconds please!")

        def is_author(m: discord.Message):
            return m.author.id == ctx.author.id

        feedback_message = await bot.wait_for("message", check=is_author, timeout=30.0)
        await ctx.send(f"Thanks for the feedback!\nReceived feedback: `{feedback_message.content}`")
        print(f"{ctx.author} says {feedback_message.content}")

        with open("feedback.txt", "w") as f:
            f.write(f"{ctx.author} says {feedback_message.content} /n")

    except asyncio.TimeoutError:
        await ctx.send("Timed out, please try again!")
        
@tasks.loop(minutes=30)
async def change_status():
    activity = discord.Activity(name=next(status), type=1)
    await bot.change_presence(activity=activity)

bot.run(os.getenv('TOKEN'))