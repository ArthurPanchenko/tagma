import requests

from discord import Embed
from bs4 import BeautifulSoup
from db.functions import change_name, change_pos, change_mmr, change_about
from utils.classes import User


def parse(id):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.2.201 Yowser/2.5 Safari/537.36',
        'accept': '*/*'
    }
    url = "https://steamid.xyz/"+str(id)
    html = requests.get(url, headers=HEADERS, params=None)
    if html.status_code == 200:
        html = html.text
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('div', id="guide")
        a = item.find('em').find_next("input").find_next("input").find_next("input").find_next("input").get('value')
        return a
    else:
        return 400


def change_profile(user_id, value, func_id, funcs=(change_pos, change_mmr, change_name, change_about)):
    return funcs[func_id](user_id, value)


def find_registration_channel(user):
    for role in user.roles:
        if role.name.startswith('new'):
            return True


def get_or_create(user_id, users: dict):
    if user_id not in list(users.keys()):
        users[user_id] = User()
    return users[user_id]


async def send_to_verification_channel(verification_channel, user):
    await verification_channel.send(f'--------------------------------------')
    await verification_channel.send(f'<@{user.nickname}>')
    await verification_channel.send(user.mmr)
    await verification_channel.send(user.mmr_screen)


def registration_over_embed(user):
    embed = Embed(
        title='Welcome to the Tagma Project!'
    ).add_field(
        name="Click on your server profile to find out your Tagma profile:",
        value=f"{user.mention}"
    )
    return embed


def embed_lft(ctx, user):
    embed = Embed(
        title="",
        description=ctx.author.mention + "\n\n",
        color=0x0001a
    ).add_field(
        name=f"{user.about}"
             "\n--------------------------------------------------------------------------------------------",
        value=f"```\t\t\tMMR — {user.mmr} \t\t\t POS — {user.role}```", inline=False
    ).set_footer(text=ctx.content)
    return embed


def embed_lfp(team):
    embed = Embed(color=0x0001a)
    embed.set_author(name=f"{team.title}"
                          "\n------------------------------------------------------"
                          "--------------------------------------")
    for i, player in enumerate(team.player_set):
        embed.add_field(name=f"Player {i + 1}",
                        value=f"<@{player.discord}>```\t\t\tMMR — {player.mmr} \t\t\t POS — {player.role}```",
                        inline=False)
    return embed


def embed_team():
    embeds = list()

    embeds.append(Embed(
        title=f"Функции для игроков в лобби", color=0xff5c00
    )
        .add_field(name="!thelp", value="Help function", inline=True)
        .add_field(name="!tmanager", value="Change the team's manager ", inline=True)
        .add_field(name="!tcoach", value="Change the team's coach ", inline=True)
        .add_field(name="!tsubstitute", value="Change the team's substitute ", inline=True)
        .add_field(name="!tceo", value="Change the team's CEO ", inline=True)
        .add_field(name="!kick", value="Kick player from the team", inline=True)
    )
    embeds.append(
        Embed(title='New team commands', color=0xff5c00)
        .add_field(name="!tname", value="Change the team's name ", inline=True)
        .add_field(name="!tcolour", value="Change the team's colour ", inline=True)
    )
    return embeds
