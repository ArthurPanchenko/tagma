from discord.ext import commands
from db.functions import get_team_by_user, change_team_name, get_team_by_text_channel, is_player_in_team
from utils.config import *

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tname(self, message):
        team = get_team_by_user(message.author.id)
        title = ' '.join([str(i) for i in message.message.content.split()[1:]])
        if change_team_name(team, title) == 200:
            await message.message.add_reaction("✅")
        else:
            await message.message.add_reaction("❌")
        team_text_channel = self.client.get_channel(int(team.text_channel))
        team_voice_channel = self.client.get_channel(int(team.voice_channel))

        await team_text_channel.edit(name=title)
        await team_voice_channel.edit(name=title)
        await message.message.delete(delay=3)

    @commands.command()
    async def tmanager(self, message):
        team = get_team_by_text_channel(message.channel.id)
        if is_player_in_team(message.author.id, team):
            mention_user = message.message.mentions[0]
            guild = self.client.get_guild(TAGMA_ID)
            role = guild.get_role(MANAGER_ROLE_ID)
            await mention_user.add_roles(role)
            await message.message.delete(delay=3)

    @commands.command()
    async def tcoach(self, message):
        team = get_team_by_text_channel(message.channel.id)
        if is_player_in_team(message.author.id, team):
            mention_user = message.message.mentions[0]
            guild = self.client.get_guild(TAGMA_ID)
            role = guild.get_role(COACH_ROLE_ID)
            await mention_user.add_roles(role)
            await message.message.delete(delay=3)

    @commands.command()
    async def tceo(self, message):
        team = get_team_by_text_channel(message.channel.id)
        if is_player_in_team(message.author.id, team):
            mention_user = message.message.mentions[0]
            guild = self.client.get_guild(TAGMA_ID)
            role = guild.get_role(CEO_ROLE_ID)
            await mention_user.add_roles(role)
            await message.message.delete(delay=3)


def setup(client):
    client.add_cog(Commands(client))