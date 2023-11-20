import nextcord
from nextcord.ext import commands
from nextcord.utils import get


class moderationCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # User joins a server 
    @commands.Cog.listener() 
    async def on_member_join(self, member):
        guild = member.guild
        channel_id = 1172051142021218314
        channel = guild.get_channel(channel_id)

        if channel:
            embed = nextcord.Embed(
                title="Welcome!",
                description=f"I'm glad you're in this wonderful server {guild.name}, enjoy your stay {member.mention}.", #This message can be edited to what you'd like
                color=nextcord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url)

            await channel.send(embed=embed)

    # User leaves a server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        channel_id = 1172051142021218314
        channel = guild.get_channel(channel_id)

        if channel:
            embed = nextcord.Embed(
                title="Darn.",
                description=f"I'm sad to see you go {member.mention}, we'll see you later.", #This message can be edited to what you'd like
                color=nextcord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)

            await channel.send(embed=embed)

    #Kicking a player
    @nextcord.slash_command(description="Kick a player from the server", default_member_permissions=8)
    async def kick(self, ctx, member : nextcord.Member, *, reason):

        dm = await member.create_dm()
        await dm.send(f"You have been kicked from this server for {reason}")

        await member.kick()
        await ctx.send(f"The member {member.name} has been kicked for {reason}")

    # Banning a player
    @nextcord.slash_command(description="Ban a player from the server", default_member_permissions=8)
    async def ban(self, ctx, member : nextcord.Member, *, reason):

        dm = await member.create_dm()
        await dm.send(f"You have been banned from this server for {reason}")

        await member.ban()
        await ctx.send(f"The member {member.name} has been banned for {reason}")

    # Unbanning a banned player
    @nextcord.slash_command(description="Unban a banned player", default_member_permissions=8)
    async def unban(self, ctx, *, member):

        ban_list = ctx.guild.bans()

        name, discriminator = member.split("#")

        async for bans in ban_list:

            user = bans.user

            if (user.name, user.discriminator) == (name, discriminator):

                await ctx.guild.unban(user)
                await ctx.send("This user has been unbanned from this server.")
                return
            
        await ctx.send("This user couldn't be found.")

    # Locking a channel

    @nextcord.slash_command(description="Lock the current channel", default_member_permissions=8)
    async def lock(self, ctx : nextcord.Interaction):

        
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("This channel has been locked.")
        
    # Unlocking a channel

    @nextcord.slash_command(description="Unlock the current channel", default_member_permissions=8)
    async def unlock(self, ctx):

        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("This channel has been unlocked.")



def setup(bot):
    bot.add_cog(moderationCmds(bot))
    print("moderationCmds-Cog has been loaded")