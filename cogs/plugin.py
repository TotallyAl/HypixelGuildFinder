import discord
import os
import asyncio
from discord.ext import commands

class Plugin(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group('plugin', invoke_without_command=True)
    async def plugin(self, ctx):
        await ctx.send("Please use a keyword, 'load', 'unload', 'reload'")

    @plugin.command('load', invoke_without_command=True)
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f"The Cogs: `{extension}` was loaded succesfully")
            print(f"Plugin: '{extension}' was loaded succesfully")
        except:
            print(f"Plugin: '{extension}' doesn't exist...")

    @plugin.command('unload', invoke_without_command=True)
    async def unload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"The Cog: `{extension}` was unloaded succesfully")
            print(f"Unloaded: {extension}.py")
        except:
            print(f"Plugin: '{extension}' doesn't exist...")

    @plugin.command('reload', invoke_without_command=True)
    async def reload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await asyncio.sleep(1)
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"The Cog: `{extension}` was reloaded succesfuly")
            print(f"Reloaded: {extension}.py")
        except:
            print(f"Plugin: '{extension}' doesn't exist...")


def setup(client):
    client.add_cog(Plugin(client))