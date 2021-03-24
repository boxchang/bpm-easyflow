import json

from bases.lib_common import dateRange
from bases.lib_database import getComList
from chart.timechart import TimeChartJS
from data_tt.stockin_data import stockin_data


class stockin(object):
    def StockInSummaryByMonth(object, date_start, date_end):
        tt = stockin_data(prod=True)
        value_keys = getComList()
        data = {}

        for com in value_keys:
            results = []
            month_date = dateRange(date_start, date_end)

            query_result = tt.getStockInSummaryByMonth(com, date_start, date_end)
            for dd in month_date:
                result = {}
                result["COM"] = com
                result["RVU03"] = dd
                result["RCOUNT"] = 0
                for d in query_result:
                    if dd == d["RVU03"]:
                        result = d
                results.append(result)

            data[com] = results
        tc = TimeChartJS()
        ajax_data = tc.TimeChartByDict(value_keys, data)

        return ajax_data

    def getAllStockInInfoByDay(self, stockin_date):
        tt = stockin_data(prod=True)
        query_result = []
        list = getComList()
        for com in list:
            query_result += tt.getStockInInfoByDay(com, stockin_date)

        ajax_data = json.dumps(query_result)

        return ajax_data

    def getStockInDetailByNo(self, com_name, sno):
        tt = stockin_data(prod=True)
        query_result = tt.getStockInDetailByNo(com_name, sno)
        ajax_data = json.dumps(query_result)
        print(ajax_data)
        return ajax_data

# yyyymm = "2020-9".split('-')
# firstDay,lastDay = getFirstAndLastDay(int(yyyymm[0]),int(yyyymm[1]))
# print(lastDay)
# si = stockin()
# si.StockInSummaryByMonth('2020-11-01', '2020-11-30')



