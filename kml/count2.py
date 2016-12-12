
#coding=utf-8


__author__ = 'Javan'


import time
import os
import xlrd
import xlwt
import re
from pyexcel import excelobject
from check import checkexcel

month = 11
year = 2016    #改这两个咯

date = str(year) + u"年" + str(month) + u"月"

sheet1_name = date+u"份采集费用补贴（日）统计表"
sheet2_name = date+u"份采集费用补贴（月）统计表"
sheet3_name = date+u"份需补贴采集数据"
dir = u"F:/dataD/"+str(year)+u"/"+str(month)+u"月/"                     #当月所有文件
save_dir = u"F:/dataD/"+str(year)+u"/"+str(month)+u"月/"+date+u"采集费用补贴统计/"
outputfile = save_dir + date + u"采集费用补贴日&月分析表.xls"
account_file_path = u"F:/dataD/采集账号.xls"        #采集账号表                           #最后保存统计excel地址


timeArray = time.localtime(time.time())
otherStyleTime = time.strftime("%Y-%m-%d", timeArray)


wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
isheet1 = wbk.add_sheet(sheet1_name, cell_overwrite_ok=True)
isheet2 = wbk.add_sheet(sheet2_name, cell_overwrite_ok=True)
isheet3 = wbk.add_sheet(sheet3_name, cell_overwrite_ok=True)
row_index = 1

filename = "down"
dict = {"0":u"0闯红灯照相",
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
    "29":u"休息区",
    "25":u"25高速出口",
    "35":u"35检查站"}

def formatDate(time):
    time = str(time)
    return time[:4] + "-" + time[4:6] + "-" + time[6:8]

def walkdir(dir, pattern, callback, *args):
	for f in os.listdir(dir):
		d = os.path.join(dir, f)
		if os.path.isfile(d) and re.match(pattern, f):
			callback(d, *args)
		elif os.path.isdir(d):
			walkdir(d, pattern, callback, *args)

def create_uni_excel(sheet_name, time_list):
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    isheet1 = wbk.add_sheet(sheet_name, cell_overwrite_ok=True)
    isheet2 = wbk.add_sheet(sheet_name+u"(日)", cell_overwrite_ok=True)
    i = 0
    for t in time_list:
        isheet1.col(i).width = 3333
        isheet1.col(i).height = 3333
        isheet1.write(0, i, t)
        i += 1
    isheet2.write(1, 1, u"采集账号")
    isheet2.write(1, 2, u"补贴金额（单位：/元）")
    isheet2.write(1, 3, u"合计（单位：/元）")

    return wbk

def parseExcel(dir, mandict):
	if not checkexcel(dir):             #base check for data
		exit()

	global row_index
	book = xlrd.open_workbook(dir)
	sheet = book.sheet_by_index(0)
	for i in range(3, sheet.nrows):
		if sheet.cell_value(i, 4) != "":
			type = re.findall(r'[0-9]{1,2}', sheet.cell_value(i, 4))
		if sheet.ncols >= 19 and sheet.cell_value(i,18) != "" and sheet.cell_value(i, 12) != "ZZF" \
			and sheet.cell_value(i, 12) != "test_zzf"  \
			and sheet.cell_value(i, 12) != "test_zbr" \
			and (type[0] == u"0" or type[0] == u"1" or type[0] == u"16" or type[0] == u"7" or type[0] == u"2" \
			or type[0] == u"8" or type[0] == u"9" or type[0] == u"3" or type[0] == u"4" or type[0] == u"6" \
			or type[0] == u"5" or type[0] == u"11" or type[0] == u"10"):
			eo = excelobject()
			eo.handletype = sheet.cell_value(i, 1)
			eo.form = dict[type[0]]
			eo.upman = sheet.cell_value(i, 12).lower()
			#eo.time = time.strftime("%Y-%m-%d",time.strptime(sheet.cell_value(i, 15), '%Y-%m-%d'))
			ti = os.path.split(dir)[1].replace('.xls', '').split('(')[0]
			eo.time = time.strftime("%Y-%m-%d",time.strptime(ti[ti.find('_')+1:], '%Y_%m_%d'))
			timeset.add(int(eo.time.replace("-", "")))
			isheet3.write(row_index, 0, eo.handletype, n_style)
			isheet3.write(row_index, 1, eo.form, n_style)
			isheet3.write(row_index, 2, eo.upman, n_style)
			isheet3.write(row_index, 3, eo.time, n_style)
			isheet3.write(row_index, 4, "1", n_style)
			row_index += 1
			if eo.upman in mandict:
				if eo.handletype in mandict[eo.upman]:
					if eo.form in mandict[eo.upman][eo.handletype]:
						if eo.time in mandict[eo.upman][eo.handletype][eo.form]:
							mandict[eo.upman][eo.handletype][eo.form][eo.time] += 1
						else:
						   mandict[eo.upman][eo.handletype][eo.form][eo.time] = 1
					else:
						mandict[eo.upman][eo.handletype][eo.form] = {}
						mandict[eo.upman][eo.handletype][eo.form][eo.time] = 1
				else:
					mandict[eo.upman][eo.handletype] = {}
					mandict[eo.upman][eo.handletype][eo.form] = {}
					mandict[eo.upman][eo.handletype][eo.form][eo.time] = 1
			else:
				mandict[eo.upman] = {}
				mandict[eo.upman][eo.handletype] = {}
				mandict[eo.upman][eo.handletype][eo.form] = {}
				mandict[eo.upman][eo.handletype][eo.form][eo.time] = 1




#header style setting
header_style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'
font.bold = True
font.colour_index = 0
header_style.font = font

alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER
header_style.alignment = alignment

pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 23
header_style.pattern = pattern

borders = xlwt.Borders()
borders.left = xlwt.Borders.THIN
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
header_style.borders = borders


#sum style setting
sum_style = xlwt.XFStyle()
font = xlwt.Font()
font.bold = True
font.colour_index = 2
font.height = 0x00CF
sum_style.font = font

pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 11
sum_style.pattern = pattern

borders = xlwt.Borders()
borders.left = xlwt.Borders.THIN
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
sum_style.borders = borders

#normal style
n_style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'
font.colour_index = 0
n_style.font = font

borders = xlwt.Borders()
borders.left = xlwt.Borders.THIN
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
n_style.borders = borders

alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER
n_style.alignment = alignment




row = 0
alllist = []
timeset = set()
accountset = set()
mandict = {}

walkdir(dir, r'pnd|caiji', parseExcel, mandict)


#sheet1  making
timelist = list(timeset)
timelist.sort()

isheet1.write(0, 0, u"上报人", header_style)
isheet1.write(0, 1, u"操作类型", header_style)
isheet1.write(0, 2, u"狗类型", header_style)
isheet1.col(0).width = 3500
isheet1.col(2).width = 3700

#sheet2 making
isheet2.write(0, 0, u"上报人", header_style)
isheet2.write(0, 1, u"操作类型", header_style)
isheet2.write(0, 2, u"狗类型", header_style)
isheet2.write(0, 3, u"合计（数量）", header_style)
isheet2.write(0, 4, u"合计（费用）", header_style)
isheet2.col(0).width = 3500
isheet2.col(1).width = 3600
isheet2.col(2).width = 3600
isheet2.col(3).width = 3600
isheet2.col(4).width = 3600


i = 3
new = map(formatDate, timelist)
for t in new:
    isheet1.col(i).width = 3333
    isheet1.col(i).height = 3333
    isheet1.write(0, i, t, header_style)
    i += 1

isheet1.write(0, i, u"合计（数量）", header_style)
isheet1.write(0, i+1, u"合计（费用）", header_style)
isheet1.col(i).width = 3600
isheet1.col(i+1).width = 3600





sumdict = {}
finalcost = 0
cost = 0
count = 0
row = 0
timeindex = 3
for k1 in mandict:
    row += 1
    m_start = row
    for k2 in mandict[k1]:  #handletype
        h_start = row
        for k3 in mandict[k1][k2]:      #form
            isheet1.write(row, 2, k3, n_style)
            isheet2.write(row, 2, k3, n_style)
            for k4 in mandict[k1][k2][k3]:     #time
                for t in timelist:
                    t = str(t)
                    t = t[:4] + "-" + t[4:6] + "-" + t[6:8]
                    if t == k4:
                        count += mandict[k1][k2][k3][k4]
                        isheet1.write(row, timeindex, mandict[k1][k2][k3][k4])  #everyday sum of handletype
                        if timeindex in sumdict:
                            sumdict[timeindex] += mandict[k1][k2][k3][k4]
                        else:
                            sumdict[timeindex] = mandict[k1][k2][k3][k4]
                    timeindex += 1
                timeindex = 3
            isheet1.write(row, i, count)   #the client sum of every handletype
            isheet2.write(row, 3, count)
            if k3 == u"16电子监控":
                if k2 == u"1新增":
                    cost += count*5
                    isheet1.write(row, i+1, count*5)
                    isheet2.write(row, 4, count*5)
                elif k2 == u"2修改":
                    pass
                elif k2 == u"3删除":
                    pass
            else:
                cost += count*10
                isheet1.write(row, i+1, count*10)  #the money of every handletype
                isheet2.write(row, 4, count*10)
            count = 0
            row += 1
        isheet1.write_merge(h_start, row-1, 1, 1, k2, n_style)
        isheet2.write_merge(h_start, row-1, 1, 1, k2, n_style)
    isheet1.write_merge(m_start, row-1, 0, 0, k1, n_style)     #sheet1
    isheet1.write(row, 0, "合计", sum_style)
    isheet2.write_merge(m_start, row-1, 0, 0, k1, n_style)     #sheet2
    isheet2.write(row, 0, "合计", sum_style)
    for x in range(1, i+1):
        isheet1.write(row, x, "", sum_style)
    for x in range(1, 3):
        isheet2.write(row, x, "", sum_style)
    isheet1.write(row, i+1, cost, sum_style)
    isheet2.write(row, 4, cost, sum_style)
    finalcost += cost
    cost = 0
    countsum = 0
    for k,v in sumdict.items():                              #数量合计,sumdict存每个操作对应的数量
        isheet1.write(row, k, v, sum_style)
        countsum += v
        isheet1.write(row, i, countsum, sum_style)
        isheet2.write(row, 3, countsum, sum_style)
    sumdict.clear()


isheet1.write(row+1, 0, "总计（费用）", sum_style)
isheet1.write(row+1, i+1, finalcost, sum_style)
isheet2.write(row+1, 0, "总计（费用）", sum_style)
isheet2.write(row+1, 4, finalcost, sum_style)






#sheet3  making


isheet3.write(0, 0, u"操作类型", header_style)
isheet3.write(0, 1, u"狗类型", header_style)
isheet3.write(0, 2, u"上报人", header_style)
isheet3.write(0, 3, u"时间", header_style)
isheet3.write(0, 4, u"数量", header_style)
isheet3.col(0).width = 3500
isheet3.col(1).width = 3700
isheet3.col(2).width = 3600
isheet3.col(3).width = 3600
isheet3.col(4).width = 3600


if not os.path.exists(save_dir):
	os.mkdir(save_dir)

wbk.save(outputfile)


##生成统计excel

def parse_account(path=""):

	if path == "":
		return

	data = xlrd.open_workbook(path, formatting_info=True)

	table = data.sheets()[0]

	detail = []

	for i in range(1, table.nrows):
		row = table.row_values(i)
		if row[0] == "":
			for crange in table.merged_cells:
				rlo, rhi, clo, chi = crange
				if rlo < i < rhi and clo == 0:
					row[0] = table.cell_value(rlo, clo)
					break
		if row[2] == "":
			for crange in table.merged_cells:
				rlo, rhi, clo, chi = crange
				if rlo < i < rhi and clo == 2:
					row[2] = table.cell_value(rlo, clo)
					break
		detail.append(row)

	return detail


def get_header_style():
	header_style = xlwt.XFStyle()
	font = xlwt.Font()
	font.bold = True
	font.colour_index = 0
	header_style.font = font

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	alignment.vert = xlwt.Alignment.VERT_CENTER
	header_style.alignment = alignment

	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = 23
	header_style.pattern = pattern

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	header_style.borders = borders
	return header_style


def get_footer_style():
	footer_style = xlwt.XFStyle()
	font = xlwt.Font()
	font.bold = True
	font.colour_index = 2
	font.height = 0x00CF
	footer_style.font = font

	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = 11
	footer_style.pattern = pattern

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	footer_style.borders = borders
	return footer_style



def get_form_style():
	n_style = xlwt.XFStyle()
	font = xlwt.Font()
	font.colour_index = 0
	n_style.font = font

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	n_style.borders = borders

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	alignment.vert = xlwt.Alignment.VERT_CENTER
	n_style.alignment = alignment
	return n_style


def get_normal_style():
	n_style = xlwt.easyxf('font:height 280;')

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	n_style.borders = borders

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	alignment.vert = xlwt.Alignment.VERT_CENTER
	n_style.alignment = alignment
	return n_style



path = outputfile

workbook = xlrd.open_workbook(path)
sheet = workbook.sheet_by_index(0)


i = 0
j = 0
t = 0
start = 1
company = ""
name = ""
date_list = []
isChanging = ""


day = 0
for t in range(3, sheet.ncols):
	if sheet.cell_value(0, t) == u"合计（数量）":
		break
	date_list.append(sheet.cell_value(0, t))
	day += 1


detail = parse_account(account_file_path)
for i in range(1, sheet.nrows):
	if sheet.cell_value(i, 0) == u"总计（费用）":
		break
	if sheet.cell_value(i, 0) != "" and sheet.cell_value(i, 0) != u"合计":
		account = sheet.cell_value(i, 0).strip()
		for row in detail:
			catch = 0
			if account.lower().split("_")[0] == "dfy":
				company = u"东方云"
				name = account
				catch = 1
				break
			if account.lower() == row[1] or account.upper() == row[1]:
				company = row[0]
				name = row[2]
				isChanging = u"(不计费)" if row[6] else u""
				catch = 1
				break

		if catch != 1:
			print account+u" 未找到采集账号信息"

		if company == "" and name != "":
			title = name
		elif name == "" and company != "":
			title = company
		elif company == "" and name == "":
			title = account
		else:
			title = company+"-"+name
		company = ""
		name = ""
		#print title, account
		wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
		isheet1 = wbk.add_sheet(title, cell_overwrite_ok=True)
		isheet2 = wbk.add_sheet(title+u"(日)", cell_overwrite_ok=True)

		isheet1.write(1, 1, u"采集账号", get_normal_style())
		isheet1.write(1, 2, u"补贴金额（单位：/元）", get_normal_style())
		isheet1.write(1, 3, u"合计（单位：/元）", get_normal_style())
		start = 1
	for j in range(0, sheet.ncols):
		if sheet.cell_value(i, 0) == u"合计":
			isheet2.write(start, j, sheet.cell_value(i, j), get_footer_style())
		else:
			isheet2.write(start, j, sheet.cell_value(i, j), get_form_style())
	start += 1
	if sheet.cell_value(i, 0) == u"合计":
		sum = sheet.cell_value(i, day+4)

		isheet1.write(2, 0, title, get_normal_style())
		isheet1.write(2, 1, account, get_normal_style())
		isheet1.write(2, 2, sum, get_normal_style())
		isheet1.write(2, 3, sum, get_normal_style())
		isheet1.write_merge(0, 0, 0, 3, date+u"份<"+title+u">采集补贴(共"+str(sum)+u"元)", get_normal_style())
		isheet1.col(0).width = 6000
		isheet1.col(1).width = 6000
		isheet1.col(2).width = 8000
		isheet1.col(3).width = 6000

		num = 0
		for i, col in enumerate(sheet.row_values(0)):
			isheet2.write(0, i, col, get_header_style())
		isheet2.col(0).width = 3600
		isheet2.col(2).width = 3800
		isheet2.write_merge(1, start-2, 0, 0, account, get_normal_style())

		wbk.save(save_dir + isChanging + date + u"份采集费用补贴（" + title + u"）.xls")
		isChanging = ""
