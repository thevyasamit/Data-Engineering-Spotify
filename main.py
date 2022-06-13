from lib2to3.pgen2 import token
from tokenize import Token
from wsgiref import headers
from matplotlib import artist
import sqlalchemy
import  requests
import json
import sqlite3
import datetime
from sqlalchemy.orm import sessionmaker
import pandas as pd

DATABASE_LOCATION = "sqlite:///my_tracks.sqlite"
USER_ID = "YOUR_SPOTIFY_USER_NAME"
TOKEN = "GET_TOKEN_FROM_SPOTIFY_DEVELOPER_ACCOUNT"
if __name__ == "__main__":
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
         
    }
    
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers = headers)
    data = r.json()
    
    song_names = []
    artist_names = []
    
    for song in data["items"]:
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        song_names.append(song["track"]["name"])
        
    songs_di ={
        "song_name" : song_names,
        "artist_names": artist_names
    }
    
    songs_df = pd.DataFrame(songs_di, columns=["song_name","artist_names"])
    print(songs_df)