#coding=utf-8
import poplib
from email import parser
import email
import os
import time


def get_charset(message, default="ascii"):
    #Get the message charset
    return message.get_charset()

def _unicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)

host = 'pop.exmail.qq.com'
username = 'zhangzhifeng@t-road.cn'
password = 'zzf1992'

today = time.time()
yesterday = today - 24*60*60
date_time = time.localtime(yesterday)
file_path = u"F:/dataD/"+str(date_time.tm_year)+"/"+str(date_time.tm_mon)+u"月/"+str(date_time.tm_mon).zfill(2)+str(date_time.tm_mday).zfill(2)+"/"
#F:/dataD/2017/2月/0206/

pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)

#Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]

#Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]

for message in messages:
    subject = unicode(message.get('subject'), 'utf-8')
    date = message.get('date')
    if date != '':
        date = date.split(',')[1].split('+')[0].strip()
        time_arr = time.strptime(date,'%d %b %Y %H:%M:%S')
        timestamp = time.mktime(time_arr)
        #只要前一天的邮件
        if yesterday > timestamp or  timestamp > today:
            continue
    h = email.Header.Header(subject)
    dh = email.Header.decode_header(h)
    if subject.find(u'PND采集数据') >= 0 or subject.find(u'昨日电子狗采集数据') >= 0:
        for part in message.walk():
            contenttype = part.get_content_type()
            filename = part.get_filename()
            charset = get_charset(part)
            #是否有附件
            if filename:
                h = email.Header.Header(filename)
                dh = email.Header.decode_header(h)
                fname = dh[0][0]
                encodeStr = dh[0][1]
                data = part.get_payload(decode=True)
                if encodeStr != None:
                    fname = fname.decode(encodeStr, charset)

                (shotname,extension) = os.path.splitext(fname)
                #只要kml文件
                if extension == '.kml':
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    fEx = open(file_path+"%s"%(fname), 'wb')
                    fEx.write(data)
                    fEx.close()
pop_conn.quit()

os.system("python pnd_caiji.py")



