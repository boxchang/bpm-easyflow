import json

from bases.lib_common import json_format
from data_bpm.base_data import base_data


class josof_data(base_data):
    def SOFProcessSumbyMonth(self):
        sql = """SELECT sum(hdnTotalPrice1) TOTAL,sum(hdnAMT_FLDCC) FLDCC,SUBSTRING(dteNeed,0,5)+SUBSTRING(dteNeed,6,2) dteNeed FROM SO WHERE hdnTotalPrice1 IS NOT NULL AND dteNeed IS NOT NULL GROUP BY SUBSTRING(dteNeed,0,5)+SUBSTRING(dteNeed,6,2)"""
        cursor = self.bpmdb.execute_select_sql(sql)
        result = str(json.dumps(json_format(cursor)))

        return result

    def SOFProcess(self, month):
        sql = "SELECT txtName,txtDept,txtJO,txtAmt_A,txtAmt_ERP,txtAmt_B,txtAmt_C,txtAMT_D,hdnTotalPrice1 TOTAL,hdnAMT_FLDCC FLDCC,dteNeed, b.OID " \
              "FROM SO a, ProcessInstance b WHERE a.processSerialNumber = b.serialNumber AND CONVERT(char(6), b.createdTime, 112) = '" + month + "'"
        print(sql)
        cursor = self.bpmdb.execute_select_sql(sql)
        result = str(json.dumps(json_format(cursor)))

        return result

    def getSOFSumIncomebyMonth(self, month):
        sql = "SELECT isnull(sum(hdnTotalPrice1),0) TOTAL,isnull(sum(hdnAMT_FLDCC),0) FLDCC,'{month}' mm FROM SO " \
              "WHERE hdnTotalPrice1 IS NOT NULL AND dteNeed IS NOT NULL " \
              "AND SUBSTRING(dteNeed,0,5)+SUBSTRING(dteNeed,6,2) <= {month}"
        sql = sql.format(month=month)
        cursor = self.bpmdb.execute_select_sql(sql)
        result = json_format(cursor)

        return result