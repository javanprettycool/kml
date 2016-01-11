__author__ = 'Javan'

class placemark(object):
    def __init__(self, name="", dogtype="", id="", form="", handletype="", match ="", longitude=0, latitude=0, heading=0, speedlimit=0, account="", time="", cost=""):
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
