#!/usr/bin/python
from steam import WebAPI, SteamID
import pprint
try:
    from local import API_KEY, STEAM_USER, APP_ID  # used for API_KEY + friends, optional
except ImportError:
    API_KEY = ""              # https://steamcommunity.com/dev/apikey
    STEAM_USER = "xfesty"     # Steam username
    APP_ID = 377160           # Fallout 4

def get_steam_id(api: WebAPI, steam_user: str) -> int:
    return api.ISteamUser.ResolveVanityURL(vanityurl=steam_user, url_type=1)['response']['steamid']

def get_steam_user_dict(api: WebAPI, sid: int) -> dict:
    return api.ISteamUser.GetPlayerSummaries(steamids=str(sid))['response']['players'][0]

def get_user_games(api: WebAPI, sid: int) -> dict:
    return api.IPlayerService.GetOwnedGames(steamid=sid, include_played_free_games=1,
                                            include_appinfo=1, appids_filter=0)

def get_single_game(games_dict: dict, app_id: int) -> dict:
    try:
        for game in games_dict['response']['games']:
            if game['appid'] == app_id:
                return game
        else:
            return None
    except KeyError:
        return None

def get_game_playtime(game: dict) -> int:
    playtime_minutes = game['playtime_forever']
    return round(playtime_minutes / 60, 2)

def get_friend_list(api: WebAPI, sid: int) -> dict:
    return api.ISteamUser.GetFriendList(steamid=sid)['friendslist']['friends']

def get_game_user_info(api: WebAPI, appid: int, uid: int) -> dict:
    games = get_user_games(api, uid)
    single_game = get_single_game(games, appid)
    if single_game:
        steam_user = get_steam_user_dict(api, uid)
        return ([
            steam_user['personaname'],
            get_game_playtime(single_game)
        ])

if __name__ == "__main__":

    try:
        steam_api = WebAPI(key=API_KEY)
    except NameError:
        print("You don't have an API_KEY set! Exiting.")
        exit()

    steam_id = get_steam_id(steam_api, STEAM_USER)
    friends = get_friend_list(steam_api, steam_id)

    users_games_played = [[get_game_user_info(steam_api, APP_ID, steam_id)]]

    for friend in friends:
        result = get_game_user_info(steam_api, APP_ID, friend['steamid'])
        if result:
            users_games_played.append(result)

    pprint.pprint(users_games_played)









