#coding=utf-8
__author__ = 'javan'

import re
import sys
from lonlat_util import *
from pyexcel import *
from placemark import placemark
import os

MAX_INT = sys.maxint



def attr_gbk(elem, name):
    return elem.attrib.get(name).encode("GBK")


def get_namespace(element):
	m = re.match('\{.*\}', element.tag)
	return m.group(0) if m else ''


def checkRange(node, list, i=0):
	for p in list:
		dist = getDist2(node.longitude, node.latitude, p.longitude, p.latitude)
		if dist < 100 and dist > 0:
			return False
	return True


def checkLalon(p, pre):
	if pre is None: return True
	return p != pre and p.longitude == pre.longitude and p.latitude == pre.latitude and p.handletype == pre.handletype



def transfor(pm, distance, angle):
	pm.longitude, pm.latitude = getLalong(pm.longitude, pm.latitude, distance, (angle+180)%360.0)


def transfromlist(list, direction):
	if direction == 1:
		return
	for j in range(0, direction):
		if j % 2 != 0:
			transfor(list[j], 40, list[j].heading)
		else:
			transfor(list[j], 30, list[j].heading)


def handleForList(list):
	length = len(list)
	if length <= 1:
		return False
	else:
		transfromlist(list, length)
	return True


# def proc_add(list, left_list, handle_list):
# 	pre1 = None
# 	pre2 = None
# 	pre3 = None
# 	pre4 = None
# 	redlightlist = []
# 	speedmeasurelist = []
# 	electronic_monitoring = []
# 	hd_head = []
# 	id_for_fee_list = []
# 	for p in list:
# 		print p.name
# 		if p.dogtype == "new" and p.handletype == "1" and checkRange(p, list):              #鏂板锛宑hecklalon閬垮厤閲嶅,checkRange閬垮厤100m鑼冨洿鍐呯殑鐐�
# 			handle_list.append(p)
# 			if p.form == "0":       #绾㈢伅
# 				if checkLalon(p, pre1):
# 					redlightlist.append(p)
# 					pre1 = p
# 				else:
# 					handleForList(redlightlist, pre1, p)
# 					redlightlist = [p]
# 					id_for_fee_list.append(pre1.id)
# 					pre1 = p
# 			elif p.form == "1":        #娴嬮��
# 				if checkLalon(p, pre2):
# 					speedmeasurelist.append(p)
# 					pre2 = p
# 				else:
# 					id_for_fee_list.append(pre2.id)
# 					pre2 = p
# 					speedmeasurelist = [p]
# 			elif p.form == "7":             #楂樻竻澶�
# 				if checkLalon(p, pre3):
# 					hd_head.append(p)
# 					pre3 = p
# 				else:
# 					handleForList(hd_head, pre3, p)
# 					hd_head = [p]
# 					id_for_fee_list.append(pre3.id)
# 					pre3 = p
# 			elif p.form == "16":            #鐢靛瓙鐩戞帶
# 				if checkLalon(p, pre4):
# 					electronic_monitoring.append(p)
# 					pre4 = p
# 				else:
# 					handleForList(electronic_monitoring, pre4, p)
# 					electronic_monitoring = [p]
# 					id_for_fee_list.append(pre4.id)
# 					pre4 = p
# 			else:
# 				#left_list.append(p)
# 				pass
# 		elif p.dogtype == "server":
# 			handle_list.append(p)
# 		else:
# 			left_list.append(p)
#
# 	if len(redlightlist) is not 0:
# 		if len(redlightlist) > 1:
# 			transfromlist(redlightlist, 2)
# 		else:
# 			pass
# 	return id_for_fee_list



def proc_del(list, doglist, offset=20):
	del_set = set()
	min_dis = MAX_INT
	dog_shadow = []
	dog_list = []
	for p in list:
		min_dis = MAX_INT
		dog_shadow = []
		for dog in doglist:
			if dog.id == p.match or (p.form == dog.form and checkDistance(p, dog, 50)):
				distance = getDist2(p.longitude, p.latitude, dog.longitude, dog.latitude)
				if (0 <= p.heading < offset and (0 <= dog.heading < p.heading+offset or (p.heading-offset)%360 < dog.heading <= 360)) \
					or (360-offset < p.heading <= 360 and (0 <= dog.heading < (p.heading+offset) % 360 or p.heading-offset < dog.heading <= 360)) \
					or (p.heading-offset < dog.heading < p.heading+offset):
					p.matchlist.append(dog.id + ":" + str(distance))
					#dog_list.append(dog)
					if distance < min_dis:
						min_dis = distance
						dog_shadow = [dog.id, dog.longitude, dog.latitude]       #匹配距离最近的狗id
		if dog_shadow:
			p.name = p.name if p.match != "?" else p.name.replace("?", dog_shadow[0])
			p.match = dog_shadow[0]
			p.longitude = dog_shadow[1]
			p.latitude = dog_shadow[2]
	return del_set


def proc_update(list, doglist, offset=20):
	update_set = set()
	min_dis = MAX_INT
	dog_shadow = []
	dog_list = []
	for p in list:
		min_dis = MAX_INT
		dog_shadow = []
		for dog in doglist:
			if dog.id == p.match or checkDistance(p, dog, 50):
				distance = getDist2(p.longitude, p.latitude, dog.longitude, dog.latitude)
				if (0 <= p.heading < offset and (0 <= dog.heading < p.heading+offset or (p.heading-offset)%360 < dog.heading <= 360)) \
					or (360-offset < p.heading <= 360 and (0 <= dog.heading < (p.heading+offset) % 360 or p.heading-offset < dog.heading <= 360)) \
					or (p.heading-offset < dog.heading < p.heading+offset):
					p.matchlist.append(dog.id + ":" + str(distance))
					#dog_list.append(dog)
					if distance < min_dis:
						min_dis = distance
						dog_shadow = [dog.id, dog.longitude, dog.latitude, dog.heading]
		if dog_shadow:
			p.name = p.name if p.match != "?" else p.name.replace("?", dog_shadow[0])
			p.match = dog_shadow[0]
			p.longitude = dog_shadow[1]
			p.latitude = dog_shadow[2]
			p.heading = dog_shadow[3]
	return update_set




def operate(list, dir, dog_list):
	pre = None
	id_for_fee_list = []
	handle_list = []
	dog = [x for x in dog_list]     #鎷疯礉
	for p in list:
		if p.dogtype == "new":
			if checkLalon(p, pre):
				pre = p
				handle_list.append(p)
			else:
				handle_type = handle_list[-1].handletype
				handle(handle_type, handle_list, dog)
				id_for_fee_list.append(pre.id)
				pre = p
				handle_list =[p]
		else:
			pass

	if len(handle_list) != 0:    #鏀跺熬
		if len(handle_list) >= 1:
			handle(handle_list[-1].handletype, handle_list, dog)
			id_for_fee_list.append(handle_list[-1].id)
		else:
			pass

	if not os.path.exists(dir):
		os.makedirs(dir)

	#璐圭敤id琛�
	createXlsForFee(id_for_fee_list, dir)

	#鍘熺嫍id琛�
	createXlsForDog(dog_list, dir)


def handle(handle_type, handle_list, dog_list):
	if handle_type == "1":
		add(handle_list)
	elif handle_type == "2":
		update(handle_list, dog_list)
	elif handle_type == "3":
		delete(handle_list, dog_list)


def add(list):
	form = list[-1].form
	if form == "1":
		pass
	else:
		handleForList(list)



def update(list, dog_list):
	handleForList(list)
	proc_update(list, dog_list)


def delete(list, dog_list):
	#form = list[-1].form
	for p in list:
		if p.match == "?":
			transfor(p, 30, p.heading)
	proc_del(list, dog_list)


#dog_id 鍒濆鐨勭嫍id琛紝 dog_list澶勭悊杩囧悗鐨勭嫍琛�
def proc_mod(list, id_for_fee_list, original_dog_list, dog_list, operator_name):
	pmlist = []
	delete_due = []  #删除删除点附近的点
	for pm in list:
		if pm.dogtype == "new":                       #处理计费和修改操作
			pmlist.append(pm)
			if pm.id in id_for_fee_list:
				pm.cost = 2
			delete_due.extend(checkMatchFromDogList(pm, dog_list))
		if pm.dogtype == "server":                    #处理被修改或删除的狗点
			for old_dog in original_dog_list:
				if pm.id == old_dog.id:
					if checkChange(pm, old_dog):
						pmlist.append(createElement("update", pm, operator_name))
					original_dog_list.remove(old_dog)

	for dog in original_dog_list:
		pmlist.append(createElement("delete", dog, operator_name))

	for dog in delete_due:
		pmlist.append(createElement("delete", dog, operator_name))
	return pmlist


def checkChange(pm, dog):
	if pm.longitude != dog.longitude:
		return True
	elif pm.latitude != dog.latitude:
		return True
	elif pm.heading != dog.heading:
		return True
	elif pm.speedlimit != dog.speedlimit:
		return True
	elif pm.form != dog.form:
		print dog.form
		return True
	else:
		return False


def createElement(operate, dog, operator_name):
	pm = placemark()

	if operate == "add":
		pm.handletype = "1"
	elif operate == "update":
		pm.handletype = "2"
	elif operate == "delete":
		pm.handletype = "3"

	pm.form = dog.form
	pm.match = dog.id
	pm.speedlimit = dog.speedlimit
	pm.longitude = dog.longitude
	pm.latitude = dog.latitude
	pm.heading = dog.heading
	pm.form = dog.form
	pm.account = operator_name
	return pm