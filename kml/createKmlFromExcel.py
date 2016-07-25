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

date = "2016_04_11"  #改这个

file = "f:/tt.xls"
data = xlrd.open_workbook(file)

table = data.sheets()[0]
doglist = []
# for row in range(3, table.nrows):
#     dog = placemark()
#     dog.name = table.row_values(row)[3]
#     dog.id = table.row_values(row)[3]
#     dog.longitude = float(table.row_values(row)[5])
#     dog.latitude = float(table.row_values(row)[6])
#     dog.heading = table.row_values(row)[9]
#     dog.speedlimit = table.row_values(row)[10]
#     dog.form = table.row_values(row)[4]
#     doglist.append(createPM(dog))

for row in range(0, table.nrows):
    dog = placemark()
    dog.name = "node"
    str = table.row_values(row)[0]
    print str
    dog.longitude,dog.latitude = Gcj02toWgps4(float(str.split(",")[0]),float(str.split(",")[1]))
    doglist.append(createPM(dog))


print len(doglist)
#输入预处理的kml
output_file(doglist, "test", "test", "f:/04142.kml")












