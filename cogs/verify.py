import discord
from discord.ext import commands
from discord.utils import get
import requests
import pymongo
from pymongo import MongoClient

class Verify(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("apikey.cfg") as f:
            self.API_KEY = f.read()

        with open("mongodb.cfg") as f:
            self.PASSWORD = f.read()

        self.database = MongoClient(f"mongodb+srv://TotallyFang:{self.PASSWORD}@cluster0.r57yi.mongodb.net/HAPIBOT?retryWrites=true&w=majority")
        self.HAPIBOT = self.database["HAPIBOT"]
        self.account = self.HAPIBOT["linkedAccount"]
        self.guild = self.HAPIBOT["Guilds"]
    
    @commands.command()
    async def verify(self, ctx, username=None):
        if username == None:
            verifyError = discord.Embed(title='The account verification was not possible', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description='Are you using the command correctly ? Are you using all of the arguments ?\nClick on the title for help.', color=discord.Colour.from_rgb(70, 67, 61))
            verifyError.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/5053_Gears.png")
            verifyError.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url="https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516")
            await ctx.send(embed=verifyError)
        else:
            try:
                user = ctx.author
                addRole = "Linked"
                addRm = "Unlinked"
                MC = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
                UUID = MC["id"]
                DATA = requests.get(f"https://api.hypixel.net/player?key={self.API_KEY}&name={username}").json()
                if not DATA["success"]:
                    verifyErrorAPI = discord.Embed(title='The account verification was not possible', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description=f'API error: \n - API cooldown \n Click on the title for help.', color=discord.Colour.from_rgb(70, 67, 61))
                    verifyErrorAPI.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/5053_Gears.png")
                    verifyErrorAPI.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url="https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516")
                    await ctx.send(embed=verifyErrorAPI)
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
                    verifySuccess = discord.Embed(title='The account verification was successful', description=f'The discord account: **{discord_tag}** was linked to the Minecraft account: **{username}**.', color=discord.Colour.from_rgb(0, 255, 122))
                    verifySuccess.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/1779_check.png")
                    verifySuccess.set_footer(text='•Hypixel Guild Finder | made by Harfang#4149', icon_url='https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516')
                    await ctx.send(embed=verifySuccess)
                    role_rm = get(user.guild.roles, name=addRm)
                    await user.remove_roles(role_rm)
                else:
                    verifyUnsuccessful = discord.Embed(title='The account verification was unsuccessful', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description='There was an error while attempting to link your account.\nClick on the title to find the possible errors.', color=discord.Colour.from_rgb(255, 0, 0))
                    verifyUnsuccessful.set_author(name="Account Verification", icon_url='https://emoji.gg/assets/emoji/1326_cross.png')
                    verifyUnsuccessful.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url='https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516')
                    await ctx.send(embed=verifyUnsuccessful)
            except:
                find = {
                    "_id": ctx.author.id
                }

                out = self.account.find_one(find)

                if out == None:
                    pass
                else:
                    if out["_id"] == ctx.author.id:
                        verifyError = discord.Embed(title='The account verification was not possible', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description='Are you using the command correctly ? Are you using all of the arguments ?\nClick on the title for help.', color=discord.Colour.from_rgb(70, 67, 61))
                        verifyError.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/5053_Gears.png")
                        verifyError.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url="https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516")
                        await ctx.send(embed=verifyError)

    @commands.command()
    async def unverify(self, ctx, confirm=None):
        if confirm != "confirm":
            await ctx.send("Please use the correct password !")
        else:
            try:
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
                verifySuccess = discord.Embed(title='The account unverification was successful', description='Your account was deleted. \n All of your files(Personnal database and Guild database) has been successfully deleted.', color=discord.Colour.from_rgb(0, 255, 122))
                verifySuccess.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/1779_check.png")
                verifySuccess.set_footer(text='•Hypixel Guild Finder | made by Harfang#4149', icon_url='https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516')
                await ctx.send(embed=verifySuccess)
            except:
                verifyError = discord.Embed(title='The account unverification was not possible', url='https://github.com/TotallyAl/HypixelGuildFinder/blob/main/README.md', description='You do not have an account to delete.', color=discord.Colour.from_rgb(70, 67, 61))
                verifyError.set_author(name='Account Verification', icon_url="https://emoji.gg/assets/emoji/5053_Gears.png")
                verifyError.set_footer(text="•Hypixel Guild Finder | made by Harfang#4149", icon_url="https://vignette.wikia.nocookie.net/youtube/images/9/90/Hypixel.jpg/revision/latest?cb=20180708014516")
                await ctx.send(embed=verifyError)
            

def setup(client):
    client.add_cog(Verify(client))