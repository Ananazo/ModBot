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
        category = await guild.create_category("ModBot")
        role = guild.get_role(1162821285592703056) 
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
        }
        await category.edit(overwrites=overwrites)
        await guild.create_text_channel("ModBot", category=category, overwrites=overwrites)

def setup(bot):
    bot.add_cog(Events(bot))