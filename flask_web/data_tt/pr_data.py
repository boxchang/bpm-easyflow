import json

from bases.database import tiptop_database
from bases.lib_common import getFirstAndLastDay, json_format, Cursor2Dict
from bases.lib_database import getDBSchema
from data_tt.base_data import base_data

class pr_data(base_data):

    #請購<-->採購<-->入庫   條件 : 入庫數量不等於採購數量 或 尚未入庫
    def getUncompletedPRByMonth(self, com_name, month):
        db_name = getDBSchema(com_name, self.prod)
        #param = data.get('yyyymm')
        yyyymm = str(month).split('-')
        firstDay, lastDay = getFirstAndLastDay(int(yyyymm[0]), int(yyyymm[1]))
        firstDay = firstDay.strftime("%Y-%m-%d")
        lastDay = lastDay.strftime("%Y-%m-%d")

        sql = """select * from (
                select to_char(pml34,'yyyymmdd') pml34,pmk01,pml041,ima021,pml02,pml20,pml07,pmk18,pmk25,gen02,gem02,pmm01,pmm18,pmm25,pmn02,pmn20,sum(rvb07) rvb07,sum(rvb33) rvb33,rvv36,rvv37,sum(rvv17) rvv17 from
                (select pml34,pml041,pml04,pmk01,pmk18,pmk25,pmk12,pmk13,pml02,pml20,pml07 from {db_name}.pmk_file a, {db_name}.pml_file b where a.pmk01 = b.pml01 
                and b.pml34 between to_date('{firstDay}','yyyy-mm-dd') and to_date('{lastDay}','yyyy-mm-dd') and a.pmk25 in ('0','1','2','S')) pr,
                (select * from {db_name}.pmm_file a, {db_name}.pmn_file b where a.pmm01 = b.pmn01 and a.pmm25 not in('6','9')) po,
                (select * from {db_name}.rva_file a, {db_name}.rvb_file b where rvb01 = rva01 and rva32 <> '9') rv,
                (select * from {db_name}.rvu_file a, {db_name}.rvv_file b where a.rvu01 = rvv01 and rvu17 <> '9') r,
                {db_name}.gen_file u, {db_name}.gem_file dept,{db_name}.ima_file ima
                where pr.pmk01 = po.pmn24(+) and pr.pml02 = po.pmn25(+) 
                and pmm01 = rv.rvb04(+) and pmn02 = rv.rvb03(+)
                and rv.rva01 = r.rvu02(+) and rv.rvb02 = r.rvv05(+) 
                and u.gen01=pmk12 and dept.gem01=pmk13
                and ima.ima01 = pr.pml04 
                group by pml34,pmk01,pml041,ima021,pml02,pml20,pml07,pmk18,pmk25,gen02,gem02,pmm01,pmm18,pmm25,pmn02,pmn20,rvv36,rvv37
                ) AA where (pmn20-rvv17>0 or rvv17 is null)"""
        sql = sql.format(sql, db_name=db_name, firstDay=firstDay, lastDay=lastDay)
        cursor = self.ttdb.execute_select_sql(sql)

        query_result = Cursor2Dict(cursor)
        return query_result


    #請購簽核完成未轉採購
    def getApprovedPRNot2PO(self, com_name):
        sql = """select pmk01,pmkud01,ta_pmk06 from {com_name}.pmk_file a where  a.pmk25 ='1'"""
        sql = sql.format(sql, com_name=com_name)
        cursor = self.ttdb.execute_select_sql(sql)
        query_result = Cursor2Dict(cursor)
        return query_result

    # 請購簽核完成項目未轉採購
    def getApprovedPRItemNot2PO(self, com_name):
        sql = """select distinct pmk01,pmkud01,ta_pmk06
                 from {com_name}.pmk_file a,{com_name}.pml_file b,{com_name}.ima_file i  where pmk25 = '2' and b.pml04 = i.ima01
                 and a.pmk01 = b.pml01 and (pml16='1' or pml16 is null)"""
        sql = sql.format(sql, com_name=com_name)
        cursor = self.ttdb.execute_select_sql(sql)
        query_result = Cursor2Dict(cursor)
        return query_result

    #採購發出未到貨
    def getIssuedPONotDeliver(self, com_name):
        sql = """select distinct pmm09,pmm01,pmn02,pmn04,pmn041,ima021,pmn20,pmn07,pmn33,pmm09||'  '||pmc03 vendor,s.apb06 from 
                (select * from {com_name}.pmm_file a,{com_name}.pmn_file b,{com_name}.ima_file i where b.pmn01 = a.pmm01 
                and b.pmn04 = i.ima01 and a.pmm25 = '2' and b.pmn33 < sysdate) p,
                (select * from {com_name}.rva_file ra,{com_name}.rvb_file rb 
                where ra.rva01 = rb.rvb01) r,{com_name}.pmc_file v,
                (select * from eaglesky.apa_file k,eaglesky.apb_file t where k.apa01=t.apb01 and apa35f > 0) s
                where  p.pmm01 = r.rvb04(+) and p.pmn02 = r.rvb03(+) and r.rvb04 is null 
                and v.pmc01 = p.pmm09 and p.pmm01 = s.apb06(+) and p.pmn02 = s.apb07(+) 
                order by pmm09,pmn33,pmn02"""
        sql = sql.format(sql, com_name=com_name)
        cursor = self.ttdb.execute_select_sql(sql)
        query_result = Cursor2Dict(cursor)
        return query_result


    def getPRList(self, com_name):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pmk01,to_char(pmk04,'YYYY/MM/DD') pmk04,pmk12,pmk13,pmkud01 from {db_name}.pmk_file where pmk25 in ('S','1','2')"""
        sql = sql.format(sql, db_name=db_name)
        cursor = self.ttdb.execute_select_sql(sql)
        results = json.dumps(json_format(cursor))
        return results


    def getPRListDetail(self, com_name, prno):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pml02,pml04,pml041,ima021,ta_ima01,ta_ima03,pml07,pml20 from {db_name}.pml_file a,{db_name}.ima_file b where a.pml04 = b.ima01 and pml01 = '{prno}'"""
        sql = sql.format(sql, db_name=db_name, prno=prno)
        cursor = self.ttdb.execute_select_sql(sql)
        results = json.dumps(json_format(cursor))
        return results

    def getPRnoPOListDetail(self, com_name, prno):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select pml02,pml04,pml041,ima021,ta_ima01,ta_ima03,pml07,pml20 from {db_name}.pmk_file a,{db_name}.pml_file b,{db_name}.ima_file i  
                 where pmk25 = '2' and b.pml04 = i.ima01
                 and a.pmk01 = b.pml01 and (pml16='1' or pml16 is null) and pmk01 ='{prno}'"""
        sql = sql.format(sql, db_name=db_name, prno=prno)
        cursor = self.ttdb.execute_select_sql(sql)
        results = json.dumps(json_format(cursor))
        return results

    #驗退資料
    def getQReject(self, com_name, date_from, date_to):
        db_name = getDBSchema(com_name, self.prod)
        sql = """select distinct case RVU00 when '2' then 'Q Return' when '3' then 'WH Return' end RVU00,
                 RVU01,RVU03,RVU04||' - '||RVU05 vendor,gem02||' - '||gen02 owner,rvv36,rvv37,rvv31,rvv031,ima021,rvv17,rvv35 
                 from {db_name}.rvu_file a, {db_name}.rvv_file b, {db_name}.gen_file u, {db_name}.gem_file d, {db_name}.ima_file i,
                 {db_name}.pmm_file m, {db_name}.pmn_file n, {db_name}.pmk_file k 
                 where rvu00 in (2,3) and rvuconf = 'Y' and a.rvu01 = b.rvv01 and u.gen01 = pmk12 and d.gem01 = pmk13 and ima01 = rvv31
                 and pmm01 = rvv36 and pmm01 = pmn01 and pmk01 = pmn24 
                 and rvu03 between to_date('{date_from}','yyyy/mm/dd') and to_date('{date_to}','yyyy/mm/dd')"""
        sql = sql.format(sql, db_name=db_name, date_from=date_from, date_to=date_to)
        cursor = self.ttdb.execute_select_sql(sql)
        query_result = Cursor2Dict(cursor)
        return query_result


# tt = pr_data(prod=True)
# query_result = tt.getPRnoPOListDetail("eaglesky","PR201-0012001000005")