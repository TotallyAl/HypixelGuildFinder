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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = "Unlinked"
        add = get(member.guild.roles, name=role)
        await member.add_roles(add)

def setup(client):
    client.add_cog(Bot(client))