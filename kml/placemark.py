#coding=utf-8
__author__ = 'Javan'

class placemark(object):
    def __init__(self, name="", dogtype="", id="", form="", handletype="", match ="", longitude=0, latitude=0, heading=0, speedlimit=0, account="", time="", cost="", matched="", create_time="",md5=""):
        self.name = name
        self.dogtype = dogtype
        self.id = id
        self.form = form
        self.match = match
        self.matchlist = []
        self.handletype = handletype
        self.longitude = longitude
        self.latitude = latitude
        self.heading = heading
        self.speedlimit = speedlimit
        self.account = account
        self.time = time
        self.cost = cost
        self.matched = matched
        self.create_time = create_time
        self.md5 = md5


    def transforForm(self):
        if self.form == u"违规稽查" or self.form == u"事故多发" or self.form == u"禁止掉头":
            pass
        elif self.form == u"红灯":
            self.form = u"0闯红灯拍照"
        elif self.form == u"测速":
            self.form = u"1测速照相"
        elif self.form == u"辅道测速照相":
            self.form = u"11右侧辅道测速照相"
        elif self.form == u"高速出口":
            self.form = u"25高速出口"
        elif self.form == u"收费站":
            self.form = u"28收费站"
        elif self.form == u"急转弯":
            self.form = u"32急转弯路段"
        elif self.form == u"休息区":
            self.form = u"29休息区"
        elif self.form == u"加油站":
            self.form = u"27加油站"
        elif self.form == u"电子监控":
            self.form = u"16电子监控"
        elif self.form == u"高清摄像":
            self.form = u"7高清摄像"
        elif self.form == u"流动测速":
            self.form = u"2流动测速"
        elif self.form == u"事故多发":
            self.form = u"23事故多发"
        elif self.form == u"进入区间测速":
            self.form = u"3进入区间测速"
        elif self.form == u"离开区间测速":
            self.form = u"4离开区间测速"


    def copy(self, pm):
        self.longitude = pm.longitude
        self.latitude = pm.latitude

    def check_diff(self, pm):
        if self.longitude == pm.longitude and self.latitude == pm.latitude and self.form == pm.form \
            and self.speedlimit == pm.speedlimit and self.heading == pm.heading and self.handletype == pm.handletype:
            return True
        else:
            return False

class rectangle(object):
    pass
