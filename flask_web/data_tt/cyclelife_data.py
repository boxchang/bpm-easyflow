from bases.lib_database import getDBSchema
from data_tt.base_data import base_data


class cyclelife_data(base_data):

    # 簽核中的請購單 AND 已簽核完成，但未開立PO
    def PR_processing(self, com_name):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pmk01 from {db_name}.pmk_file where pmk25 = 'S'"""
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        results = cursor.fetchall()
        return results

    # 簽核中的採購單
    def PO_processing(self, com_name):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pmm01 from {db_name}.pmm_file where pmm25 = 'S'"""
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        results = cursor.fetchall()
        return results

    # 採購已簽核但未收貨
    def RR_processing(self, com_name):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pmm01 from (
                 select pmm01,rva01 from {db_name}.pmm_file a,{db_name}.rva_file b where pmm25 = '2' and a.pmm01 = b.rva02(+)) aa where aa.rva01 is null """
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        results = cursor.fetchall()
        return results

    # 已收貨，應付帳款未建
    def AP_processing(self, com_name):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select rvu02 from (
                 select rvu02,apb01 from {db_name}.rvu_file a,{db_name}.apb_file b where rvu17 = '1' and a.rvu02 = b.apb21(+)) aa where aa.apb01 is null """
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        results = cursor.fetchall()
        return results