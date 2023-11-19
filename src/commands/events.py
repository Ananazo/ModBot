from discord.ext import commands
import discord
import sqlfu

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is online")
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        category = await guild.create_category("ModBot")
        role = guild.get_role(sqlfu.get_admin_role_id(guild)) 
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
        }
        await category.edit(overwrites=overwrites)
        await guild.create_text_channel("ModBot", category=category, overwrites=overwrites)
        testh_value = 24
        warn_count_value = 3
        sqlfu.sqlfunc("INSERT INTO guilds (guild, testh, warn_count) VALUES (%s, %s, %s)", (guild.id, testh_value, warn_count_value))
def setup(bot):
    bot.add_cog(Events(bot))