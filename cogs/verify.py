import discord
from discord.ext import commands
from discord.utils import get
import requests
import pymongo
from pymongo import MongoClient

class Verify(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.API_KEY = '28c4f2e7-229e-418f-8fa8-490ab83fdda5'

        with open("mongodb.cfg") as f:
            self.PASSWORD = f.read()

        self.database = MongoClient(f"mongodb+srv://TotallyFang:{self.PASSWORD}@cluster0.r57yi.mongodb.net/HAPIBOT?retryWrites=true&w=majority")
        self.HAPIBOT = self.database["HAPIBOT"]
        self.account = self.HAPIBOT["linkedAccount"]
        self.guild = self.HAPIBOT["Guilds"]
    
    @commands.command()
    @commands.has_role("Unlinked")
    async def verify(self, ctx, username):
        try:
            user = ctx.author
            addRole = "Linked"
            addRm = "Unlinked"
            MC = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
            UUID = MC["id"]
            DATA = requests.get(f"https://api.hypixel.net/player?key={self.API_KEY}&name={username}").json()
            if not DATA["success"]:
                await ctx.send(f"API error: {DATA['cause']}")
                return
            discord_tag = DATA["player"]["socialMedia"]["links"]["DISCORD"]
            if str(discord_tag) == str(user):
                role_add = get(user.guild.roles, name=addRole)
                await user.add_roles(role_add)
                link = {
                    "_id": ctx.author.id,
                    "Minecraft Username": f"{username}",
                    "Minecraft UUID": UUID
                }
                self.account.insert_one(link)
                await ctx.send("Your account has been linked")
                role_rm = get(user.guild.roles, name=addRm)
                await user.remove_roles(role_rm)
        except:
            find = {
                "_id": ctx.author.id
            }

            out = self.account.find_one(find)
            
            if out["_id"] == ctx.author.id:
                await ctx.send("You account has already been linked...")

    @commands.command()
    @commands.has_role("Linked")
    async def unverify(self, ctx):
        user = ctx.author
        add_role = "Unlinked"
        rm_role = "Linked"
        delete_account = {"_id": ctx.author.id}
        find = {"_id": ctx.author.id}
        minecraft_account_name = self.account.find_one(find)
        self.account.delete_one(delete_account)
        ADD = get(user.guild.roles, name=add_role)
        RM = get(user.guild.roles, name=rm_role)
        delete_guild = {"guild_master": f"{minecraft_account_name['Minecraft Username']}"}
        self.guild.delete_one(delete_guild)
        await user.add_roles(ADD)
        await user.remove_roles(RM)
        await ctx.send("Your account has been unlinked !")
        await ctx.send("All of your files were deleted !")
        

def setup(client):
    client.add_cog(Verify(client))