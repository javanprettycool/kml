#coding=utf-8
__author__ = 'Javan'


import xlrd
import xlwt
import time
import kmlparse2
from pyexcel import *
from process import *
from kmlparse2 import *
import codecs
import sys
from lonlat_util import *

path1 = u'E:/MyDownloads/Download/tt.kml'

path2 = u'E:/MyDownloads/Download/xz.kml'

filename = "gg"

dir = "e:/"

date = "2016-01-27"

list_tt = kmlparse2.parse_ts(path1)
#print list_tt

list_xz = kmlparse2.parse_ts(path2)
#print list_xz

offset = 20
impact = False
handlelist = []
lastlist = []
for xz in list_xz:
	for tt in list_tt:
		if xz.form == u"红灯" and checkDistance(xz, tt, 80):
			impact = True
			break
		else:
			if checkDistance(xz, tt, 40):
				impact = True
				break
	if not impact:
		handlelist.append(xz)
	impact = False

for p in handlelist:
	if p.form == u"违规稽查" or p.form == u"事故多发" or p.form == u"禁止掉头":
		continue
	elif p.form == u"红灯":
		p.form = u"0闯红灯拍照"
	elif p.form == u"测速":
		p.form = u"1测速照相"
	elif p.form == u"辅道测速照相":
		p.form = u"11右侧辅道测速照相"
	elif p.form == u"高速出口":
		p.form = u"25高速出口"
	elif p.form == u"收费站":
		p.form = u"28收费站"
	elif p.form == u"急转弯":
		p.form = u"32急转弯路段"
	elif p.form == u"休息区":
		p.form = u"29休息区"
	lastlist.append(p)

createXls(lastlist, dir, filename, date)
