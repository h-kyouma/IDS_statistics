import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from matplotlib.image import imread

from chiSquareTestOfIndependence import chi_square_independence_test, get_chi_square_distribution_value
from pearsonLinearCorrelationCoefficient import pearson_linear_correlation_coefficient
from linear_regression import draw_linear_regression, linear_regression

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadDataButton.setGeometry(QtCore.QRect(710, 10, 75, 31))
        self.loadDataButton.setObjectName("loadDataButton")
        self.loadDataTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.loadDataTextEdit.setGeometry(QtCore.QRect(270, 10, 431, 31))
        self.loadDataTextEdit.setObjectName("loadDataTextEdit")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 241, 541))
        self.treeWidget.setAnimated(False)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Data relationships")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(270, 80, 511, 431))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label_title_linear_regression = QtWidgets.QLabel(self.page)
        self.label_title_linear_regression.setGeometry(QtCore.QRect(20, 20, 311, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_title_linear_regression.setFont(font)
        self.label_title_linear_regression.setObjectName("label_title_linear_regression")
        self.chart = QtWidgets.QLabel(self.page)
        self.chart.setGeometry(QtCore.QRect(0, 60, 421, 301))
        self.chart.setText("")
        self.chart.setObjectName("chart")
        self.stackedWidget.addWidget(self.page)
        self.page_linear_regression = QtWidgets.QWidget()
        self.page_linear_regression.setObjectName("page_linear_regression")
        self.label_title_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_title_chi2.setGeometry(QtCore.QRect(20, 20, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_title_chi2.setFont(font)
        self.label_title_chi2.setObjectName("label_title_chi2")
        self.comboBox_significance_level_chi2 = QtWidgets.QComboBox(self.page_linear_regression)
        self.comboBox_significance_level_chi2.setGeometry(QtCore.QRect(130, 60, 69, 22))
        self.comboBox_significance_level_chi2.setObjectName("comboBox_significance_level_chi2")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.comboBox_significance_level_chi2.addItem("")
        self.label_equation = QtWidgets.QLabel(self.page)
        self.label_equation.setGeometry(QtCore.QRect(20, 40, 311, 16))
        self.label_equation.setObjectName("label_equation")
        self.label_param_significance_level_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_param_significance_level_chi2.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.label_param_significance_level_chi2.setObjectName("label_param_significance_level_chi2")
        self.label_param_hypothesis_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_param_hypothesis_chi2.setGeometry(QtCore.QRect(20, 100, 91, 16))
        self.label_param_hypothesis_chi2.setObjectName("label_param_hypothesis_chi2")
        self.label_hypothesis_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_hypothesis_chi2.setGeometry(QtCore.QRect(130, 100, 141, 16))
        self.label_hypothesis_chi2.setObjectName("label_hypothesis_chi2")
        self.label_param_dof_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_param_dof_chi2.setGeometry(QtCore.QRect(20, 140, 91, 16))
        self.label_param_dof_chi2.setObjectName("label_param_dof_chi2")
        self.label_dof_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_dof_chi2.setEnabled(False)
        self.label_dof_chi2.setGeometry(QtCore.QRect(130, 140, 91, 16))
        self.label_dof_chi2.setObjectName("label_dof_chi2")
        self.label_param_chi2_value_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_param_chi2_value_chi2.setGeometry(QtCore.QRect(20, 180, 91, 16))
        self.label_param_chi2_value_chi2.setObjectName("label_param_chi2_value_chi2")
        self.label_chi2_value_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_chi2_value_chi2.setEnabled(False)
        self.label_chi2_value_chi2.setGeometry(QtCore.QRect(130, 180, 91, 16))
        self.label_chi2_value_chi2.setObjectName("label_chi2_value_chi2")
        self.label_param_verdict_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_param_verdict_chi2.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_param_verdict_chi2.setObjectName("label_param_verdict_chi2")
        self.label_verdict_chi2 = QtWidgets.QLabel(self.page_linear_regression)
        self.label_verdict_chi2.setEnabled(False)
        self.label_verdict_chi2.setGeometry(QtCore.QRect(130, 220, 121, 16))
        self.label_verdict_chi2.setObjectName("label_verdict_chi2")
        self.stackedWidget.addWidget(self.page_linear_regression)
        self.page_pearson = QtWidgets.QWidget()
        self.page_pearson.setObjectName("page_pearson")
        self.label_title_pearson = QtWidgets.QLabel(self.page_pearson)
        self.label_title_pearson.setGeometry(QtCore.QRect(20, 20, 311, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_title_pearson.setFont(font)
        self.label_title_pearson.setObjectName("label_title_pearson")
        self.label_param_coefficient_value_pearson = QtWidgets.QLabel(self.page_pearson)
        self.label_param_coefficient_value_pearson.setGeometry(QtCore.QRect(20, 50, 221, 16))
        self.label_param_coefficient_value_pearson.setObjectName("label_param_coefficient_value_pearson")
        self.label_coefficient_value_person = QtWidgets.QLabel(self.page_pearson)
        self.label_coefficient_value_person.setEnabled(False)
        self.label_coefficient_value_person.setGeometry(QtCore.QRect(150, 50, 151, 16))
        self.label_coefficient_value_person.setObjectName("label_coefficient_value_person")
        self.stackedWidget.addWidget(self.page_pearson)
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(260, 522, 521, 31))
        self.button_start.setObjectName("button_start")
        self.label_data_validator = QtWidgets.QLabel(self.centralwidget)
        self.label_data_validator.setGeometry(QtCore.QRect(270, 50, 511, 16))
        self.label_data_validator.setText("")
        self.label_data_validator.setObjectName("label_data_validator")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionDelete_data = QtWidgets.QAction(MainWindow)
        self.actionDelete_data.setObjectName("actionDelete_data")
        self.actionInstruction = QtWidgets.QAction(MainWindow)
        self.actionInstruction.setObjectName("actionInstruction")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionDelete_data)
        self.menuHelp.addAction(self.actionInstruction)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.actionLoad.triggered.connect(self.loadDataFromFile)
        self.actionDelete_data.triggered.connect(self.emptyString)
        self.actionAbout.triggered.connect(self.showAboutDialog)
        self.actionInstruction.triggered.connect(self.showInstructionDialog)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.loadDataButton.clicked.connect(self.loadDataFromFile)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.button_start.clicked.connect(self.startCalculator)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadDataButton.setText(_translate("MainWindow", "Load data"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Linear Regression"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Pearson Linear Correlation Coefficient"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "Chi2 Independence Test"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.label_title_linear_regression.setText(_translate("MainWindow", "Linear Regression"))
        self.label_title_chi2.setText(_translate("MainWindow", "Chi2 Independence Test"))
        self.comboBox_significance_level_chi2.setItemText(0, _translate("MainWindow", "0.05"))
        self.comboBox_significance_level_chi2.setItemText(1, _translate("MainWindow", "0.001"))
        self.comboBox_significance_level_chi2.setItemText(2, _translate("MainWindow", "0.002"))
        self.comboBox_significance_level_chi2.setItemText(3, _translate("MainWindow", "0.005"))
        self.comboBox_significance_level_chi2.setItemText(4, _translate("MainWindow", "0.01"))
        self.comboBox_significance_level_chi2.setItemText(5, _translate("MainWindow", "0.02"))
        self.comboBox_significance_level_chi2.setItemText(6, _translate("MainWindow", "0.025"))
        self.comboBox_significance_level_chi2.setItemText(7, _translate("MainWindow", "0.1"))
        self.comboBox_significance_level_chi2.setItemText(8, _translate("MainWindow", "0.2"))
        self.comboBox_significance_level_chi2.setItemText(9, _translate("MainWindow", "0.5"))
        self.comboBox_significance_level_chi2.setItemText(10, _translate("MainWindow", "0.9"))
        self.comboBox_significance_level_chi2.setItemText(11, _translate("MainWindow", "0.95"))
        self.comboBox_significance_level_chi2.setItemText(12, _translate("MainWindow", "0.975"))
        self.comboBox_significance_level_chi2.setItemText(13, _translate("MainWindow", "0.99"))
        self.comboBox_significance_level_chi2.setItemText(14, _translate("MainWindow", "0.995"))
        self.label_param_significance_level_chi2.setText(_translate("MainWindow", "Significance level:"))
        self.label_param_hypothesis_chi2.setText(_translate("MainWindow", "Hypothesis:"))
        self.label_hypothesis_chi2.setText(_translate("MainWindow", "Data are independent."))
        self.label_param_dof_chi2.setText(_translate("MainWindow", "test value:"))
        self.label_dof_chi2.setText(_translate("MainWindow", "0.0"))
        self.label_param_chi2_value_chi2.setText(_translate("MainWindow", "Chi2 alpha value:"))
        self.label_chi2_value_chi2.setText(_translate("MainWindow", "0.0"))
        self.label_param_verdict_chi2.setText(_translate("MainWindow", "Verdict:"))
        self.label_verdict_chi2.setText(_translate("MainWindow", "Not calculated yet."))
        self.label_title_pearson.setText(_translate("MainWindow", "Pearson Linear Correlation Coefficient"))
        self.label_param_coefficient_value_pearson.setText(_translate("MainWindow", "Coefficient value:"))
        self.label_coefficient_value_person.setText(_translate("MainWindow", "0.00"))
        self.button_start.setText(_translate("MainWindow", "Start calculator"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionLoad.setText(_translate("MainWindow", "Load data"))
        self.actionLoad.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionDelete_data.setText(_translate("MainWindow", "Delete data"))
        self.actionDelete_data.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionInstruction.setText(_translate("MainWindow", "Instruction"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.label_equation.setText(_translate("MainWindow", ""))


    def emptyString(self):
        self.loadDataTextEdit.setText("")

    def showAboutDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Statistics IDS 2022\nBarbara Morawska")
        msgBox.setWindowTitle("About")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def showInstructionDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("To run the calculator, select an algorithm in the list on the left. "
                       "Then load the data (on top), and fill in the parameters (if needed). "
                       "Then press the 'Start Calculator' button. If the data you loaded "
                       "were correct, you will see the result of the algorithm on the screen. ")
        msgBox.setWindowTitle("Instruction")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def onItemClicked(self, it, col):
        self.label_data_validator.setStyleSheet("color: black;  background-color: None")
        self.label_data_validator.setText("")

        if it.text(col) == 'Linear Regression':
            self.stackedWidget.setCurrentIndex(0)
        elif it.text(col) == 'Pearson Linear Correlation Coefficient':
            self.stackedWidget.setCurrentIndex(2)
        elif it.text(col) == 'Chi2 Independence Test':
            self.stackedWidget.setCurrentIndex(1)

    def loadDataFromFile(self):
        file_filter = 'Data File (*.csv)'

        response = QFileDialog.getOpenFileName(
            self.loadDataButton,
            caption='Select a csv data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data file (*.csv)'
        )
        self.loadDataTextEdit.setText(response[0])

    def startCalculator(self):

        filename = self.loadDataTextEdit.toPlainText()
        if filename == '':
            self.label_data_validator.setText("   Loaded string is empty.")
            self.label_data_validator.setStyleSheet("color: white;  background-color: red")
            return
        else:
            self.label_data_validator.setStyleSheet("color: black;  background-color: None")
            self.label_data_validator.setText("")

        page = self.stackedWidget.currentIndex()
        if page == 0:
            try:
                a, b = linear_regression(filename)
            except Exception as e:
                self.label_data_validator.setText("   Loaded data is not valid.")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
                return

            r = pearson_linear_correlation_coefficient(filename)
            if abs(r) < 0.5:
                self.label_data_validator.setText("   Correlation coefficient is smaller than 0.5!")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
            print(f"a: {a}")
            print(f"b: {b}")
            print(f"r: {r}")
            if b < 0:
                tb = b * (-1)
                self.label_equation.setText(f"y={a:{6}.{4}}x - {tb:{6}.{4}};     r={r:{6}.{4}}")
            else:
                self.label_equation.setText(f"y={a:{6}.{4}}x + {b:{6}.{4}};     r={r:{6}.{4}}")
            self.label_equation.adjustSize()
            draw_linear_regression(a, b, filename)

            pixmap = QPixmap('temp_regression_chart.png')
            self.chart.setPixmap(pixmap)
            self.chart.resize(pixmap.width(), pixmap.height())
            self.chart.setAlignment(QtCore.Qt.AlignCenter)
            self.chart.setScaledContents(True)
            self.chart.setMinimumSize(1, 1)
            self.chart.show()

        elif page == 2:
            try:
                r = pearson_linear_correlation_coefficient(filename)
            except Exception as e:
                self.label_data_validator.setText("   Loaded data is not valid.")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
                return
            self.label_coefficient_value_person.setEnabled(True)
            print(f"Correlation coefficient: {r}")

            state = 'positive'
            if r < 0:
                state = 'negative'

            if -0.01 <= r < 0.01:
                self.label_coefficient_value_person.setText(f"{r:{6}.{4}},  (no correlation)")
            elif 0.01 <= abs(r) < 0.3:
                self.label_coefficient_value_person.setText(f"{r:{6}.{4}},  (weak {state} correlation)")
            elif 0.3 <= abs(r) < 0.5:
                self.label_coefficient_value_person.setText(f"{r:{6}.{4}},  ({state} correlation)")
            elif 0.5 <= abs(r) < 0.7:
                self.label_coefficient_value_person.setText(f"{r:{6}.{4}},  (strong {state} correlation)")
            elif 0.7 <= abs(r) <= 1:
                self.label_coefficient_value_person.setText(f"{r:{6}.{4}},  (very strong {state} correlation)")
            self.label_coefficient_value_person.adjustSize()

        elif page == 1:
            significance_level = self.comboBox_significance_level_chi2.currentText()
            try:
                test_value, dof = chi_square_independence_test(filename)
                chi2_value = get_chi_square_distribution_value(dof, significance_level)
            except Exception as e:
                self.label_data_validator.setText("   Loaded data is not valid.")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
                return

            chi2_value = get_chi_square_distribution_value(dof, significance_level)
            print(f"Test value:\t{test_value}"
                  f"\nDOF:\t\t{dof}"
                  f"\nα:\t\t\t{significance_level}"
                  f"\nchi2 value:\t{chi2_value}")

            if test_value > chi2_value:
                self.label_verdict_chi2.setText("Hypothesis rejected. There is some relationship between data.")
            else:
                self.label_verdict_chi2.setText("Hypothesis not rejected.")
            self.label_verdict_chi2.adjustSize()
            self.label_verdict_chi2.setEnabled(True)

            self.label_chi2_value_chi2.setText(f"{chi2_value:{6}.{4}}")
            self.label_chi2_value_chi2.adjustSize()
            self.label_chi2_value_chi2.setEnabled(True)

            self.label_dof_chi2.setText(f"{test_value:{6}.{4}}")
            self.label_dof_chi2.setEnabled(True)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
