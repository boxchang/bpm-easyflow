import datetime
import json

from bases.lib_database import getComList
from data_bpm.approve_data import approve_data
from data_tt.pr_data import pr_data


class purmng(object):

    def getPRnot2PO(self):
        today = datetime.datetime.today()
        query_result = []
        tt = pr_data(prod=True)
        coms = getComList()
        bpm = approve_data()

        for com_name in coms:
            tmp_results = tt.getApprovedPRNot2PO(com_name)  #取得TT PR未轉PO的單據
            for tmp_result in tmp_results:
                pr_no = tmp_result['PMK01']  #請購單號
                approved_time, oid = bpm.pr_approved_data(pr_no)  #獲得BPM的資料 by PR No
                queue_time = today - approved_time  #算出QTime
                tmp_result['APPROVED_TIME'] = approved_time.strftime('%Y-%m-%d %H:%M:%S')  #簽核完成時間
                tmp_result['OID'] = oid  #取得OID要在前端可以開啟單據
                tmp_result['QUEUE_TIME'] = queue_time.days  #QTime時間格式轉成天
                tmp_result['COM'] = com_name.upper()   #資料放入公司名稱
            query_result += tmp_results

        query_result.sort(key=lambda k: (k.get('QUEUE_TIME', 0)), reverse=True)

        return json.dumps(query_result)


    def getPRItemNot2PO(self):
        today = datetime.datetime.today()
        query_result = []
        tt = pr_data(prod=True)
        coms = getComList()
        bpm = approve_data()

        for com_name in coms:
            tmp_results = tt.getApprovedPRItemNot2PO(com_name)  #取得TT PR未轉PO的單據
            for tmp_result in tmp_results:
                pr_no = tmp_result['PMK01']  #請購單號
                approved_time, oid = bpm.pr_approved_data(pr_no)  #獲得BPM的資料 by PR No
                if approved_time is not None:
                    queue_time = today - approved_time  #算出QTime
                    tmp_result['APPROVED_TIME'] = approved_time.strftime('%Y-%m-%d %H:%M:%S')  #簽核完成時間
                    tmp_result['OID'] = oid
                else:
                    tmp_result['APPROVED_TIME'] = None
                tmp_result['QUEUE_TIME'] = queue_time.days  #QTime時間格式轉成天
                tmp_result['COM'] = com_name.upper()   #資料放入公司名稱
            query_result += tmp_results

        query_result.sort(key=lambda k: (k.get('QUEUE_TIME', 0)), reverse=True)

        return json.dumps(query_result)

    def getPOnot2Deliver(self):
        today = datetime.datetime.today()
        query_result = []
        tt = pr_data(prod=True)
        coms = getComList()
        for com_name in coms:
            tmp_results = tt.getIssuedPONotDeliver(com_name)
            for tmp_result in tmp_results:
                queue_time = today - tmp_result["PMN33"]  # 算出QTime
                tmp_result["PMN33"] = tmp_result["PMN33"].strftime('%Y-%m-%d')
                tmp_result['QUEUE_TIME'] = int(queue_time.days)  # QTime時間格式轉成天
                tmp_result['COM'] = com_name.upper()
                if tmp_result['APB06'] is not None:
                    tmp_result['PREPAY'] = 'Y'
                else:
                    tmp_result['PREPAY'] = 'N'
                query_result.append(tmp_result)

        #query_result.sort(key=lambda k: (k.get('QUEUE_TIME', 0)), reverse=True)
        query_result = sorted(query_result, key=lambda k: (k['VENDOR'].lower(), k['QUEUE_TIME']))

        return json.dumps(query_result)

    def getRejectData(self, date_from, date_to):
        today = datetime.datetime.today()
        query_result = []
        tt = pr_data(prod=True)
        coms = getComList()
        for com_name in coms:
            tmp_results = tt.getQReject(com_name, date_from, date_to)
            for tmp_result in tmp_results:
                tmp_result["RVU03"] = tmp_result["RVU03"].strftime('%Y-%m-%d')
                tmp_result['COM'] = com_name.upper()
                query_result.append(tmp_result)

        query_result = sorted(query_result, key=lambda k: (k['VENDOR'].lower()))

        return json.dumps(query_result)

pur = purmng()
results = pur.getPRnot2PO()