from db.connect import db
from db.models import Player, Team


def check_int(value):
    try:
        if int(value) > 0:
            return 200
    except ValueError:
        return 400


def is_nickname_freely(nickname):
    with db:
        query = Player.select()
    if nickname in [user.nickname for user in query]:
        return False
    return True


def is_team_title_freely(title):
    with db:
        query = Team.select()
    if title in [team.title for team in query]:
        return False
    return True


def is_player_in_team(user_id, team):
    user = get_user(user_id)
    if user in team.player_set:
        return True
    return False


def get_team_by_user(user_id):
    with db:
        user = get_user(user_id)
        return Team.get(Team.id == user.team)


def get_team_by_text_channel(text_channel_id):
    with db:
        team = Team.get(Team.text_channel == text_channel_id)
        return team


def get_user(user_id):
    with db:
        user = Player.get(Player.discord == user_id)
    return user


def create_team(user, text_channel, voice_channel, color='#fff'):
    with db:
        team = Team.insert(
            title=f"{user.nick}'s team",
            color=color,
            text_channel=text_channel,
            voice_channel=voice_channel
        ).execute()
        user_db = get_user(user.id)
        user_db.team = team
        user_db.save()


def registration(user):
    with db:
        Player.insert(
            nickname=user.nickname,
            discord=user.discord_id,
            dota_id=user.dota,
            mmr=user.mmr,
            role=user.pos,
            about=user.about,
            steam_id=user.steam
        ).execute()


def change_name(user_id, nickname):
    if is_nickname_freely(nickname):
        with db:
            user = get_user(user_id)
            user.nickname = nickname
            user.save()
        return 200
    else:
        return 100


def change_pos(user_id, pos):
    if check_int(pos) == 200:
        with db:
            user = get_user(user_id)
            user.role = int(pos)
            user.save()
        return 200
    else:
        return 400


def change_mmr(user_id, mmr):
    if check_int(mmr) == 200:
        with db:
            user = get_user(user_id)
            user.mmr = int(mmr)
            user.save()
        return 200
    else:
        return 400


def change_about(user_id, about):
    with db:
        user = get_user(user_id)
        user.about = about
        user.save()
        return 200


def change_team_name(team, title):
    if is_team_title_freely(title):
        with db:
            team.title = title
            team.save()
        return 200
    else:
        return 100
