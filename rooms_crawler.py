#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 23:07:22 2017

@author: norbertdanisik
"""

from bs4 import BeautifulSoup
import requests as req
import json
import os
import time

def get_content(url):
    r = req.get(url)
    bs = BeautifulSoup(r.content, 'html.parser')
    return bs 

def save(path,link,content,index,room_id):
    f=open(path+room_id+"_.txt","w")
    f.write(str(content))
    f.close()

path_links = ".//Saved_links//"
path_get_links = ".//Crawled_links//"
path_rooms = ".//Crawled_rooms//"
path_reviews = ".//Reviews_crawl//"

xml_checked_file = "xml_files_checked.txt"

all_files = os.listdir(path_get_links)

for pos,room_file in enumerate(all_files):
    print("STARTING ROOMS FROM FILE " + str(pos))
    if str(room_file).find(r'.txt') == -1:
        continue
    all_links = []
    states = []
    all_hosts = []
    rooms = open(path_get_links + room_file,"r")
    for room in rooms.readlines():
        all_links.append(room.strip("\n"))
        states.append(False)
    if not os.path.exists(path_rooms+str(room_file)[:12]+"//"):
        try:
            os.mkdir(path_rooms+str(room_file)[:12])
        except:
            print("Error while creating folder")
    for index,link in enumerate(all_links):
        room_id = link.strip(r'https://www.airbnb.com/rooms/')
        try:
            content = get_content(link)
#            save(path_rooms, link, content, index,room_id)
            states[index] = True
            print("Vsetko okej - " + room_id)
            scripts = content.find_all("script",attrs={"data-hypernova-key":"p3show_marketplacebundlejs"})
            json_data = scripts[0].get_text()[4:-3]
            json_data = json.loads(json_data)
            
            json_data_useful = json_data["bootstrapData"]
#            listingId = json_data_useful["listingId"]
            host = json_data_useful["reduxData"]["marketplacePdp"]["listingInfo"]["listing"]["primary_host"]["id"]
            
            json_file = open(path_rooms + str(room_file)[:12] + "//" + str(index).zfill(5) + "__" + room_id  + ".txt","w")
            json_file.write(json.dumps(json_data_useful))
            json_file.close()
            
            all_hosts.append(host)
            print("Zapisane")
            time.sleep(0.5)
        except:
            print("Error nastal")
    #        states[index] = 'Error'
            continue
    
    for idx,state in enumerate(states):
        if not state:
            err_file = open("errors.txt","w")
            err_file.write(all_links[idx])
            err_file.close()
    
    review_file = open(path_reviews + str(room_file)[:12] + "__for_review.txt","w")       
    for host_it in all_hosts:
        review_file.write(str(host_it) + "\n")
    review_file.close() 
    rooms.close()    


