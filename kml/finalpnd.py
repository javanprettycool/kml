#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

dir = u"F:/dataD/2016/8月/0825/pnd/"
#dir = u"F:/dataD/2016/4月/0401/caiji/"

filename = "3.kml"

path = dir + filename

id_for_fee = readFeeFromExcel(dir + "id_for_fee.xls")
original_dog_list = readDogIdFromExcel(dir + "dog_detail.xls")
#print original_dog_list

dog_list = []
list, handle_list, dog_list = kmlparse2.parse_pnd(path, "test_zzf")
#list, handle_list, dog_list = kmlparse2.parse_caiji(path, "test_zzf")


pmlist = proc_mod(list, id_for_fee, original_dog_list, dog_list, "test_zzf")
print len(handle_list), len(pmlist)




createXls(pmlist, dir, "pnd_2016_08_25(3)", "2016-08-25", u"张志锋")
#createXls(pmlist, dir, "caiji_2016_04_01", "2016-04-01", u"张志锋")


