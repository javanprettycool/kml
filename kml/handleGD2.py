#coding=utf-8

__author__ = 'javan'


import kmlparse2
from pyexcel import *
from process import *


EXT = ".kml"

date = "2016-07-21"

dir = u"F:/dataD/高速/G1111伊绥高速采集处理20160720/G1111伊绥高速采集处理20160720/"  #改这个

pmlist = []

gd_filename = u"local2_gd2"
gd_path = dir + gd_filename + EXT
gd_list = kmlparse2.parse_gd(gd_path)

for p in gd_list:
    pmlist.append(createElement("add", p, "gaode"))


#exit()
createXls(pmlist, dir, "handleGD_"+date+"(4)", date, u"高德")





















