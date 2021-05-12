import discord
from discord.ext import commands
import datetime

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def success(self, ctx):
        verifySuccess = discord.Embed(title='The account verification was successful', description='The discord account: **Harfang#4149** was linked to the Minecraft account: **Harfang**.', color=discord.Colour.from_rgb(0, 255, 122))
        verifySuccess.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/1779_check.png")
        verifySuccess.set_footer(text='•Hypixel Guild Finder | made by Harfang#4149', icon_url='https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516')
        await ctx.send(embed=verifySuccess)

    @commands.command()
    async def error(self, ctx):
        verifyError = discord.Embed(title='The account verification was not possible', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description='Are you using the command correctly ? Are you using all of the arguments ?\nClick on the title for help.', color=discord.Colour.from_rgb(70, 67, 61))
        verifyError.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/5053_Gears.png")
        verifyError.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url="https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516")
        await ctx.send(embed=verifyError)

    @commands.command()
    async def api(self, ctx):
        verifyErrorAPI = discord.Embed(title='The account verification was not possible', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description=f'API error: \n - API cooldown \n Click on the title for help.', color=discord.Colour.from_rgb(70, 67, 61))
        verifyErrorAPI.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/5053_Gears.png")
        verifyErrorAPI.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url="https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516")
        await ctx.send(embed=verifyErrorAPI)

    @commands.command()
    async def unsuccessful(self, ctx):
        verifyUnsuccessful = discord.Embed(title='The account verification was unsuccessful', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description='There was an error while attempting to link your account.\nClick on the title to find the possible errors.', color=discord.Colour.from_rgb(255, 0, 0))
        verifyUnsuccessful.set_author(name="Account Verification", icon_url='https://emoji.gg/assets/emoji/1326_cross.png')
        verifyUnsuccessful.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url='https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516')
        await ctx.send(embed=verifyUnsuccessful)


def setup(client):
    client.add_cog(Embed(client))