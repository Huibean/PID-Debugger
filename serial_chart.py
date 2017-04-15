from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton, QScrollArea
from PyQt5.QtGui import QIcon, QPalette, QColor, QPainter
from PyQt5.QtCore import QPointF, QTimer, Qt, QMargins

from data_chart import DataChart, DataLine, SeriesData

from PyQt5.QtChart import QChartView


class SerialChart(QWidget):

    chart_settings = [['x', (0, 0)], ['y', (0, 1)], ['z', (1, 0)], ['r', (1, 1)]]

    def __init__(self, log_window):
        super().__init__()
        self.log_window = log_window
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.data_index = 0
        self.positions = []
        self.rotations = []
        self.charts = []
        self.init_charts()

        self.update_data_timer = QTimer(self)
        self.update_data_timer.timeout.connect(self.update_data)

    def update_data(self):
        currentData = self.log_window.serial_data.data
        if len(currentData) >= self.data_index + 1:
            positions = currentData
            for index, item in enumerate(self.charts):
                if index == 3:
                    pass
                else:
                    item['line'] = DataLine()
                    item['data'].store(float(currentData[self.data_index][index]))
                    item['line'].append(item['data'].data)
                    item['chart'].removeAllSeries()
                    item['chart'].addSeries(item['line'])
                    item['chart'].axes(Qt.Vertical)
                    item['chart'].createDefaultAxes()
            self.data_index += 1



    def init_charts(self):
        for setting in SerialChart.chart_settings:
            scroll_area = QScrollArea()
            chart = DataChart()
            chart.setTitle(setting[0])
            #  chart.scroll(1, 1)
            chart_view = QChartView(chart)
            #  chart_view.setRenderHint(QPainter.Antialiasing)
            chart_view.setRubberBand(QChartView.HorizontalRubberBand)
            scroll_area.setWidget(chart_view)
            scroll_area.setAlignment(Qt.AlignRight)
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            self.layout.addWidget(scroll_area, *setting[1])
            line = DataLine()
            series_data = SeriesData()
            self.charts.append({'chart': chart, 'line': line, 'view': chart_view, 'data': series_data})

