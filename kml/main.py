#coding=utf-8

import re
from lonlat_util import getLalong,getDist,getDist2
from kmlparse2 import *
from pyexcel import *
import kmlparse2
import codecs
from lxml import etree
from process import *
import datetime


#获得当前时间
now = datetime.datetime.now()
#转换为指定的格式:
date = now.strftime("%Y-%m-%d")

dir =  u"E:/MyDownloads/Download"
path = u"E:/MyDownloads/Download/newmake_tt_0902.kml"
filename = "tt2"

parse_ts(path, filename, date)









# pm_list = []
# for pm in list:
# 	pm_list.append(createPM(pm.name, True if pm.match != "?" or pm.match == " " else False, pm.longitude, pm.latitude, pm.heading))
#
# doc = createKML(docname, fodername, pm_list)
# output_file = codecs.open(dir + "pnd_test_left.kml", "w")
# output_file.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
# output_file.close()
