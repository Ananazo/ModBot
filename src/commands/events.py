from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is online")
        self.bot.get_cog("Main").change_status.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Your on_guild_join code here

    @commands.Cog.listener()
    async def on_message(self, message):
        # Your on_message code here

def setup(bot):
    bot.add_cog(Events(bot))