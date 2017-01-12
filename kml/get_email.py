#coding=utf-8
import poplib
from email import parser
import email
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

file_path = 'file/'

pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)

#Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]

messages.reverse()
tmp = messages[:]
messages = tmp[:5]

#Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
for message in messages:
    subject = unicode(message.get('subject'), 'utf-8')
    h = email.Header.Header(subject)
    dh = email.Header.decode_header(h)
    if subject.find('PND采集数据') >= 0 or subject.find('昨日电子狗采集数据') >= 0:
        print subject


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
                #end if
                fEx = open(file_path+"%s"%(fname), 'wb')
                fEx.write(data)
                fEx.close()

pop_conn.quit()



