#!/usr/bin/env python3
from mysteamfriends import MySteamFriends
from flask import Flask
from flask import render_template

try:
    from local import API_KEY, DEBUG    # used for API_KEY + friends, optional
except ImportError:
    API_KEY = ""                        # from https://steamcommunity.com/dev/apikey
    DEBUG = True                        # Enable debugging, False or True

app = Flask(__name__.split('.')[0])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<steam_id>/<app_id>')
def steamid_appid(steam_id=None, app_id=None):
    print("Connecting to Steam API server and populating friends...")
    me = MySteamFriends(
        api_key=API_KEY,
        steam_id=steam_id,
        debugging=DEBUG)

    print("Connected, collecting friends in-game time...")
    all_game_stats = me.get_everyones_gamestats(app_id)

    print("Done, looking up steam usernames...")
    all_game_stats_detailed = me.get_game_stats_detailed(all_game_stats)

    return render_template('steamid_appid.html',
                           game_stats_detailed=all_game_stats_detailed,
                           appid=app_id,
                           personaname=me.get_steam_username(me.my_steam_id),
                           game_title=me.get_game_name(app_id))


@app.route('/user/<user_identifier>')
def username(user_identifier=None):
    if 17 <= len(user_identifier) <= 18 and user_identifier.isdigit():
        steam_username = None
        steam_id = user_identifier
    else:
        steam_username = user_identifier
        steam_id = None

    print("Connecting to Steam API server and populating friends...")
    me = MySteamFriends(
        api_key=API_KEY,
        steam_username=steam_username,
        steam_id=steam_id,
        debugging=DEBUG)

    return render_template('games_list.html',
                           games_list=me.my_games_list,
                           steamid=me.my_steam_id,
                           personaname=me.get_steam_username(me.my_steam_id))


if __name__ == "__main__":
    app.debug = DEBUG
    print("Starting...")
    app.run(threaded=True)
