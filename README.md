### Compare my Steam friends in-game "played" times

Basic Flask web app to show all friends playtime for a specific game on Steam.  This is a very early version; no caching/storage - all queries are done live against Steam's Web API (using threading to speed up queries).  Be patient, queries can take some time.

Requires Python 3.4+ and a Steam Web API key (see start of steam-friends-played.py).

### Instructions

Before running, change these settings in steam-friends-played.py:
* Fill out API_KEY 
* Optionally enable DEBUG mode (disabled by default; if enable, ensure this is not public accessible).

```
pip install -r requirements.txt
python3 steam-friends-played.py
```

Then visit http://127.0.0.1:5000/
