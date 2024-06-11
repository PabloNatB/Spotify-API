# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 18:22:45 2024

@author: pablo
"""


from API_functions import search,get_token



file = open("data.txt")
lines=file.readlines()
file.close()

client_ID=lines[0][:-1]
client_secret=lines[1]

token = get_token(client_ID,client_secret)
       

names=["Thom Yorke" , "Radiohead" , "Interpol" , "Arctic Monkeys" , "Muse" , "Deftones"]
for name in names:
    search(token,name)