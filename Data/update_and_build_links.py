'''
Authors: Austin Connick, Ryan Rizzo
File: This file scraps cyverse for dates and plant names and builds and tests 
public links
requirements/tested on:
        python=2.7.18
        GCC=9.3.0
        Ubuntu 20.04.3 LTS

'''
import json
import os
import subprocess
import re
import time
import requests
import bs4
from bs4 import BeautifulSoup
url = "https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/"
file_to_find = "/combined_multiway_registered.npy"
'''
getAllDates returns a list of all dates
returns list
'''
def getAllDates():
    domtree = requests.get(url)
    tree = domtree.text
    dates = []
    web = BeautifulSoup(domtree.content, "html.parser")
    dates =  web.find_all("tr", class_="object collection")
    list_of_dates = []
    for i in dates:
        #print(i.text)
        i = str(i.text).split("/")[0]
        print(i)
        list_of_dates.append(i)
    return list_of_dates
    #print(domtree.text)
'''
build_names takes a date and returns a list of all plant names under the date
returns list
'''
def build_names(date):
    #https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds/
    new_url = url + date + "/plantcrop/combined_pointclouds/"
    domtree = requests.get(new_url)
    web = BeautifulSoup(domtree.content, "html.parser")
    names =  web.find_all("tr", class_="object collection")
    dates_list = []
    for i in names:
        i = str(i.text).split("/")[0]
        #print(i)
        dates_list.append(i)
    return dates_list
'''
sets starting path
'''
def set_path(url_set):
    url =""
    url = url_set
def set_file_to_find(find):
    file_to_find = ""
    file_to_find = find
'''
build_public_link takes in a name and date and builds a public link
returns string
'''
#https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds/
def build_public_link(plant_name,plant_date):
    mid = url+"/"+plant_date+"/plantcrop/combined_pointclouds/"+plant_name
    test_link = mid + file_to_find
    link_code = requests.get(test_link, stream=True).status_code
    if link_code == 404:
        print('invalid link')
        return ''
    else:
        return test_link
'''
def main():
   dateL = getAllDates()
   names = build_names(dateL[0])
   #print(build_public_link(names[0],dateL[1]))
   print(names)
if __name__=="__main__":
    main()
'''