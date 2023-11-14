import discord
from discord.ext import commands
from discord.commands import Option
import datetime 
import src.sqlfu as sqlfu

class GuildSettings(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Change Testh and Warn Count")
        self.add_item(discord.ui.InputText(label="Testh", placeholder="Enter new Testh value"))
        self.add_item(discord.ui.InputText(label="Warn Count", placeholder="Enter new Warn Count value"))

    async def callback(self, interaction: discord.Interaction):
        try:
            testh_value = int(self.children[0].value)
            warn_count_value = int(self.children[1].value)
            guild_id = interaction.guild.id
            sqlfu.sqlfunc("UPDATE guilds SET testh = %s, warn_count = %s WHERE guild = %s", (testh_value, warn_count_value, guild_id))
            await interaction.response.send_message("Testh and Warn Count updated successfully", ephemeral=True)
        except Exception as e:
            print(f"Error updating Testh and Warn Count: {e}")

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Clear messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: Option(int, "How many messages to delete (default 5)", required=False, default=5)):
        await ctx.defer()
        await ctx.channel.purge(limit=amount+1)
        sqlfu.sqlfunc("INSERT INTO clemess (Date, Server, Channel, Deleter, Count) VALUES (%s, %s, %s, %s, %s)", 
                       (datetime.datetime.now(), ctx.guild.id, ctx.channel.id, ctx.author.id, str(amount+1))) 
        
    async def kick_user(self, ctx, who, reason, guild_id):
        try:
            await who.kick(reason=reason)
            sqlfu.sqlfunc("INSERT INTO kicks (Date, Kicker, Kicked, Reason, Guild) VALUES (%s, %s, %s, %s, %s)", 
                        (datetime.datetime.now(), ctx.channel.id, str(who.id), str(reason), guild_id))
            return True
        except Exception as e:
            print(f"Error kicking user: {e}")
            return False

    @commands.slash_command(description="guild settings")
    @commands.has_permissions(administrator=True)
    async def change_testh_warn_count(self, ctx: commands.Context):
        view = GuildSettings()
        await ctx.respond("guild settings", view=view)

    @commands.slash_command(description="Kick")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, who: Option(discord.User, "Who to kick?", required=True), why: Option(str, "Why", required=True)):
        guild_id = ctx.guild.id
        if await self.kick_user(ctx, who, why, guild_id):
            await ctx.respond(f"Kicked {who}", ephemeral=True)
        else:
            await ctx.respond(f"Failed to kick {who}", ephemeral=True)
            
    async def warn_user(self, ctx, who, reason):
        try:
            guild_id = ctx.guild.id
            result = sqlfu.sqlfunc("SELECT testh, warn_count FROM guilds WHERE guild = %s", (guild_id,))
            if result:
                testh, warn_count = result[0]
            else:
                print(f"No settings found for guild: {guild_id}")
                return False

            sqlfu.sqlfunc("INSERT INTO warns (Date, Warner, Warned, Reason, Guild) VALUES (%s, %s, %s, %s, %s)",
                        (datetime.datetime.now(), ctx.author.id, str(who.id), str(reason), guild_id))
            warnings_count = sqlfu.sqlfunc("SELECT COUNT(*) FROM warns WHERE Warned = %s AND Guild = %s", (str(who.id), guild_id))
            last_kick = sqlfu.sqlfunc("SELECT MAX(Date) FROM kicks WHERE Kicked = %s AND Guild = %s", (str(who.id), guild_id))
            if last_kick is not None and last_kick[0][0] is not None and (datetime.datetime.now() - last_kick[0][0]).total_seconds() < testh * 60 * 60:
                await self.ban_user(ctx, who, f"Banned for receiving a warning within {testh} hours of being kicked", 1, guild_id)
            elif int(warnings_count[0][0]) > int(warn_count):
                await self.kick_user(ctx, who, f"Kicked for receiving more than {warn_count} warnings", guild_id)
            ep = discord.Embed(title="You have been warned", description=(f"{str(reason)}\nThis is your {warnings_count[0][0]} warning."), color=discord.Colour.red())
            await who.send(embed=ep)
            return True
        except Exception as e:
            print(f"Error warning user: {e}")
            return False

    @commands.slash_command(description="Warn")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx: commands.Context, who: Option(discord.User, "Who to warn?", required=True), why: Option(str, "Reason?", required=True)): 
        if await self.warn_user(ctx, who, why):
            await ctx.respond(f"Warned {who}", ephemeral=True)
        else:
            await ctx.respond(f"Failed to warn {who}", ephemeral=True)

    async def ban_user(self, ctx, who, reason, duration, guild_id):
        try:
            await ctx.guild.ban(who, reason=reason)
            sqlfu.sqlfunc("INSERT INTO bans (Date, Banner, Banned, Reason, Duration, Guild) VALUES (%s, %s, %s, %s, %s, %s)",
                        (datetime.datetime.now(), ctx.author.id, str(who.id), str(reason), duration, guild_id))
            return True
        except Exception as e:
            print(f"Error banning user: {e}")
            return False

    @commands.slash_command(description="Ban")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: commands.Context, who: Option(discord.User, "Who to ban?", required=True), reason: Option(str, "Reason?", required=True), duration: Option(int, "Duration in hours?", required=True)): 
        guild_id = ctx.guild.id
        if await self.ban_user(ctx, who, reason, duration, guild_id):
            asyncio.create_task(self.unban_after_delay(ctx, who, duration))
            await ctx.respond(f"Banned {who} for {duration} hours", ephemeral=True)
        else:
            await ctx.respond(f"Failed to ban {who}", ephemeral=True)

    async def unban_after_delay(self, ctx, who, duration):
        await asyncio.sleep(duration * 60 * 60)
        try:
            await ctx.guild.unban(who)
        except Exception as e:
            print(f"Error unbanning user: {e}")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("Missing permissions", ephemeral=True)

    async def get_or_create_channel(self, ctx, who):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="ModBot")
        role = guild.get_role(sqlfu.get_admin_role_id(guild))
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
        }

        channel = discord.utils.get(category.text_channels, name=str(who.id))
        if channel is None:
            channel = await category.create_text_channel(str(who.id), overwrites=overwrites)
        
        return channel

def setup(bot):
    bot.add_cog(Admin(bot))