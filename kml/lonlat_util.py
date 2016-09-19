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


#检查修改和删除的匹配
def checkMatchFromDogList(placemark, dog_list):

	min_dist = MAX_INT
	catch = 0
	target = None
	dog_list_copy = [x for x in dog_list]
	delete_list = []
	if placemark.handletype == "1":      #是新增类型返回
		# catch = 1
		return True

	else:
		for dog in dog_list_copy:
			dist = getDist2(placemark.longitude, placemark.latitude, dog.longitude, dog.latitude)
			if dist <= 10:
				if placemark.match == dog.id:
					dog.matched = placemark.id
					catch = 1
					target = dog
					break
				else:
					if dist < min_dist:
						min_dist = dist
						catch = 1
						target = dog
		if catch:
			if placemark.handletype == "2" and placemark.speedlimit == target.speedlimit and placemark.form == target.form:
				print u"匹配的点未做修改："+placemark.name
				return False
			placemark.match = target.id
			placemark.longitude = target.longitude
			placemark.latitude = target.latitude
			placemark.heading = target.heading
			dog_list.remove(target)
		else:
			print u"检查匹配的点：（实际未匹配到）"+placemark.name

	return True




def baiduTranstoGoogle(lon, lat):  #BD09 to gcj02
	x = lon - 0.0065
	y = lat - 0.006
	z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * math.pi)
	theta = math.atan2(y, x) - 0.000003 * math.cos(x * math.pi)
	lon = z * math.cos(theta)
	lat = z * math.sin(theta)
	return lon,lat


def Gcj02transtoMercator(lon, lat):
	x = lon *20037508.34/180
	y = math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
	y = y *20037508.34/180
	return x, y


def Gcj02toWgps4(lon, lat):
	lon1,lat1 = transform(lon, lat)
	lontitude = lon * 2 - lon1
	latitude = lat * 2 - lat1
	return lontitude,latitude

def transform(lon, lat) :
	ee = 0.00669342162296594323
	a = 6378245.0
	dLat = transformLat(lon - 105.0, lat - 35.0)
	dLon = transformLon(lon - 105.0, lat - 35.0)
	radLat = lat / 180.0 * math.pi
	magic = math.sin(radLat)
	magic = 1 - ee * magic * magic
	sqrtMagic = math.sqrt(magic)
	dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
	dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)
	mgLat = lat + dLat
	mgLon = lon + dLon
	return mgLon, mgLat


def transformLat(x,y):
	ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
	ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
	ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
	ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
	return ret

def transformLon(x, y):
	ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
	ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
	ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
	ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
	return ret
