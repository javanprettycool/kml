#coding=utf-8
from placemark import placemark
import time
import xlrd
import re
import kmlparse2
import lonlat_util
from process import *
import re
#from fuckgd import check_match

# def test(a, callback, *avg):
# 	print a
# 	callback(*avg)
#
#
# def gg(*a):
# 	for s in a:
# 		print s
#
# test('test', gg, 'gg', 'haha')
# exit()
#
# def walkdir(dir, pattern):
# 	for f in os.listdir(dir):
# 		d = os.path.join(dir, f)
# 		if os.path.isfile(d) and re.match(pattern, f):
# 			yield d
# 		elif os.path.isdir(d):
# 			walkdir(d, pattern)
#
# for p in walkdir(path, r"pnd|caiji"):
# 	print p
# exit()
a = {1:'a'}

print 1 in a
exit()
track_length = 0
test = "132.175182704993,45.70474797442787,0 132.1835326618747,45.70446571192661,0 132.1891286071757,45.7043559106189,0 132.1967000742702,45.70403513198301,0 132.2036523311633,45.70377497778015,0 132.2109814980524,45.70364836711157,0 132.216221552648,45.70396924675234,0 132.2220282171861,45.70456555901741,0 132.227441849744,45.7054965337822,0 132.2317985719735,45.7065562887331,0 132.2358908361277,45.70775120761536,0 132.2388546179986,45.70884701160039,0 132.2434360356151,45.71064896981267,0 132.2487096222409,45.71304174471249,0 132.2546878383772,45.71562223901669,0 132.2591495302027,45.71740072883841,0 132.2625183444135,45.71854187067571,0 132.2667981261536,45.71981718539617,0 132.2716708985297,45.72106927101016,0 132.2785076481322,45.72283335418432,0 132.2834012482591,45.72413268401166,0 132.2881404895022,45.72523582022635,0 132.2937130076548,45.72611208098405,0 132.297353816216,45.72646312120747,0 132.3021786582774,45.72680685466279,0 132.30601881901,45.72692896535205,0 132.3112523123391,45.72703915013199,0 132.3187395246348,45.72713684094586,0 132.3250224889917,45.72738184230522,0 132.3314864383666,45.72776930034276,0 132.3356715451802,45.72824460680435,0 132.3424079529154,45.72915914527305,0 132.3496812620555,45.73011676824226,0 132.358265892503,45.73127961289366,0 132.3680424059329,45.73255506527332,0 132.3771000676538,45.73370538444669,0 132.3850056212239,45.73487995325532,0 "
track = test.strip(",0 ").split(",0 ")
tmp = []
for i, p in enumerate(track):
	lon = float("%.6f" % float(p.split(',')[0]))
	la = float("%.6f" % float(p.split(',')[1]))
	tmp.append([lon, la])

track = tmp
start = track[0]
part_length = 0
for t in track:
	next = t
	l = lonlat_util.getDist2(start[0], start[1], next[0], next[1])
	print start,next,l
	start = t
	track_length += l
print track_length / 1000
exit()

# str = u"(G1501沈阳绕城高速)26KM沈阳市苏家屯区--沈阳市于洪区2"
# print re.search('(\d+KM)', str).group()
# exit()


path = u"F:/dataD/高速统计/我的地点.kml"
track = kmlparse2.parse_linestring(path)
track_length = 0
statistic_length = 0

for p in track:
	track = p.track_list
	start = track[0]
	part_length = 0
	print p.name
	for t in track:
		next = t
		l = lonlat_util.getDist2(start[0], start[1], next[0], next[1])
		start = t
		track_length += l
		part_length += l
	print str(part_length / 1000) + "km"
	if re.search("(\d+KM)", p.name):
		len_from_str = re.search("(\d+KM)", p.name).group()
		statistic_length += float(len_from_str.strip("KM"))
		print len_from_str

print "total: " + str(track_length / 1000) + "km"
print "str_total: " + str(statistic_length) + "km"
exit()


dir = u"F:\dataD\高速\G25长深高速4\caiji_2016_09_01(1).xls"
#path = unicode(dir,  "utf8")
a = os.path.split(dir)[1].replace('.xls', '').split('(')[0]
print a[a.find('_')+1:]
exit()

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


