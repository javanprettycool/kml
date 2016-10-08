#coding=utf-8
__author__ = 'javan'

import re
import sys
from lonlat_util import *
from pyexcel import *
from placemark import placemark
import os

MAX_INT = sys.maxint
id_for_fee_list = []

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
	if pre is None:
		return True
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
	direction = len(list)
	if direction <= 1:
		return False
	else:
		transfromlist(list, direction)
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



def proc_del(list, doglist, dist=50, offset=20):
	del_set = set()
	min_dis = MAX_INT
	dog_shadow = []
	dog_list = []
	for p in list:
		min_dis = MAX_INT
		dog_shadow = []
		for dog in doglist:
			if dog.id == p.match or (p.form == dog.form and (checkDistance(p, dog, dist) or checkDistance(p, dog, dist*2))):
				distance = getDist2(p.longitude, p.latitude, dog.longitude, dog.latitude)
				if (0 <= p.heading < offset and (0 <= dog.heading < p.heading+offset or (p.heading-offset)%360 < dog.heading <= 360)) \
					or (360-offset < p.heading <= 360 and (0 <= dog.heading < (p.heading+offset) % 360 or p.heading-offset < dog.heading <= 360)) \
					or (p.heading-offset < dog.heading < p.heading+offset):
					p.matchlist.append(dog.id + ":" + str(distance))
					#dog_list.append(dog)
					if distance < min_dis:
						min_dis = distance
						dog_shadow = [dog.id, dog.longitude, dog.latitude, dog]       #匹配距离最近的狗id
		if dog_shadow:
			p.name = p.name if p.match != "?" else p.name.replace("?", dog_shadow[0])
			p.match = dog_shadow[0]
			p.longitude = dog_shadow[1]
			p.latitude = dog_shadow[2]
			dog_shadow[3].matched = p.id
			if p.account.lower() != dog_shadow[3].account.lower():
				p.need_to_pay = True

	fee_id = None
	for p in list:
		if p.need_to_pay:
			fee_id = p.id
			break

	return fee_id


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
						dog_shadow = [dog.id, dog.longitude, dog.latitude, dog.heading, dog.account]
		if dog_shadow:
			p.name = p.name.replace("?", dog_shadow[0]) if p.match == "?" else p.name.split("{")[0]+"{"+dog_shadow[0]+"}"+p.name.split("}")[1]
			p.match = dog_shadow[0]
			p.longitude = dog_shadow[1]
			p.latitude = dog_shadow[2]
			p.heading = dog_shadow[3]
			if p.account.lower() != dog_shadow[4].lower():
				p.need_to_pay = True

	fee_id = None
	for p in list:
		if p.need_to_pay:
			fee_id = p.id
			break

	return fee_id


def proc_add(list, doglist, distance=50, offset=20):

	tmp_list = [x for x in list]
	for p in tmp_list:
		for dog in doglist:
			if p.form == dog.form:   #新增类型相同,可以扩大匹配范围
				if check_match(p, dog, distance, offset) or check_match(p, dog, distance*2, offset+10) or check_match(p, dog, distance*2, offset+20):
					if p.speedlimit == dog.speedlimit:
						list.remove(p)
						if p.id in id_for_fee_list:
							id_for_fee_list.remove(p.id)        #删除重复计费的点
						break
					else:
						if str(p.account).lower() == str(dog.account).lower():
							p.change_match(dog)
							p.need_to_pay = False
						else:
							p.change_match(dog)
			else:                 #新增类型不相同,扩大匹配距离
				if check_match(p, dog, distance, offset) and dog.form != "27":  #不匹配27加油站
					if str(p.account).lower() == str(dog.account).lower():   #比较是否是同一个采集员
						p.change_match(dog)
						p.need_to_pay = False
					else:
						p.change_match(dog)

	fee_id = None       #返回需要计费的id，一组取一个
	for p in list:
		if p.need_to_pay:
			fee_id = p.id
			break
	return fee_id




def operate(list, dir, dog_list):
	pre = None
	handle_list = []
	id_for_fee_list = []
	result = []
	dog = [x for x in dog_list]     #鎷疯礉
	for p in list:
		if checkLalon(p, pre):
			pre = p
			handle_list.append(p)
		else:
			handle_type = handle_list[-1].handletype
			fee = handle(handle_type, handle_list, dog)    #返回算费用的点id,不算费用返回none
			if fee:
				id_for_fee_list.append(fee)     #这个必须在handle前面
			result.append(handle_list)
			pre = p
			handle_list = [p]

	if len(handle_list) != 0:    #鏀跺熬
		if len(handle_list) >= 1:
			fee = handle(handle_list[-1].handletype, handle_list, dog)
			if fee:
				id_for_fee_list.append(fee)     #这个必须在handle前面
		result.append(handle_list)

	if not os.path.exists(dir):
		os.makedirs(dir)


	#最后检测一下重复
	distance = 50
	offset = 20
	new_list = [x for j in result for x in j]
	dul_list = []
	i = 0
	while i < len(new_list):
		j = i + 1
		p1 = new_list[i]
		while j < len(new_list):
			p2 = new_list[j]
			if p1.cmp(p2):
				if p1.handletype == p2.handletype:
					dul_list.append(p2 if p1.create_time > p2.create_time else p1)
				else:
					dul_list.append(p1 if p1.handletype > p2.handletype else p2)
			j += 1
		i += 1

	for j in dul_list:
		for q in result[:]:
			j in q and q.remove(j)
		j in id_for_fee_list and id_for_fee_list.remove(j)

	#exit()
	createXlsForFee(id_for_fee_list, dir)

	createXlsForDog(dog_list, dir)

	return result


def handle(handle_type, handle_list, dog_list, fee_id=None):
	to_type = int(handle_type)

	if len(handle_list) == 3:   #对于三方向的点修正
		mid_point = handle_list[-1]
		mid_point.heading = (mid_point.heading + 180) % 360

	if to_type == placemark.HANDLE_ADD:
		fee_id = add(handle_list ,dog_list)
	elif to_type == placemark.HANDLE_UPDATE:
		fee_id = update(handle_list, dog_list)
	elif to_type == placemark.HANDLE_DELETE:
		fee_id = delete(handle_list, dog_list)
	return fee_id


def add(list, dog_list):
	form = list[-1].form
	if form == "1" or form == "2":  #流动测速和测速不处理
		fee_id = proc_add(list, dog_list)
	elif form == "0":       #单检查匹配重复红灯和测速
		handleForList(list)
		fee_id = proc_add(list, dog_list, 80, 30)
	elif form == "16" or form == "7":
		handleForList(list)
		fee_id = proc_add(list, dog_list)
	else:
		fee_id = list[-1].id
		handleForList(list)

	return fee_id



def update(list, dog_list):
	handleForList(list)
	fee_id = proc_update(list, dog_list)
	return fee_id

def delete(list, dog_list):
	#form = list[-1].form
	for p in list:
		if p.match == "?":
			transfor(p, 50, p.heading)    #反向
	fee_id = proc_del(list, dog_list)
	return fee_id

#dog_id 鍒濆鐨勭嫍id琛紝 dog_list澶勭悊杩囧悗鐨勭嫍琛�
def proc_mod(list, id_for_fee_list, original_dog_list, dog_list, operator_name):
	pmlist = []
	for pm in list:
		if pm.dogtype == "new":                       #处理计费和修改操作
			if pm.id in id_for_fee_list:
				pm.cost = 2
			if checkMatchFromDogList(pm, dog_list):
				pmlist.append(pm)
		if pm.dogtype == "server":                    #处理被修改或删除的狗点
			for old_dog in original_dog_list[:]:
				if pm.id == old_dog.id:
					if checkChange(pm, old_dog):
						pmlist.append(createElement("update", pm, operator_name))
					original_dog_list.remove(old_dog)

	#不在原来的dog中，即留下的的dog，删除
	for dog in original_dog_list:
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
		return True
	else:
		return False


def createElement(operate, dog, operator_name):
	pm = placemark()

	if operate == "add":
		pm.handletype = placemark.HANDLE_ADD
	elif operate == "update":
		pm.handletype = placemark.HANDLE_UPDATE
	elif operate == "delete":
		pm.handletype = placemark.HANDLE_DELETE

	pm.form = dog.form
	pm.match = dog.id
	pm.speedlimit = dog.speedlimit
	pm.longitude = dog.longitude
	pm.latitude = dog.latitude
	pm.heading = dog.heading
	pm.form = dog.form
	pm.account = operator_name
	pm.id = dog.matched if dog.matched else ""
	return pm

def check_duplicate(list):
	tmp_list = list[:]
	hash_set = set()

	for pm in tmp_list:
		if pm.md5 not in hash_set:
			hash_set.add(pm.md5)
		else:
			list.remove(pm)