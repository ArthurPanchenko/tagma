import discord
import os
from discord.ext import commands

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)


for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run("OTU5Nzk2Njc2MTE2MjM4MzY2.YkhGTw.yN0qAV6owtvhxOhl4r-7_TDkNLg")

# rega -> profile ->
