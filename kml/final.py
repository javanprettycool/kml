#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

dir = u"E:/dataD/2015/12月/1227/caiji/"

filename = "1.kml"

path = dir + filename

id_for_fee = readFeeFromExcel(dir + "id_for_fee.xls")
original_dog_list = readDogIdFromExcel(dir + "dog_detail.xls")
#print original_dog_list

dog_list = []
#list, handle_list, dog_list = kmlparse2.parse_pnd(path, "test_zzf")
list, handle_list, dog_list = kmlparse2.parse_caiji(path)

pmlist = proc_mod(list, id_for_fee, original_dog_list, dog_list, "test_zzf")

print len(handle_list), len(list), len(dog_list)

# for p in pmlist:
# 	print p.name


createXls(pmlist, dir, "caiji_zzf_2015_12_27", "2015-12-27", u"张志锋")


