import json

class LineChart(object):
    type = "line"
    label = ""
    fill = "true"
    borderColor = ""
    borderWidth = "3"
    backgroundColor = ""
    pointRadius = ""
    borderDash = ""
    pointHoverRadius = ""
    data = []

    def setPointRadius(self, pointRadius):
        self.pointRadius = str(pointRadius)

    def getPointRadius(self):
        return self.pointRadius

    def setBorderDash(self, borderDash):
        self.borderDash = str(borderDash)

    def getBorderDash(self):
        return self.borderDash

    def setPointHoverRadius(self, pointHoverRadius):
        self.pointHoverRadius = str(pointHoverRadius)

    def getPointHoverRadius(self):
        return self.pointHoverRadius

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setFill(self, fill):
        self.fill = fill

    def getFill(self):
        return self.fill

    def setBorderColor(self, borderColor):
        self.borderColor = borderColor

    def getBorderColor(self):
        return self.borderColor

    def setBackgroundColor(self, backgroundColor):
        self.backgroundColor = backgroundColor

    def getBackgroundColor(self):
        return self.backgroundColor

    def setBorderWidth(self, borderWidth):
        self.borderWidth = borderWidth

    def getBorderWidth(self):
        return self.borderWidth

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

class LineChartJS(object):
    def linechart_dataset_format(self, chart):
        database_format = ""
        type = chart.getType()
        label = chart.getLabel()
        fill = chart.getFill()
        borderColor = chart.getBorderColor()
        borderWidth = chart.getBorderWidth()
        backgroundColor = chart.getBackgroundColor()
        pointRadius = chart.getPointRadius()
        borderDash = chart.getBorderDash()
        pointHoverRadius = chart.getPointHoverRadius()
        data = chart.getData()

        if len(type) > 0:
            database_format += "\"type\":" + json.dumps(type) + ","

        if len(label) > 0:
            database_format += "\"label\":" + json.dumps(label) + ","

        if len(fill) > 0:
            database_format += "\"fill\":" + json.dumps(fill) + ","

        if len(borderColor) > 0:
            database_format += "\"borderColor\":" + json.dumps(borderColor) + ","

        if len(borderWidth) > 0:
            database_format += "\"borderWidth\":" + json.dumps(borderWidth) + ","

        if len(backgroundColor) > 0:
            database_format += "\"backgroundColor\":" + json.dumps(backgroundColor) + ","

        if len(pointRadius) > 0:
            database_format += "\"pointRadius\":" + json.dumps(pointRadius) + ","

        if len(borderDash) > 0:
            database_format += "\"borderDash\":" + json.dumps(borderDash) + ","

        if len(pointHoverRadius) > 0:
            database_format += "\"pointHoverRadius\":" + json.dumps(pointHoverRadius) + ","

        if len(data) > 0:
            database_format += "\"data\":" + str(data) + ","

        database_format = "{" + database_format[:-1] + "},"
        return database_format

    def linechart_format(self, labels, datasets):
        dataset_format = ""

        for dataset in datasets:
            dataset_format += self.linechart_dataset_format(dataset) + ","
        dataset_format = dataset_format[:-1]
        dataset_format = "{\"labels\": "+json.dumps(labels)+", \"datasets\": ["+dataset_format+"]}"

        return dataset_format