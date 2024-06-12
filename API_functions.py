# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 18:23:27 2024

@author: pablo
"""

from requests import post,get
import base64
import json
import pandas as pd
from skimage import io
import matplotlib.pyplot as plt
import sqlite3

class spotify_top_ten_songs:
    
    __slots__ = ["__client_ID" , "__client_secret" , "__token" , "__df" , "__artist_name" ]
    
    @staticmethod
    def get_token(self):
        # Encode client credentials
        auth_string = f"{self.__client_ID}:{self.__client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        result = post(url, data=data, headers=headers)
        
        if result.status_code != 200:
            print("Error:", result.json())
            return None
        
        json_result = result.json()
        token = json_result.get("access_token")
        return token
    
    def __init__(self,client_id,client_secret):
        self.__client_ID = client_id
        self.__client_secret = client_secret
        self.__token = self.get_token(self)
        
    @property
    def artist_name(self):
        return self.__artist_name
    
    @artist_name.setter
    def artist_name(self,value):
        if not isinstance(value, str):
            raise TypeError("Artist name must be a string")
        self.__artist_name = value


    @staticmethod
    def get_auth_header(obj):
        return {"Authorization": "Bearer " + obj.__token}
    
    @staticmethod
    def search_artist( obj  ):
        url = "https://api.spotify.com/v1/search"
        headers = obj.get_auth_header(obj)
        query = f"?q={obj.__artist_name}&type=artist&limit=1"
        
        query_complete = url + query
        
        results = get(query_complete,headers=headers)
        json_res=json.loads(results.content)["artists"]["items"]
        return json_res[0]
    
    @staticmethod
    def get_songs_artist( obj , artist_id ):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=MX"
        headers = obj.get_auth_header(obj)
        res = get(url,headers=headers)
        json_res = json.loads(res.content)["tracks"]
        return json_res
    
    
    def search(self):
        result=self.search_artist(self )
        
        artist_id=result["id"]
        
        songs=self.get_songs_artist(self , artist_id )
        
        self.__df=pd.DataFrame(columns=["Place","Song Name", "Album","Duration in minutes","Image URL"] )
        
        for i,song in enumerate(songs):
            #print(i+1,"._ ",song["name"],", ", song["album"]["name"] ,", ", round(song['duration_ms']/(60_000),2),sep="")
            self.__df.loc[i]=[i + 1 , song["name"] , song["album"]["name"] , round(song['duration_ms']/(60_000),2 ), song["album"]["images"][0]["url"]]
        
        urls  = list( self.__df["Image URL"] )
        names = list( self.__df["Song Name"] )
        
        #df_name= "Top 10 " + self.__artist_name + " songs.csv"
        #self.__df.set_index('Place', inplace = True)
        #self.__df.to_csv(df_name)
        
        fig , axs = plt.subplots(3,3)
        for i in range(3):
            for j in range(3):
                index=j + 3*i
                image = io.imread(urls[index])
                axs[i,j].imshow(image)
                axs[i,j].axis("off")
                title= str(index + 1) + ". " + names[index]
                axs[i,j].set_title(title,size=7)
                
        title="Top 9 songs from: " + self.__artist_name
        fig.suptitle(title)    
        # Set background color for the entire figure
        fig.patch.set_facecolor('#556B2F')
        
        plot_name = "Top 9 " + self.__artist_name + " songs.png" 
        fig.savefig(plot_name, dpi=300)
        
    @staticmethod
    def df_to_tuple(df):
        for i in range(len(df)):
            yield tuple( df.loc[ i ]) 
             
        
        
        
        
    def to_database(self):
        
        database_name= self.__artist_name.replace(" ","_") + ".db"
        #print(database_name)
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        #preparing statement
        sql1 = "DROP TABLE IF EXISTS data" 
        sql2 = '''CREATE TABLE data (
        
        Place INT NOT NULL,
        Song name CHAR,
        Album CHAR,
        Duration FLOAT,
        Image_URL CHAR
        
        )'''
        cursor.execute(sql1)
        cursor.execute(sql2)
        
        sql3 = "INSERT INTO data VALUES (?,?,?,?,?)"
        data = self.df_to_tuple(self.__df)
        for _ in range( len( self.__df ) ):
            cursor.execute(sql3,next(data))
            
        conn.commit()
        conn.close()
    
        
        
        
        
        
        
        