#!/usr/bin/env python3
from mysteamfriends import MySteamFriends
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

try:
    from local import API_KEY, DEBUG, CONCURRENT_API, FLASK_THREADED, SERVER_NAME  # local.py optional
except ImportError:
    API_KEY = ""                        # from https://steamcommunity.com/dev/apikey
    DEBUG = False                       # Enable debugging (default False)
    CONCURRENT_API = 8                  # How many concurrent Steam API requests to make (default 8)
    FLASK_THREADED = True               # Run multithreaded Flask (default True)
    SERVER_NAME = None                  # Hostname of server (default None)


app = Flask(__name__.split('.')[0])
app.config["SERVER_NAME"] = SERVER_NAME
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<steam_id>/<app_id>')
def steamid_appid(steam_id=None, app_id=None):
    print("Connecting to Steam API server and populating friends...")
    me = MySteamFriends(
        api_key=API_KEY,
        steam_id=steam_id,
        debugging=DEBUG,
        concurrent_api=CONCURRENT_API)

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


@app.errorhandler(NameError)
def nameerror_exception(e):
    return render_template('index.html', e=e), 500


if DEBUG is False:
    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.error('Unhandled Exception: %s', e)
        return render_template('500.html', e=e), 500

if __name__ == "__main__":
    app.debug = DEBUG
    print("Starting...")
    app.run(threaded=FLASK_THREADED)
