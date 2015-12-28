#coding:utf-8
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
import codecs

def createKML(name, longitude, latitude, heading):
  return KML.Folder(
      KML.name(u'PND\u91c7\u96c6[10_14_21-00 ~ 10_15_ 20-59]'),
      KML.open('1'),
      KML.Placemark(
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
        KML.styleUrl('#m_ylw-pushpin'),
        KML.Point(
          KML.coordinates("%.6f"%longitude + "," + "%.6f"%latitude + ",0"),
        ),
      ),
    )



doc = KML.kml(
  KML.Document(
    KML.name(u'PND\u91c7\u96c6[10_14_21-00 ~ 10_15_ 20-59]'),
    KML.Style(
      KML.IconStyle(
        KML.scale('1.3'),
        KML.Icon(
          KML.href('http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'),
        ),
        KML.hotSpot(  x="20",
  y="2",
  xunits="pixels",
  yunits="pixels",
),
      ),
      id="s_ylw-pushpin_hl",
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
      id="m_ylw-pushpin",
    ),
    KML.Style(
      KML.IconStyle(
        KML.scale('1.1'),
        KML.Icon(
          KML.href('http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'),
        ),
        KML.hotSpot(  x="20",
  y="2",
  xunits="pixels",
  yunits="pixels",
),
      ),
      id="s_ylw-pushpin",
    ),
    KML.Folder(
      KML.name(u'PND\u91c7\u96c6[10_14_21-00 ~ 10_15_ 20-59]'),
      KML.open('1'),
      KML.Placemark(
        KML.name(u'[采集ID_39701]_1红灯_{}_(0)\u7ea2\u706f_\u89d2\u5ea6161_\u9650\u901f40\u7528\u6237(ZYCTCJ0002)\u91c7\u96c6@2015-10-09 17:32:48'),
        KML.LookAt(
          KML.longitude('114.889114'),
          KML.latitude('40.766674'),
          KML.altitude('0'),
          KML.heading('161.0'),
          KML.tilt('0'),
          KML.range('503.63751684255'),
          GX.altitudeMode('relativeToSeaFloor'),
        ),
        KML.styleUrl('#m_ylw-pushpin'),
        KML.Point(
          KML.coordinates('114.889114,40.766674,0'),
        ),
      ),
    ),
  ),
)
output_file = codecs.open("e:/gqss.kml", "w")
output_file.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
output_file.close()
