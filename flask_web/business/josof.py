import datetime

from bases.database import bpm_database
from chart.barchart import BarChartJS

#Sample
from data_bpm.josof_data import josof_data


class josof(object):
    bpmdb = None

    def __init__(self):
        self.bpmdb = bpm_database()

    def SOFIncomeAddEveryMonth(self):
        today = datetime.date.today()
        result = []
        for mm in range(1, 13):
            if mm <= today.month:
                result.append(list(josof_data().getSOFSumIncomebyMonth("2020"+str(mm).zfill(2)))[0])
            else:
                result.append({'TOTAL': 0.0, 'FLDCC': 0.0, 'mm': '2020'+str(mm).zfill(2)})

        print(result)

        labels = [x['mm'] for x in result]
        value_keys = ["FLDCC", "TOTAL"]

        chartjs = BarChartJS()
        ajax_data = chartjs.BarChartByDict(value_keys, labels, result)

        return ajax_data

    def SOFIncomeByMonth(self):
        sql = "SELECT sum(hdnTotalPrice1) TOTAL,sum(hdnAMT_FLDCC) FLDCC,SUBSTRING(dteNeed,0,5)+SUBSTRING(dteNeed,6,2) dteNeed FROM SO WHERE hdnTotalPrice1 IS NOT NULL AND dteNeed IS NOT NULL GROUP BY SUBSTRING(dteNeed,0,5)+SUBSTRING(dteNeed,6,2)"
        cursor = self.bpmdb.execute_select_sql(sql)

        query_result = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

        labels = [x['dteNeed'] for x in query_result]
        value_keys = ["FLDCC", "TOTAL"]

        chartjs = BarChartJS()
        ajax_data = chartjs.BarChartByDict(value_keys, labels, query_result)

        return ajax_data



# jsof = josof()
# jsof.SOFIncomeAddEveryMonth()
