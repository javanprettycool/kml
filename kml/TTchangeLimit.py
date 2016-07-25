#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

path = "E:/newmake_tt_2301.kml"


list_tt = kmlparse2.parse_ts(path)

list =[]
for p in list_tt:
    # if 122.108330 > p.longitude > 122.017231 and 46.051130 < p.latitude < 46.088154:
    #     if (p.form == u"红灯" or p.form == u"测速") and p.speedlimit == 50 :
    #         p.speedlimit = 70
    #         list.append(p)
    # else:
    #     if p.form == u"红灯" and p.speedlimit == 40 :
    #         p.speedlimit = 70
    #         list.append(p)
    if p.speedlimit ==40 :
        p.speedlimit = 60
        list.append(p)
print len(list)


filename = "gg"

dir = "e:/"

date = "2016-06-23"

createXlsForUpdate(list, filename)





