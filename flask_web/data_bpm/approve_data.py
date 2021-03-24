from bases.lib_common import Cursor2Dict
from data_bpm.base_data import base_data


class approve_data(base_data):
    def pr_approved_data(self, pr_no):
        datetime = None
        oid = ""
        sql = """SELECT p.OID,completedTime FROM apmt420 a, ProcessInstance p, WorkItem i
                 WHERE pmk01 = '{pr_no}' AND a.processSerialNumber = p.serialNumber AND p.contextOID = i.contextOID
                 AND workItemName = 'Save the form' AND i.currentState = 3"""
        sql = sql.format(pr_no=pr_no)
        cursor = self.bpmdb.execute_select_sql(sql)
        results = Cursor2Dict(cursor)
        if len(results) > 0:
            datetime = results[0]["completedTime"]
            oid = results[0]["OID"]
        return datetime, oid