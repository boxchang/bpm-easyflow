import json
from bases.lib_common import json_format
from bases.lib_database import getDBSchema
from data_tt.base_data import base_data


class stockin_data(base_data):
    def getPOListDetail(self, com_name, prno):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pmn01,pmn04,pmn041,ima021,pmn20,pmn31t,pmn88 from {db_name}.pmn_file a, {db_name}.ima_file b where a.pmn04 = b.ima01 and pmn24 = '{prno}'"""
        sql = sql.format(sql, db_name=db_name, prno=prno)
        cursor = self.ttdb.execute_select_sql(sql)
        results = json.dumps(json_format(cursor))
        return results

    def getStockInSummaryByMonth(self, com_name, date_start, date_end):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select '{com_name}' com,to_char(rvu03,'yyyy-mm-dd') rvu03,count(rvu03) rcount from {db_name}.rvu_file where rvu03 between to_date('{date_start}','YYYY/MM/DD') and to_date('{date_end}','YYYY/MM/DD') group by '{com_name}',rvu03 order by rvu03"""
        sql = sql.format(sql, db_name=db_name, com_name=com_name, date_start=date_start, date_end=date_end)
        cursor = self.ttdb.execute_select_sql(sql)

        query_result = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

        return query_result

    def getStockInInfoByDay(self, com_name, stockin_date):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select '{com_name}' com,rvu01,to_char(rvu03,'yyyy-mm-dd') rvu03,gem02,zx02,rvu05,ta_rvu02,rvuconf from {db_name}.rvu_file a,{db_name}.zx_file b,{db_name}.gem_file c where a.rvu07 = b.zx01 and a.rvu06 = c.gem01 and a.rvu03 = to_date('{stockin_date}','YYYY/MM/DD') order by zx02"""
        sql = sql.format(sql, db_name=db_name, com_name=str(com_name).upper(), stockin_date=stockin_date)
        print(sql)
        cursor = self.ttdb.execute_select_sql(sql)

        query_result = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

        return query_result

    def getStockInDetailByNo(self, com_name, sno):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select rvv05,rvv31,rvv031,ima021,rvv17,rvv35,rvv36,imd02,ime03 from {db_name}.rvv_file a, {db_name}.ima_file b,(select * from {db_name}.imd_file x,{db_name}.ime_file y where x.imd01=y.ime01) c where a.rvv31 = ima01 and a.rvv32 = c.imd01(+) and a.rvv33 = c.ime02(+) and rvv01 = '{sno}'"""
        sql = sql.format(sql, db_name=db_name, sno=sno)
        print(sql)
        cursor = self.ttdb.execute_select_sql(sql)

        query_result = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

        return query_result

# tt = stockin_data(prod=True)
# query_result = tt.getStockInInfoByDay("eaglesky", "2020-10-16")

