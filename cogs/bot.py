import discord
from discord.ext import commands
from discord.utils import get

class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))
        print(f"{self.client.user} successfully started.")

def setup(client):
    client.add_cog(Bot(client))