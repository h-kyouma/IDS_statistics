# Kacper Kubicki 23.02.2022

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
import pandas as pd
from scipy.stats import skewnorm
import sys

from symmetry.measures_of_symmetry import nonparametric_skew, standardized_central_moment


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Measures of symmetry")

        self.load_csv_action = QAction('Load from csv', self)
        self.load_csv_action.triggered.connect(self.open_csv)

        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction(self.load_csv_action)

        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

        self.show()

    def open_csv(self):
        filename = self.get_filename_from_dialog("CSV Files (*.csv)")
        data = pd.read_csv(filename)['data'].tolist()
        self.central_widget.set_data(data)
        self.__update_central_widget_figure(data)

    def get_filename_from_dialog(self, filter):
        options = QFileDialog().Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", filter, options=options)
        return file_name

    def __update_central_widget_figure(self, data):
        self.central_widget.update_figure(data)


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.data = None

        self.resize(500, 500)
        self.__center()

        self.figure = Figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)

        self.nonparam_button = QPushButton()
        self.nonparam_button.clicked.connect(self.__nonparam_on_click)
        self.nonparam_button.setText("Calculate nonparametric skew")
        self.nonparam_button.setEnabled(False)

        self.nonparam_result = QLabel()

        self.subsublayout1 = QVBoxLayout()
        self.subsublayout1.addWidget(self.nonparam_button, alignment=Qt.AlignHCenter)
        self.subsublayout1.addWidget(self.nonparam_result, alignment=Qt.AlignHCenter)

        self.central_moment_label = QLabel()
        self.central_moment_label.setText("Calculate standardized central moment")

        self.third_moment_button = QPushButton()
        self.third_moment_button.clicked.connect(self.__third_central_moment_on_click)
        self.third_moment_button.setText("3rd")
        self.third_moment_button.setEnabled(False)

        self.fourth_moment_button = QPushButton()
        self.fourth_moment_button.clicked.connect(self.__fourth_central_moment_on_click)
        self.fourth_moment_button.setText('4th')
        self.fourth_moment_button.setEnabled(False)

        self.subsubsublayout = QHBoxLayout()
        self.subsubsublayout.addWidget(self.central_moment_label)
        self.subsubsublayout.addWidget(self.third_moment_button)
        self.subsubsublayout.addWidget(self.fourth_moment_button)

        self.central_moment_result = QLabel()

        self.subsublayout2 = QVBoxLayout()
        self.subsublayout2.addLayout(self.subsubsublayout)
        self.subsublayout2.addWidget(self.central_moment_result, alignment=Qt.AlignHCenter)

        self.sublayout = QHBoxLayout()
        self.sublayout.addLayout(self.subsublayout1)
        self.sublayout.addLayout(self.subsublayout2)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.sublayout)
        self.layout.addWidget(self.canvas, alignment=Qt.AlignVCenter)
        self.setLayout(self.layout)

        self.show()

    def update_figure(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.hist(data, density=True, bins=20)
        self.canvas.draw()

    def set_data(self, d):
        self.nonparam_button.setEnabled(True)
        self.third_moment_button.setEnabled(True)
        self.fourth_moment_button.setEnabled(True)
        self.data = d

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __nonparam_on_click(self):
        skewness, info = nonparametric_skew(self.data)
        self.nonparam_result.setText(f"skewness: {skewness:.8f}, {info}")

    def __third_central_moment_on_click(self):
        standardized_moment, info = standardized_central_moment(self.data, 3)
        self.central_moment_result.setText(f"standardized third central moment: {standardized_moment:.8f}, {info}")

    def __fourth_central_moment_on_click(self):
        standardized_moment, info = standardized_central_moment(self.data, 4)
        self.central_moment_result.setText(f"standardized fourth central moment: {standardized_moment:.8f}, {info}, excess kurtosis: {standardized_moment-3:.8f}")


def prepare_data():
    left_skewed = skewnorm.rvs(-4, size=1000)
    df2 = pd.DataFrame.from_dict({'data': left_skewed})
    df2.to_csv('left_skewed_data.csv')

    right_skewed = skewnorm.rvs(4, size=1000)
    df3 = pd.DataFrame.from_dict({'data': right_skewed})
    df3.to_csv('right_skewed_data.csv')


if __name__ == '__main__':
    prepare_data()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    ex = App()
    sys.exit(app.exec_())
