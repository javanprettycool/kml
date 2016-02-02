#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

dir = u"E:/dataD/2016/1月/0129/pnd/"

filename = "1.kml"

path = dir + filename

id_for_fee = readFeeFromExcel(dir + "id_for_fee.xls")
original_dog_list = readDogIdFromExcel(dir + "dog_detail.xls")
#print original_dog_list

dog_list = []
list, handle_list, dog_list = kmlparse2.parse_pnd(path, "test_zbr")
#list, handle_list, dog_list = kmlparse2.parse_caiji(path)


pmlist = proc_mod(list, id_for_fee, original_dog_list, dog_list, "test_zbr")
print len(handle_list), len(pmlist)




createXls(pmlist, dir, "pnd_2016_01_29(ff)", "2016-01-29", u"张宝茹")


