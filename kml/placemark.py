#coding=utf-8
__author__ = 'Javan'
import re

class placemark(object):


    __dict = {"0":u"0闯红灯照相",
        "1":u"1测速照相",
        "16":u"16电子监控",
        "7":u"7高清摄像抓拍",
        "2":u"2流动测速",
        "3":u"3区间测速起点",
        "4":u"4区间测速终点",
        "5":u"5高架桥上测速照相",
        "6":u"6区间测速路段",
        "8":u"8桥下闯红灯照相",
        "9":u"9右侧辅道闯红灯照相",
        "10":u"10右侧辅道流动测速区",
        "11":u"11右侧辅道测速照相",
        "45":u"45路口安全提示",
        "46":u"45违规拍照",
        "40":u"40禁止变道",
        "27":u"27加油站",
        "41":u"41铁路道口",
        "42":u"42公交专用车道监控路段",
        "43":u"43临时停车禁止路段",
        "44":u"44压线拍照",
        "17":u"17单行道",
        "18":u"18禁止左转",
        "19":u"19禁止右转",
        "20":u"20禁止掉头",
        "22":u"22落石路段",
        "23":u"23事故多发路段",
        "24":u"24急下坡路段",
        "26":u"26违规稽查路段",
        "32":u"32急转弯路段",
        "33":u"33山区路段",
        "34":u"34冰雪路段",
        "28":u"28收费站",
        "29":u"休息区",
        "25":u"25高速出口",
        "35":u"35检查站"}

    __broter = None

    scale = []    #存放周围的点
    match_each = None
    need_to_pay = True

    HANDLE_ADD = 1   #处理类型
    HANDLE_UPDATE = 2
    HANDLE_DELETE = 3

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

    def get_type(self, type):
        if type in self.__dict.keys():
            return self.__dict[type]
        return None

    def get_brother(self):
        return self.__broter

    def set_brother(self, placemark):
        self.__broter = placemark


    def change_handletype(self, change_to):
        type = int(change_to)
        name = self.name

        if type == self.HANDLE_UPDATE:
           self.name = name.replace(u"1新增", u"2修改")
        elif type == self.HANDLE_DELETE:
            self.name = name.replace(u"1新增", u"3删除")

    def cmp(self, pm):
        if self.latitude == pm.latitude and self.longitude == pm.longitude  \
            and ( pm.heading-10 < self.heading < pm.heading+10 or self.heading-10 < pm.heading < self.heading+10):
            return True
        return False

    #改变状态为修改，匹配到相应的点
    def change_match(self, dog):
        self.handletype = placemark.HANDLE_UPDATE
        self.longitude = dog.longitude
        self.latitude = dog.latitude
        self.heading = dog.heading
        self.match = dog.id
        self.change_handletype(placemark.HANDLE_UPDATE)

class rectangle(object):
    pass
