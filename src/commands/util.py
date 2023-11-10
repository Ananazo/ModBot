import discord
from discord.ext import commands
from discord.commands import Option
import datetime
import sqlfu

class MyModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Feedback")
        self.add_item(discord.ui.InputText(label="Feedback", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Feedback")
            value = self.children[0].value
            embed.add_field(name="**Feedback**", value=value)
            await interaction.response.send_message(embeds=[embed], ephemeral=True)
            sqlfu.sqlfunc("INSERT INTO feedback (Date, Giver, Feedback) VALUES (%s, %s, %s)", 
                          (datetime.datetime.now(), interaction.user.id, value))
        except Exception as e:
            print(f"Error handling feedback: {e}")

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get the bot's current latency! (30s cooldown)")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency * 1000)}ms", ephemeral=True)

    @commands.slash_command()
    async def feedback(self, ctx: discord.ApplicationContext):
        try:
            await ctx.send_modal(MyModal())
        except Exception as e:
            print(f"Error sending feedback modal: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            await member.send('Welcome to the server!')
        except Exception as e:
            print(f"Error sending welcome message: {e}")

def setup(bot):
    bot.add_cog(Util(bot))