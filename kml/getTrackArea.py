#coding=utf-8
__author__ = 'Javan'

from kmlparse2 import *

class node(object):
	def __init__(self, lon="", lat="", track=""):
		self.lon = lon
		self.lat = lat
		self.track = track

#path = u"F:\dataD\全国高速优化"
path = u"E:\shanghai"
offset = 0.000711
result = []

for rt, dirs, files in os.walk(path):
    for f in files:
        r1 = re.compile('.kml$')
        if r1.search(f):
			dir =  rt + '\\' + f
			list = parse_normal(dir)

			tracklist = []

			p = list.pop(0)              #first start node
			lon1 = p.longitude + offset
			lon2 = p.longitude - offset
			lat1 = p.latitude + offset
			lat2 = p.latitude - offset
			plon = p.longitude
			plat = p.latitude
			track = [[lon1, lat1], [lon1, lat2], [lon2, lat2], [lon2, lat1]]
			n = node(p.longitude, p.latitude, track)
			tracklist.append(n)

			for p in list:
				lon = p.longitude
				lat = p.latitude

				if (lon2 < lon < lon1) and (lat2 < lat < lat1):
					continue
				elif lon > lon1 and lat > lat1:  #right top
					x = lon - lon1
					y = lat - lat1
					if x >= y :    #right & top
						lon2 = lon1
						lon1 = lon + offset
						lat1 = lat + offset
						lat2 = plat
					else:		   #top right
						lat2 = lat1
						lat1 = lat + offset
						lon1 = lon + offset
						lon2 = plon
				elif lon >= lon1 and lat2 <= lat <= lat1:	#right
					lon2 = lon1
					lon1 = lon + offset
					lat1 = lat + offset
					lat2 = lat - offset
				elif lon > lon1 and lat < lat2:	#right bottom
					x = lon - lon1
					y = lat - lat2
					if -x <= y:		#right & bottom
						lon2 = lon1
						lon1 = lon + offset
						lat1 = plat
						lat2 = lat - offset
					else:			#bottom & right
						lat1 = lat2
						lat2 = lat - offset
						lon1 = lon + offset
						lon2 = plon
				elif lon2 <= lon <= lon1 and lat <= lat2:	#bottom
					lat1 = lat2
					lat2 = lat - offset
					lon1 = lon + offset
					lon2 = lon - offset
				elif lon < lon2 and lat < lat2:	#left bottom
					x = lon - lon2
					y = lat - lat2
					if x >= y:
						lon1 = lon2
						lon2 = lon - offset
						lat1 = plat
						lat2 = lat - offset
					else:
						lat1 = lat2
						lat2 = lat - offset
						lon1 = plon
						lon2 = lon - offset
				elif lon <= lon2 and lat2 <= lat <= lat1:	#left
					lon1 = lon2
					lon2 = lon - offset
					lat1 = lat + offset
					lat2 = lat - offset
				elif lon < lon2 and lat > lat1:	#left top
					x = lon - lon2
					y = lat - lat1
					if -x <= y:
						lat2 = lat1
						lat1 = lat + offset
						lon1 = plon
						lon2 = lon - offset
					else:
						lon1 = lon2
						lon2 = lon - offset
						lat1 = lat + offset
						lat2 = plat
				elif lon2 <= lon <= lon1 and lat >= lat1:	#top
					lat2 = lat1
					lat1 = lat + offset
					lon1 = lon + offset
					lon2 = lon - offset

				plon = lon
				plat = lat

				track = [[lon1, lat1], [lon1, lat2], [lon2, lat2], [lon2, lat1]]
				n = node(lon, lat, track)
				tracklist.append(n)



			for p in tracklist:
				g = placemark()
				g.longitude = p.lon
				g.latitude = p.lat
				#result.append(createPM(g))
				result.append(createLS(p.track))
				print "("+str(p.track[3][0])+","+str(p.track[3][1])+","+str(p.track[1][0])+","+str(p.track[1][1])+")"


	
	
output_file(result,"test","test","f:/S207done.kml")





