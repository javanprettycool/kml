#coding=utf-8



#采集和pnd一起处理
__author__ = 'javan'

import xlrd
import xlwt
import time
import kmlparse2
from pyexcel import *
from process import *
from kmlparse2 import *
import codecs
import sys

EXT = ".kml"

date = "2015_12_27"  #改这个

dir = u"E:/dataD/2015/12月/1227/"  #改这个

pnd_filename = u"PNDCJ_" + date + u"_22pm"
caiji_filename = u"CAIJI_" + date + u"_21pm"

pnd_path = dir + pnd_filename + EXT
caiji_path = dir + caiji_filename + EXT

docname = u'PND&CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'
fodername = u'PND&CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'

pm_list = []

pnd_list, pnd_handle_list, pnd_dog_list = kmlparse2.parse_pnd(pnd_path)


caiji_list, caiji_handle_list, caiji_dog_list = kmlparse2.parse_caiji(caiji_path)

print "pnd:"+str(len(pnd_handle_list))+" caiji:"+str(len(caiji_handle_list))+" all_pnd:"+str(len(pnd_list))+" pnd_dog:"+str(len(pnd_dog_list))+" caiji_all:"+str(len(caiji_list))
# for p in pnd_list:
# 	p.name = "pnd"+p.name
#
# for g in caiji_list:
# 	print g.name, g.match

pnd_list.extend(caiji_list)
list = pnd_list

pnd_dog_list.extend(caiji_dog_list)
dog_list = pnd_dog_list

pnd_handle_list.extend(caiji_handle_list)
handle_list = pnd_handle_list

print len(list), len(handle_list)


operate(list, dir+"handle/", dog_list)
#
# for p in list:
# 	if p.handletype == "3":
# 		print p.name, p.matchlist

#输入预处理的kml
outputKml((list, handle_list, dog_list), docname, fodername, dir+"handle/", "new_PND&CAIJI_"+date[5:], 400)












