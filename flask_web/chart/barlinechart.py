import json

from bases.lib_common import pickColor
from chart.dataset_factory import dataset_factory


class BarlineChartJS(object):
    def barlinechart_format(self, labels, charts):
        dataset_format = ""
        for chart in charts:
            dataset_format += dataset_factory(chart.getType()).getDatasetFormat(chart)
            #dataset_format += "{\"label\": "+json.dumps(str(dataset["label"]))+", \"backgroundColor\": "+json.dumps(dataset["bgColor"])+", \"borderColor\": "+json.dumps(str(dataset["borderColor"]))+", \"borderWidth\": 1,\"data\": "+str(dataset["data"])+"},"
        dataset_format = dataset_format[:-1]
        barlineChartData = "{\"labels\": "+json.dumps(labels)+", \"datasets\": ["+dataset_format+"]}"

        return barlineChartData

    # Database data transfer to JSON, label and datasets
    def BarlineChart(self, charts, labels):
        color_index = 0
        for chart in charts:
            chart.setBackgroundColor(pickColor(color_index))
            chart.setBorderColor(pickColor(color_index))
            color_index += 1

        ajax_data = self.barlinechart_format(labels, charts)
        print(ajax_data)
        return ajax_data