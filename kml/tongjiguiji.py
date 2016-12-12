#coding=utf-8
from placemark import placemark
import time
import xlrd
import re
import kmlparse2
import lonlat_util
from process import *
import re


path = u"F:/dataD/高速统计/我的地点.kml"
track = kmlparse2.parse_linestring(path)
track_length = 0
statistic_length = 0

for p in track:
	track = p.track_list
	start = track[0]
	part_length = 0
	print p.name
	for t in track:
		next = t
		l = lonlat_util.getDist2(start[0], start[1], next[0], next[1])
		start = t
		track_length += l
		part_length += l
	print str(part_length / 1000) + "km"
	if re.search("(\d+KM)", p.name):
		len_from_str = re.search("(\d+KM)", p.name).group()
		statistic_length += float(len_from_str.strip("KM"))
		print len_from_str

print "total: " + str(track_length / 1000) + "km"
print "str_total: " + str(statistic_length) + "km"
exit()
