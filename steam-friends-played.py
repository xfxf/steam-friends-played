#!/usr/bin/python
from steamfriends import SteamFriends

import pprint
try:
    from local import API_KEY, STEAM_USER, APP_ID  # used for API_KEY + friends, optional
except ImportError:
    API_KEY = ""              # https://steamcommunity.com/dev/apikey
    STEAM_USER = "xfesty"     # Steam username
    APP_ID = 377160           # Fallout 4

if __name__ == "__main__":

    my_friends = SteamFriends(API_KEY)

    steam_id = my_friends.get_steam_id(STEAM_USER)
    friends = my_friends.get_friend_list(steam_id)
    users_games_played = [my_friends.get_game_user_info(APP_ID, steam_id)]

    for friend in friends:
        result = my_friends.get_game_user_info(APP_ID, friend['steamid'])
        if result:
            users_games_played.append(result)

    users_games_played_sorted = sorted(users_games_played, key=lambda k: (k['hours']))
    pprint.pprint(users_games_played_sorted)










