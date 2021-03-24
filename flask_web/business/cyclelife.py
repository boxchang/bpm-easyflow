from bases.database import tiptop_database
from bases.lib_database import getDBSchema
from chart.barchart import BarChartJS
from data_tt.cyclelife_data import cyclelife_data


class cyclelife(object):
    ttdb = None
    db_name = None
    com_name = None

    def __init__(self,com_name):
        print('com_name:' + str(com_name))
        self.ttdb = tiptop_database()
        self.db_name = getDBSchema(com_name)
        self.com_name = com_name

    def execute(self):
        query_result = []
        tt = cyclelife_data()

        results = tt.PR_processing(self.com_name)
        print(len(results))
        ct_data = {}
        ct_data["key"] = "PR"
        ct_data[self.com_name] = len(results)
        query_result.append(ct_data)

        results = tt.PO_processing(self.com_name)
        ct_data = {}
        ct_data["key"] = "PO"
        ct_data[self.com_name] = len(results)
        query_result.append(ct_data)

        results = tt.RR_processing(self.com_name)
        ct_data = {}
        ct_data["key"] = "RR"
        ct_data[self.com_name] = len(results)
        query_result.append(ct_data)

        results = tt.AP_processing(self.com_name)
        ct_data = {}
        ct_data["key"] = "AP"
        ct_data[self.com_name] = len(results)
        query_result.append(ct_data)

        chartjs = BarChartJS()
        ajax_data = chartjs.BarChartByDict([self.com_name], ["PR","PO","RR","AP"], query_result)
        return ajax_data

