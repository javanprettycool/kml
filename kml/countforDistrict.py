#coding=utf-8
__author__ = 'Javan'

import os
import re
import xlrd
import xlwt



path = "F:/dataD/2016/"
#print os.path.isdir(path)
#recusiveDir(path)

coordinate = {
    '铁岭市':[123.45,125.1,41.9833,43.3833],
    '上海市':[120.85,122.2,30.6667,31.8833],
    '高平市':[112.6666,113.1666,35.666,36.0],
    '阳江市':[111.2763,112.3641,21.47916,22.6838],
    '衡阳市':[110.5377,113.2755,26.1180,27.4567],
    '武汉市':[113.6994,115.0869,29.9828,31.3703],
    '珠海市':[113.0661,114.3203,21.8161,22.4536],
    '江门市':[111.9994,113.2536,21.4661,22.8536],
    '三明市':[116.3827,118.6536,25.4994,27.1203],
    '永济市':[110.2661,112.0702,34.5994,35.8202],
    '长春市':[124.3161,127.0369,43.0994,45.2536],
    '通辽市':[119.2661,123.7203,42.2661,45.6869],
    '贵阳市':[106.1327,107.2864,26.1994,27.3697],
    '天津市':[116.7327,118.2364,38.5827,40.2531],
    '云南省':[97.5167,106.1833,21.1333,29.25],
    '黑龙江省':[121.183,135.0833,43.4167,53.55],
    '广东省':[109.75,117.334,20.2,25.51],
    '山西省':[110.2494,114.5536,34.5827,40.7203],
    '山东省':[114.3327,122.7203,34.3827,38.3869],
    '河北省':[113.0827,119.8669,36.0327,42.6203],
    '河南省':[110.3661,116.6531,31.3994,36.3827],
    '贵州省':[103.6161,109.5869,24.6327,29.2203],
    '福建省':[115.8494,120.6702,23.5161,28.3702],
    '辽宁省':[118.8994,125.7703,38.7327,43.4369],
    '吉林省':[121.6494,131.3203,40.8827,46.3036],
    '江苏省':[116.3036,121.9661,30.7531,35.3364],
    '江西省':[114.0494,1184703,24.1327,29.1536],
    '浙江省':[118,123,27.2161,31.5203],
    '安徽省':[114.9161,119.6203,29.6864,34.6494],
    '湖北省':[108.3661,116.1327,29.0994,33.3364],
    '湖南省':[],
    '陕西省':[105.4864,111.2661,31.7030,39.5864],
    '甘肃省':[92.2327,108.7697,32.1864,42.9661],
    '台湾省':[119.3036,124.5703,20.7661,25.9369],
    '海南省':[108.6203,111.0994,18.1697,20.1697],
    '四川省':[97.3661,108.5329,26.0661,34.3203],
    '内蒙古':[97.2161,126.0702,37.4161,53.3869],
    '青海省':[89.4161,103.0702  ,314161,39.0703],
    '宁夏':[104.2869,107.6536,35.2494,39.8758],
    '西藏':[78.4167,99.1,26.7333,36.5333],
    '新疆':[],
    '广西壮族自治区':[104.4864,112.0827,20.9161,26.3994]

}

result = {}
for rt, dirs, files in os.walk(path):
    for f in files:
        r1 = re.compile('pnd\S*(\.xls|\.xlsx)|caiji\S*(\.xls|\.xlsx)$')
        if r1.search(f):

            book = xlrd.open_workbook(rt+"/"+f)
            sheet = book.sheet_by_index(0)
            for i in range(3, sheet.nrows):
                if sheet.cell_value(i, 6) != "":
                    longitude = sheet.cell_value(i, 5)
                    latitude = sheet.cell_value(i, 6)
                    handlePerson = sheet.cell_value(i, 12)
                    handleDate = sheet.cell_value(i, 15)
                    if handlePerson == "test_zzf" or handlePerson == "test_zbr":
                        continue
                    #print longitude,latitude,handlePerson,handleDate
                    for k, v in coordinate.items():
                        if len(v) > 0:
                            if v[1] > longitude > v[0] and v[3] > latitude > v[2]:
                                if not result.has_key(k):
                                    person = {}
                                    person[handlePerson] = [handleDate]
                                    result[k] = person
                                    break
                                else:
                                    if not result[k].has_key(handlePerson):
                                        result[k][handlePerson] = [handleDate]
                                    else:
                                        result[k][handlePerson].append(handleDate)
                                    break

print result


wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
isheet = wbk.add_sheet("统计数据", cell_overwrite_ok=True)

isheet.write(0, 1, u"地区")
isheet.write(0, 2, u"采集人")
isheet.write(0, 3, u"时间")

i = 1
for city, handlelist in result.items():
    isheet.write(i, 1, city)
    for handleperson, datelist in handlelist.items():
        isheet.write(i, 2, handleperson)
        datelist = set(datelist)
        datastr = ""
        for date in datelist:
            datastr = datastr + "/ " +date
        isheet.write(i, 3, datastr)
        i = i + 1
    i = i + 1

wbk.save("e:/test.xls")




