#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 00:54:26 2017

@author: norbertdanisik
"""

from bs4 import BeautifulSoup
import requests as req
import json
import os
import time
import io

def get_content(url):
    r = req.get(url)
    bs = BeautifulSoup(r.content, 'html.parser')
    return bs 

path_get_links = ".//Review_links//"
path_review_content = ".//Review_content//"

all_files = os.listdir(path_get_links)

for pos,review_file in enumerate(all_files):
    print("STARTING REVIEWS FROM FILE " + str(pos))
    
    if str(review_file).find(r'.txt') == -1:
        continue
    reviews = open(path_get_links + review_file,"r")
    all_hosts = []
#    states = []
    for host in reviews.readlines():
        all_hosts.append(host.strip("\n"))
#        states.append(False)        
    all_hosts = list(set(all_hosts))
    if not os.path.exists(path_review_content+str(review_file)[:-4]+ "__revs"+"//"):
        try:
            os.mkdir(path_review_content+str(review_file)[:-4]+ "__revs")
        except:
            print("Error while creating folder")
    
    for index,host in enumerate(all_hosts):
        all_reviews = {"user":host,"reviews":[]}
        print(host)
        page_num = 0
        while True:
            time.sleep(0.25)
            page_num += 1
            try:
                link = "https://www.airbnb.com/users/review_page/" + host + "?page=" + str(page_num) + "&role=host"
                print(link)
                content = get_content(link)
                json_content = json.loads(content.get_text())
                if json_content["last_page"] == True:
                    break
#                reviews = json_content["review_content"]
                text_reviews = [text.get_text() for text in content.find_all("p")]
                names = [name.get('title')[2:-2] for name in content.find_all("img")]
                
                for i in range(len(json_content["review_ids"])):
#                    print(names[i] + "  ---  " + text_reviews[i] + "\n")
                    all_reviews["reviews"].append({"r_id":str(json_content["review_ids"][i]),"name":names[i],"r_txt":text_reviews[i]})
                    
                
            #if there is an error JSONDecoding
            except ValueError:
                try:
                    print("Decode error - trying again")
                    cs = content.get_text().split("]")
                    for slice in cs:
                        if slice.find("review_ids") > -1:
                            corr_slice = slice.split("[")
                            review_ids = corr_slice[-1].split(",")
                    
                    text_reviews = [text.get_text() for text in content.find_all("p")]
                    names = [name.get('title')[2:-2] for name in content.find_all("img")]
                    for i in range(len(review_ids)):
    #                    print(names[i] + "  ---  " + text_reviews[i] + "\n")
                        all_reviews["reviews"].append({"r_id":review_ids[i],"name":names[i],"r_txt":text_reviews[i]})
                except:
                    print("Not successful on the 2nd time either  " + link)
#                if json_content["last_page"] == True:
#                    break        
            except: 
                print("Different mistake")
                if link == 'https://www.airbnb.com/users/review_page/?page=2&role=host':
                    break
#        file_json = open(path_review_content+str(review_file).strip(r".txt")+ "__revs" + "//" + host +  "__json_reviews.txt","w")
#        file_json.write(json.dumps(all_reviews,encoding="utf-8"))
#        file_json.close()
        with io.open(path_review_content+str(review_file)[:-4]+ "__revs" + "//" + host +  "__json_reviews.txt", 'w', encoding='utf8') as json_file1:
            data = json.dumps(all_reviews, ensure_ascii=False)
            # unicode(data) auto-decodes data to unicode if str
            json_file1.write(str(data))
                
                
            