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

EXT = ".kml"

date = "2015_12_22"

dir = u"D:/code/"

filename = u"PNDCJ_" + date + u"_22pm"

path = dir + filename + EXT

docname = u'PND\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'
fodername = u'PND\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'

pm_list = []

list, handle_list, dog_list = kmlparse2.parse_pnd(path)

operate(list, dir, dog_list)


#输入预处理的kml
outputKml((list, handle_list, dog_list), docname, fodername, dir, "test"+filename, 1)



