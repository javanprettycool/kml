#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

path = u"F:/dataD/投诉/处理/0913投诉/矩形txt-09月-22日-2016-S212_安仁县到郴州60改80_1026_tt_0922.kml"
path = path.replace("\\","/")


list_tt, re_list = kmlparse2.parse_ts(path)

list = []
for p in list_tt:
    # if 122.108330 > p.longitude > 122.017231 and 46.051130 < p.latitude < 46.088154:
    #     if (p.form == u"红灯" or p.form == u"测速") and p.speedlimit == 50 :
    #         p.speedlimit = 70
    #         list.append(p)
    # else:
    #     if p.form == u"红灯" and p.speedlimit == 40 :
    #         p.speedlimit = 70
    #         list.append(p)

    if p.form == u"1测速照相" and p.speedlimit <= 70:
        p.speedlimit = 70
        # if p.form == u"违规稽查" or p.form == u"事故多发" or p.form == u"禁止掉头":
        #     continue
        # elif p.form == u"红灯":
        #     p.form = u"0闯红灯拍照"
        # elif p.form == u"测速":
        #     p.form = u"1测速照相"
        # elif p.form == u"辅道测速照相":
        #     p.form = u"11右侧辅道测速照相"
        # elif p.form == u"高速出口":
        #     p.form = u"25高速出口"
        # elif p.form == u"收费站":
        #     p.form = u"28收费站"
        # elif p.form == u"急转弯":
        #     p.form = u"32急转弯路段"
        # elif p.form == u"休息区":
        #     p.form = u"29休息区"
        list.append(p)
print len(list)


filename = "tousu"

dir = "e:/"

date = "2016-09-23"

createXlsForUpdate(list, filename)





