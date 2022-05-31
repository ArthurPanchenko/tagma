import discord
from discord.ext import commands
from utils.config import *
from utils.functions import find_registration_channel
from db.functions import registration, is_nickname_freely



class UserRegistration(commands.Cog):

    users = {}

    def __init__(self, client):
        self.client = client

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     if payload.message_id == REGISTRATION_MESSAGE_ID:
    #         if find_registration_channel(payload.member):
    #             return
    #         i = 0
    #         for role_id in NEW_MEMBER_ROLES:
    #             role = payload.member.guild.get_role(role_id)
    #             if not role.members:
    #                 break
    #             i += 1
    #             if i == 15:
    #                 return await payload.member.send(
    #                     "Слишком много новых пользователей проходят регистрацию, "
    #                     "нажми на эмодзи еще раз через несколько секунд "
    #                 )
    #
    #         await payload.member.add_roles(role)
    #         text_channel = await self.client.fetch_channel(NEW_MEMBER_CHANNELS[i])
    #         user = await self.client.fetch_user(payload.user_id)
    #         embedVar = discord.Embed(title=f"Как тиммейты могут к тебе обращаться? ", color=0xff5c00)
    #         embedVar.add_field(name="```!name```", value="Данный ник будет виден всем пользователям", inline=True)
    #         embedVar.add_field(name="Пример", value="!name Raykirie", inline=False)
    #         embedVar.add_field(name="Эмодзи на твоих сообщениях:",
    #                            value="Эмодзи ❕ : Превышено количество символов в нике.\nЭмодзи ❗ : Имя уже занято.",
    #                            inline=False)
    #         await text_channel.send(user.mention + " РЕГИСТРАЦИЮ НУЖНО ПРОЙТИ ОДИН РАЗ, ПОЖАЛУЙСТА, ОТНЕСИСЬ К НЕЙ СЕРЬЕЗНО!")
    #         await text_channel.send(embed=embedVar)




    @commands.command()
    async def name(self, ctx, name):
        user = User()
        if is_nickname_freely(name):
            user.name = name
            user.discord_id = ctx.message.author.id
            self.users[str(user.discord_id)] = user
        else:
            print('same name error')
            return

    @commands.command()
    async def dota(self, ctx, dota):

        if self.users[f'{ctx.message.author.id}']:
            user = self.users[f'{ctx.message.author.id}']
            user.dota = dota
        else:
            return  # no user create error

    @commands.command()
    async def mmr(self, ctx, mmr):
        if self.users[f'{ctx.message.author.id}']:
            print('here')
            user = self.users[f'{ctx.message.author.id}']
            user.mmr = mmr
            if ctx.message.attachments:
                user.mmr_screen = ctx.message.attachments[0].url
            else:
                return  # no screen error
        else:
            return  # no user create error

    @commands.command()
    async def pos(self, ctx, pos):
        if self.users[f'{ctx.message.author.id}']:
            user = self.users[f'{ctx.message.author.id}']
            user.pos = pos
            registration(user)
            text_channel = await self.client.fetch_channel(967789966878986362)
            ds_user = self.client.fetch_user(ctx.message.author.id)
            ds_user.add_role(TAGMA_MEMBER_ROLE_ID)
            await text_channel.send(f'--------------------------------------')
            await text_channel.send(f'<@{ctx.author.id}>')
            await text_channel.send(user.mmr)
            await text_channel.send(user.mmr_screen)

    @commands.command()
    async def clear(self, ctx, amount=5):
        channel_id = ctx.message.content.split()[2]
        channel = await self.client.fetch_channel(channel_id)
        await channel.purge(limit=amount)

def setup(client):
    client.add_cog(UserRegistration(client))
