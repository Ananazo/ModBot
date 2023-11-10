import discord
from discord.ext import commands
from discord.commands import Option
import datetime
import sqlfu

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Clear messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: Option(int, "How many messages to delete (default 5)", required=False, default=5)):
        await ctx.defer()
        await ctx.channel.purge(limit=amount+1)
        sqlfu.sqlfunc("INSERT INTO clemess (Date, Channel, Deleter, Count) VALUES (%s, %s, %s, %s)", 
                       (datetime.datetime.now(), ctx.channel.id, ctx.author.id, str(amount+1)))

    @commands.slash_command(description="Dm")
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx: commands.Context, who: Option(discord.User, "Who to dm?", required=True), what: Option(str, "What to dm?", required=True)):
        await who.send(what)
        await ctx.respond(f"{what} sent to {who}", ephemeral=True)
        channel = await self.get_or_create_channel(ctx, who)
        await channel.send(f"{what} sent to {who}")

    async def kick_user(self, ctx, who, reason):
        try:
            await who.kick(reason=reason)
            sqlfu.sqlfunc("INSERT INTO kicks (Date, Kicker, Kicked, Reason) VALUES (%s, %s, %s, %s)", 
                          (datetime.datetime.now(), ctx.channel.id, str(who.id), str(reason)))
            return True
        except Exception as e:
            print(f"Error kicking user: {e}")
            return False

    @commands.slash_command(description="Kick")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, who: Option(discord.User, "Who to kick?", required=True), why: Option(str, "Why", required=False)):
        if await self.kick_user(ctx, who, why):
            await ctx.respond(f"Kicked {who}", ephemeral=True)
        else:
            await ctx.respond(f"Failed to kick {who}", ephemeral=True)
            
    async def warn_user(self, ctx, who, reason):
        try:
            sqlfu.sqlfunc("INSERT INTO warns (Date, Warner, Warned, Reason) VALUES (%s, %s, %s, %s)",
                          (datetime.datetime.now(), ctx.author.id, str(who.id), str(reason)))
            warnings_count = sqlfu.sqlfunc("SELECT COUNT(*) FROM warns WHERE Warned = %s", (str(who.id),))
            last_kick = sqlfu.sqlfunc("SELECT MAX(Date) FROM kicks WHERE Kicked = %s", (str(who.id),))
            if last_kick and (datetime.datetime.now() - last_kick).total_seconds() < 24 * 60 * 60:
                await self.ban_user(ctx, who, "Banned for receiving a warning within 24 hours of being kicked", 1)
            elif warnings_count > 3:
                await self.kick_user(ctx, who, "Kicked for receiving more than three warnings")
            ep = discord.Embed(title="You have been warned", description=(f"{str(reason)}\nThis is your {warnings_count} warning."), color=discord.Colour.red())
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

    async def ban_user(self, ctx, who, reason, duration):
        try:
            await ctx.guild.ban(who, reason=reason)
            sqlfu.sqlfunc("INSERT INTO bans (Date, Banner, Banned, Reason, Duration) VALUES (%s, %s, %s, %s, %s)",
                          (datetime.datetime.now(), ctx.author.id, str(who.id), str(reason), duration))
            return True
        except Exception as e:
            print(f"Error banning user: {e}")
            return False

    @commands.slash_command(description="Ban")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: commands.Context, who: Option(discord.User, "Who to ban?", required=True), reason: Option(str, "Reason?", required=True), duration: Option(int, "Duration in hours?", required=True)): 

        if await self.ban_user(ctx, who, reason, duration):
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
        role = guild.get_role(1162821285592703056)
        
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