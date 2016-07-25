#coding=utf-8

__author__ = 'javan'


import kmlparse2
from pyexcel import *
from process import *


EXT = ".kml"

date = "2016-07-21"

dir = u"F:/dataD/高速/G1111伊绥高速采集处理20160720/G1111伊绥高速采集处理20160720/"  #改这个
pnd_filename = u"矩形txt-07月-20日-2016-(G1111伊绥高速)126KM绥化市北林区宝山镇林场村--伊春市铁力市朗乡林业局建设经营所1_tt_0720"
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
    pmlist.append(createElement("delete", p, "test_zzf"))


#exit()
createXls(pmlist, dir, "local2_"+date, date, u"张志锋")


















