import discord
import datetime
from discord.ext import commands
from discord.commands import Option
import mysql.connector
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        mydb = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASS'),
        database="ModBot"
        )

        mycursor = mydb.cursor()

    @commands.slash_command(description="Clear messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: Option(int, "How many messages to delete (default 5)", required = False, default = 5)):
        await ctx.defer()
        await ctx.channel.purge(limit=amount)
        sql = "INSERT INTO `cleared messages` (Date, Channel, Deleter, Count, Content) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), ctx.channel, ctx.author, str(amount))
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record inserted.")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("Missing permissions", ephemeral=True)

def setup(bot):
    bot.add_cog(Admin(bot))