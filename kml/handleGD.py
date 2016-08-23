#coding=utf-8

__author__ = 'javan'

#处理导出的
import kmlparse2
from pyexcel import *
from process import *


EXT = ".kml"

date = "2016-08-17"

dir = u"F:\dataD\高速\G25长深高速"  #改这个

dir = dir.replace("\\","/")

if dir[-1] != "/":
    dir+="/"

pnd_filename = u"矩形txt-08月-17日-2016-(G25长深高速)109KM四平市双辽市卧虎镇大富村--沈阳市康平县两家子乡聂家窝堡村2_tt_0817"
done_filename = u"local2"

pmlist = []

kml_path = dir + pnd_filename + EXT
done_path = dir + done_filename + EXT

kml_list = kmlparse2.parse_ts(kml_path)
done_list = kmlparse2.parse_ts(done_path)

copy_kml = [x for x in kml_list]

for p in kml_list:
    for q in done_list:
        if p.name == q.name:
            copy_kml.remove(p)


for p in copy_kml:
    if p.form == u"违规稽查" or p.form == u"事故多发" or p.form == u"禁止掉头":
        continue
    elif p.form == u"红灯":
        p.form = u"0闯红灯拍照"
    elif p.form == u"测速":
        p.form = u"1测速照相"
    elif p.form == u"辅道测速照相":
        p.form = u"11右侧辅道测速照相"
    elif p.form == u"高速出口":
        p.form = u"25高速出口"
    elif p.form == u"收费站":
        p.form = u"28收费站"
    elif p.form == u"急转弯":
        p.form = u"32急转弯路段"
    elif p.form == u"休息区":
        p.form = u"29休息区"
    elif p.form == u"加油站":
        p.form = u"27加油站"
    elif p.form == u"电子监控":
        p.form = u"16电子监控"
    elif p.form == u"高清摄像":
        p.form = u"7高清摄像"
    elif p.form == u"流动测速":
        p.form = u"2流动测速"
    pmlist.append(createElement("delete", p, "by_gd_zzf"))


#exit()
createXls(pmlist, dir, done_filename+"_"+date, date, u"张志锋")


















