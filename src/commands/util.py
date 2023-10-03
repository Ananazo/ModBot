import discord
from discord.ext import commands
from discord.commands import Option

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Feedback", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Feedback")
        embed.add_field(name="**Feedback**", value=self.children[0].value)
        await interaction.response.send_message(embeds=[embed])

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get the bot's current latency! (30s cooldown)")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency * 1000)}ms", ephemeral=True)

    @commands.slash_command()
    async def feedback(self, ctx: discord.ApplicationContext):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Feedback")
        await ctx.send_modal(modal)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send('Welcome to the server!')


def setup(bot):
    bot.add_cog(Util(bot))