from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton, QScrollArea
from PyQt5.QtGui import QIcon, QPalette, QColor, QPainter
from PyQt5.QtCore import QPointF, QTimer, Qt, QMargins

from data_chart import DataChart, DataLine, SeriesData

from PyQt5.QtChart import QChartView

class NatNetChart(QWidget):

    chart_settings = [['x', (0, 0)], ['y', (0, 1)], ['z', (1, 0)], ['r', (1, 1)]]

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.positions = []
        self.rotations = []
        self.charts = []
        self.init_charts()

        self.update_data_timer = QTimer(self)
        self.update_data_timer.timeout.connect(self.update_data)

    def update_data(self):
        positions = self.main_window.nat_net_controller.positions_buffer
        rotations = self.main_window.nat_net_controller.rotations_buffer

        if len(positions) > 0:

            for index, item in enumerate(self.charts):
                if index == 3:
                    pass
                else:
                    item['line'] = DataLine()
                    item['data'].store(positions[1][index])
                    item['line'].append(item['data'].data)
                    item['chart'].removeAllSeries()
                    item['chart'].addSeries(item['line'])
                    item['chart'].axes(Qt.Vertical)
                    item['chart'].createDefaultAxes()

    def init_charts(self):
        for setting in NatNetChart.chart_settings:
            scroll_area = QScrollArea()
            chart = DataChart()
            chart.setTitle(setting[0])
            chart.scroll(1, 1)
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)
            scroll_area.setWidget(chart_view)
            scroll_area.setAlignment(Qt.AlignRight)
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            self.layout.addWidget(scroll_area, *setting[1])
            line = DataLine()
            series_data = SeriesData()
            self.charts.append({'chart': chart, 'line': line, 'view': chart_view, 'data': series_data})
