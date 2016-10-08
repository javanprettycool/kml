#coding=utf-8
from placemark import placemark
import time
import xlrd
import re
import kmlparse2
from process import *
#from fuckgd import check_match

# def test(a, callback, *avg):
# 	print a
# 	callback(*avg)
#
#
# def gg(*a):
# 	for s in a:
# 		print s
#
# test('test', gg, 'gg', 'haha')
# exit()
#
# def walkdir(dir, pattern):
# 	for f in os.listdir(dir):
# 		d = os.path.join(dir, f)
# 		if os.path.isfile(d) and re.match(pattern, f):
# 			yield d
# 		elif os.path.isdir(d):
# 			walkdir(d, pattern)
#
# for p in walkdir(path, r"pnd|caiji"):
# 	print p
# exit()



dir = u"F:\dataD\高速\G25长深高速4\caiji_2016_09_01(1).xls"
#path = unicode(dir,  "utf8")
a = os.path.split(dir)[1].replace('.xls', '').split('(')[0]
print a[a.find('_')+1:]
exit()

filename = u"G25长深高速4_test"

pm_list = []
book = xlrd.open_workbook(dir)
sheet = book.sheet_by_index(0)
for i in range(3, sheet.nrows):
	if sheet.ncols >= 18:
		pm = placemark()
		pm.id = sheet.cell_value(i, 3)
		type = re.findall(r'[0-9]{1,2}', sheet.cell_value(i, 4))
		pm.form = pm.get_type(type.pop() if type else sheet.cell_value(i, 4))
		pm.handletype = sheet.cell_value(i, 1)
		pm.account = sheet.cell_value(i, 12).lower()
		pm.create_time = time.strftime("%Y-%m-%d",time.strptime(sheet.cell_value(i, 15), '%Y-%m-%d'))
		pm.longitude = float(sheet.cell_value(i, 5))
		pm.latitude = float(sheet.cell_value(i, 6))
		pm.heading = sheet.cell_value(i, 9)
		pm.speedlimit = sheet.cell_value(i, 10)
		pm.name = pm.handletype+"_"+str(pm.id)+"_"+str(pm.form)+"_"+str(pm.heading)+"_"+str(pm.speedlimit)
		pm_list.append(kmlparse2.createPM(pm))

kmlparse2.output_file(pm_list, filename, filename, dir + filename + ".kml")


