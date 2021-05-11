#!/usr/bin/env python
import os
import discord
from discord.ext import commands
import json
import asyncio
from discord import guild

# read the token from token.cfg
with open('token.cfg') as token_file:
    TOKEN = token_file.read()

# All user commands have to start with >
client = commands.Bot(command_prefix='!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded file: {filename}")

client.run(TOKEN)