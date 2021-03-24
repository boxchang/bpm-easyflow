import calendar
import datetime
import time

def json_format(cursor):
    return [dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()]


def pickColor(index):
    colors = ['#42E3F5', '#19E37D', '#D1F542', '#F5F242', '#FF9EEA', '#FFBAC8', '#FFBAE8', '', '', '', '', '', '', '',
              '', '']
    return colors[index]


# 獲取第一天
def getFirstAndLastDay(year, month):
    # 獲取當前月的第一天的星期和當月總天數
    weekDay, monthCountDay = calendar.monthrange(year, month)
    # 獲取當前月份第一天
    firstDay = datetime.date(year, month, day=1)
    # 獲取当前月份最后一天
    lastDay = datetime.date(year, month, day=monthCountDay)
    # 返回第一天和最后一天
    return firstDay, lastDay

#Cursor to Dictionary
def Cursor2Dict(cursor):
    results = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))

    return results


def AppendCursor2Dict(cursor, results):
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))

    return results


def dateRange(bgn, end):
    fmt = '%Y-%m-%d'
    bgn = int(time.mktime(time.strptime(bgn,fmt)))
    end = int(time.mktime(time.strptime(end,fmt)))
    return [time.strftime(fmt,time.localtime(i)) for i in range(bgn,end+1,3600*24)]





