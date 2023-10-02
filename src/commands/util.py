import discord
from discord.ext import commands
from discord.commands import Option

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get the bot's current latency! (30s cooldown)")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency * 1000)}ms")

    @commands.slash_command(description="Clear messages")
    async def clear(self, ctx: commands.Context, amount: Option(int, "How many messages to delete (default 5)", required = False, default = 5)):
        await ctx.defer()
        await ctx.channel.purge(limit=amount)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send('Welcome to the server!')

def setup(bot):
    bot.add_cog(Util(bot))