#coding=utf-8
import math
import sys

Ea = 6378137
Eb = 6356725
distDict = {"0":100, "1":100, "16":100}
MAX_INT = sys.maxint


def rad(d):
	return d * math.pi / 180.0


def getLalong(lon, lat, distance, angle):
	dx = distance * math.sin(angle * math.pi / 180.0)
	dy = distance * math.cos(angle * math.pi / 180.0)
	ec = Eb + (Ea - Eb) * (90.0 - lat) / 90.0
	ed = ec * math.cos(lat * math.pi /180)
	newLon = (dx / ed + lon * math.pi /180.0) * 180.0 / math.pi
	newLat = (dy / ec + lat * math.pi / 180.0) * 180.0 / math.pi
	return newLon, newLat


#113.847054,35.309376,113.847054,35.309376 this magic data getDist cant pass
def getDist(lon1, lat1, lon2, lat2):
	radLat1 = rad(lat1)
	radLat2 = rad(lat2)
	s = math.acos(math.sin(radLat1)*math.sin(radLat2)+math.cos(radLat1)*math.cos(radLat2)*math.cos(rad(lon1)-rad(lon2)))
	return s * Ea


def getDist2(lon1, lat1, lon2, lat2):
	radLat1 = rad(lat1)
	radLat2 = rad(lat2)
	a = radLat1 - radLat2
	b = rad(lon1) - rad(lon2)
	s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2)+math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2), 2)))
	return s * Ea


def checkDistance(p, dog, space=50):
	distance = getDist2(p.longitude, p.latitude, dog.longitude, dog.latitude)
	if distance <= space:
		return True
	else:
		return False


#检查修改和删除的匹配
def checkMatchFromDogList(placemark, dog_list):
	if placemark.handletype == "1":      #是新增类型返回
		return
	min_dist = MAX_INT
	catch = 0
	for dog in dog_list:
		dist = getDist2(placemark.longitude, placemark.latitude, dog.longitude, dog.latitude)
		if dist <= 10:
			if placemark.match == dog.id:
				catch = 1
				break
			else:
				if dist < min_dist:
					min_dist = dist
					catch = 1
					placemark.match = dog.id
					placemark.longitude = dog.longitude
					placemark.latitude = dog.latitude
					placemark.heading = dog.heading
	#print u"匹配："+placemark.id+" match "+placemark.match

	if not catch and placemark.match == "?":  #没有匹配到，则可能是多余的修改操作
		print u"未匹配的点："+placemark.name





