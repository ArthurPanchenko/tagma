from discord.ext import commands
from utils.config import *
from db.functions import registration, check_int, is_nickname_freely, get_user, create_team, get_team_by_user
from utils.functions import find_registration_channel, \
                            change_profile, \
                            get_or_create, \
                            send_to_verification_channel, \
                            parse, \
                            registration_over_embed, \
                            embed_lft, \
                            embed_team, \
                            embed_lfp


class Events(commands.Cog):

    users = {}

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.client.get_guild(TAGMA_ID)
        tagma_role = guild.get_role(TAGMA_MEMBER_ROLE_ID)
        if tagma_role not in before.roles and tagma_role in after.roles:
            channel = self.client.get_channel(WELCOME_CHANNEL)
            await channel.send(embed=registration_over_embed(before))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == REGISTRATION_MESSAGE_ID:
            if find_registration_channel(payload.member):
                return
            i = 0
            for role_id in NEW_MEMBER_ROLES:
                role = payload.member.guild.get_role(role_id)
                if not role.members:
                    break
                i += 1
                if i == 15:
                    return await payload.member.send(
                        "Слишком много новых пользователей проходят регистрацию, "
                        "нажми на эмодзи еще раз через несколько секунд "
                    )

            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == PROFILE_CHANNEL_ID:
            if message.reference:
                if message.reference.message_id == 977124853758971904:
                    code = change_profile(message.author.id, message.content, 0)
                    if code == 200:
                        await message.message.add_reaction("✅")
                    elif code == 400:
                        await message.add_reaction("❌")

                if message.reference.message_id == 977124854866264064:
                    code = change_profile(message.author.id, message.content, 1)
                    if code == 200:
                        await message.add_reaction("✅")
                    elif code == 400:
                        await message.add_reaction("❌")

                if message.reference.message_id == 977124855470239765:
                    code = change_profile(message.author.id, message.content, 2)
                    if code == 200:
                        await message.add_reaction("✅")
                    elif code == 100:
                        await message.add_reaction("❗")
                if message.reference.message_id == 977124856577552446:
                    code = change_profile(message.author.id, message.content, 3)
                    if code == 200:
                        await message.add_reaction("✅")
                    elif code == 100:
                        await message.add_reaction("❗")
            else:
                await message.add_reaction("❌")
                await message.delete(delay=1)
            await message.delete(delay=3)
        if message.channel.id in REGISTRATION_CHANNELS_ID:
            if message.reference:
                user = get_or_create(message.author.id, self.users)
                channel = self.client.get_channel(message.reference.channel_id)
                embed_message = await channel.fetch_message(message.reference.message_id)

                if message.reference.message_id == 973874908658552843:
                    if len(message.content) > 15:
                        await message.add_reaction("❌")
                    elif not is_nickname_freely(message.content):
                        await message.add_reaction("❗")
                    else:
                        user.nickname = message.content
                        user.discord_id = message.author.id
                        await embed_message.add_reaction("✅")
                        await message.author.edit(nick=user.nickname)
                elif message.reference.message_id == 973874909530980354:
                    if check_int(message.content) == 200:
                        user.dota = message.content
                        steam_parse = parse(int(user.dota))
                        if steam_parse != 400:
                            user.steam = steam_parse
                            await embed_message.add_reaction("✅")
                            return await message.delete(delay=2)
                    await message.add_reaction("❌")
                elif message.reference.message_id == 973874910852165642:
                    if check_int(message.content) == 200:
                        if message.attachments:
                            user.mmr_screen = message.attachments[0].url
                            user.mmr = message.content

                            await embed_message.add_reaction("✅")
                        else:
                            await message.add_reaction("📋")
                    else:
                        await message.add_reaction("❌")
                elif message.reference.message_id == 973874911888179230:
                    if check_int(message.content) == 200 and len(message.content) == 1:
                        user.pos = message.content
                        await embed_message.add_reaction("✅")
                    else:
                        await message.add_reaction("❌")
                elif message.reference.message_id == 973874929219026975:
                    user.about = message.content
                    await embed_message.add_reaction("✅")
                if hasattr(user, 'nickname') and \
                    hasattr(user, 'discord_id') and \
                    hasattr(user, 'dota') and \
                    hasattr(user, 'mmr') and \
                    hasattr(user, 'pos') and \
                    hasattr(user, 'steam') and \
                        hasattr(user, 'about'):
                    registration(user)

                    verification_channel = self.client.get_channel(VERIFICATION_CHANNEL)
                    await send_to_verification_channel(verification_channel, user)

                    role = message.guild.get_role(TAGMA_MEMBER_ROLE_ID)
                    member = message.guild.get_member(user.discord_id)
                    await member.add_roles(role)
                    await member.remove_roles([role for role in member.roles if role.name.startswith('new')][0])

                    del self.users[message.author.id]
                    async for channel_message in channel.history(limit=50):
                        await channel_message.clear_reactions()
            else:
                await message.add_reaction("❌")
                await message.delete(delay=1)
            await message.delete(delay=2)
        if message.channel.id == FUNCTION_CHANNEL_ID:
            if message.reference:
                if message.reference.message_id == 976526539019657266:
                    user_db = get_user(message.author.id)
                    embed = embed_lft(message, user_db)
                    text_channel = self.client.get_channel(LFT_CHANNEL_ID)
                    await text_channel.send(embed=embed)
                if message.reference.message_id == 976526540043079762:
                    team = get_team_by_user(message.author.id)
                    text_channel = self.client.get_channel(LFP_CHANNEL_ID)
                    embed = embed_lfp(team)
                    await text_channel.send(message.content, embed=embed)
            else:
                await message.add_reaction("❌")
                await message.delete(delay=1)
            await message.delete(delay=3)
        if message.channel.id == INVITE_CHANNEL_ID:
            team = get_team_by_user(message.author.id)
            invited_users = message.mentions
            for invited_user in invited_users:
                await invited_user.send(f'{team.title}')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel.id == CREATE_TEAM_CHANNEL_ID:
            if after.channel:
                if before.channel != after.channel:
                    if after.channel.category_id == TEAMS_CATEGORY_ID:
                        guild = self.client.get_guild(TAGMA_ID)
                        voice_channel = await guild.create_voice_channel(
                            name=f"{member.nick}'s team",
                            category=self.client.get_channel(TEAMS_CATEGORY_ID)
                        )
                        text_channel = await guild.create_text_channel(
                            name=f"{member.nick}'s team",
                            category=self.client.get_channel(TEAMS_CATEGORY_ID)
                        )

                        await voice_channel.set_permissions(guild.default_role, connect=False)
                        await voice_channel.set_permissions(guild.get_role(TAGMA_MEMBER_ROLE_ID), connect=False)

                        await text_channel.set_permissions(guild.default_role,  view_channel=False)
                        await text_channel.set_permissions(guild.get_role(TAGMA_MEMBER_ROLE_ID),  view_channel=False)

                        await voice_channel.set_permissions(member, connect=True)
                        await text_channel.set_permissions(member, view_channel=True)
                        for embed in embed_team():
                            await text_channel.send(embed=embed)
                        await member.move_to(voice_channel)
                        create_team(member, text_channel.id, voice_channel.id)


def setup(client):
    client.add_cog(Events(client))
