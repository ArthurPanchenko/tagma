from discord import Embed
from discord.ext import commands
from utils.functions import embed_team

class Embeds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def embed_profile(self, ctx):
        embeds = list()
        embeds.append(
            Embed(
                title=f"Reply to the desired message with the new value", color=0xff5c00
            ).add_field(
                name="Emoji on your message",
                value=" ``` ❗ | Nickname already taken. \n ❌ | Invalid value.```",
                inline=False
            )
        )
        embeds.append(Embed(title="Position", color=0xff5c00))
        embeds.append(Embed(title="MMR", color=0xff5c00))
        embeds.append(Embed(title="Nickname", color=0xff5c00))
        embeds.append(Embed(title="Prime time & time zone", color=0xff5c00))
        text_channel = await self.client.fetch_channel(953759739903373393)
        for embed in embeds:
            await text_channel.send(embed=embed)

    @commands.command()
    async def embed_functions(self, ctx):
        embeds = list()
        embeds.append(Embed(title="-----------------------------"
                                  "\nLFT | Looking for team\n"
                                  "-----------------------------",
                            color=0xff5c00))
        embeds.append(Embed(title="-----------------------------"
                                  "\nLFP | Looking for player\n"
                                  "-----------------------------",
                            color=0xff5c00))
        embeds.append(Embed(title="-----------------------------"
                                  "\nLFS | Looking for scream\n"
                                  "-----------------------------",
                            color=0xff5c00))

        text_channel = await self.client.fetch_channel(ctx.message.channel.id)
        for embed in embeds:
            await text_channel.send(embed=embed)

    @commands.command()
    async def embed_registration(self, ctx):
        embeds = list()
        embeds.append(
            Embed(
                title="Reply to the message and write the value:"
            ).add_field(
                name="Emoji on your message",
                value="``` ❗ | Nickname already taken. \n "
                      "❌ | Invalid value. \n"
                      " 📋 | Add a screenshot to confirm the rating```",
                inline=False
            )
        )
        embeds.append(Embed(title="Nickname", color=0xff5c00))
        embeds.append(Embed(title="Dota accouts's ID", color=0xff5c00))
        embeds.append(Embed(title="MMR", color=0xff5c00))
        embeds.append(Embed(title="Position", color=0xff5c00))
        embeds.append(Embed(title="Prime time and time zone", color=0xff5c00))

        text_channel = await self.client.fetch_channel(ctx.message.channel.id)
        for embed in embeds:
            await text_channel.send(embed=embed)

    @commands.command()
    async def thelp(self, ctx):
        embed = embed_team()
        text_channel = await self.client.fetch_channel(ctx.message.channel.id)
        await text_channel.send(embed=embed)


def setup(client):
    client.add_cog(Embeds(client))
