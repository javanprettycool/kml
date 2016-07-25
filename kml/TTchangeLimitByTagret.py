#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

path = "E:/fff.kml"


list_tt = kmlparse2.parse_ts(path)

list = []
for p in list_tt:
    print p.name,p.longitude,p.latitude
    if p.name == "0" or p.name == "1":
        continue
    list.append(p)


result = []
kml = []
for p in list_tt:
    if p.name == "0" or p.name == "1":
        for t in list:
            print p.name,p.longitude,p.latitude, t.name, t.longitude, t.latitude,getDist2(p.longitude, p.latitude, t.longitude, t.latitude)
            if getDist2(p.longitude, p.latitude, t.longitude, t.latitude) < 100:
                print t.name
                t.speedlimit = 50
                kml.append(createPM(t))
                result.append(t)

print len(result)
kmlparse2.output_file(kml, "test", "test", "e:/test.kml")



filename = "411"

dir = "e:/"

date = "2016-04-06"

createXlsForUpdate(result, filename)





