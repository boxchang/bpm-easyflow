import json

from bases.database import tiptop_database
from bases.lib_database import getDBSchema
from data_tt.pr_data import pr_data
from enum import Enum

class Status(Enum):  #狀態初始排序順序，數字越小越前面
    PR_WAIT_APPROVE = 1
    PR_APPROVING = 10
    WAIT_PO = 20
    PO_APPROVING = 30
    WAIT_PO_ISSUE = 40
    WAIT_RECEIVING = 50
    WAIT_ACCEPTANCE = 60
    WAIT_STOCK = 70
    DONE = 80

class prprogress(object):
    status = ""

    def getPRProcessStatus(self, dictData):
        for data in dictData:
            print(data)
            if data['PMK25'] == '0':
                status = Status.PR_WAIT_APPROVE
            elif data['PMK25'] == 'S':
                status = Status.PR_APPROVING
            elif data['PMK18'] == 'Y' and data['PMM01'] is None: #請購單確認 未開立採購
                status = Status.WAIT_PO
            elif data['PMM25'] == 'S':
                status = Status.PO_APPROVING
            elif data['PMM18'] == 'Y' and data['PMM25'] == '1':
                status = Status.WAIT_PO_ISSUE
            elif data['PMM18'] == 'Y' and data['PMM25'] == '2':
                status = Status.WAIT_RECEIVING
            elif data['RVB07'] != '' and (data['RVB33'] is None or data['RVB33'] == ''):
                status = Status.WAIT_ACCEPTANCE
            elif data['RVB33'] != '' and (data['RVV17'] is None or data['RVV17'] == ''):
                status = Status.WAIT_STOCK
            data['STATUS_VALUE'] = status.value
            data['STATUS_NAME'] = status.name

        return dictData


    def getPRProgress(self, com_name, month):
        tt = pr_data(prod=True)
        query_result = tt.getUncompletedPRByMonth(com_name, month)

        #取得每筆PR的狀態
        query_result = self.getPRProcessStatus(query_result)

        #刪除不必要的欄位後，做Distinct，主要使用同一個來源，再對資料進行處理
        for temp in query_result:
            if 'PML02' in temp:
                del temp['PML02'] #請購項次
            if 'PML20' in temp:
                del temp['PML20'] #請購數量
            if 'PMN02' in temp:
                del temp['PMN02'] #採購項次
            if 'PMN20' in temp:
                del temp['PMN20'] #採購數量
            if 'RVB33' in temp:
                del temp['RVB33'] #驗收數量
            if 'RVV07' in temp:
                del temp['RVV07'] #收貨數量
            if 'RVV37' in temp:
                del temp['RVV37'] #入庫項次
            if 'RVV17' in temp:
                del temp['RVV17'] #入庫數量
            if 'RVV36' in temp:
                del temp['RVV36'] #入庫採購單號

        #進行Distinct的動作
        query_result = list({v['PMK01']:v for v in query_result}.values())
        print(query_result)
        print(query_result.__len__())
        return json.dumps(query_result)




# pg = prprogress()
# pg.getPRProgress('eaglesky', '2021-3')