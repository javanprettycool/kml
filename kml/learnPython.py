#coding=utf-8
import os
import time

#os.system("python pnd_caiji.py")

exit()
print time.localtime().tm_year

a = "Mon, 6 Feb 2017 09:00:41 +0800"
if a != '':
    date = a.split(',')[1].split('+')[0].strip()
print date
time_arr = time.strptime(date,'%d %b %Y %H:%M:%S')
timestamp = time.mktime(time_arr)
print timestamp


today = time.time()
yesterday = today - 24*60*60
print today

x = time.localtime(timestamp - 24*60*60)
print x
print time.strftime('%Y-%m-%d %H:%M:%S',x)


exit()
s = '中国'

su = u'中国'

#s为unicode先转为utf-8

#因为s为所在的.py(# -*- coding=UTF-8 -*-)编码为utf-8


filename = 'CAIJI_2017_02_05_21pm.html'
(filepath,tempfilename) = os.path.split(filename)
(shotname,extension) = os.path.splitext(tempfilename)

print filepath
exit()

u = unicode(s, 'utf8')
print u.encode('utf8')
exit()

a = s.decode('utf-8').encode('utf-8')
print a
exit()
s_unicode =  s.encode('UTF-8')
print s_unicode
print s_unicode == su
exit()
string = unicode('é',  'utf8')
log = open('file/debug.log', 'w')
log.write(string)
