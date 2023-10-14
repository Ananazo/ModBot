import discord
import datetime
from discord.ext import commands
from discord.commands import Option
import sys
sys.path.insert(1, 'src')
import sqlfu
import time

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Clear messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: Option(int, "How many messages to delete (default 5)", required=False, default=5)):
        amount += 1
        await ctx.defer()
        await ctx.channel.purge(limit=amount)
        sql = "INSERT INTO clemess (Date, Channel, Deleter, Count) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.channel.id, ctx.author.id, str(amount))
        sqlfu.sqlfunc(sql, val)

    @commands.slash_command(description="Dm")
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx: commands.Context, who: Option(discord.User, "Who to dm?", required=True), what: Option(str, "What to dm?", required=True)):
        await who.send(what)
        await ctx.respond(f"{what} sent to {who}", ephemeral=True)
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="ModBot")
        role = guild.get_role(1162821285592703056)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
        }

        channel = discord.utils.get(category.text_channels, name=str(who.id))
        if channel is None:
            channel = await category.create_text_channel(str(who.id), overwrites=overwrites)
        
        await channel.send(f"{what} sent to {who}")

    @commands.slash_command(description="Kick")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, who: Option(discord.User, "Who to kick?", required=True), why: Option(str, "Why", required=False)):
        await who.kick(why)
        sql = "INSERT INTO kicks (Date, Kicker, Kicked, Reason) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.channel.id, str(who.id), str(why))
        sqlfu.sqlfunc(sql, val)
        await ctx.respond(f"Kicked {who}", ephemeral=True)

    @commands.slash_command(description="Warn")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx: commands.Context, who: Option(discord.User, "Who to warn?", required=True), why: Option(str, "Reason?", required=True)):
        ep = discord.Embed(
            title="You have been warned",
            description=(f"{str(why)}"),
            color=discord.Colour.red(),
        )
        await who.send(embed=ep)
        sql = "INSERT INTO warns (Date, Warner, Warned, Reason) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.author.id, str(who.id), str(why))
        sqlfu.sqlfunc(sql, val)
        await ctx.respond(f"Warned {who}", ephemeral=True)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("Missing permissions", ephemeral=True)

def setup(bot):
    bot.add_cog(Admin(bot))