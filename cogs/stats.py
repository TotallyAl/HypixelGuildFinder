import discord
from discord.ext import commands
import requests
import time

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.API_KEY = "28c4f2e7-229e-418f-8fa8-490ab83fdda5"

    @commands.command()
    async def bedwars(self, ctx, user, mode=None):
        DATA = requests.get(f"https://api.hypixel.net/player?key={self.API_KEY}&name={user}").json()
        if mode == None:
            if DATA["success"] is True:
                bw_winstreak = DATA["player"]["stats"]["Bedwars"]["winstreak"]
                bw_coins = DATA["player"]["stats"]["Bedwars"]["coins"]
                bw_stars = DATA["player"]["achievements"]["bedwars_level"]
                bw_wins = DATA["player"]["stats"]["Bedwars"]["wins_bedwars"]
                bw_losses = DATA["player"]["stats"]["Bedwars"]["losses_bedwars"]
                bw_WLR = 0
                bw_kills = DATA["player"]["stats"]["Bedwars"]["kills_bedwars"]
                bw_deaths = DATA["player"]["stats"]["Bedwars"]["deaths_bedwars"]
                bw_KDR = 0
                bw_final_kills = 0
                bw_final_deaths = 0
                bw_FKDR = 0
                bw_bed_broken = 0
                bw_bed_lost = 0
                bw_BBLR = 0
                bw_finals_game = 0
                bw_beds_game = 0
                bw_total_games = 0
                OverallStats = discord.Embed(title="Overall Bedwars Stats", description=f"{user}", color=discord.Colour.blue())
                OverallStats.add_field(name="**Star:**", value=f"`{bw_stars}`", inline=True)
                OverallStats.add_field(name="**Coins:**", value=f"`{bw_coins}`", inline=True)
                OverallStats.add_field(name="**Winstreak:**", value=f"`{bw_winstreak}`", inline=True)
                OverallStats.add_field(name="**Wins:**", value=f"`{bw_wins}`", inline=True)
                OverallStats.add_field(name="**Losses:**", value=f"`{bw_losses}`", inline=True)
                OverallStats.add_field(name="**Deaths**", value=f"`{bw_deaths}`", inline=True)
                await ctx.send(embed=OverallStats)
            if DATA["success"] is False:
                ErrorStats = discord.Embed(title="Error", description="There was an error", color=discord.Colour.light_grey())
                ErrorStats.add_field(name="Error", value=DATA["cause"])
                await ctx.send(embed=ErrorStats)

        if mode == "1v1" or mode == "solo" or mode == "1":
            pass


def setup(client):
    client.add_cog(Stats(client))