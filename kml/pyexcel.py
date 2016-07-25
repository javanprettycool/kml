#coding=utf-8
__author__ = 'Tiny'

import xlrd
import xlwt
import time
import sys
import os
from placemark import *

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

handletypedict = {
    "1":u"1新增",
    "2":u"2修改",
    "3":u"3删除"
}


class excelobject(object):
     def __init__(self, name="", dogtype="", id="", form="", handletype="",match ="",longitude=0, latitude=0, heading=0, speedlimit=0, account="", time="", cost="", upman=""):
        self.name = name
        self.dogtype = dogtype
        self.id = id
        self.form = form
        self.match = match
        self.matchlist = []
        self.handletype = handletype
        self.longitude = longitude
        self.latitude = latitude
        self.heading = heading
        self.speedlimit = speedlimit
        self.account = account
        self.time = time
        self.cost = cost
        self.upman = upman



def setTableStyle(table):

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'SimSun'
    font.bold = True
    font.colour_index = 1
    style.font = font

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 23
    style.pattern = pattern

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    style.borders = borders

    table.write_merge(0, 2, 0, 0, u'编号', style) # Merges row 0's columns 0 through 3.
    table.write(0, 1, "", style)
    table.write_merge(1, 2, 1, 1, u'操作类型', style) # Merges row 1 through 2's columns 0 through 3.
    table.write_merge(0, 0, 2, 10, u'电子狗属性', style)
    table.write_merge(1, 2, 2, 2, u'采集ID', style)
    table.write_merge(1, 2, 3, 3, u'狗ID', style)
    table.write_merge(1, 2, 4, 4, u'狗类型', style)
    table.write_merge(1, 1, 5, 6, u'位置', style)
    table.write(2, 5, u'经度', style)
    table.write(2, 6, u'纬度', style)
    table.write_merge(1, 1, 7, 9, u'角度', style)
    table.write(2, 7, u'起始角度经度', style)
    table.write(2, 8, u'起始角度纬度', style)
    table.write(2, 9, u'度数', style)
    table.write_merge(1, 2, 10, 10, u'限速', style)
    table.write_merge(0, 2, 11, 11, u'大概位置说明', style)
    table.write_merge(0, 2, 12, 12, u'上报人', style)
    table.write_merge(0, 2, 13, 13, u'时间', style)
    table.write_merge(0, 2, 14, 14, u'操作人', style)
    table.write_merge(0, 2, 15, 15, u'时间', style)
    table.write_merge(0, 2, 16, 16, u'确认人', style)
    table.write_merge(0, 2, 17, 17, u'时间', style)
    table.col(3).width = 4000
    table.col(4).width = 3333
    table.col(5).width = 3333
    table.col(6).width = 3333
    table.col(7).width = 3333
    table.col(8).width = 3333
    table.col(11).width = 3333
    table.col(15).width = 3333



def createXls(datalist, dir, filename="test", date="", operator_name=u"张志锋"):
    if not datalist:
        print "no data today"
        return
    file = xlwt.Workbook()
    timeArray = time.localtime(time.time())
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

    table = file.add_sheet(u'采集数据', cell_overwrite_ok=True)
    setTableStyle(table)

    i = 3
    for pm in datalist:
        if checkForList(pm):
            table.write(i, 1, gethandletype(pm.handletype))
            table.write(i, 2, pm.id)
            table.write(i, 3, pm.match if pm.handletype != '1' else '')
            table.write(i, 4, getform(pm.form) if getform(pm.form) else pm.form)
            table.write(i, 5, "%.6f" % pm.longitude)
            table.write(i, 6, "%.6f" % pm.latitude)
            table.write(i, 9, pm.heading)
            table.write(i, 10, pm.speedlimit if int(pm.speedlimit) < 150 else "0")   #去掉那些bug限速
            table.write(i, 12, pm.account)
            table.write(i, 13, date.split("-")[1]+u"月")
            table.write(i, 14, operator_name)
            table.write(i, 15, date)
            table.write(i, 18, pm.cost)
        else:
            sys.exit()
        i += 1
    file.save(dir+"/"+filename+".xls")

def createXlsForDel(dataSet, filename="test"):
    if not dataSet:
        print "no del data"
        return
    font = xlwt.Font()
    font.name = 'SimSun'
    style = xlwt.XFStyle()
    style.font = font
    file = xlwt.Workbook()
    table = file.add_sheet(u'采集数据', cell_overwrite_ok=True)
    timeArray = time.localtime(time.time())
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    setTableStyle(table)

    i = 3
    for pm in dataSet:
        for m in pm.matchlist:
            table.write(i, 1, gethandletype(pm.handletype))
            table.write(i, 2, pm.id)
            table.write(i, 3, m)
            table.write(i, 4, getform(pm.form))
            table.write(i, 13, u"3月")
            table.write(i, 14, u"张志锋")
            table.write(i, 15, otherStyleTime)
            i += 1
    file.save('e:/file.xls'.replace("file", filename))


def createXlsForUpdate(dataSet, filename="test"):
    if not dataSet:
        print "no update data"
        return
    font = xlwt.Font()
    font.name = 'SimSun'
    style = xlwt.XFStyle()
    style.font = font
    file = xlwt.Workbook()
    table = file.add_sheet(u'采集数据', cell_overwrite_ok=True)
    timeArray = time.localtime(time.time())
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    setTableStyle(table)

    i = 3
    for pm in dataSet:
        table.write(i, 1, u"2修改")
        table.write(i, 3, pm.match)
        table.write(i, 5, "%.6f" % pm.longitude)
        table.write(i, 6, "%.6f" % pm.latitude)
        table.write(i, 4, pm.form)
        table.write(i, 9, pm.heading)
        table.write(i, 10, pm.speedlimit if int(pm.speedlimit) < 150 else "0")   #去掉那些bug限速
        table.write(i, 12, u"test_zzf")
        table.write(i, 13, u"06月")
        table.write(i, 14, u"张志锋")
        table.write(i, 15, otherStyleTime)
        i += 1
    file.save('e:/file.xls'.replace("file", filename))


def createXlsForFee(list, dir, filename="id_for_fee"):
    if not list:
        print "no data today"
        return

    table = xlwt.Workbook()

    sheet = table.add_sheet(u'费用id', cell_overwrite_ok=True)

    i = 0
    for p in list:
        sheet.write(i, 0, p)
        i += 1
    table.save(dir+"/"+filename+".xls")

def createXlsForDog(list, dir, filename="dog_detail"):
    if not list:
        print "no dog data"
        return

    table = xlwt.Workbook()

    sheet = table.add_sheet(u'费用id', cell_overwrite_ok=True)

    i = 0
    for p in list:
        sheet.write(i, 0, p.id)
        sheet.write(i, 1, p.longitude)
        sheet.write(i, 2, p.latitude)
        sheet.write(i, 3, p.heading)
        sheet.write(i, 4, p.speedlimit)
        sheet.write(i, 5, p.form)
        sheet.write(i, 6, p.matched)
        i += 1
    table.save(dir+"/"+filename+".xls")

def readDogIdFromExcel(file):
    if not os.path.exists(file):
        print "dog_detail.xls不存在"
        return []
    doglist = []
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    for row in range(0, table.nrows):
        dog = placemark()
        dog.id = table.row_values(row)[0]
        dog.longitude = table.row_values(row)[1]
        dog.latitude = table.row_values(row)[2]
        dog.heading = table.row_values(row)[3]
        dog.speedlimit = table.row_values(row)[4]
        dog.form = table.row_values(row)[5]
        #dog.matched = table.row_values(row)[6]
        doglist.append(dog)
    return doglist

def readFeeFromExcel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    return table.col_values(0)

def getform(num):
    global formdict
    num = str(num)
    if num in formdict:
        return formdict[num]
    else :
        return None

def gethandletype(num):
    global handletypedict
    if num is "":
        return None
    return handletypedict[num]


def checkForList(pm):
    if isinstance(pm, placemark):
        if pm.handletype == "2" or pm.handletype == "3":
            if pm.match == "?" or pm.match == "":
                print u"没有匹配的点(匹配为?)：" + pm.name
                return False
            else:
                return True
        else:
            return True
    else:
        return False

