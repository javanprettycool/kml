#coding=utf-8

__author__ = 'javan'

#处理导出的
import kmlparse2
from pyexcel import *
from process import *
import re
import os


EXT = ".kml"

date = "2016-09-08"

dir = u'F:\dataD\高速\G2京沪高速4'  #改这个

operator_name = "gd_test_zzf"

filename = os.path.split(dir)[-1]

dir = dir.replace("\\","/")

if dir[-1] != "/":
    dir+="/"

#读文件

def parsefile(dir):
	file_dict = {}
	for i in os.listdir(dir):
		if os.path.isfile(os.path.join(dir,i)):
			if i.find('矩形txt') >= 0:
				tt_filename = i
				file_dict[tt_filename] = []
				start = tt_filename.split('KM')[1].split('--')[0]
				destination = tt_filename.split('KM')[1].split('--')[1].split('_')[0]
				pattern = re.compile(r"\d")
				destination = pattern.subn('', destination)[0]

				for f in os.listdir(dir):
					if os.path.isfile(os.path.join(dir,f)):
						gd_file1 = start + "--" + destination
						gd_file2 = destination + "--" + start
						if (f.find(gd_file1) >= 0 or f.find(gd_file2) >= 0) and f.find('矩形txt') < 0:
							file_dict[tt_filename].append(f)
	return file_dict

def cmp_pm(pm1, pm2):
	if not (isinstance(pm1, placemark) and isinstance(pm2, placemark)):
		return False

	if pm1.latitude > pm2.latitude and pm1.longitude > pm2.longitude:
		return 1
	if pm1.latitude < pm2.latitude and pm1.longitude < pm2.longitude:
		return -1
	return 0


def check_match(target, o, distance, offset):
	if checkDistance(target, o, distance):
		if (0 <= target.heading < offset and (0 <= o.heading < target.heading+offset or (target.heading-offset)%360 < o.heading <= 360)) \
			or (360-offset < target.heading <= 360 and (0 <= o.heading < (target.heading+offset) % 360 or target.heading-offset < o.heading <= 360)) \
			or (target.heading-offset < o.heading < target.heading+offset):
			return True
	return False

def handle_gd(handle_list, gd_list, distance=50, offset=20):
	if not handle_list:
		return False

	del_list = []           #final ouput the del server point in need

	#step 1: del 2013 which not match gd
	for pm in handle_list[:]:
		if pm.dogtype == 'server' and (pm.form == u'1测速照相' or pm.form == u'7高清摄像' or pm.form == u'16电子监控') and int(pm.create_time.split("-")[0]) <= 2013:
			to_del = True
			for gd in gd_list:
				if check_match(pm, gd, distance, offset) or check_match(pm, gd, distance*2, offset):     #100m
					to_del = False
					break
			if to_del:
				handle_list.remove(pm)
				del_list.append(pm)

		#del the other type
		if pm.dogtype == 'server' and (pm.form != u'1测速照相' and pm.form != u'7高清摄像' and pm.form != u'16电子监控'):
			handle_list.remove(pm)
			continue


	#step 2: del dul
	i = 0
	while i < len(handle_list):
		pm = handle_list[i]
		j = i + 1
		while j < len(handle_list):
			ob = handle_list[j]
			if pm.id != ob.id and pm.form == ob.form and pm.speedlimit == ob.speedlimit and check_match(pm, ob, distance, offset):
				handle_list.remove(ob)
				del_list.append(ob)
				j -= 1
			j += 1
		i += 1


	#step 3:handle gd
	gd_del_list = []
	for pm in handle_list[:]:
		for gd in gd_list[:]:
			if check_match(pm, gd, distance, offset) or check_match(pm, gd, distance*2, offset):
				if pm.account[0].lower() == 'k':             #留下采集人的点
					gd_list.remove(gd)
					#handle_list.remove(pm)
					gd_del_list.append(gd)
				elif pm.form == gd.form and pm.speedlimit != gd.speedlimit:    #相对类型一样限速不同，留高德
					handle_list.remove(pm)
					del_list.append(pm)
					gd.copy(pm)            # 将后台点的坐标付给高德，防止因为高德采集的偏移
				else:									#其他的，不采纳高德，也不修改后台的
					#handle_list.remove(pm)    #匹到不同类型的点限速相同或者不同，删除
					gd_list.remove(gd)
					gd_del_list.append(gd)
				break

	handle_list.extend(gd_list)

	return handle_list, del_list, gd_del_list


	# tmp_list = handle_list[:]
	# final_list = handle_list[:]
	#
	# for pm in handle_list:
	# 	#step 2: remove match pm and gd
	# 	target = pm
	# 	del_L = []  #del after loop
	# 	alone = True
	# 	clear = False
	# 	if pm.dogtype == 'server':
	# 		#pm in tmp_list and tmp_list.remove(pm)
	# 		for o in tmp_list:
	# 			if o.dogtype == 'server':
	# 				if target.form == o.form and target.speedlimit == o.speedlimit and check_match(target, o, distance, offset):  #50m match
	# 					del_L.append(o)
	# 					tt_del_list.append(o)
	# 					final_list.remove(o)
	# 					clear = True
	# 					alone = False
	# 				elif alone and getDist2(target.longitude, target.latitude, o.longitude, o.latitude) < distance+50: 	#del alone point < 100m not match
	# 					clear = True
	#
	# 			if o.dogtype == 'gd' and check_match(target, o, distance, offset):
	# 				clear = True
	# 				if target.account[0].lower() == 'k':
	# 					del_L.append(o)
	# 				elif target.form == o.form and target.speedlimit != o.speedlimit:
	# 					tt_del_list.append(target)
	# 				else:
	# 					del_L.append(o)
	#
	#
	# 		if clear:
	# 			final_list.remove(target)
	# 			tmp_list.remove(target)
	#
	# 		#del the match point
	# 		for p in del_L:
	# 			p in tmp_list and tmp_list.remove(p)
	#
	#
	# for o in tt_del_list:
	# 	o in final_list and final_list.remove(o)
	#
	# return final_list, tt_del_list


print "handle the gd collection track..."
file_dict = parsefile(dir)
whole_list = []
gd_list = []
rectangles = []
for tt, gd in file_dict.items():
	tt_path = dir + tt
	gd_path1 = dir + gd[0]
	gd_path2 = dir + gd[1]
	#print gd_path1, gd_path2
	tt_list, rectangle_list = kmlparse2.parse_ts(tt_path)
	gd_list1 = kmlparse2.parse_gd(gd_path1)
	gd_list2 = kmlparse2.parse_gd(gd_path2)

	rectangles.extend(rectangle_list)

	gd_list1.extend(gd_list2)
	gd_list.extend(gd_list1)

	whole_list.extend(tt_list)

print "parsing the ts,gd file... successfully"

whole_list = sorted(whole_list, cmp=lambda x,y: cmp(x.longitude, y.longitude))

result_list, del_list, gd_del= handle_gd(whole_list, gd_list)

output_list = []
#上色，被删除的点
for p in del_list:
	p.dogtype = "tt"

#被删除的高德
for p in gd_del:
	p.dogtype = "del_gd"

#生成kml对象
pm_list = []
for m in del_list:
	pm_list.append(createElement("delete", m, operator_name))

for m in result_list:
	pm_list.append(createElement("add", m, operator_name))


del_list.extend(gd_del)
result_list.extend(del_list)
for p in result_list:
	output_list.append(kmlparse2.createPM(p))

for r in rectangles:
	output_list.append(kmlparse2.createLS(r))



createXls(pm_list, dir, filename, date, u"张志锋")

kmlparse2.output_file(output_list, filename, filename, dir + filename + ".kml")
print "dir: " + dir + filename + ".kml was done successfully"
#exit()
#createXls(pmlist, dir, done_filename+"_"+date, date, u"张志锋")
