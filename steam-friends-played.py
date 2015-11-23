#!/usr/bin/python
from steamfriends import MySteamFriends

from pprint import pprint
try:
    from local import API_KEY, STEAM_USER, APP_ID, DEBUG  # used for API_KEY + friends, optional
except ImportError:
    API_KEY = ""              # from https://steamcommunity.com/dev/apikey
    STEAM_USER = "xfesty"     # Steam username
    APP_ID = 377160           # Fallout 4
    DEBUG = False             # Enable debugging, False or True

if __name__ == "__main__":
    print("Connecting to Steam API server and populating friends...")
    me = MySteamFriends(
        api_key=API_KEY,
        steam_username=STEAM_USER,
        #steam_id=STEAM_ID,
        debugging=DEBUG)
    print("Connected, collecting friends in-game time for %s..." % (me.get_game_name(APP_ID)))
    game_stats = me.get_everyones_gamestats(APP_ID)
    print("Done, calculating sorted playtimes and looking up steam usernames...")
    play_times = me.sort_playtimes(game_stats)
    pprint(play_times)
