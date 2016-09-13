#coding=utf-8
from placemark import placemark
import time
import xlrd
import re
import kmlparse2
from process import *
#from fuckgd import check_match



gd = placemark()
ob = placemark()

gd.longitude = 114.215440
gd.latitdue = 22.604880
gd.heading = 326
ob.longitude = 114.216000
ob.latitdue = 22.605160
ob.heading =

print getDist2(gd.longitude,gd.latitude,ob.longitude,ob.latitude)
#print check_match(gd, ob, 100, 20, True)


exit()



dir = u"F:\dataD\高速\G25长深高速4\G25长深高速4.xls"
#path = unicode(dir,  "utf8")

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


