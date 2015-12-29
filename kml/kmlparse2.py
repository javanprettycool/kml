#coding=utf-8
from lxml import etree, objectify
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from pykml import parser
from placemark import placemark
from pyexcel import createXls
import re
import xlwt
import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

def createPM(pm):
    name = pm.name
    longitude = pm.longitude
    latitude = pm.latitude
    heading = pm.heading
    style = changeStyle(pm)

    return KML.Placemark(
        KML.name(name),
        KML.LookAt(
          KML.longitude(longitude),
          KML.latitude(latitude),
          KML.altitude('0'),
          KML.heading(heading),
          KML.tilt('0'),
          KML.range('503.63751684255'),
          GX.altitudeMode('relativeToSeaFloor'),
        ),
        style,
        KML.Point(
          KML.coordinates("%.6f" % longitude + "," + "%.6f" % latitude + ",0"),
        ),
      )
def isDog(type):
    if type == "server":
        return True
    else:
        return False

def changeStyle(pm):
    if pm.dogtype == "new":
        if pm.handletype == "2" or pm.handletype == "3":
            return KML.styleUrl('#match_style')
        else:
            return KML.styleUrl('#no_style')
    else:
        return KML.styleUrl('#dog_style')



def createKML(docname, fodername, placemarkList):
    folder = KML.Folder(KML.name(fodername),KML.open('1'))
    for placemark in placemarkList:
        folder.append(placemark)

    return KML.kml(KML.Document(
                KML.name(docname),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('1.3'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/shapes/track.png'),
                        ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="s_ylw-pushpin_hl",
                    ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('1.1'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/shapes/track.png'),
                        ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="no_style",
                    ),
                KML.Style(
                    KML.IconStyle(
                        KML.color("ff34ff19"),
                        KML.scale('1.1'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/shapes/track.png'),
                            ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="dog_style",
                    ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('1.1'),
                        KML.Icon(
                          KML.href('http://maps.google.com/mapfiles/kml/shapes/donut.png'),
                        ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="match_style",
                    ),
                KML.StyleMap(
                    KML.Pair(
                        KML.key('normal'),
                        KML.styleUrl('#s_ylw-pushpin'),
                        ),
                    KML.Pair(
                        KML.key('highlight'),
                        KML.styleUrl('#s_ylw-pushpin_hl'),
                    ),
                    id="s_ylw-pushpin_hl",
                    ),
                folder,
                )
    )


def get_namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''
	

def parse_pnd(path, operator_name="test_zzf"):
    list = []
    dog_list = []
    handle_list = []
    tree = etree.parse(path)
    #print(etree.tostring(tree, pretty_print=True, encoding='utf-8'))
    namespace = get_namespace(tree.getroot())
    tree.findall('//{0}longitude'.format(namespace))

    #tree = xml2dict.parse(path)
    #for data in tree.Placemark.LookAt:
    #     print data.longitude, data.latitude

    for elem in tree.getroot().iter():
        if elem.tag == '{0}Placemark'.format(namespace):
            pm = placemark()
            for node in elem.getchildren():
                if node.tag == '{0}name'.format(namespace):
                    pm.name = node.text
                    if node.text[0] == "[":
                        pm.dogtype = "new"
                        pm.id = node.text.split("_")[1][:-1]
                        pm.handletype = node.text.split("_")[2][0]
                        pm.match = node.text.split("_")[3][1:-1]
                        pm.form = node.text.split("_")[4].split("(")[1].split(")")[0]
                        pm.speedlimit = node.text.split("_")[6].split("(")[0][2:-2]
                        pm.account = node.text.split("(")[-1].split(")")[0]
                        handle_list.append(pm)
                    elif node.text[0] == "!":
                        pm.dogtype = "server"
                        pm.id = node.text.split("_")[1]
                        pm.speedlimit = node.text.split("_")[4][2:]
                        pm.form = node.text.split("_")[2].split("(")[1].split(")")[0]
                        dog_list.append(pm)
                    else:
                        pm.dogtype = "new"                                      #操作员手动新增的点
                        #pm.id = node.text.split("_")[1][:-1]
                        pm.handletype = "1"
                        #pm.match = node.text.split("_")[3][1:-1]
                        pm.form = node.text.split("_")[0]
                        pm.speedlimit = node.text.split("_")[1]
                        pm.account = operator_name
                        handle_list.append(pm)
                if node.tag == '{0}LookAt'.format(namespace):
                    for data in node.getchildren():
                        # if data.tag == '{0}longitude'.format(namespace):
                        #     pm.longitude = float(data.text)
                        # if data.tag == '{0}latitude'.format(namespace):
                        #     pm.latitude = float(data.text)
                        if data.tag == '{0}heading'.format(namespace):
                            pm.heading = round(float(data.text))
                            if (pm.heading<0):
                                pm.heading = 360 + pm.heading
                if node.tag == '{0}Point'.format(namespace):
                    for data in node.getchildren():
                        if data.tag == '{0}coordinates'.format(namespace):
                            part = data.text.split(",")
                            pm.longitude = float("%.6f" % float(part[0]))
                            pm.latitude = float("%.6f" % float(part[1]))
            list.append(pm)
    return list, handle_list, dog_list


def parse_caiji(path, operator_name="test_zzf"):
        list = []
        handle_list = []
        dog_list = []
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
                            handle_list.append(pm)
                        elif node.text[1] == u"狗":
                            pm.dogtype = "server"
                            pm.id = node.text.split("_")[1][:-1]
                            pm.form = node.text.split("_")[2].split("(")[1].split(")")[0]
                            dog_list.append(pm)
                        else:
                            pm.dogtype = "new"                                      #操作员手动新增的点
                            #pm.id = node.text.split("_")[1][:-1]
                            pm.handletype = "1"
                            #pm.match = node.text.split("_")[3][1:-1]
                            pm.form = node.text.split("_")[0]
                            pm.speedlimit = node.text.split("_")[1]
                            pm.account = operator_name
                            handle_list.append(pm)
                    if node.tag == '{0}LookAt'.format(namespace):
                        for data in node.getchildren():
                            if data.tag == '{0}heading'.format(namespace):
                                pm.heading = round(float(data.text))
                                if (pm.heading<0):
                                    pm.heading = 360 + pm.heading
                    if node.tag == '{0}Point'.format(namespace):
                        for data in node.getchildren():
                            if data.tag == '{0}coordinates'.format(namespace):
                                part = data.text.split(",")
                                pm.longitude = float("%.6f" % float(part[0]))
                                pm.latitude = float("%.6f" % float(part[1]))
                list.append(pm)
        return list, handle_list, dog_list


def parse_ts(path):
        list = []
        tree = etree.parse(path)
        namespace = get_namespace(tree.getroot())
        for elem in tree.getroot().iter():
            if elem.tag == '{0}Placemark'.format(namespace):
                pm = placemark()
                for node in elem.getchildren():
                    if node.tag == '{0}name'.format(namespace):
                        pm.name = node.text
                        pm.dogtype = "server"
                        pm.id = node.text.split("_")[0][1:] + "," + node.text.split("_")[1][:-1] + "," + node.text.split("_")[2].split("-")[0][3:-1]
                        pm.handletype = "2"
                        pm.form = node.text.split("_")[2].split("-")[1][5:-1]
                        pm.speedlimit = int(node.text.split("_")[-1][6:-1])
                    if node.tag == '{0}LookAt'.format(namespace):
                        for data in node.getchildren():
                            if data.tag == '{0}longitude'.format(namespace):
                                pm.longitude = float(data.text)
                            if data.tag == '{0}latitude'.format(namespace):
                                pm.latitude = float(data.text)
                            if data.tag == '{0}heading'.format(namespace):
                                pm.heading = float(data.text)
                list.append(pm)
        if not list:
            print "no data today"
            return
        font = xlwt.Font()
        font.name = 'SimSun'
        style = xlwt.XFStyle()
        style.font = font
        file = xlwt.Workbook()
        table = file.add_sheet(u'投诉数据', cell_overwrite_ok=True)
        i = 0
        for pm in list:
            if (pm.form == u"测速" or pm.form == u"高清头" or pm.form == u"流动测速")and pm.speedlimit > 100:
                table.write(i, 1, pm.handletype)
                table.write(i, 3, pm.id)
                table.write(i, 4, pm.form)
                table.write(i, 10, "100")
                table.write(i, 12, "test_zzf")
                table.write(i, 13, u"11月")
                table.write(i, 14, u"张志锋")
                table.write(i, 15, "2015-12-11")
                i += 1
        file.save('e:/tt.xls')

def outputKml(handle_tuple, docname, fodername, dir, filename, segment=1):
    whole_pm_list = []
    pm_list = []
    dog_pm_list = []
    whole_list = handle_tuple[0]
    handle_list = handle_tuple[1]
    dog_list = handle_tuple[2]

    for pm in whole_list:
        whole_pm_list.append(createPM(pm))

    for pm in handle_list:
        pm_list.append(createPM(pm))

    for dog in dog_list:
        dog_pm_list.append(createPM(dog))

    if segment > 1 and segment < len(handle_list):
        i, j = 0, 1
        while(i < len(pm_list)):
            slist = pm_list[i:i+segment]
            slist.extend(dog_pm_list)
            path = dir + filename + "(" + str(j) + ")" + ".kml"
            output_file(slist, docname, fodername, path)
            i = i + segment
            j += 1
    else:
        output_file(whole_pm_list, docname, fodername, dir + filename + ".kml")


def output_file(list, docname, fodername, file):
    doc = createKML(docname, fodername, list)
    output_file = codecs.open(file, "w")
    output_file.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
    output_file.close()


