#coding=utf-8
from lxml import etree
from pyexcel import createXls
from placemark import placemark
from process import get_namespace


path = u"E:/dataD/2015/12月/1224/CAIJI_2015_12_24_21pm.kml"


def parse_caiji(path):
	list = []
	tree = etree.parse(path)
	#print(etree.tostring(tree, pretty_print=True, encoding='utf-8'))
	namespace = get_namespace(tree.getroot())
	for elem in tree.getroot().iter():
		if elem.tag == '{0}Placemark'.format(namespace):
			pm = placemark()
			for node in elem.getchildren():
				if node.tag == '{0}name'.format(namespace):
					pm.name = node.text
					if node.text[1] == u"采":
						pm.dogtype = "new"
						pm.id = node.text.split("_")[1][:-1]
						pm.handletype = node.text.split("_")[2][0]
						pm.form = node.text.split("_")[4].split("(")[1].split(")")[0]
						pm.speedlimit = node.text.split("_")[6][2:]
						pm.account = node.text.split("_")[8][1:-12]
						list.append(pm)
					else:
						pm.dogtype = "server"
						pm.id = node.text.split("_")[1][:-1]
						pm.form = node.text.split("_")[2].split("(")[1].split(")")[0]
				if node.tag == '{0}LookAt'.format(namespace):
					for data in node.getchildren():
						if data.tag == '{0}longitude'.format(namespace):
							pm.longitude = float(data.text)
						if data.tag == '{0}latitude'.format(namespace):
							pm.latitude = float(data.text)
						if data.tag == '{0}heading'.format(namespace):
							pm.heading = float(data.text)
	return list


list = parse_caiji(path)
createXls(list, u"E:/", "caiji_zbr_2015_12_24", "2015-12-24")