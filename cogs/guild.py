import discord
from discord.ext import commands
import json
import pymongo
from pymongo import MongoClient
import requests

class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("apikey.cfg") as f:
            self.API_KEY = f.read()

        self.API_KEY = "28c4f2e7-229e-418f-8fa8-490ab83fdda5"

        with open("mongodb.cfg") as f:
            self.PASSWORD = f.read()

        self.database = MongoClient(f"mongodb+srv://TotallyFang:{self.PASSWORD}@cluster0.r57yi.mongodb.net/HAPIBOT?retryWrites=true&w=majority")
        self.HAPIBOT = self.database["HAPIBOT"]
        self.guild = self.HAPIBOT["Guilds"]
        self.account = self.HAPIBOT["linkedAccount"]

    @commands.group(name="guild", invoke_without_command=True)
    async def guild(self, ctx):
        await ctx.send("Please use the subcommand: addGuild, rmGuild, findGuild, reqGuild")
    
    @guild.command(name='oldRegisterGuild')
    async def oldRegisterGuild_subcommand(self, ctx):
        find = {"_id": ctx.author.id}
        account = self.account.find_one(find)
        UUID = account["Minecraft UUID"]
        GUILD = requests.get(f"https://api.hypixel.net/findGuild?key={self.API_KEY}&byUuid={account['Minecraft UUID']}").json()
        find_guild = requests.get(f"https://api.hypixel.net/guild?key={self.API_KEY}&id={GUILD['guild']}").json()
        user = find_guild["guild"]["members"]
        guild_name = find_guild["guild"]["name"]
        find = {"_id": f"{guild_name}"}
        output = self.guild.find_one(find)
        if output == None:
            #Make loop to find rank
            index = 0
            while index < len(user):
                rank = user[index]
                if rank["rank"] == "Guild Master" or rank["rank"] == "GUILDMASTER":
                    if UUID == rank["uuid"]:
                        guild = ctx.guild
                        role_name = find_guild["guild"]["name"]
                        await guild.create_role(name=f"{role_name}")
                        role = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
                        user = ctx.message.author
                        await user.add_roles(role)
                        await ctx.send(f"You have been given the role {role_name}")
                        path = {"_id": ctx.author.id}
                        add_guild_name_account = {
                            "$set": {
                                "guild": f"{guild_name}"
                            }
                        }
                        self.account.update_one(path, add_guild_name_account)
                        insert = {"_id": f"{guild_name}"}
                        self.guild.insert_one(insert)
                        return
                index += 1
        else:
            await ctx.send("Guild is already registered !")

    @guild.command(name='edit')
    async def edit_subcommand(self, ctx, setting=None, game=None, stat=None, value=None):
        find = {"_id": ctx.author.id}
        user = self.account.find_one(find)
        name = user['guild']
        if setting == "requirements":
            try:
                guild_requirements = self.guild.find_one({"_id": f"{name}"})
                guild_game = guild_requirements[f"{game}"]
                del guild_game[f"{stat}"]
                guild_game[f"{stat}"] = int(value)
                path = {
                    "_id": f"{name}"
                }
                update = {
                    "$set": {f"{game}": guild_game}
                }
                self.guild.update_one(path, update)
                await ctx.send(guild_game)

            except KeyError:
                await ctx.send("Did you use the command correctly ?")
                await ctx.send("Check the spelling of the gamemode/stat/value")
            
        if setting == "discordLink":
            try:
                path = {}
                discord_link = {}
                self.guilds.update_one(path, discord)
            except KeyError:
                await ctx.send("You are not using the command correctly !")

    @guild.command(name='find')
    async def find_subcommand(self, ctx, name):
        out = self.guilds.find_one({"_id": f"{name}"})
        await ctx.send(f"{name} Guild: ")
        await ctx.send(f"{out}")
    
    @guild.command(name='deleteGuild')
    async def deleteGuild_subcommand(self, ctx):
        find = {"_id": ctx.author.id}
        user = self.account.find_one(find)
        name = user['guild']
        guild_rm = {"guild_name": f"{name}"}
        self.guild.delete_one(guild_rm)
        await ctx.send(f"The guild: `{name}` has been deleted !")

    @guild.command(name='registerGuild')
    async def registerGuild_subcommand(self, ctx):
        try:
            #Variables to find the user's information(Registered)
            find = {"_id": ctx.author.id}
            account = self.account.find_one(find)
            UUID = account["Minecraft UUID"]
            #Variables for looking if the player is in a guild
            GUILD = requests.get(f"https://api.hypixel.net/findGuild?key={self.API_KEY}&byUuid={account['Minecraft UUID']}").json()
            if GUILD["guild"] == "null":
                await ctx.send("You are not in a guild.")
                return
            find_guild = requests.get(f"https://api.hypixel.net/guild?key={self.API_KEY}&id={GUILD['guild']}").json()
            try:
                user = find_guild["guild"]["members"]
                guild_name = find_guild["guild"]["name"]
            except KeyError:
                await ctx.send("API error: You have already looked up this name recently")
            #Variables to find if the guild is already registered
            find = {"_id": f"{guild_name}"}
            output = self.guild.find_one(find)
            #Looking if the guild is already registered in the database
            if output == None:
                #Make loop to find rank
                for rank in user:
                    #Checking if the user's rank is GUILD MASTER
                    if rank["rank"] == "Guild Master" or rank["rank"] == "GUILDMASTER":
                        if UUID == rank["uuid"]:
                            #Giving the user a rank
                            guild = ctx.guild
                            role_name = find_guild["guild"]["name"]
                            await guild.create_role(name=f"{role_name}")
                            role = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
                            user = ctx.message.author
                            await user.add_roles(role)
                            await ctx.send(f"You have been given the role {role_name}")
                            path = {"_id": ctx.author.id}
                            add_guild_name_account = {
                                "$set": {
                                    "guild": f"{guild_name}",
                                    "requirements": {

                                    }
                                }
                            }
                            self.account.update_one(path, add_guild_name_account)
                            insert = {"_id": f"{guild_name}"}
                            self.guild.insert_one(insert)
                            return
            else:
                await ctx.send("Your guild is already registered !")
        except KeyError:
            print("There was an error.")
    

def setup(client):
    client.add_cog(Guild(client))