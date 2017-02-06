#coding=utf-8

__author__ = 'javan'


import kmlparse2
from process import *
from kmlparse2 import *
import os,sys
import zipfile
import time

EXT = ".kml"

#date = "2017_01_14"  #改这个
date = time.strftime('%Y_%m_%d', time.localtime(time.time()-24*60*60))

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
#
# for p in pnd_handle_list[:]:
#     if p.id < 124836:
#         print p.id
#         pnd_handle_list.remove(p)

if len(pnd_handle_list) != 0:
    result_query = operate(pnd_handle_list, dir+"pnd/", pnd_dog_list)
    _query = []
    _tmp = []
    for i in result_query[:]:
        #print i
        if not i:
            print i
            continue

        if i[0].form == '1' and i[0].handletype == placemark.HANDLE_DELETE:
            _query.insert(0, i)
        elif i[0].form == '0':
            _query.append(i)
        else:
            _tmp.append(i)

    _query.extend(_tmp)
    result_query = _query
    outputKml((pnd_list, result_query, pnd_dog_list), pnd_docname, pnd_fodername, dir+"pnd/", "new_"+pnd_filename+"_"+date[5:], 400)
    count = 0
    for q in result_query:
        count += len(q)
    print str(count)+u"条pnd数据"
else:
    print u"没有pnd数据"


#caiji
caiji_list, caiji_handle_list, caiji_dog_list = kmlparse2.parse_caiji(caiji_path)
check_duplicate(caiji_handle_list) #caiji的去重复,pnd暂时不无需要
if len(caiji_handle_list) != 0:
    result_query = operate(caiji_handle_list, dir+"caiji/", caiji_dog_list)
    outputKml((caiji_list, result_query, caiji_dog_list), caiji_docname, caiji_fodername, dir+"caiji/", "new_"+caiji_filename+"_"+date[5:], 1)
    count = 0
    for q in result_query:
        count += len(q)
    print str(count)+u"条caiji数据"

else:
    print u"没有caiji数据"

#打开文件夹
os.startfile(dir)











