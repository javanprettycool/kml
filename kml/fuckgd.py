#coding=utf-8

__author__ = 'javan'

#处理导出的
import kmlparse2
from pyexcel import *
from process import *
import re


EXT = ".kml"

date = "2016-09-05"

dir = u'F:\dataD\高速\G2京沪高速4'  #改这个

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

def handle_gd(tt_list, distance=50, offset=20):
	if not tt_list:
		return False

	tmp_list = tt_list[:]
	del_list = []
	for pm in tt_list:
		#step 1: del 2013
		if int(pm.create_time.split("-")[0]) <= 2013:
			del_list.append(pm)
			continue
		tmp_list.remove(pm)
		#step 2: remove match pm and gd
		target = pm
		for o in tmp_list:
			del_L = []
			if (o.id != target.id and o.dogtype == 'server') or o.dogtype == 'gd':
				if check_match(target, o, distance, offset):
					del_L.append = o





file_dict = parsefile(dir)
for tt, gd in file_dict.items():
	tt_path = dir + tt
	gd_path1 = dir + gd[0]
	gd_path2 = dir + gd[1]
	#print gd_path1, gd_path2
	tt_list, rectangle_list = kmlparse2.parse_ts(tt_path)
	gd_list = kmlparse2.parse_gd(gd_path1)
	gd_list2 = kmlparse2.parse_gd(gd_path2)

	gd_list.extend(gd_list2)
	tt_list.extend(gd_list)

	whole_list = sorted(tt_list, cmp=lambda x, y: cmp(x.longitude, y.longitude))
	handle_gd(whole_list)

	#for p in whole_list:
		# print "dogtype:" + p.dogtype
		# print p.latitude, p.longitude

#exit()
#createXls(pmlist, dir, done_filename+"_"+date, date, u"张志锋")
