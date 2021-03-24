

#資料型態

#Dictionary
import json

from bases.database import bpm_database
from bases.lib_common import Cursor2Dict
from bases.lib_database import getDBSchema

dict1 = {"1": "January", "2": "February"}
print(dict1)

dict1["3"] = "March"
print(dict1)

#dict1合併dict2
dict2 = {"4": "April", "5": "May"}
dict3 = dict( dict1, **dict2 )
print(dict3)

#移除資料3
dict3.pop('3')
print(dict3)

for tmp in dict3:
    print(tmp)

for tmp in dict3.values():
    print(tmp)

#List
list1 = ['1', '2', '3', '4']
print(list1)

list1.append('5')
print(list1)

list1.append(dict3)
print(list1)

for tmp in list1:
    print(tmp)


#if判斷式
a = None
if 1 == 1:
    pass

if a is None:
    print("None")


#字串處理
a = "abcdefg"
print(a[2:])
print(a[2:5])

a = "abcd{name}"
a = a.format(name="Box")
print(a)


#Class
class test(object):
    prod = False

    #建構子
    def __init__(self, prod=False):
        self.prod = prod

    def test1_func(self):
        return self.prod

    # 取得TIPTOP資料
    def tiptop_data(self, com_name):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pmk01 from {db_name}.pmk_file where pmk25 = 'S'"""
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        results = cursor.fetchall()
        print(results)

        #將資料內容轉成DICT
        dict_result = Cursor2Dict(cursor)

        return dict_result

    def bpm_data(self):
        bpmdb = bpm_database(self.prod)
        sql = 'xxx'
        sql = "xxxxxxxxxxxxxxxxxxxxx" \
              "xxxxxxxxxxxxxxx"

        sql = """xxxxxxxxxxxxxxxxxxxxxxxxxx
                xx"""
        sql = """SELECT p.OID,'xxx',zo10 FROM apmt420 a, ProcessInstance p, WorkItem i
                         WHERE pmk01 = '{pr_no}' AND a.processSerialNumber = p.serialNumber AND p.contextOID = i.contextOID
                         AND workItemName = 'Save the form' AND i.currentState = 3"""
        sql = sql.format(pr_no="PR201-S211911000090")
        print(sql)
        cursor = bpmdb.execute_select_sql(sql)
        results = Cursor2Dict(cursor)

        if len(results) > 0:
            print("0")
        print(results)
        print(json.dumps(results))
        return json.dumps(results)


t = test()
print(t.test1_func())
print(t.bpm_data())






















