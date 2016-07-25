#coding=utf-8
__author__ = 'Javan'

import urllib2
import urllib
from bs4 import BeautifulSoup
from kmlparse2 import *
from lonlat_util import *
import re


query = urllib.quote("大鹏新区/全部/")

url = "http://szjj.u-road.com/szjjpro/index.php?/infoquery/robotpolicequery/robotListShow/" + query

#print url

req = urllib2.Request(url)
con = urllib2.urlopen(req)

doc = con.read()


soup = BeautifulSoup(doc)

list = soup.html.body.find('ul', {'id': 'robotlist'})

pmlist = []

i = 0
for item in list:
    pm = placemark()
    lon = item.get('longitude')
    lat = item.get('latitude')
    array = baiduTranstoGoogle(float(lon), float(lat))
    lon, lat = Gcj02toWgps4(*array)
    pm.longitude = lon
    pm.latitude = lat + 0.000539   #稍微修正
    pm.name = item.i.text + ": " + item.get('violationtype')
    pmlist.append(createPM(pm))
    #print item.get('longitude'), item.get('latitude'), item.get('violationtype'), item.i.text
    i+=1

print i

output_file(pmlist, u"大鹏新区全部", u"大鹏新区全部", u"e:/大鹏新区.kml")

con.close()



