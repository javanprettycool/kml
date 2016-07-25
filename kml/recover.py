#coding=utf-8
__author__ = 'Javan'

from placemark import placemark

from kmlparse2 import createKML,createPM
from pyexcel import *
import kmlparse2
from lonlat_util import *
from process import *

formdict = {"0":u"0闯红灯照相",
    "1":u"1测速照相",
    "16":u"16电子监控",
    "7":u"7高清摄像抓拍",
    "2":u"2流动测速",
    "3":u"3区间测速起点",
    "4":u"4区间测速终点",
    "5":u"5高架桥上测速照相",
    "6":u"6区间测速路段",
    "8":u"8桥下闯红灯照相",
    "9":u"9右侧辅道闯红灯照相",
    "10":u"10右侧辅道流动测速区",
    "11":u"11右侧辅道测速照相",
    "45":u"45路口安全提示",
    "46":u"45违规拍照",
    "40":u"40禁止变道",
    "27":u"27加油站",
    "41":u"41铁路道口",
    "42":u"42公交专用车道监控路段",
    "43":u"43临时停车禁止路段",
    "44":u"44压线拍照",
    "17":u"17单行道",
    "18":u"18禁止左转",
    "19":u"19禁止右转",
    "20":u"20禁止掉头",
    "22":u"22落石路段",
    "23":u"23事故多发路段",
    "24":u"24急下坡路段",
    "26":u"26违规稽查路段",
    "32":u"32急转弯路段",
    "33":u"33山区路段",
    "34":u"34冰雪路段",
    "28":u"28收费站",
    "29":u"29休息区",
    "25":u"25高速出口",
    "35":u"35检查站"}


path = "E:/70.kml"


list_tt = kmlparse2.parse_ts_from_device(path)




filename = "gg"

dir = "e:/"

date = "2016-06-27"


list = []
for tt in list_tt:
    tt.form = formdict[tt.form]
    list.append(tt)

createXlsForUpdate(list, filename)





