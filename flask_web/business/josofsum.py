import time

from bases.database import bpm_database
from bases.lib_common import pickColor
from chart.barchart import BarChart
from chart.barlinechart import BarlineChartJS
from chart.linechart import LineChart
from data_bpm.josofsum_data import josofsum_data


class josofsummary(object):
    bpmdb = None

    def __init__(self):
        self.bpmdb = bpm_database()

    def JOSOFSummaryByYear(self, year):
        charts = []
        bpm = josofsum_data()
        labels = [str(mm).zfill(2) for mm in range(1, 13)]

        results = bpm.getJOSOFSummary(year)

        chart1 = BarChart()
        data = [result.jo_qty for result in results.values()]
        chart1.setData(data)
        chart1.setLabel("JO QTY")


        chart2 = BarChart()
        data = [result.sof_qty for result in results.values()]
        chart2.setData(data)
        chart2.setLabel("SOF QTY")

        chart3 = BarChart()
        data = [result.sofc_qty for result in results.values()]
        chart3.setData(data)
        chart3.setLabel("SOF CHANGE QTY")

        chart4 = LineChart()
        data = []
        for result in results.values():
            if result.jo_done > 0:
                value = (result.jo_done/(result.jo_done+result.wait_sof))*100
                data.append(round(value, 2))
            else:
                data.append(0)
        chart4.setData(data)
        chart4.setLabel("JO DONE RATE")
        chart4.setPointRadius("5")
        chart4.setPointHoverRadius("3")

        chart5 = LineChart()
        data = []
        for result in results.values():
            if result.sof_done > 0:
                data.append(round((result.sof_done / result.sof_qty) * 100, 2))
            else:
                data.append(0)
        chart5.setData(data)
        chart5.setLabel("SOF DONE RATE")
        chart5.setPointRadius("5")
        chart5.setPointHoverRadius("3")

        #Line圖先加才能秀在最上層
        charts.append(chart4)
        charts.append(chart5)
        charts.append(chart1)
        charts.append(chart2)
        charts.append(chart3)

        blc = BarlineChartJS()
        ajax_data = blc.BarlineChart(charts, labels)

        return ajax_data


# bpm = josofsummary()
# results = bpm.JOSOFSummaryByYear("2020")
