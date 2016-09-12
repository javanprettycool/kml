#coding=utf-8

__author__ = 'javan'

#处理导出的
import kmlparse2
from pyexcel import *
from process import *
import re
import os


EXT = ".kml"

date = "2016-09-12"

dir = u'F:\dataD\高速\G12珲乌高速4'  #改这个

operator_name = "gd_test_zzf"

filename = os.path.split(dir)[-1]

dir = dir.replace("\\","/")

if dir[-1] != "/":
    dir+="/"

type_list = [
	u'1测速照相',
	u'7高清摄像',
	u'16电子监控',
	u'辅道测速照相',
	u'事故多发'
]

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


def check_match(target, o, distance, offset, reserve=False):

	angle = target.heading
	if reserve:
		angle = ( angle + 180 ) % 360    #反向匹配

	if checkDistance(target, o, distance):
		if (0 <= angle < offset and (0 <= o.heading < angle+offset or (angle-offset)%360 < o.heading <= 360)) \
			or (360-offset < angle <= 360 and (0 <= o.heading < (angle+offset) % 360 or angle-offset < o.heading <= 360)) \
			or (angle-offset < o.heading < angle+offset):
			return True
	return False

def handle_gd(handle_list, gd_list, distance=100, offset=20):
	if not handle_list:
		return False

	del_list = []           #final ouput the del server point in need

	#step 1: del 2013 which not match gd
	#tmp_gd = gd_list[:]
	for pm in handle_list[:]:
		# if pm.dogtype == 'server' and (pm.form in type_list) and int(pm.create_time.split("-")[0]) <= 2013:
		# 	to_del = True
		# 	for gd in tmp_gd:
		# 		if check_match(pm, gd, distance, offset) or check_match(pm, gd, distance*2, offset):     #100m
		# 			to_del = False
		# 			tmp_gd.remove(gd)
		# 			print pm.name, gd.name
		# 			break
		#
		# 	if to_del:
		# 		handle_list.remove(pm)
		# 		del_list.append(pm)

		#del the other type
		if pm.dogtype == 'server' and (pm.form != u'1测速照相' and pm.form != u'7高清摄像' and pm.form != u'16电子监控'):
			pm in handle_list and handle_list.remove(pm)
			continue


	#match the min distance for gd
	for gd in gd_list:
		min_distance = MAX_INT
		aim = None
		pm_tmp = []
		for pm in handle_list:
			if pm.dogtype == 'server' and (pm.form in type_list) and int(pm.create_time.split("-")[0]) <= 2013:
				if check_match(pm, gd, distance, offset) or check_match(pm, gd, distance*2, offset):
					d = getDist2(pm.longitude, pm.latitude, gd.longitude, gd.latitude)
					if d < min_distance:
						aim = pm
						pm_tmp.append(pm)
				else:
					#pm not in del_list and del_list.append(pm)
					pass
		if aim and pm_tmp:
			g = pm_tmp.pop()
			gd.copy(g)
			for p in pm_tmp:
				p in handle_list and handle_list.remove(p)
				p not in del_list and del_list.append(p)




	# for p in handle_list:
	# 	print p.name


	#step 2: del dul
	i = 0
	while i < len(handle_list):
		pm = handle_list[i]
		j = i + 1
		while j < len(handle_list):
			ob = handle_list[j]
			if pm.id != ob.id and pm.form == ob.form and pm.speedlimit == ob.speedlimit:
				if check_match(pm, ob, distance, offset):
					handle_list.remove(ob)
					del_list.append(ob)
					j -= 1

				if check_match(pm, ob, distance, offset, True):    #匹配相邻点
					if not pm.get_brother() and not ob.get_brother():
						pm.set_brother(ob)
						ob.set_brother(pm)
			elif pm.id != ob.id and check_match(pm, ob, distance, offset):
				kill = ob if pm.create_time > ob.create_time else pm
				handle_list.remove(kill)
				del_list.append(kill)
				j -= 1
			j += 1
		i += 1

	# for p in handle_list:
	# 	b = p.get_brother()
	# 	if isinstance(b, placemark):
	# 		print p.name,p.longitude,p.latitude,b.name,b.longitude,b.latitude
	#
	# exit()

	#step 3:handle gd
	gd_del_list = []
	for pm in handle_list[:]:
		for gd in gd_list[:]:
			if check_match(pm, gd, distance, offset) or check_match(pm, gd, distance*2, offset):
				#pm in handle_list and handle_list.remove(pm)  #以防高德重复采，list index报错
				if pm.account[0].lower() == 'k':             #留下采集人的点
					gd_list.remove(gd)
					gd_del_list.append(gd)
				elif pm.form == gd.form and pm.speedlimit != gd.speedlimit:    #相对类型一样限速不同，留高德
					if int(pm.create_time.split("-")[0]) <= 2013:
						del_list.append(pm)
						gd.copy(pm)            # 将后台点的坐标付给高德，防止因为高德采集的偏移
					else:
						gd_list.remove(gd)   #匹到不同类型的点限速相同或者不同，删除
						gd_del_list.append(gd)

				else:									#其他的，不采纳高德，也不修改后台的
					gd_list.remove(gd)   #匹到不同类型的点限速相同或者不同，删除
					gd_del_list.append(gd)
				break
			else:
				bo = pm.get_brother()
				if bo and check_match(bo, gd, distance, offset, True):    #通过相邻的点反向匹配
					gd_list.remove(gd)   #匹到不同类型的点限速相同或者不同，删除
					gd_del_list.append(gd)


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
	for path in gd:
		gd_list.extend(kmlparse2.parse_gd(dir + path))
	#print gd_path1, gd_path2
	tt_list, rectangle_list = kmlparse2.parse_ts(tt_path)

	rectangles.extend(rectangle_list)

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
	if m.dogtype == "gd":
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
