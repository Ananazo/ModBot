import discord
from discord.ext import commands
from discord.commands import Option
import datetime
import sqlfu
from datetime import datetime

class MyModal(discord.ui.Modal):
    def __init__(self, guild):
        super().__init__(title="Feedback")
        self.guild = guild
        self.add_item(discord.ui.InputText(label="Feedback", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Feedback")
        value = self.children[0].value
        embed.add_field(name="**Feedback**", value=value)
        await interaction.response.send_message(embeds=[embed], ephemeral=True)
        sqlfu.sqlfunc("INSERT INTO feedback (Date, Giver, Feedback, Guild) VALUES (%s, %s, %s, %s)", 
                      (datetime.now(), interaction.user.id, value, self.guild.id))

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.slash_command(description="Get server and bot info")
    async def info(self, ctx: commands.Context, member: discord.Member):
        server = ctx.guild
        uptime = datetime.now() - self.start_time
        counter = 0 
        async for message in ctx.channel.history(limit = 10000):
            if message.author == member:
                counter += 1
        info = (
            f"Server size: {len(server.members)} members\n"
            f"Bot uptime: {uptime}\n"
            f"I'm in {len(self.bot.guilds)} servers!\n" 
            f'{member.mention} has sent **{counter}** messages in this channel.'
        )
        await ctx.respond(info, ephemeral=True)

        
    @commands.slash_command(description="Get the bot's current latency! (30s cooldown)")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency * 1000)}ms", ephemeral=True)

    @commands.slash_command()
    async def feedback(self, ctx: discord.ApplicationContext):
        await ctx.send_modal(MyModal(ctx.guild))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send('Welcome to the server!')

def setup(bot):
    bot.add_cog(Util(bot))