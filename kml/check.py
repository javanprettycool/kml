#coding=utf-8
import xlrd



def checkexcel(path):
    list = []
    if path is None or "":
        return False
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    i = 3



    while i < table.nrows:
        array = table.row_values(i)
        if array[1] == u"1新增":
            if array[4] == "" or array[5] == "" or array[6] == "" or array[9] == "" or array[10] == "":
                list.append(array)
        if array[1] == u"2修改" or array[1] == u"3删除":
            if array[3] == "" :
                list.append(array)
        i += 1
    if list:
        print "some mistake in above "+ path + ":"
        print list
        return False
    else:
        print path + " is almost ok"
        return True


checkexcel(u"E:/dataD/2015/12月/1216/pnd_zzf_2015_12_16(2).xls")