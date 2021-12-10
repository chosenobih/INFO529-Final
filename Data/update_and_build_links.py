'''
Authors: Austin Connick, Ryan Rizzo
File: This file scraps cyverse for date and plant names and builds and tests 
public links
Note: has not been tested on more than one date but should still find any
if they exist

requirements/tested on:
        python=2.7.18
        GCC=9.3.0
        iRODS=4.2.10
        Ubuntu 20.04.3 LTS

'''
import json
import os
import subprocess
import re
import time
import requests, urllib, urllib2
#plant_name, location, index, data, treatment, plot, genotype, lon, lat, min_x, max_x, min_y, nw_lat,nw_lon,se_lat,se_lon,bounding,roi_temp,quartile_1,mean,median,quartile_3,variance,std_dev,labels,double_lettuce
#https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds/

default_location = "/iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes"
file_to_find = "/combined_multiway_registered.npy"

sample_location = "/iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds"

'''
getAllDates returns a list of all dates
returns list
'''
#todo add a test for date
def getAllDates(url):
    allFoundDates = []
    os.system("touch plants_date")
    err = os.system("ils " + url +" >> plants_date")
    if err != 0:
        print("error " + str(err))
        os._exit(1)
        return []
    #add rex to find data
    fp = open('plants_date','r')
    for i in fp:
        k = i.split("/")
        if k[0] == "  C- ":
            f = k[-1]
            f = f.replace('\n','')
            allFoundDates.append(f)
    fp.close()
    os.system("rm plants_date")
    return allFoundDates

'''
build_names takes a date and returns a list of all plant names under the date
returns list
'''
def build_names(names):
    #/iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds
    sub_url_path = default_location +"/"+names+"/plantcrop/combined_pointclouds"
    os.system("touch plants_name")
    err = os.system("ils " + sub_url_path +" >> plants_name")
    if err != 0:
        print("error " + str(err))
        os._exit(1)
        return []
    fp = open("plants_name", 'r')
    all_names = []
    for i in fp:
        k = i.split('/')
        if k[0] == "  C- ":
            k = k[-1].replace('\n','')
            all_names.append(k)
    fp.close()
    os.system("rm plants_name")
    
    return all_names


'''
build_public_link takes in a name and date and builds a public link
returns string
'''
#https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds/
#builds a public link
#todo fix hard code of path
def build_public_link(plant_name,plant_date,location):
    start = "https://data.cyverse.org/dav-anon/"
    mid = default_location+"/"+plant_date+"/plantcrop/combined_pointclouds/"+plant_name
    test_link = start + mid + file_to_find
    link_code = requests.get(test_link, stream=True).status_code
    if link_code == 404:
        print('invalid link')
        return ''
    else:
        return test_link
    return test_link

#def prosses_url(url):
'''
build_public_link_All takes in the list of names and the date and builds all public links
returns map of names to links
returns dict
'''
def build_public_link_All(plant_names,plant_date):
    map_plant_to_public_link = {}
    for i in plant_names:
        tmp = build_public_link(i,plant_date)
        map_plant_to_public_link[i] = tmp
    return map_plant_to_public_link

#this is just for testing
def main():
   time1 = time.time()
   #gets a list of all dates in data store
   plant_dates = getAllDates(default_location)
   #gets all names under date in index 1
   date_to_name = build_names(plant_dates[1])
   #builds and test a public link 
   public_link = build_public_link(date_to_name[0],plant_dates[1],'')
   print(public_link)
   time2 = time.time()
   total = time2 - time1
   #timing link testing adds about 1.5s
   print("time-> "+str(total)+"s")
if __name__=="__main__":
    main()
