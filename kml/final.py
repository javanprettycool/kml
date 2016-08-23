#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

dir = u"F:/dataD/2016/7月/0727"


filename = "2.kml"

path = dir + filename

id_for_fee = readFeeFromExcel(dir + "id_for_fee.xls")
original_dog_list = readDogIdFromExcel(dir + "dog_detail.xls")
#print original_dog_list

dog_list = []
list, handle_list, dog_list = kmlparse2.parse_pnd(path, "test_zzf")
#list, handle_list, dog_list = kmlparse2.parse_caiji(path, "test_zzf")


pmlist = proc_mod(list, id_for_fee, original_dog_list, dog_list, "test_zzf")
print len(handle_list), len(pmlist)




createXls(pmlist, dir, "pnd_2016_07_27(2)", "2016-07-27", u"张志锋")
#createXls(pmlist, dir, "caiji_2016_04_01", "2016-04-01", u"张志锋")


