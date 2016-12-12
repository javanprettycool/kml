#coding=utf-8

import re
import json
from city import city
import xlrd



path = u"E:/qq/357500663/FileRecv/20161014_数据处理(1).xlsx"
book = xlrd.open_workbook(path)
sheet = book.sheet_by_index(0)


china = json.loads(city)

area_map = {}
result = []

for i in range(1, sheet.nrows):
	receive = sheet.cell_value(i, 1)
	contact = sheet.cell_value(i, 7)
	create_time = sheet.cell_value(i, 3)

	for p in china:
		location = ''
		province = ''
		city = ''
		pattern = p['name']
		m = re.search(pattern, receive)
		if m:
			province = m.group()
			location += province
			if not area_map.get(p['name']):
				area_map[p['name']] = {'value':1,'city':{}}
			else:
				area_map[p['name']]['value'] += 1

		for c in p['city']:
			pattern = c['name']
			m = re.search(pattern, receive)
			if m:
				city = m.group()
				location += city
				if not area_map.get(p['name']):
					area_map[p['name']] = {'value':0,'city':{}}

				if not province:
					area_map[p['name']]['value'] += 1

				if city not in area_map[p['name']]['city']:
					area_map[p['name']]['city'][c['name']] = {'value':1,'area':{}}
				else:
					area_map[p['name']]['city'][c['name']]['value'] += 1

			for a in c['area']:
				pattern = a
				m = re.search(pattern, receive)
				if m:
					area = m.group()
					location += area

					if not area_map.get(p['name']):
						area_map[p['name']] = {'value':0,'city':{c['name']:{'value':0,'area':{}}}}
					elif not area_map[p['name']]['city'].get(c['name']):
						area_map[p['name']]['city'][c['name']] = {'value':0,'area':{}}

					if not city:
						area_map[p['name']]['city'][c['name']]['value'] += 1
					if not province:
						area_map[p['name']]['value'] += 1
					elif city and not province:
						area_map[p['name']]['value'] += 1

					if area not in area_map[p['name']]['city'][c['name']]['area']:
						area_map[p['name']]['city'][c['name']]['area'][a] = {'value':1}
					else:
						area_map[p['name']]['city'][c['name']]['area'][a]['value'] += 1
					break

		if not location:
			pattern = p['name']
			m = re.search(pattern, contact)
			if m:
				province = m.group()

				if not area_map.get(p['name']):
					area_map[p['name']] = {'value':1,'city':{}}
				else:
					area_map[p['name']]['value'] += 1

			for c in p['city']:
				pattern = c['name']
				m = re.search(pattern, contact)
				if m:
					city = m.group()

					if not area_map.get(p['name']):
						area_map[p['name']] = {'value':0,'city':{}}

					if not province:
						area_map[p['name']]['value'] += 1

					if city not in area_map[p['name']]['city']:
						area_map[p['name']]['city'][c['name']] = {'value':1,'area':{}}
					else:
						area_map[p['name']]['city'][c['name']]['value'] += 1

				for a in c['area']:
					pattern = a
					m = re.search(pattern, contact)
					if m:
						area = m.group()

						if not area_map.get(p['name']):
							area_map[p['name']] = {'value':0,'city':{c['name']:{'value':0,'area':{}}}}
						elif not area_map[p['name']]['city'].get(c['name']):
							area_map[p['name']]['city'][c['name']] = {'value':0,'area':{}}

						if not city:
							area_map[p['name']]['city'][c['name']]['value'] += 1
						if not province:
							area_map[p['name']]['value'] += 1
						elif city and not province:
							area_map[p['name']]['value'] += 1

						if area not in area_map[p['name']]['city'][c['name']]['area']:
							area_map[p['name']]['city'][c['name']]['area'][a] = {'value':1}
						else:
							area_map[p['name']]['city'][c['name']]['area'][a]['value'] += 1
						break


		else:
			location = location.encode("utf8")
			#print location

sum = 0
for p,c in area_map.items():
	print p,c['value']
	sum += c['value']
	for city,v in c['city'].items():
		if v['area']:
			for a,g in v['area'].items():
				print p+u"省 "+city+u"市 "+a+" "+str(g['value'])
		else:
			print p+u"省 "+city+u"市 "+str(v['value'])


print sum