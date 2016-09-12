#coding=utf-8
from placemark import placemark
import time
import xlrd
import re
import kmlparse2







dir = u"F:\dataD\高速\G1113丹阜高速\G1113丹阜高速.xls"
#path = unicode(dir,  "utf8")

filename = u"G1113丹阜高速_test"

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


