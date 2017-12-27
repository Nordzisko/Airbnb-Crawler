# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 22:11:10 2017

@author: Norbert
"""


import os
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def set_data(input_folder, index_name = "content_engine", doc_type_name="en"):
    print(index_name)
    print(doc_type_name)
    all_files = os.listdir(input_folder)
    for pos,room_file in enumerate(all_files):
        if pos % 300 == 0 and pos > 0:
            print("Inserting file number " + str(pos))
        if str(room_file).find(r'.json') == -1:
            continue
        
        with open(input_folder + room_file) as json_data:
            data = json.load(json_data)   
        yield{
            "_index": index_name,
            "_type": doc_type_name,
            "_id": data["listing_id"],
            "_source": data
        }
            
def load(es,input_folder,**kwargs): 
    success, _ = bulk(es, set_data(input_folder, **kwargs))

es = Elasticsearch([{'host':'localhost','port':9200}])
start_folder = ".//Json_data_files//sitemap-p34_//"
index_name = "airbnb_index"
doc_type_name = "room"

load(es,start_folder,index_name = index_name,doc_type_name=doc_type_name)

