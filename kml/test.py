
from placemark import placemark



pm1 = placemark()
pm2 = placemark()
pm3 = placemark()

pm1.latitude = 12
pm1.longitude = 12

pm2.latitude = 1
pm2.longitude = 1

pm3.latitude = 11
pm3.longitude = 11

list_p = [pm1, pm2, pm3]

r = sorted(list_p, cmp=lambda x, y: (cmp(x.latitude, y.latitude) and cmp(x.longitude, y.longitude)))

for p in r:
	print p.latitude, p.longitude
