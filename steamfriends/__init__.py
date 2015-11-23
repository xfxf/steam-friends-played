#!/usr/bin/python
from steam import WebAPI
from logging import debug, basicConfig, DEBUG
from multiprocessing.dummy import Pool as ThreadPool
import sys
import itertools


class MySteamFriends(object):

    # concurrent Steam Web API requests to run
    api_pool = ThreadPool(6)

    def __init__(self, api_key: str, steam_username: str = None, steam_id: str = None, debugging: bool = False):
        """Initialises a connection to the Steam Web API and populates a list of friends.

        Args:
            api_key (str): API key from https://steamcommunity.com/dev/apikey
            steam_username (Optional[str]): steam username to base friends list from
            steam_id (Optional[str]): steam ID to base friends list from (alternative to steam_username)
            debugging (Optional[bool]): Enable debugging info.  Defaults to off.
        """

        if api_key is "":
            raise NameError("You don't have an api_key set!")
        if debugging is 1:
            basicConfig(stream=sys.stdout, level=DEBUG)

        self.steam_api = WebAPI(key=api_key)

        if steam_id is None and steam_username is None:
            raise NameError("You don't have a steam_username or steam_id set!")
        self.my_steam_id = steam_id
        if self.my_steam_id is None:
            self.my_steam_id = self.__get_my_steam_id(steam_username)

        self.friends_list = self.__get_my_friends_list()
        self.my_games_list = self.get_users_games(self.my_steam_id)

        debug("api_key: %s, steam_ide: %s, my_steam_id: %s" % (api_key, self.my_steam_id, self.my_steam_id))

    def __get_my_steam_id(self, steam_user: str) -> str:
        return self.steam_api.ISteamUser.ResolveVanityURL(vanityurl=steam_user, url_type=1)['response']['steamid']

    def __get_my_friends_list(self) -> dict:
        friends = self.steam_api.ISteamUser.GetFriendList(steamid=self.my_steam_id)['friendslist']['friends']
        friends_list = [f['steamid'] for f in friends]
        friends_list.append(self.my_steam_id)
        #friends_list = __populate_my_friends_list()
        return friends_list

    def __populate_my_friends_list(self):
        friends_list_detailed = self.api_pool.map(self.get_steam_user_dict, self.friends_list)
        return friends_list_detailed

    def get_game_name(self, appid: str) -> str:
        return [game['name'] for game in self.my_games_list if game['appid'] == appid][0]

    def get_steam_user(self, sid: str) -> dict:
        return self.steam_api.ISteamUser.GetPlayerSummaries(steamids=str(sid))['response']['players'][0]

    def get_steam_user_dict(self, sid: str) -> dict:
        result = self.get_steam_user(sid)
        if result:
            return {sid: result}

    def get_users_games(self, sid: str) -> dict:
        result = self.steam_api.IPlayerService.GetOwnedGames(steamid=sid, include_played_free_games=1,
                                                           include_appinfo=1, appids_filter=0)['response']
        if result:
            debug(result)
            return result['games']

    def get_game_user_info(self, uid: str, appid: int) -> dict:
        games = self.get_users_games(uid)
        if games:
            return [game for game in games if game['appid'] == appid]

    def _get_game_user_info_dict(self, uid: str, appid: int) -> dict:
        gameinfo = self.get_game_user_info(uid, appid)
        if gameinfo:
            return {uid: gameinfo}

    def get_everyones_gamestats(self, appid: str) -> dict:
        # steam API is slow; use multiprocessing to submit concurrent HTTPS requests about each friend
        results = self.api_pool.starmap(self._get_game_user_info_dict, zip(self.friends_list, itertools.repeat(appid)))

        # transform result (list) into a dict only containing actual results, where key is sid
        result_dict = {}
        for result in list(filter(None.__ne__, results)):
            for key, value in result.items():
                result_dict[key] = value[0]

        return result_dict

    def sort_playtimes(self, gamestats: dict) -> list:
        game_playtime = [self.get_game_playtime(sid, data) for sid, data in gamestats.items()]
        return sorted(game_playtime, key=lambda k: (k['hours']))

    def get_game_playtime(self, sid: str, data: dict) -> dict:
        playtime_hours = round(data['playtime_forever'] / 60, 2)
        return ({
            "steam_user": self.get_steam_user(sid)['personaname'], #self.friends_list[sid]['personaname'],
            "hours": playtime_hours
        })
