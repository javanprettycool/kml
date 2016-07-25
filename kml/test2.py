#coding=utf-8

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












