#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 02:09:21 2017

@author: norbertdanisik
"""

import json
import os

path_rooms = ".//Crawled_rooms//"
path_reviews = ".//Review_content//"
path_final = ".//Json_data_files//"

sitemaps = ['sitemap-p32_','sitemap-p33_','sitemap-p34_']
ind = 2 
amen_map = json.loads(open("mapping_amenities.txt","r",encoding='utf-8').readlines()[0])

all_files = os.listdir(path_rooms + sitemaps[ind] + "//")

if not os.path.exists(path_final + sitemaps[ind] + "//"):
    try:
        os.mkdir(path_final + sitemaps[ind] +"//")
    except:
        print("Error while creating folder")
            
for pos,room_file in enumerate(all_files):
    if pos % 1000 == 0 and pos > 0:
        print("PARSING FILE " + str(pos))
#        break
    if str(room_file).find(r'.txt') == -1:
        continue
    room = open(path_rooms + sitemaps[ind] + "//" + room_file,"r",encoding='utf-8')
    room = room.readlines()
    js = json.loads(room[0])
    
    sub_js = js["reduxData"]["marketplacePdp"]["listingInfo"]
    
    listing_id = str(sub_js["listingId"])
    host_id = str(sub_js["listing"]["primary_host"]["id"])
    title = sub_js["listing"]["p3_summary_title"]
    host_name = sub_js["listing"]["primary_host"]["host_name"]
    is_superhost = sub_js["listing"]["primary_host"]["is_superhost"]
    beds = sub_js["listing"]["beds"]
    bedrooms = sub_js["listing"]["bedrooms"]
    guests = sub_js["listing"]["guest_label"]
    house_rules = sub_js["listing"]["house_rules"] if sub_js["listing"]["house_rules"] == sub_js["listing"]["additional_house_rules"] else sub_js["listing"]["house_rules"] + " " + sub_js["listing"]["additional_house_rules"] 
    location_name =  " ".join([item["link_text"] for item in sub_js["listing"]["p3_neighborhood_breadcrumb_details"] ])
    location = [sub_js["listing"]["lng"],sub_js["listing"]["lat"]]
    price = sub_js["listing"]["p3_event_data_logging"]["price"]     
    rating = sub_js["listing"]["star_rating"]
    reviews_count = sub_js["listing"]["visible_review_count"]
    room_type = sub_js["listing"]["localized_room_type"]
    amenities_count = len(sub_js["listing"]["p3_event_data_logging"]["amenities"])
    city = sub_js["listing"]["city"]
    country = sub_js["listing"]["country"]
    desc_lang = sub_js["listing"]["p3_event_data_logging"]["description_language"]

    if city == "" or city is None:
        city = "_undef"
    if country == "" or country is None:
        country = "_undef"
    if location_name == ""or location_name is None:
        location_name = "_undef"
    if desc_lang == "en":
        desc_en = sub_js["listing"]["description"]
        desc_other = ""
    else:
        desc_en = "" 
        desc_other = sub_js["listing"]["description"]
    if amenities_count > 0:
#        amenities = [amen_map[str(am)] for am in sub_js["listing"]["p3_event_data_logging"]["amenities"] ]
        amenities = list(filter(lambda x : x != '', [amen_map[str(am)] for am in sub_js["listing"]["p3_event_data_logging"]["amenities"] ]))
    try:
        review = open(path_reviews + sitemaps[ind] + "__for_review__revs//" + str(host_id) + "__json_reviews.txt","r",encoding='utf-8')
        review = review.readlines()
        js_rev = json.loads(review[0])
        
        reviews = []
        for rv in js_rev["reviews"]:
            reviews.append(rv["r_txt"].replace("\r\n", "").replace("\n", ""))
    except:
        reviews = []
    final_json = {  "reviews":reviews,  #slovne hodnotenia
                    "host_id":str(host_id), #ID hostujuceho
                    "listing_id": str(listing_id), # ID ubytovania
                    "title":title, #titulok izby
                    "host_name":host_name, #meno hostujuceho
                    "is_superhost":is_superhost, #superhost - ano/nie
                    "desc_en":desc_en, #anglicky opis ubytovania
                    "desc_other":desc_other, #opis v inom jazyku
                    "desc_lang":desc_lang, #druh jazyka
                    "beds":beds, #pocet posteli
                    "bedrooms":bedrooms, #pocet izieb
                    "guests":guests, #pocet hostov
                    "house_rules":house_rules, #podmienky ubytovania - pravidla
                    "location_name":location_name, #nazov lokacie
                    "location":location, #GPS Suradnice
                    "price":price, #cena
                    "rating":rating, #hodnotenie v hviedzickach
                    "reviews_count":reviews_count, #pocet hodnoteni
                    "room_type":room_type, #typ izby
                    "amenities_count":amenities_count, #pocet typov vybavenia
                    "amenities":amenities, #samotne vypisane vybavenia
                    "city":city, #mesto
                    "country":country #krajina
                  }
    
    with open(path_final + sitemaps[ind] + "//" + str(listing_id) + "__data.json", "w") as fp:
        json.dump(final_json, fp)
    
    