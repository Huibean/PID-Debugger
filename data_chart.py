from PyQt5.QtChart import QChart, QChartView, QLineSeries

from PyQt5.QtCore import QPointF

class DataChart(QChart):

    def __init__(self):
        super().__init__()
        self.legend().hide()

class DataLine(QLineSeries):

    def __init__(self):
        super().__init__()

        line_pen = self.pen() 
        line_pen.setWidth(0.5)
        self.setPen(line_pen)
        self.setUseOpenGL(True)

class SeriesData(object):

    def __init__(self):
        self.data = []

    def store(self, value):
        index = len(self.data)
        self.data.append(QPointF(index, value))
