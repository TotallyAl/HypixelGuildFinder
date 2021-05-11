import discord
from discord.ext import commands

class Function(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def hidden_command(self, ctx, name):
        await ctx.send(f"Hello {name}")

    @commands.command()
    async def test(self, ctx, name):
        await self.hidden_command(ctx, name)

def setup(client):
    client.add_cog(Function(client))