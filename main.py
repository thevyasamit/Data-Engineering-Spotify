from lib2to3.pgen2 import token
from tokenize import Token
from wsgiref import headers
from matplotlib import artist
from matplotlib.ft2font import BOLD
from numpy import append
import sqlalchemy
import  requests
import json
import sqlite3
import datetime
from sqlalchemy.orm import sessionmaker
import pandas as pd

DATABASE_LOCATION = "sqlite:///my_tracks.sqlite"
USER_ID = "YOUR_SPOTIFY_USERNAME"
TOKEN = "GET_YOUR_TOKEN"
def check_valid_data(df: pd.DataFrame) -> bool:

    if df.empty:
        print("No Data")
        return False
    
    if df.isnull().values.any():
        raise Exception("Null Value found.")

# This is extraction of the data.

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
    
    # This is Transforming/checking/Validating data 
    
    if check_valid_data(songs_df):
        print("Data is Valid")

    # This is for loading the data in a table using bthe traditional SQL.
    
    eng =  sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_spotify_list')
    cur = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS my_spotify_list(
        song_name VARCHAR(100),
        artist_name VARCHAR(100)   
    )
    
    """
    cur.execute(query)
    try:
        songs_df.to_sql("my_spotify_list",eng,if_exists= 'append')
    except:
        print("Data already exists")
    conn.close()