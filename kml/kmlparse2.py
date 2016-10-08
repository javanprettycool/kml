#coding=utf-8
from lxml import etree, objectify
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from pykml import parser
from placemark import placemark
import re
import xlwt
import sys
import codecs
import os
import hashlib
import time
import pyexcel

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

def createLS(line):  #linestring

    return KML.Placemark(
        KML.name('gx:altitudeMode Example'),
        KML.LineString(
          KML.extrude('1'),
          GX.altitudeMode('relativeToSeaFloor'),
          KML.coordinates(
          str(line[0][0])+','+str(line[0][1])+',0 '+
          str(line[1][0])+','+str(line[1][1])+',0 '+
          str(line[2][0])+','+str(line[2][1])+',0 '+
          str(line[3][0])+','+str(line[3][1])+',0 '+
          str(line[4][0])+','+str(line[4][1])+',0 '
          ),
        ),
      )

def isDog(type):
    if type == "server":
        return True
    else:
        return False

def changeStyle(pm):
    if pm.dogtype == "new":
        if pm.handletype == placemark.HANDLE_UPDATE or pm.handletype == placemark.HANDLE_DELETE:
            return KML.styleUrl('#match_style')
        else:
            return KML.styleUrl('#no_style')
    elif pm.dogtype == "gd":
        return KML.styleUrl('#gd_style')
    elif pm.dogtype == "tt":
        return KML.styleUrl('#tt_style')
    elif pm.dogtype == "del_gd":
        return KML.styleUrl('#dgd_style')
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
                KML.Style(
                    KML.IconStyle(
                        KML.scale('1.1'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/pushpin/ltblu-pushpin.png'),
                        ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="tt_style",
                    ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('1.1'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/paddle/G.png'),
                        ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="gd_style",
                    ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('1.1'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/paddle/blu-circle.png'),
                        ),
                        KML.hotSpot(
                            x="20",
                            y="2",
                            xunits="pixels",
                            yunits="pixels",
                            ),
                        ),
                    id="dgd_style",
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
    if not os.path.exists(path):
        print u"目录不存在，请检查文件路径"
        exit()
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
                        pm.id = int(node.text.split("_")[1][:-1])
                        pm.handletype = int(node.text.split("_")[2][0])
                        pm.match = node.text.split("_")[3][1:-1]
                        pm.form = node.text.split("_")[4].split("(")[1].split(")")[0]
                        pm.speedlimit = node.text.split("_")[6].split("(")[0][2:-2]
                        pm.account = node.text.split("(")[-1].split(")")[0]
                        pm.create_time = node.text.split("@")[1]
                        handle_list.append(pm)
                    elif node.text[0] == "!":
                        pm.dogtype = "server"
                        pm.id = node.text.split("_")[1]
                        pm.speedlimit = node.text.split("_")[4][2:]
                        pm.form = node.text.split("_")[2].split("(")[1].split(")")[0]
                        pm.account = node.text.split(":")[1]
                        dog_list.append(pm)
                    else:
                        try:
                            name = node.text.replace("-", "_")
                            pm.dogtype = "new"                                      #操作员手动新增的点
                            #pm.id = name.split("_")[1][:-1]
                            pm.handletype = 1
                            #pm.match = name.split("_")[3][1:-1]
                            pm.form = name.split("_")[0]
                            pm.speedlimit = name.split("_")[1]
                            pm.account = operator_name
                            handle_list.append(pm)
                        except StandardError, e:
                            print "检查你新增的点 " + pm.name
                            sys.exit()
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

            hash_code = "form:"+str(pm.form)+";long:"+str(pm.longitude)+";lat:"+str(pm.latitude)+";angle:"+str(pm.heading)+";limit:"+str(pm.speedlimit)+";"
            m = hashlib.md5()
            m.update(hash_code)
            pm.md5 = m.hexdigest()
            list.append(pm)
    return list, handle_list, dog_list


def parse_caiji(path, operator_name="test_zzf"):
        if not os.path.exists(path):
            print u"没有采集数据"
            return (None)
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
                            pm.handletype = int(node.text.split("_")[2][0])
                            pm.form = node.text.split("_")[4].split("(")[1].split(")")[0]
                            pm.speedlimit = node.text.split("_")[6][2:]
                            pm.account = node.text.split("@")[1][0:-12]
                            pm.match = node.text.split("{")[1].split("}")[0]
                            handle_list.append(pm)
                        elif node.text[1] == u"狗":
                            pm.dogtype = "server"
                            pm.id = node.text.split("_")[1][:-1]
                            pm.speedlimit = node.text.split("_")[4][2:]
                            pm.form = node.text.split("_")[2].split("(")[1].split(")")[0]
                            pm.account = node.text.split(":")[1]
                            dog_list.append(pm)
                        else:
                            try:
                                name = node.text.replace("-", "_")
                                pm.dogtype = "new"                                      #操作员手动新增的点
                                #pm.id = name.split("_")[1][:-1]
                                pm.handletype = 1
                                #pm.match = name.split("_")[3][1:-1]
                                pm.form = name.split("_")[0]
                                pm.speedlimit = name.split("_")[1]
                                pm.account = operator_name
                                handle_list.append(pm)
                            except StandardError, e:
                                print "检查你新增的点 " + pm.name
                                sys.exit()
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

                hash_code = "form:"+str(pm.form)+";long:"+str(pm.longitude)+";lat:"+str(pm.latitude)+";angle:"+str(pm.heading)+";limit:"+str(pm.speedlimit)+";"
                m = hashlib.md5()
                m.update(hash_code)
                pm.md5 = m.hexdigest()
                list.append(pm)
        return list, handle_list, dog_list


def parse_ts(path, filename="tt", date="", operator_name=u"张志锋"):
        dir = os.path.dirname(path)
        list = []
        rectangle_list = []

        tree = etree.parse(path)
        namespace = get_namespace(tree.getroot())
        for elem in tree.getroot().iter():
            if elem.tag == '{0}Placemark'.format(namespace):
                pm = placemark()
                for node in elem.getchildren():
                    if node.tag == '{0}name'.format(namespace):
                        if node.text == u"未命名路径":  #去除未命名路径
                            continue
                        if node.text == "0" or node.text == "1":
                            pm.name = node.text
                            list.append(pm)
                            continue
                        else:
                            pm.name = node.text
                            pm.dogtype = "server"
                            pm.match = node.text.split("_")[0][1:] + "," + node.text.split("_")[1][:-1] + "," + node.text.split("_")[2].split("-")[0][3:-1]
                            pm.id = pm.match
                            pm.handletype = "2"
                            pm.form = node.text.split("_")[2].split("-")[1][5:-1]
                            pm.transforForm()
                            pm.account = "test_zzf"
                            pm.speedlimit = int(node.text.split("_")[4][6:-1])
                            pm.create_time = node.text.split("~")[1][:-1].strip()
                            list.append(pm)
                    if node.tag == '{0}LookAt'.format(namespace):
                        for data in node.getchildren():
                            if data.tag == '{0}heading'.format(namespace):
                                pm.heading = round(float(data.text))
                                if (pm.heading<0):
                                    pm.heading = 360 + pm.heading
                    if node.tag == '{0}Point'.format(namespace):                 #需要获取point下的coordinate的坐标，lookat下的坐标是google转换过的
                        for data in node.getchildren():
                            if data.tag == '{0}coordinates'.format(namespace):
                                part = data.text.split(",")
                                pm.longitude = float("%.6f" % float(part[0]))
                                pm.latitude = float("%.6f" % float(part[1]))

                    # if node.tag == '{0}LineString'.format(namespace):
                    #     for data in node.getchildren():
                    #         if data.tag == '{0}coordinates'.format(namespace):
                    #             part = data.text.strip(",0 \n").split(",0 ")
                    #             tmp = []
                    #             for i, p in enumerate(part):
                    #                 lon = float("%.6f" % float(p.split(',')[0]))
                    #                 la = float("%.6f" % float(p.split(',')[1]))
                    #                 tmp.append([lon, la])
                    #             rectangle_list.append(tmp)
        if not list:
            print "no data today"
            return

        handle_list = [x for x in list]
        # for p in handle_list:
        #     if p.form != u"测速" :
        #         list.remove(p)
        #     else:
        #         if p.speedlimit >= 60:
        #             list.remove(p)
        #         else:
        #             p.speedlimit = 60
        #             p.form = "1"


        # createXls(list, dir, filename, date, operator_name)
        return list, rectangle_list

def parse_gd(path, filename="tt", date="", operator_name=u"张志锋"):
        dir = os.path.dirname(path)
        list = []

        tree = etree.parse(path)
        namespace = get_namespace(tree.getroot())
        for elem in tree.getroot().iter():
            if elem.tag == '{0}Placemark'.format(namespace):
                pm = placemark()
                for node in elem.getchildren():
                    if node.tag == '{0}name'.format(namespace):
                        node.text = node.text.replace("-", "_")
                        if node.text == u"未命名路径":  #去除未命名路径
                            break
                        elif node.text.split('_')[0]=='0' or node.text.split('_')[0]=='1':
                            try:
                                name = node.text.replace("-", "_")
                                pm.dogtype = "new"                                      #操作员手动新增的点
                                #pm.id = name.split("_")[1][:-1]
                                pm.handletype = "1"
                                #pm.match = name.split("_")[3][1:-1]
                                pm.form = name.split("_")[0]
                                pm.speedlimit = name.split("_")[1]
                                pm.account = operator_name
                                list.append(pm)
                            except StandardError:
                                print "检查你新增的点 " + pm.name
                                sys.exit()
                        else :
                            pm.name = node.text
                            pm.dogtype = "gd"
                            #pm.match = node.text.split("_")[0][1:] + "," + node.text.split("_")[1][:-1] + "," + node.text.split("_")[2].split("-")[0][3:-1]
                            #pm.id = pm.match
                            pm.handletype = "1"
                            pm.form = pyexcel.getform(node.text.split("_")[2].split("(")[1].split(")")[0])
                            pm.account = "test_zzf"
                            pm.speedlimit = int(node.text.split("_")[4][2:])
                            t = time.strptime(node.text.split("_")[-1], "%Y/%b/%d")
                            pm.create_time = time.strftime("%Y-%m-%d", t)
                            list.append(pm)
                    if node.tag == '{0}LookAt'.format(namespace):
                        for data in node.getchildren():
                            if data.tag == '{0}heading'.format(namespace):
                                pm.heading = round(float(data.text))
                                if (pm.heading<0):
                                    pm.heading = 360 + pm.heading
                    if node.tag == '{0}Point'.format(namespace):                 #需要获取point下的coordinate的坐标，lookat下的坐标是google转换过的
                        for data in node.getchildren():
                            if data.tag == '{0}coordinates'.format(namespace):
                                part = data.text.split(",")
                                pm.longitude = float("%.6f" % float(part[0]))
                                pm.latitude = float("%.6f" % float(part[1]))

        if not list:
            print "no data today"
            return []

        handle_list = [x for x in list]
        # for p in handle_list:
        #     if p.form != u"测速" :
        #         list.remove(p)
        #     else:
        #         if p.speedlimit >= 60:
        #             list.remove(p)
        #         else:
        #             p.speedlimit = 60
        #             p.form = "1"


        # createXls(list, dir, filename, date, operator_name)
        return list
def parse_normal(path):
    dir = os.path.dirname(path)
    list = []
    tree = etree.parse(path)
    namespace = get_namespace(tree.getroot())
    for elem in tree.getroot().iter():
        if elem.tag == '{0}Placemark'.format(namespace):
            pm = placemark()
            for node in elem.getchildren():
                if node.tag == '{0}name'.format(namespace):
                    pm.name = node.text
                if node.tag == '{0}LookAt'.format(namespace):
                    for data in node.getchildren():
                        if data.tag == '{0}heading'.format(namespace):
                            pm.heading = round(float(data.text))
                            if pm.heading < 0:
                                pm.heading += 360
                if node.tag == '{0}Point'.format(namespace):                 #需要获取point下的coordinate的坐标，lookat下的坐标是google转换过的
                    for data in node.getchildren():
                        if data.tag == '{0}coordinates'.format(namespace):
                            part = data.text.split(",")
                            pm.longitude = float("%.6f" % float(part[0]))
                            pm.latitude = float("%.6f" % float(part[1]))
            list.append(pm)
    return list

def parse_ts_from_device(path, filename="tt", date="", operator_name=u"张志锋"):
        dir = os.path.dirname(path)
        list = []
        tree = etree.parse(path)
        namespace = get_namespace(tree.getroot())
        for elem in tree.getroot().iter():
            if elem.tag == '{0}Placemark'.format(namespace):
                pm = placemark()
                for node in elem.getchildren():
                    if node.tag == '{0}name'.format(namespace):
                        if node.text == u"未命名路径":  #去除未命名路径
                            break
                        if node.text == "0" or node.text == "1":
                            pm.name = node.text
                            list.append(pm)
                            continue
                        pm.name = node.text
                        pm.dogtype = "server"
                        pm.match = node.text.split("_")[1][0:-1]
                        pm.handletype = "2"
                        pm.form = node.text.split("_")[2].split("(")[1].split(")")[0]
                        pm.account = "test_zzf"
                        pm.speedlimit = int(node.text.split("_")[4][2:])
                        list.append(pm)
                    if node.tag == '{0}LookAt'.format(namespace):
                        for data in node.getchildren():
                            if data.tag == '{0}heading'.format(namespace):
                                pm.heading = round(float(data.text))
                                if (pm.heading<0):
                                    pm.heading = 360 + pm.heading
                    if node.tag == '{0}Point'.format(namespace):                 #需要获取point下的coordinate的坐标，lookat下的坐标是google转换过的
                        for data in node.getchildren():
                            if data.tag == '{0}coordinates'.format(namespace):
                                part = data.text.split(",")
                                pm.longitude = float("%.6f" % float(part[0]))
                                pm.latitude = float("%.6f" % float(part[1]))
        if not list:
            print "no data today"
            return

        handle_list = [x for x in list]
        # for p in handle_list:
        #     if p.form != u"测速" :
        #         list.remove(p)
        #     else:
        #         if p.speedlimit >= 60:
        #             list.remove(p)
        #         else:
        #             p.speedlimit = 60
        #             p.form = "1"


        # createXls(list, dir, filename, date, operator_name)
        return list;


def outputKml(handle_tuple, docname, fodername, dir, filename, segment=1):
    whole_pm_list = []
    dog_pm_list = []
    whole_list = handle_tuple[0]
    handle_list = handle_tuple[1]
    dog_list = handle_tuple[2]
    pm_count = 0

    for p in handle_list:
        pm_count += len(p)

    for dog in dog_list:
        dog_pm_list.append(createPM(dog))

    if 1 < segment < pm_count:
        i, count, slist = 0, 0, []
        for p in handle_list:
            count += len(p)
            for o in p:
                slist.append(createPM(o))
            if count >= segment:
                i += 1
                count = 0
                slist.extend(dog_pm_list)
                path = dir + filename + "(" + str(i) + ")" + ".kml"
                output_file(slist, docname, fodername, path)
                slist = []
        if count != 0:
            slist.extend(dog_pm_list)
            path = dir + filename + "(" + str(i+1) + ")" + ".kml"
            output_file(slist, docname, fodername, path)

    else:
        for p in handle_list:
            for o in p:
                whole_pm_list.append(createPM(o))
        whole_pm_list.extend(dog_pm_list)
        output_file(whole_pm_list, docname, fodername, dir + filename + ".kml")


def output_file(list, docname, fodername, file):
    doc = createKML(docname, fodername, list)
    output_file = codecs.open(file, "w")
    output_file.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
    output_file.close()


