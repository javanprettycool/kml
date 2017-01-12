#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *
import time

EXT = ".kml"

date = "2017_01_02"  #改这个

filename = "3"

year = date.split('_')[0]
month = date.split('_')[1]
day = date.split('_')[2]

dir = u"F:/dataD/"+year+"/"+str(int(month))+u"月/"+month+day+"/pnd/"  #改这个

path = dir + filename + EXT

id_for_fee = readFeeFromExcel(dir + "id_for_fee.xls")
original_dog_list = readDogIdFromExcel(dir + "dog_detail.xls")
#print original_dog_list

dog_list = []
list, handle_list, dog_list = kmlparse2.parse_pnd(path, "test_zzf")
#list, handle_list, dog_list = kmlparse2.parse_caiji(path, "test_zzf")

pmlist = proc_mod(list, id_for_fee, original_dog_list, dog_list, "test_zzf")


new_filename = "pnd_" + date + ("("+filename+")" if re.match(r"\d+$", filename) else "")
createXls(pmlist, dir, new_filename, time.strftime("%Y-%m-%d", time.localtime() ), u"张志锋")
#createXls(pmlist, dir, "caiji_2016_04_01", "2016-04-01", u"张志锋")


print len(handle_list), len(pmlist)