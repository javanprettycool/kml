#coding=utf-8
__author__ = 'tt'

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

date = "2015_12_27"

dir = u"E:/dataD/2015/12月/1227/"

#filename = u"PNDCJ_" + date + u"_22pm"
filename = u"CAIJI_" + date + u"_21pm"

path = dir + filename + EXT

docname = u'CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'
fodername = u'CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'

pm_list = []

list, handle_list, dog_list = kmlparse2.parse_caiji(path)

print len(handle_list)
operate(list, dir+"caiji/", dog_list)
#
# for p in list:
# 	if p.handletype == "3":
# 		print p.name, p.matchlist

#输入预处理的kml
outputKml((list, handle_list, dog_list), docname, fodername, dir+"caiji/", "new_"+filename+"_"+date[5:], 1)



