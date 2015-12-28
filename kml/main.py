#coding=utf-8

import re
from lonlat_util import getLalong,getDist,getDist2
from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
import codecs
from lxml import etree
from process import *


list = []
redlightlist = []
speedmeasurelist = []
rightlist = []
leftlist = []
alllist = []
log = []
dog_list = []

left_list = [] #除新增剩下的点
pm_list = []
handle_list = []  #新增的点
id_for_fee_list = [] #记录算费用的采集id

date = "2015-12-16"
dir =  u"E:/dataD/2015/12月/1216/"
path = u"E:/dataD/2015/12月/1216/PNDCJ_2015_12_16_22pm.kml"
docname = u'PND\u91c7\u96c6[12_16_21-00 ~ 12_16_ 20-59]'
fodername = u'PND\u91c7\u96c6[12_16_21-00 ~ 12_16_ 20-59]'


list, dog_list = kmlparse2.parse_pnd(path)


# del_set = proc_del(newlist, doglist, 30)
#
# for g in del_set:
# 	str = ""
# 	for s in g.matchlist:
# 		str = str + s + ":"
# 	g.name = str + g.name


id_for_fee_list = operate(list, left_list, handle_list)

print len(list), len(left_list), len(handle_list), len(dog_list)

for pm in handle_list:
	pm_list.append(createPM(pm))


doc = createKML(docname, fodername, pm_list)

#生成新增类型的kml
output_file = codecs.open(dir + "pnd_test.kml", "w")
output_file.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
output_file.close()

#剩下的生成excel
createXls(left_list, dir, "pnd_test", "2015-12-16")

#费用id表
createXlsForFee(id_for_fee_list, dir)

#原狗id表
createXlsForDog(dog_list, dir)

#生成剩余的kml
left_list.extend(dog_list)
pm_list = []
for pm in left_list:
	pm_list.append(createPM(pm.name, True if pm.match != "?" or pm.match == " " else False, pm.longitude, pm.latitude, pm.heading))

doc = createKML(docname, fodername, pm_list)
output_file = codecs.open(dir + "pnd_test_left.kml", "w")
output_file.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
output_file.close()
