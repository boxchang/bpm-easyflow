import json
import time
from enum import Enum

from bases.lib_common import Cursor2Dict, AppendCursor2Dict
from data_bpm.base_data import base_data

class Status(Enum): #狀態初始排序順序，數字越小越前面
    JO_ONGOING = 1
    WAIT_SOF = 2
    JO_DONE = 3
    WAIT_SOF_CHANGE = 4
    SOF_ONGOING = 5
    SOF_WORKING = 6
    SOF_CONFIRM = 7
    SOF_DONE = 8
    SOF_REJECT = 9
    JO_REJECT = 10
    JO_CANCEL = 11


class ProcessDetailObject(object):
    oid = ""
    subject = ""
    com = ""
    status = ""
    status_key = 0

    def __init__(self, oid, subject, status_key, status, form_type):
        self.oid = oid
        self.subject = subject
        self.com = self.getCompany(subject, form_type)  # 從主旨取得公司名稱
        self.status_key = status_key.value
        self.status = status

    def getCompany(self, subject, form_type):
        result = ""

        if form_type == "JO":
            index_s = subject.find('：') + 2
            index_e = subject.find('-')
            result = subject[index_s:index_e] if subject != None else ""
        elif form_type == "SOF":
            index_s = subject.find('JO：') + 3
            index_e = subject.find('-')
            result = subject[index_s:index_e] if subject != None else ""


        return result


class ProcessObject(base_data):
    month = ""
    jo_qty = 0
    jo_ongoing = 0
    jo_done = 0
    wait_sof = 0
    jo_reject = 0
    jo_cancel = 0

    sof_qty = 0
    sof_ongoing = 0
    wait_sof_change = 0
    sof_working = 0
    sof_done = 0
    sof_reject = 0
    sof_confirm = 0
    sofc_qty = 0

    detail_list = []

    def __init__(self, month):
        self.month = month
        self.jo_qty = 0
        self.jo_ongoing = 0
        self.jo_done = 0
        self.wait_sof = 0
        self.jo_reject = 0
        self.jo_cancel = 0
        self.sof_qty = 0
        self.sof_ongoing = 0
        self.wait_sof_change = 0
        self.sof_working = 0
        self.sof_done = 0
        self.sof_reject = 0
        self.sof_confirm = 0
        self.sofc_qty = 0
        super(ProcessObject, self).__init__()

    def isFLDCCActivity(self, OID):
        result = False
        sql = """SELECT * FROM ProcessInstance a, WorkItem b WHERE a.OID ='{OID}' 
                 AND a.contextOID = b.contextOID AND b.currentState in (0,1) AND b.workItemName = 'FLDCC Staff'"""
        sql = sql.format(OID=OID)
        cursor = self.bpmdb.execute_select_sql(sql)
        results = Cursor2Dict(cursor)
        if len(results) > 0:
            result = True

        return result

    def isConfirmActivity(self, OID):
        result = False
        sql = """SELECT * FROM ProcessInstance a, WorkItem b WHERE a.OID ='{OID}' 
                 AND a.contextOID = b.contextOID AND b.currentState in (0,1) AND b.workItemName = 'Confirmation'"""
        sql = sql.format(OID=OID)
        cursor = self.bpmdb.execute_select_sql(sql)
        results = Cursor2Dict(cursor)
        if len(results) > 0:
            result = True

        return result

    def haveSOFChange(self, OID):
        return False

    def getFormType(self, form_id):
        result = ""

        if form_id == "PKG_SOF" or form_id == "PKG_SO_FORM" or form_id == "JOPROCESS_SOF" \
                        or form_id == "PKG_SOF_CNGNOTE" or form_id == "JOPROCESS_SOF_CHG":
            result = "SOF"
        elif form_id == "PKG_JO_FORM" or form_id == "JOPROCESS_JOF":
            result = "JO"

        return result


    def analyze(self, db_datas):
        self.detail_list = []
        for db_data in db_datas:
            if self.month == db_data["createdTime"]:
                status = ""
                form_type = self.getFormType(db_data["ID"])
                if form_type == "JO":  # JO資料統計
                    # JO呈現欄位定義有四種
                    # JO總數量 = JO簽核中 + JO完成簽核 + JO FLDCC退件 (由Chart呈現)
                    # JO簽核中 = 狀態<3
                    # JO完成簽核(待開SOF)
                    # JOFLDCC退件
                    if db_data["currentState"] < 3:  # JO 進行中
                        status_key = Status.JO_ONGOING

                    elif db_data["currentState"] == 3 and db_data["chkSOF"] == "Y":  # JO 完成簽核

                        if db_data["SOFN"] is None:  # 沒有SOF單號
                            status_key = Status.WAIT_SOF  #JO單尚未開出SOF
                        else:
                            status_key = Status.JO_DONE   #JO單已經開出SOF

                    elif db_data["currentState"] == 3 and db_data["chkSOF"] == "":  # JO FLDCC退件
                        status_key = Status.JO_REJECT

                    elif db_data["currentState"] == 4 or db_data["currentState"] == 5:  # JO 取消
                        status_key = Status.JO_CANCEL


                if form_type == "SOF":  # SOF資料統計
                    # SOF呈現欄位定義有六種
                    # SOF總數量 = SOF簽核中(包含SOF Change)+SOF完成簽核(包含SOF Change)+SOF退件 (由Chart呈現)
                    # SOF簽核中 = (SOF 狀態<3 and Brayn關卡之前) or (SOF Change Note狀態<3 and Brayn關卡之前)
                    # SOF施工中 = (SOF 狀態=1 and Brayn關卡) or (SOF Change Note and Bryan關卡)
                    # 待開SOF Change Note = ((SOF rdoCloseStatus<>"Close JO") and (SOF Change Note沒有資料))
                    # SOF完成 = 狀態=3 and rdoCloseStatus = "Close JO"
                    # SOF取消 = 狀態=4 or 5

                    if db_data["currentState"] == 1 and (self.isFLDCCActivity(db_data["OID"])):  # SOF施工中
                        status_key = Status.SOF_WORKING

                    if db_data["currentState"] == 1 and (self.isConfirmActivity(db_data["OID"])):  # SOF確認中
                        status_key = Status.SOF_CONFIRM

                    elif db_data["currentState"] < 3:  # SOF簽核中
                        status_key = Status.SOF_ONGOING

                    elif db_data["SOF_CLS"] == "Requirement Change" and len(db_data["SOFCN"]) == 0:  # 待開SOF Change Note
                        status_key = Status.WAIT_SOF_CHANGE

                    elif db_data["currentState"] == 3:
                        if (db_data["SOF_CLS"] == "Close JO" or db_data["SOFC_CLS"] == "Close JO"):  # SOF完成
                            status_key = Status.SOF_DONE
                        else:
                            if not self.haveSOFChange(db_data["SOFCN"]):
                                status_key = Status.WAIT_SOF_CHANGE

                    if db_data["currentState"] == 4 or db_data["currentState"] == 5:  # SOF取消
                        status_key = Status.SOF_REJECT


                    if db_data["ID"] == "PKG_SOF_CNGNOTE" or db_data["ID"] == "JOPROCESS_SOF_CHG":  # SOF資料統計
                        self.sofc_qty += 1  # SOF Change數量的加總

                status = self.buildStatus(status_key)
                process_detail = ProcessDetailObject(db_data["OID"], db_data["subject"], status_key, status, form_type)
                self.detail_list.append(process_detail)

        self.jo_qty = self.jo_ongoing + self.wait_sof + self.jo_done + self.jo_reject # 數量的加總，JO_CANCEL是部門主管退件，暫時不列入
        self.sof_qty += self.sof_ongoing + self.sof_done + self.sof_reject + self.sof_confirm  # 數量的加總


    def buildStatus(self, status_code):
        status = ""

        if status_code == Status.JO_ONGOING:
            self.jo_ongoing += 1
            status = "JO ON-GOING"
        elif status_code == Status.JO_DONE:
            self.jo_done += 1
            status = "JO DONE"
        elif status_code == Status.WAIT_SOF:
            self.wait_sof += 1
            status = "WAIT SOF"
        elif status_code == Status.JO_REJECT:
            self.jo_reject += 1
            status = "JO REJECT"
        elif status_code == Status.JO_CANCEL:
            self.jo_cancel += 1
            status = "JO CANCEL"
        elif status_code == Status.SOF_ONGOING:
            self.sof_ongoing += 1
            status = "SOF ON-GOING"
        elif status_code == Status.WAIT_SOF_CHANGE:
            self.wait_sof_change += 1
            status = "WAIT SOF CHANGE"
        elif status_code == Status.SOF_WORKING:
            self.sof_working += 1
            status = "SOF WORKING"
        elif status_code == Status.SOF_DONE:
            self.sof_done += 1
            status = "SOF DONE"
        elif status_code == Status.SOF_REJECT:
            self.sof_reject += 1
            status = "SOF REJECT"
        elif status_code == Status.SOF_CONFIRM:
            self.sof_confirm += 1
            status = "SOF CONFIRM"

        return status


    def setJoQty(self, jo_qty):
        self.jo_qty = jo_qty

    def getJoQty(self):
        self.jo_qty

    def setSofQty(self, sof_qty):
        self.sof_qty = sof_qty

    def getSofQty(self):
        self.sof_qty


class josofsum_data(base_data):


    #JOSOF Summary
    def getJOSOFSummary(self, year):
        month_data = {year + str(mm).zfill(2): 0 for mm in range(1, 13)}

        sql = """SELECT a.OID,format(a.createdTime,'yyyyMM') createdTime,processDefinitionId ID,a.subject,a.currentState, 
                 b.chkSOF,b.SerialNumber24 JON,c.SerialNumber24 SOFN,'' SOFCN,'' SOF_CLS, '' SOFC_CLS
                    FROM ProcessInstance a 
                    LEFT OUTER JOIN JO b ON a.serialNumber=b.processSerialNumber 
                    LEFT OUTER JOIN SO c ON c.txtJO = b.SerialNumber24 
                    WHERE a.processDefinitionId IN ('PKG_JO_FORM','JOPROCESS_JOF')
                    AND createdTime BETWEEN CAST('{year}0101' as DATETIME) AND CAST('{year}1231' as DATETIME)"""
        sql = sql.format(year=year)
        print(sql)
        cursor = self.bpmdb.execute_select_sql(sql)
        results = Cursor2Dict(cursor)

        sql = """SELECT a.OID,format(a.createdTime,'yyyyMM') createdTime,processDefinitionId ID,a.subject,a.currentState, 
                    'Y' chkSOF,c.txtJO JON,c.SerialNumber24 SOFN,'' SOFCN,c.rdoCloseStatus SOF_CLS, '' SOFC_CLS
                    FROM ProcessInstance a 
                    LEFT OUTER JOIN SO c ON c.processSerialNumber = a.serialNumber 
                    WHERE a.processDefinitionId IN ('PKG_SOF','PKG_SO_FORM','JOPROCESS_SOF')
                    AND createdTime BETWEEN CAST('{year}0101' as DATETIME) AND CAST('{year}1231' as DATETIME)"""
        sql = sql.format(year=year)
        print(sql)
        cursor = self.bpmdb.execute_select_sql(sql)
        AppendCursor2Dict(cursor, results)

        sql = """SELECT a.OID,format(a.createdTime,'yyyyMM') createdTime,processDefinitionId ID,a.subject,a.currentState, 
                    '' chkSOF,d.txtJO JON,'' SOFN,d.SerialNumber24 SOFCN,'' SOF_CLS, d.rdoCloseStatus SOFC_CLS
                    FROM ProcessInstance a 
                    LEFT OUTER JOIN SOF_Change_Note d ON d.processSerialNumber = a.serialNumber
                    WHERE a.processDefinitionId IN ('PKG_SOF_CNGNOTE','JOPROCESS_SOF_CHG')
                                     AND createdTime BETWEEN CAST('{year}0101' as DATETIME) AND CAST('{year}1231' as DATETIME)"""
        sql = sql.format(year=year)
        print(sql)
        cursor = self.bpmdb.execute_select_sql(sql)
        AppendCursor2Dict(cursor, results)


        summary = {}
        for month in month_data:
            process = ProcessObject(month)
            process.analyze(results)
            summary[month] = process

        return summary




# js = josofsum_data()
# results = js.getJOSOFSummary("2020")
# month = "202009"
# ajax_data = [result.__dict__ for result in js.getJOSOFSummary(month[0:4])[month].detail_list]
# ajax_data = sorted(ajax_data, key=lambda i: int(i['status_key']))
# print(ajax_data)

