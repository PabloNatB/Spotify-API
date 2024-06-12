# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 18:22:45 2024

@author: pablo
"""


from API_functions import spotify_top_ten_songs



file = open("data.txt")
lines=file.readlines()
file.close()

client_ID=lines[0][:-1]
client_secret=lines[1]

top_ten = spotify_top_ten_songs(client_ID, client_secret)
       

names=["Thom Yorke" , "Radiohead" , "Interpol" , "Arctic Monkeys" , "Muse" , "Deftones"]
for name in names:
    top_ten.artist_name = name
    top_ten.search()
    top_ten.to_database()