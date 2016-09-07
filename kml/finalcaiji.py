#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

date = "2016_08_17"
year = date.split('_')[0]
month = date.split('_')[1]
day = date.split('_')[2]

dir = u"F:/dataD/"+year+"/"+str(int(month))+u"月/"+month+day+"/caiji/"  #改这个

filename = u'CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59].kml'

path = dir + filename

id_for_fee = readFeeFromExcel(dir + "id_for_fee.xls")
original_dog_list = readDogIdFromExcel(dir + "dog_detail.xls")
#print original_dog_list

dog_list = []
#list, handle_list, dog_list = kmlparse2.parse_pnd(path, "test_zbr")
list, handle_list, dog_list = kmlparse2.parse_caiji(path, "test_zzf")


pmlist = proc_mod(list, id_for_fee, original_dog_list, dog_list, "test_zzf")
print len(handle_list), len(pmlist)




#createXls(pmlist, dir, "pnd_2016_03_30(7)", "2016-03-30", u"张宝茹")
createXls(pmlist, dir, "caiji_"+date, date.replace("_", "-"), u"张志锋")


