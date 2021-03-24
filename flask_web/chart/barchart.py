import json
import random

from bases.lib_common import pickColor


class BarChart(object):
    type = "bar"
    label = ""
    bgColor = ""
    borderColor = ""
    data = []

    def getType(self):
        return self.type

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setBackgroundColor(self, bgColor):
        self.bgColor = bgColor

    def getBackgroundColor(self):
        return self.bgColor

    def setBorderColor(self, borderColor):
        self.borderColor = borderColor

    def getBorderColor(self):
        return self.borderColor

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data


class BarChartJS(object):
    def barchart_dataset_format(self, chart):
        database_format = ""
        type = chart.getType()
        label = chart.getLabel()
        bgColor = chart.getBackgroundColor()
        borderColor = chart.getBorderColor()
        data = chart.getData()

        if len(type) > 0:
            database_format += "\"type\":" + json.dumps(type) + ","

        if len(label) > 0:
            database_format += "\"label\":" + json.dumps(label) + ","

        if len(bgColor) > 0:
            database_format += "\"backgroundColor\":" + json.dumps(bgColor) + ","

        if len(borderColor) > 0:
            database_format += "\"borderColor\":" + json.dumps(borderColor) + ","

        if len(data) > 0:
            database_format += "\"data\":" + str(data)

        database_format = "{" + database_format + "},"
        return database_format

    def barchart_format(self, labels, datasets):
        dataset_format = ""

        for dataset in datasets:
            dataset_format += self.barchart_dataset_format(dataset)
        dataset_format = dataset_format[:-1]
        dataset_format = "{\"labels\": " + json.dumps(labels) + ", \"datasets\": [" + dataset_format + "]}"

        return dataset_format

    def randomcolor(self):
        colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        return "#" + color

    # Database data transfer to JSON, label and datasets
    def BarChartByDict(self, value_keys, labels, dict_data):
        color_index = 0
        datasets = []
        for key in value_keys:
            # dataset = {}
            # data = [x[key] for x in dict_data]
            # dataset["label"] = key
            # dataset["bgColor"] = pickColor(color_index)
            # dataset["borderColor"] = pickColor(color_index)
            # dataset["data"] = data
            # datasets.append(dataset)

            dataset = BarChart()
            dataset.setData([x[key] for x in dict_data])
            dataset.setLabel(key)
            dataset.setBackgroundColor(pickColor(color_index))
            dataset.setBorderColor(pickColor(color_index))
            datasets.append(dataset)
            color_index += 1

        ajax_data = self.barchart_format(labels, datasets)
        print(ajax_data)
        return ajax_data

    def BarChartByCursor(self, cursor):
        query_result = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

        for item in query_result:
            print(item)

        labels = [row["label"] for row in query_result]
        data = [row["result"] for row in query_result]

        colors = []
        index = 0
        for item in query_result:
            colors.append(self.randomcolor())
            index += 1

        labels = json.dumps(labels, ensure_ascii=False)
        data = json.dumps(data, ensure_ascii=False)
        colors = json.dumps(colors, ensure_ascii=False)

        ajax_data = "{\"datasets\": [{ \"data\": " + data + ",\"backgroundColor\": " + colors + ",\"label\": \"Dataset 1\"}],\"labels\": " + labels + "}"

        return ajax_data
