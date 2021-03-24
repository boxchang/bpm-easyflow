import json

from bases.lib_common import pickColor


class TimeChartJS(object):
    def timechart_format(self, datasets):
        dataset_format = ""

        for dataset in datasets:
            dataset_format += "{\"fill\": false, \"label\": "+json.dumps(str(dataset["label"]))+", \"backgroundColor\": "+json.dumps(dataset["bgColor"])+", \"borderColor\": "+json.dumps(str(dataset["borderColor"]))+", \"borderWidth\": 3,\"data\": "+str(dataset["data"])+"},"
        dataset_format = dataset_format[:-1]
        timeChartData = "{\"datasets\": ["+dataset_format+"]}"

        return timeChartData

    def TimeChartByDict(self, value_keys, dict_data):
        color_index = 0
        datasets = []

        for key in value_keys:
            dataset = {}

            point_list = []
            for x in dict_data[key]:
                point_data = {}
                point_data["x"] = str(x['RVU03'])
                point_data["y"] = str(x['RCOUNT'])
                point_list.append(point_data)
            dataset["label"] = key.upper()
            dataset["bgColor"] = pickColor(color_index)
            dataset["borderColor"] = pickColor(color_index)
            dataset["data"] = json.dumps(point_list)
            datasets.append(dataset)
            color_index += 1

        ajax_data = self.timechart_format(datasets)
        print(ajax_data)
        return ajax_data