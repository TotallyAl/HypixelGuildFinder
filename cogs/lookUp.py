import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import requests

class LookUp(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("apikey.cfg") as f:
            self.API_KEY = f.read()

        with open("mongodb.cfg") as f:
            self.PASSWORD = f.read()

        self.database = MongoClient(f"mongodb+srv://TotallyFang:{self.PASSWORD}@cluster0.r57yi.mongodb.net/HAPIBOT?retryWrites=true&w=majority")
        self.HAPIBOT = self.database["HAPIBOT"]
        self.guild = self.HAPIBOT["Guilds"]
        self.account = self.HAPIBOT["linkedAccount"]

    @commands.command()
    @commands.has_role("Linked")
    async def lookUpGuild(self, ctx):
        find = {"_id": ctx.author.id}
        user = self.account.find_one(find)
        USERNAME = user["Minecraft Username"]
        DATA = requests.get(f"https://api.hypixel.net/player?key={self.API_KEY}&name={USERNAME}").json()


def setup(client):
    client.add_cog(LookUp(client))