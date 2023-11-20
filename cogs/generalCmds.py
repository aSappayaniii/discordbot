import nextcord
import requests, json
from datetime import datetime, timezone
from nextcord.ext import commands

helpGuide = json.load(open("./json_files/help.json"))

def createHelpEmbed(pageNum=0, inline=False):
    pageNum = pageNum % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]

    embed = nextcord.Embed(
            color=0x0080ff, 
            title=list(helpGuide)[pageNum]
        )
    
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name="/" + key, value = val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpGuide))}")
    return embed

class generalCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Showcases all of Panda's commands

    @nextcord.slash_command(description="Shows all of Panda's commands!")
    async def help(self, ctx):
        currentPage = 0

        async def next_callback(interaction):
            nonlocal currentPage, sent_msg
            currentPage += 1
            await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

        async def previous_callback(interaction):
            nonlocal currentPage, sent_msg
            currentPage -= 1
            await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

        nextButton = nextcord.ui.Button(label=">", style=nextcord.ButtonStyle.blurple)
        nextButton.callback = next_callback

        previousButton = nextcord.ui.Button(label="<", style=nextcord.ButtonStyle.blurple)
        previousButton.callback = previous_callback

        myview = nextcord.ui.View(timeout=180)
        myview.add_item(previousButton)
        myview.add_item(nextButton)

        sent_msg = await ctx.send(embed=createHelpEmbed(), view=myview)

    #Information about the bot

    @nextcord.slash_command(description="Gives you information about Panda")  #Replace Panda with your own bot's name
    async def about(self, ctx):
        await ctx.send("I went to Mexico and sat on a cactus.")

    #Bot's Current Latency

    @nextcord.slash_command(description = "Shows the current latency of Panda") #Replace Panda with your own bot's name
    async def ping(self, ctx):
        latency = self.bot.latency * 1000

        embed = nextcord.Embed(
            title="Ping",
            description=f'My current ping is {latency: .2f}ms 😜',
            color=nextcord.Color.orange()
        )

        await ctx.send(embed=embed)

    #Random Dog Image Generator

    @nextcord.slash_command(description="A random image of a dog")
    async def dog(self, ctx):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        image_link = response.json()["message"]
        await ctx.send(image_link)

    #Random Cat Image Generator

    @nextcord.slash_command(description="A random image of a cat")
    async def cat(self, ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        image_link = response.json()[0]["url"]
        await ctx.send(image_link)


    #User Info Command
    @nextcord.slash_command(description = "Shows info about a server member")
    async def userinfo(self, ctx : nextcord.Interaction, member : nextcord.Member):
        member = member 
        join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.now(timezone.utc)
        time_on_server = current_time - member.joined_at
        time_on_sever_minutes = divmod(time_on_server.total_seconds(), 60)
        hours, minutes = divmod(time_on_sever_minutes[0], 60)

        embed = nextcord.Embed(
            title="User Information",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name="Name", value=member.name, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Joined Server", value=join_date, inline=False)
        embed.add_field(name="Time on Server", value=f'{int(hours)} hours, {int(minutes)} minutes', inline=False)
 
        await ctx.send(embed=embed)

    #Server Info Command
    @nextcord.slash_command(description="Shows info about the server")
    async def serverinfo(self, ctx):
        server_created_at = ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
        member_count = ctx.guild.member_count
        uptime = datetime.now(timezone.utc) - self.bot.user.created_at
        uptime_hours = uptime.seconds // 3600
        uptime_minutes = (uptime.seconds % 3600) // 60

        embed = nextcord.Embed(
            title="Server Information",
            color = nextcord.Color.blue()
        )

        embed.add_field(name="Server Created At:", value=server_created_at, inline=False)
        embed.add_field(name="Member Count:", value=member_count, inline=False)
        embed.add_field(name="Uptime:", value=f'{uptime_hours} hours, {uptime_minutes} minutes', inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(generalCmds(bot))
    print("generalCmds-Cog has been loaded")