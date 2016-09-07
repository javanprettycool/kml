#coding=utf-8

__author__ = 'javan'


import kmlparse2
from pyexcel import *
from process import *


EXT = ".kml"

date = "2016-09-05"
#处理高德的
dir = u"F:\dataD\投诉\\0905投诉"  #改这个

dir = dir.replace("\\","/")

if dir[-1] != "/":
    dir+="/"

pmlist = []
gd_list = []

for i in os.listdir(dir):
    if os.path.isfile(os.path.join(dir,i)):
        if i.find('XUEHUACJ_2016-09-05') >= 0:
            gd_filename = i
            gd_path = dir + gd_filename
            gd_list = kmlparse2.parse_gd(gd_path)
            for p in gd_list:
                 pmlist.append(createElement("add", p, "by_gd_zzf"))


#exit()
createXls(pmlist, dir, "handleGD_"+date, date, u"高德")





















