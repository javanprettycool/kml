#coding=utf-8

__author__ = 'javan'


import kmlparse2
from process import *
from kmlparse2 import *
import os,sys
import zipfile

EXT = ".kml"

date = "2016_08_28"  #改这个

year = date.split('_')[0]
month = date.split('_')[1]
day = date.split('_')[2]

dir = u"F:/dataD/"+year+"/"+str(int(month))+u"月/"+month+day+"/"  #改这个

def unzip_file(filename, dirname):
    if dirname[:-1] != "/":
        dirname += "/"
    dir = dirname+filename

    if not os.path.exists(dir):
        print u"文件不存在"
        return

    srcZip = zipfile.ZipFile(dir, "r")
    for eachfile in srcZip.namelist():
        print "Unzip file %s ..." % eachfile
        eachfilename = os.path.normpath(os.path.join(dirname, eachfile))
        eachdirname = os.path.dirname(eachfilename)
        if not os.path.exists(eachdirname):
            os.makedirs(eachdirname)
        fd=open(eachfilename, "wb")
        fd.write(srcZip.read(eachfile))
        fd.close()
    srcZip.close()
    print "Unzip file succeed!"


pnd_filename = u"PNDCJ_" + date + u"_22pm"
caiji_filename = u"CAIJI_" + date + u"_21pm"

pnd_docname = u'PND\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'
pnd_fodername = u'PND\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'

caiji_docname = u'CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'
caiji_fodername = u'CAIJI\u91c7\u96c6[' + date[5:] + '_21-00 ~ ' + date[5:] + '_ 20-59]'

for i in os.listdir(dir):
    temp = os.path.join(dir,i)
    if os.path.isfile(temp):
        if os.path.splitext(temp)[1] == '.zip':
            unzip_file(i, dir)


pnd_path = dir + pnd_filename + EXT
caiji_path = dir + caiji_filename + EXT
pm_list = []

#pnd
pnd_list, pnd_handle_list, pnd_dog_list = kmlparse2.parse_pnd(pnd_path)
if len(pnd_handle_list) != 0:
    operate(pnd_list, dir+"pnd/", pnd_dog_list)
    outputKml((pnd_list, pnd_handle_list, pnd_dog_list), pnd_docname, pnd_fodername, dir+"pnd/", "new_"+pnd_filename+"_"+date[5:], 400)
    print str(len(pnd_handle_list))+u"条pnd数据"
else:
    print u"没有pnd数据"


#caiji
caiji_list, caiji_handle_list, caiji_dog_list = kmlparse2.parse_caiji(caiji_path)
check_duplicate(caiji_handle_list) #caiji的去重复,pnd暂时不无需要
if len(caiji_handle_list) != 0:
    operate(caiji_list, dir+"caiji/", caiji_dog_list)
    outputKml((caiji_list, caiji_handle_list, caiji_dog_list), caiji_docname, caiji_fodername, dir+"caiji/", "new_"+caiji_filename+"_"+date[5:], 1)
    print str(len(caiji_handle_list))+u"条caiji数据"
else:
    print u"没有caiji数据"














