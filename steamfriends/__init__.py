#!/usr/bin/python
from steam import WebAPI, SteamID

class SteamFriends(object):

    def __init__(self, api_key):
        if api_key is "":
            raise NameError("You don't have an API_KEY set!")
        self.steam_api = WebAPI(key=api_key)

    def get_steam_id(self, steam_user: str) -> int:
        return self.steam_api.ISteamUser.ResolveVanityURL(vanityurl=steam_user, url_type=1)['response']['steamid']

    def get_steam_user(self, sid: int) -> dict:
        return self.steam_api.ISteamUser.GetPlayerSummaries(steamids=str(sid))['response']['players'][0]

    def get_user_games(self, sid: int) -> dict:
        return self.steam_api.IPlayerService.GetOwnedGames(steamid=sid, include_played_free_games=1,
                                                           include_appinfo=1, appids_filter=0)

    def get_friend_list(self, sid: int) -> list:
        return self.steam_api.ISteamUser.GetFriendList(steamid=sid)['friendslist']['friends']

    def get_game_user_info(self, appid: int, uid: int) -> dict:
        games = self.get_user_games(uid)
        single_game = self.get_single_game(games, appid)
        if single_game:
            steam_user = self.get_steam_user(uid)
            return ({
                "name": steam_user['personaname'],
                "hours": self.get_game_playtime(single_game)
            })

    @staticmethod
    def get_single_game(games_dict: dict, app_id: int) -> dict:
        try:
            for game in games_dict['response']['games']:
                if game['appid'] == app_id:
                    return game
            else:
                return None
        except KeyError:
            return None

    @staticmethod
    def get_game_playtime(game: dict) -> int:
        playtime_minutes = game['playtime_forever']
        return round(playtime_minutes / 60, 2)

