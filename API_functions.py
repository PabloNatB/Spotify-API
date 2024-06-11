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


def get_token(client_ID,client_secret):
    # Encode client credentials
    auth_string = f"{client_ID}:{client_secret}"
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



def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_artist(token,name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={name}&type=artist&limit=1"
    
    query_complete= url + query
    
    results = get(query_complete,headers=headers)
    json_res=json.loads(results.content)["artists"]["items"]
    return json_res[0]


def get_songs_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=MX"
    headers = get_auth_header(token)
    res = get(url,headers=headers)
    json_res = json.loads(res.content)["tracks"]
    return json_res


def search(token,name):
    result=search_artist(token, name)
    
    artist_id=result["id"]
    
    songs=get_songs_artist(token, artist_id)
    
    df=pd.DataFrame(columns=["Place","Song Name", "Album","Duration in minutes","Image URL"])
    
    for i,song in enumerate(songs):
        #print(i+1,"._ ",song["name"],", ", song["album"]["name"] ,", ", round(song['duration_ms']/(60_000),2),sep="")
        df.loc[i]=[i + 1 , song["name"] , song["album"]["name"] , round(song['duration_ms']/(60_000),2 ), song["album"]["images"][0]["url"]]
    
    urls  = list( df["Image URL"] )
    names = list( df["Song Name"] )
    
    df_name= "Top 10 " + name + " songs.csv"
    df.to_csv(df_name)
    
    fig , axs = plt.subplots(3,3)
    for i in range(3):
        for j in range(3):
            index=j + 3*i
            image = io.imread(urls[index])
            axs[i,j].imshow(image)
            axs[i,j].axis("off")
            title= str(index + 1) + ". " + names[index]
            axs[i,j].set_title(title,size=7)
            
    title="Top 9 songs from: " + name
    fig.suptitle(title)    
    # Set background color for the entire figure
    fig.patch.set_facecolor('#556B2F')
    
    plot_name = "Top 9 " + name + " songs.png" 
    fig.savefig(plot_name, dpi=300)