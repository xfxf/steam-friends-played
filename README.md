# peerpressure.us / steam-friends-played
## Compare my Steam friends in-game "played" times

### Overview

Flask web app + MySteamFriends library (wrapping 'steam' library) to show all friends playtime on a leaderboard for a user on Steam.  This is a early version that directly queries the Steam API with no caching/storage; I'd love to add more features; see the Issue Tracker on Github: <https://github.com/xfxf/steam-friends-played/issues>.  Pull Requests are very welcome.


Requires Python 3.4+ and a Steam Web API key (see start of steam-friends-played.py).


### Instructions (dev)

Before running, change these settings in steam_friends_played_app.py:
* Fill out API_KEY 
* Optionally enable DEBUG mode (disabled by default; if enable, ensure this is not public accessible).

```
pip install -r requirements.txt
python3 steam_friends_played_app.py
```

Then visit http://127.0.0.1:5000/

---
Ryan Verner <ryan.verner@gmail.com>




