import discord
import datetime
from discord.ext import commands
from discord.commands import Option
import mysql.connector
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = mysql.connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASS'),
            database="ModBot"
        )

        self.mycursor = self.mydb.cursor()

    @commands.slash_command(description="Clear messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: Option(int, "How many messages to delete (default 5)", required=False, default=5)):
        amount += 1
        await ctx.defer()
        await ctx.channel.purge(limit=amount)
        sql = "INSERT INTO clemess (Date, Channel, Deleter, Count) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.channel.id, ctx.author.id, str(amount))
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    @commands.slash_command(description="Dm")
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx: commands.Context, who: Option(discord.User, "Who to dm?", required=True), what: Option(str, "What to dm?", required=True)):
        await who.send(what)
        sql = "INSERT INTO dm (Date, Sender, Reciver, Content) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.author.id, who, what)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    @commands.slash_command(description="Kick")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, who: Option(discord.User, "Who to kick?", required=True), why: Option(str, "Why", required=False)):
        await who.kick(why)
        sql = "INSERT INTO kicks (Date, Kicker, Kicked, Reason) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.channel.id, who, why)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    @commands.slash_command(description="Warn")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx: commands.Context, who: Option(discord.User, "Who to warn?", required=True), why: Option(str, "Reason?", required=True)):
        embed = discord.Embed(title=f"**You have been warned**")
        await who.send(embeds=[embed])
        sql = "INSERT INTO warns (Date, Warner, Warned, Reason) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.author.id, who, what)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("Missing permissions", ephemeral=True)

def setup(bot):
    bot.add_cog(Admin(bot))