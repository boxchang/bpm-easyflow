from chart.barchart import BarChartJS
from chart.linechart import LineChartJS


class dataset_factory(object):
    chartType = ""

    def __init__(self, chartType):
        self.chartType = chartType

    def getDatasetFormat(self, chart):
        database_format = ""
        if self.chartType=="bar":
            database_format = BarChartJS().barchart_dataset_format(chart)
        elif self.chartType=="line":
            database_format = LineChartJS().linechart_dataset_format(chart)

        return database_format

dataset_format = ""

