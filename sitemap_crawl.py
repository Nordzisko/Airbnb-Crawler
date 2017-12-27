#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 18:56:49 2017

@author: norbertdanisik
"""


from bs4 import BeautifulSoup
import urllib.request
import re
import gzip

blacklist = [line.rstrip('\n') for line in open('blacklist.txt')]
path_xml=".//Saved_sites_xml//"
path_links=".//Saved_links//"


root_file = "airbnb-sitemap.xml"
xml_unchecked_file = "xml_files_unchecked.txt"
xml_checked_file = "xml_files_checked.txt"

root = open(root_file,"r")
xml_checked = open(xml_checked_file,"w")
xml_unchecked = open(xml_unchecked_file,"w")

#Define user agent and URL opener
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

#Getting links for xml.gz files -> download and store them
soup_root = BeautifulSoup(root, "lxml")
for root_links in soup_root.findAll('loc'):
    print(root_links.get_text())
    print("Getting: " + root_links.text)
    name_of_file = re.sub(r'https://www.airbnb.com/','',str(root_links.get_text()))
    urllib.request.urlretrieve(root_links.get_text(), path_xml + name_of_file)
    xml_unchecked.write(name_of_file + "\n")

xml_unchecked.close()
print("Start unzipping files")

#Getting and saving direct links to content 
xml_unchecked = open(xml_unchecked_file,"r")
for unch_file in xml_unchecked.readlines():
    print("Unzipping " + unch_file)
    with gzip.open(path_xml + unch_file.strip("\n"), 'rb') as file:
        links_file = open(path_links + unch_file.strip(".xml.gz\n") + "_uncrawled_links.txt","w")
        rooms_file = open(path_links + unch_file.strip(".xml.gz\n") + "_rooms_links.txt","w")
        file_content = file.read()
        soup_file = BeautifulSoup(file_content,"lxml")
        for enu,link in enumerate(soup_file.findAll('loc')):
#            print(link.get_text())
            if link.get_text().find(r'/rooms/') > -1:
                rooms_file.write(link.get_text() + "\n")
            else:
                links_file.write(link.get_text() + "\n")
            if enu % 100 == 0:
                print("Checking line " + str(enu))
        links_file.close()
        rooms_file.close()
        xml_checked.write(unch_file)

xml_checked.close()
    

print("Finished")


