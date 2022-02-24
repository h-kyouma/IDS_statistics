import os
from zipimport import zipimporter

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from matplotlib.image import imread

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from chiSquareTestOfIndependence import chi_square_independence_test, get_chi_square_distribution_value
from pearsonLinearCorrelationCoefficient import pearson_linear_correlation_coefficient
from linear_regression import draw_linear_regression, linear_regression

import sys
sys.path.append("../../")

import functions.PearsonChi2 as PearsonChi2
import functions.WaldWolfowits as WaldWolfowits
import functions.ShapiroWilk as ShapiroWilk

import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionDelete_data = QAction(MainWindow)
        self.actionDelete_data.setObjectName(u"actionDelete_data")
        self.actionInstruction = QAction(MainWindow)
        self.actionInstruction.setObjectName(u"actionInstruction")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.loadDataButton = QPushButton(self.centralwidget)
        self.loadDataButton.setObjectName(u"loadDataButton")
        self.loadDataButton.setGeometry(QRect(710, 10, 75, 31))
        self.loadDataTextEdit = QTextEdit(self.centralwidget)
        self.loadDataTextEdit.setObjectName(u"loadDataTextEdit")
        self.loadDataTextEdit.setGeometry(QRect(270, 10, 431, 31))
        self.treeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Data relationships");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(10, 10, 241, 541))
        self.treeWidget.setAnimated(False)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(270, 80, 511, 431))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label_title_linear_regression = QLabel(self.page)
        self.label_title_linear_regression.setObjectName(u"label_title_linear_regression")
        self.label_title_linear_regression.setGeometry(QRect(20, 20, 311, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_title_linear_regression.setFont(font)
        self.chart = QLabel(self.page)
        self.chart.setObjectName(u"chart")
        self.chart.setGeometry(QRect(10, 60, 421, 301))
        self.stackedWidget.addWidget(self.page)
        self.page_linear_regression = QWidget()
        self.page_linear_regression.setObjectName(u"page_linear_regression")
        self.label_title_chi2 = QLabel(self.page_linear_regression)
        self.label_title_chi2.setObjectName(u"label_title_chi2")
        self.label_title_chi2.setGeometry(QRect(20, 20, 171, 16))
        self.label_title_chi2.setFont(font)
        self.comboBox_significance_level_chi2 = QComboBox(self.page_linear_regression)
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
        self.comboBox_significance_level_chi2.setObjectName(u"comboBox_significance_level_chi2")
        self.comboBox_significance_level_chi2.setGeometry(QRect(130, 60, 69, 22))
        self.label_param_significance_level_chi2 = QLabel(self.page_linear_regression)
        self.label_param_significance_level_chi2.setObjectName(u"label_param_significance_level_chi2")
        self.label_param_significance_level_chi2.setGeometry(QRect(20, 60, 101, 16))
        self.label_param_hypothesis_chi2 = QLabel(self.page_linear_regression)
        self.label_param_hypothesis_chi2.setObjectName(u"label_param_hypothesis_chi2")
        self.label_param_hypothesis_chi2.setGeometry(QRect(20, 100, 91, 16))
        self.label_hypothesis_chi2 = QLabel(self.page_linear_regression)
        self.label_hypothesis_chi2.setObjectName(u"label_hypothesis_chi2")
        self.label_hypothesis_chi2.setGeometry(QRect(130, 100, 141, 16))
        self.label_param_dof_chi2 = QLabel(self.page_linear_regression)
        self.label_param_dof_chi2.setObjectName(u"label_param_dof_chi2")
        self.label_param_dof_chi2.setGeometry(QRect(20, 140, 91, 16))
        self.label_dof_chi2 = QLabel(self.page_linear_regression)
        self.label_dof_chi2.setObjectName(u"label_dof_chi2")
        self.label_dof_chi2.setEnabled(False)
        self.label_dof_chi2.setGeometry(QRect(130, 140, 91, 16))
        self.label_param_chi2_value_chi2 = QLabel(self.page_linear_regression)
        self.label_param_chi2_value_chi2.setObjectName(u"label_param_chi2_value_chi2")
        self.label_param_chi2_value_chi2.setGeometry(QRect(20, 180, 91, 16))
        self.label_chi2_value_chi2 = QLabel(self.page_linear_regression)
        self.label_chi2_value_chi2.setObjectName(u"label_chi2_value_chi2")
        self.label_chi2_value_chi2.setEnabled(False)
        self.label_chi2_value_chi2.setGeometry(QRect(130, 180, 91, 16))
        self.label_param_verdict_chi2 = QLabel(self.page_linear_regression)
        self.label_param_verdict_chi2.setObjectName(u"label_param_verdict_chi2")
        self.label_param_verdict_chi2.setGeometry(QRect(20, 220, 91, 16))
        self.label_verdict_chi2 = QLabel(self.page_linear_regression)
        self.label_verdict_chi2.setObjectName(u"label_verdict_chi2")
        self.label_verdict_chi2.setEnabled(False)
        self.label_verdict_chi2.setGeometry(QRect(130, 220, 121, 16))
        self.stackedWidget.addWidget(self.page_linear_regression)
        self.page_linear_regression1 = QWidget()
        self.page_linear_regression1.setObjectName(u"page_linear_regression1")
        self.label_title_chi21 = QLabel(self.page_linear_regression1)
        self.label_title_chi21.setObjectName(u"label_title_chi21")
        self.label_title_chi21.setGeometry(QRect(20, 20, 171, 16))
        self.label_title_chi21.setFont(font)
        self.comboBox_significance_level_chi21 = QComboBox(self.page_linear_regression1)
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.addItem("")
        self.comboBox_significance_level_chi21.setObjectName(u"comboBox_significance_level_chi21")
        self.comboBox_significance_level_chi21.setGeometry(QRect(130, 60, 69, 22))
        self.label_param_significance_level_chi21 = QLabel(self.page_linear_regression1)
        self.label_param_significance_level_chi21.setObjectName(u"label_param_significance_level_chi21")
        self.label_param_significance_level_chi21.setGeometry(QRect(20, 60, 101, 16))
        self.label_param_hypothesis_chi21 = QLabel(self.page_linear_regression1)
        self.label_param_hypothesis_chi21.setObjectName(u"label_param_hypothesis_chi21")
        self.label_param_hypothesis_chi21.setGeometry(QRect(20, 100, 91, 16))
        self.label_hypothesis_chi21 = QLabel(self.page_linear_regression1)
        self.label_hypothesis_chi21.setObjectName(u"label_hypothesis_chi21")
        self.label_hypothesis_chi21.setGeometry(QRect(130, 100, 271, 16))
        self.label_param_chi2_value_chi21 = QLabel(self.page_linear_regression1)
        self.label_param_chi2_value_chi21.setObjectName(u"label_param_chi2_value_chi21")
        self.label_param_chi2_value_chi21.setGeometry(QRect(20, 180, 91, 16))
        self.label_chi2_value_chi21 = QLabel(self.page_linear_regression1)
        self.label_chi2_value_chi21.setObjectName(u"label_chi2_value_chi21")
        self.label_chi2_value_chi21.setEnabled(False)
        self.label_chi2_value_chi21.setGeometry(QRect(130, 180, 91, 16))
        self.label_param_verdict_chi21 = QLabel(self.page_linear_regression1)
        self.label_param_verdict_chi21.setObjectName(u"label_param_verdict_chi21")
        self.label_param_verdict_chi21.setGeometry(QRect(20, 220, 91, 16))
        self.label_verdict_chi21 = QLabel(self.page_linear_regression1)
        self.label_verdict_chi21.setObjectName(u"label_verdict_chi21")
        self.label_verdict_chi21.setEnabled(False)
        self.label_verdict_chi21.setGeometry(QRect(130, 220, 121, 16))
        self.stackedWidget.addWidget(self.page_linear_regression1)
        self.page_linear_regression2 = QWidget()
        self.page_linear_regression2.setObjectName(u"page_linear_regression2")
        self.label_title_chi22 = QLabel(self.page_linear_regression2)
        self.label_title_chi22.setObjectName(u"label_title_chi22")
        self.label_title_chi22.setGeometry(QRect(20, 20, 171, 16))
        self.label_title_chi22.setFont(font)
        self.comboBox_significance_level_chi22 = QComboBox(self.page_linear_regression2)
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.addItem("")
        self.comboBox_significance_level_chi22.setObjectName(u"comboBox_significance_level_chi22")
        self.comboBox_significance_level_chi22.setGeometry(QRect(130, 60, 69, 22))
        self.label_param_significance_level_chi22 = QLabel(self.page_linear_regression2)
        self.label_param_significance_level_chi22.setObjectName(u"label_param_significance_level_chi22")
        self.label_param_significance_level_chi22.setGeometry(QRect(20, 60, 101, 16))
        self.label_param_hypothesis_chi22 = QLabel(self.page_linear_regression2)
        self.label_param_hypothesis_chi22.setObjectName(u"label_param_hypothesis_chi22")
        self.label_param_hypothesis_chi22.setGeometry(QRect(20, 100, 91, 16))
        self.label_hypothesis_chi22 = QLabel(self.page_linear_regression2)
        self.label_hypothesis_chi22.setObjectName(u"label_hypothesis_chi22")
        self.label_hypothesis_chi22.setGeometry(QRect(130, 100, 141, 16))
        self.label_param_chi2_value_chi22 = QLabel(self.page_linear_regression2)
        self.label_param_chi2_value_chi22.setObjectName(u"label_param_chi2_value_chi22")
        self.label_param_chi2_value_chi22.setGeometry(QRect(20, 180, 91, 16))
        self.label_chi2_value_chi22 = QLabel(self.page_linear_regression2)
        self.label_chi2_value_chi22.setObjectName(u"label_chi2_value_chi22")
        self.label_chi2_value_chi22.setEnabled(False)
        self.label_chi2_value_chi22.setGeometry(QRect(130, 180, 91, 16))
        self.label_param_verdict_chi22 = QLabel(self.page_linear_regression2)
        self.label_param_verdict_chi22.setObjectName(u"label_param_verdict_chi22")
        self.label_param_verdict_chi22.setGeometry(QRect(20, 220, 91, 16))
        self.label_verdict_chi22 = QLabel(self.page_linear_regression2)
        self.label_verdict_chi22.setObjectName(u"label_verdict_chi22")
        self.label_verdict_chi22.setEnabled(False)
        self.label_verdict_chi22.setGeometry(QRect(130, 220, 121, 16))
        self.stackedWidget.addWidget(self.page_linear_regression2)
        self.page_linear_regression3 = QWidget()
        self.page_linear_regression3.setObjectName(u"page_linear_regression3")
        self.label_title_chi23 = QLabel(self.page_linear_regression3)
        self.label_title_chi23.setObjectName(u"label_title_chi23")
        self.label_title_chi23.setGeometry(QRect(20, 20, 171, 16))
        self.label_title_chi23.setFont(font)
        self.comboBox_significance_level_chi23 = QComboBox(self.page_linear_regression3)
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.addItem("")
        self.comboBox_significance_level_chi23.setObjectName(u"comboBox_significance_level_chi23")
        self.comboBox_significance_level_chi23.setGeometry(QRect(130, 60, 69, 22))
        self.label_param_significance_level_chi23 = QLabel(self.page_linear_regression3)
        self.label_param_significance_level_chi23.setObjectName(u"label_param_significance_level_chi23")
        self.label_param_significance_level_chi23.setGeometry(QRect(20, 60, 101, 16))
        self.label_param_hypothesis_chi23 = QLabel(self.page_linear_regression3)
        self.label_param_hypothesis_chi23.setObjectName(u"label_param_hypothesis_chi23")
        self.label_param_hypothesis_chi23.setGeometry(QRect(20, 100, 91, 16))
        self.label_hypothesis_chi23 = QLabel(self.page_linear_regression3)
        self.label_hypothesis_chi23.setObjectName(u"label_hypothesis_chi23")
        self.label_hypothesis_chi23.setGeometry(QRect(130, 100, 141, 16))
        self.label_param_chi2_value_chi23 = QLabel(self.page_linear_regression3)
        self.label_param_chi2_value_chi23.setObjectName(u"label_param_chi2_value_chi23")
        self.label_param_chi2_value_chi23.setGeometry(QRect(20, 180, 91, 16))
        self.label_chi2_value_chi23 = QLabel(self.page_linear_regression3)
        self.label_chi2_value_chi23.setObjectName(u"label_chi2_value_chi23")
        self.label_chi2_value_chi23.setEnabled(False)
        self.label_chi2_value_chi23.setGeometry(QRect(130, 180, 91, 16))
        self.label_param_verdict_chi23 = QLabel(self.page_linear_regression3)
        self.label_param_verdict_chi23.setObjectName(u"label_param_verdict_chi23")
        self.label_param_verdict_chi23.setGeometry(QRect(20, 220, 91, 16))
        self.label_verdict_chi23 = QLabel(self.page_linear_regression3)
        self.label_verdict_chi23.setObjectName(u"label_verdict_chi23")
        self.label_verdict_chi23.setEnabled(False)
        self.label_verdict_chi23.setGeometry(QRect(130, 220, 121, 16))
        self.stackedWidget.addWidget(self.page_linear_regression3)
        self.page_pearson = QWidget()
        self.page_pearson.setObjectName(u"page_pearson")
        self.label_title_pearson = QLabel(self.page_pearson)
        self.label_title_pearson.setObjectName(u"label_title_pearson")
        self.label_title_pearson.setGeometry(QRect(20, 20, 311, 16))
        self.label_title_pearson.setFont(font)
        self.label_param_coefficient_value_pearson = QLabel(self.page_pearson)
        self.label_param_coefficient_value_pearson.setObjectName(u"label_param_coefficient_value_pearson")
        self.label_param_coefficient_value_pearson.setGeometry(QRect(20, 50, 121, 16))
        self.label_coefficient_value_person = QLabel(self.page_pearson)
        self.label_coefficient_value_person.setObjectName(u"label_coefficient_value_person")
        self.label_coefficient_value_person.setEnabled(False)
        self.label_coefficient_value_person.setGeometry(QRect(150, 50, 151, 16))
        self.stackedWidget.addWidget(self.page_pearson)
        self.button_start = QPushButton(self.centralwidget)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setGeometry(QRect(260, 522, 521, 31))
        self.label_data_validator = QLabel(self.centralwidget)
        self.label_data_validator.setObjectName(u"label_data_validator")
        self.label_data_validator.setGeometry(QRect(270, 50, 511, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.label_equation = QtWidgets.QLabel(self.page)
        self.label_equation.setGeometry(QtCore.QRect(20, 40, 311, 16))
        self.label_equation.setObjectName("label_equation")

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionDelete_data)
        self.menuHelp.addAction(self.actionInstruction)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load data", None))
#if QT_CONFIG(shortcut)
        self.actionLoad.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete_data.setText(QCoreApplication.translate("MainWindow", u"Delete data", None))
#if QT_CONFIG(shortcut)
        self.actionDelete_data.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionInstruction.setText(QCoreApplication.translate("MainWindow", u"Instruction", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.loadDataButton.setText(QCoreApplication.translate("MainWindow", u"Load data", None))

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Linear Regression", None));
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Pearson Linear Correlation Coefficient", None));
        ___qtreewidgetitem2 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Chi2 Independence Test", None));
        ___qtreewidgetitem3 = self.treeWidget.topLevelItem(3)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Pearson Chi2 Test", None));
        ___qtreewidgetitem4 = self.treeWidget.topLevelItem(4)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"Wald-Wolfowitz Test", None));
        ___qtreewidgetitem5 = self.treeWidget.topLevelItem(5)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"Shapiro-Wilk Test", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.label_title_linear_regression.setText(QCoreApplication.translate("MainWindow", u"Linear Regression", None))
        self.chart.setText("")
        self.label_title_chi2.setText(QCoreApplication.translate("MainWindow", u"Chi2 Independence Test", None))
        self.comboBox_significance_level_chi2.setItemText(0, QCoreApplication.translate("MainWindow", u"0.05", None))
        self.comboBox_significance_level_chi2.setItemText(1, QCoreApplication.translate("MainWindow", u"0.001", None))
        self.comboBox_significance_level_chi2.setItemText(2, QCoreApplication.translate("MainWindow", u"0.002", None))
        self.comboBox_significance_level_chi2.setItemText(3, QCoreApplication.translate("MainWindow", u"0.005", None))
        self.comboBox_significance_level_chi2.setItemText(4, QCoreApplication.translate("MainWindow", u"0.01", None))
        self.comboBox_significance_level_chi2.setItemText(5, QCoreApplication.translate("MainWindow", u"0.02", None))
        self.comboBox_significance_level_chi2.setItemText(6, QCoreApplication.translate("MainWindow", u"0.025", None))
        self.comboBox_significance_level_chi2.setItemText(7, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.comboBox_significance_level_chi2.setItemText(8, QCoreApplication.translate("MainWindow", u"0.2", None))
        self.comboBox_significance_level_chi2.setItemText(9, QCoreApplication.translate("MainWindow", u"0.5", None))
        self.comboBox_significance_level_chi2.setItemText(10, QCoreApplication.translate("MainWindow", u"0.9", None))
        self.comboBox_significance_level_chi2.setItemText(11, QCoreApplication.translate("MainWindow", u"0.95", None))
        self.comboBox_significance_level_chi2.setItemText(12, QCoreApplication.translate("MainWindow", u"0.975", None))
        self.comboBox_significance_level_chi2.setItemText(13, QCoreApplication.translate("MainWindow", u"0.99", None))
        self.comboBox_significance_level_chi2.setItemText(14, QCoreApplication.translate("MainWindow", u"0.995", None))

        self.label_param_significance_level_chi2.setText(QCoreApplication.translate("MainWindow", u"Significance level:", None))
        self.label_param_hypothesis_chi2.setText(QCoreApplication.translate("MainWindow", u"Hypothesis:", None))
        self.label_hypothesis_chi2.setText(QCoreApplication.translate("MainWindow", u"Data are independent.", None))
        self.label_param_dof_chi2.setText(QCoreApplication.translate("MainWindow", u"DOF:", None))
        self.label_dof_chi2.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_param_chi2_value_chi2.setText(QCoreApplication.translate("MainWindow", u"Chi2 value:", None))
        self.label_chi2_value_chi2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_param_verdict_chi2.setText(QCoreApplication.translate("MainWindow", u"Verdict:", None))
        self.label_verdict_chi2.setText(QCoreApplication.translate("MainWindow", u"Not calculated yet.", None))
        self.label_title_chi21.setText(QCoreApplication.translate("MainWindow", u"Pearson Chi2 Test", None))
        self.comboBox_significance_level_chi21.setItemText(0, QCoreApplication.translate("MainWindow", u"0.05", None))
        self.comboBox_significance_level_chi21.setItemText(1, QCoreApplication.translate("MainWindow", u"0.001", None))
        self.comboBox_significance_level_chi21.setItemText(2, QCoreApplication.translate("MainWindow", u"0.002", None))
        self.comboBox_significance_level_chi21.setItemText(3, QCoreApplication.translate("MainWindow", u"0.005", None))
        self.comboBox_significance_level_chi21.setItemText(4, QCoreApplication.translate("MainWindow", u"0.01", None))
        self.comboBox_significance_level_chi21.setItemText(5, QCoreApplication.translate("MainWindow", u"0.02", None))
        self.comboBox_significance_level_chi21.setItemText(6, QCoreApplication.translate("MainWindow", u"0.025", None))
        self.comboBox_significance_level_chi21.setItemText(7, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.comboBox_significance_level_chi21.setItemText(8, QCoreApplication.translate("MainWindow", u"0.2", None))
        self.comboBox_significance_level_chi21.setItemText(9, QCoreApplication.translate("MainWindow", u"0.5", None))
        self.comboBox_significance_level_chi21.setItemText(10, QCoreApplication.translate("MainWindow", u"0.9", None))
        self.comboBox_significance_level_chi21.setItemText(11, QCoreApplication.translate("MainWindow", u"0.95", None))
        self.comboBox_significance_level_chi21.setItemText(12, QCoreApplication.translate("MainWindow", u"0.975", None))
        self.comboBox_significance_level_chi21.setItemText(13, QCoreApplication.translate("MainWindow", u"0.99", None))
        self.comboBox_significance_level_chi21.setItemText(14, QCoreApplication.translate("MainWindow", u"0.995", None))

        self.label_param_significance_level_chi21.setText(QCoreApplication.translate("MainWindow", u"Significance level:", None))
        self.label_param_hypothesis_chi21.setText(QCoreApplication.translate("MainWindow", u"Hypothesis:", None))
        self.label_hypothesis_chi21.setText(QCoreApplication.translate("MainWindow", u"Data are from different distributions", None))
        self.label_param_chi2_value_chi21.setText(QCoreApplication.translate("MainWindow", u"Chi2 value:", None))
        self.label_chi2_value_chi21.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_param_verdict_chi21.setText(QCoreApplication.translate("MainWindow", u"Verdict:", None))
        self.label_verdict_chi21.setText(QCoreApplication.translate("MainWindow", u"Not calculated yet.", None))
        self.label_title_chi22.setText(QCoreApplication.translate("MainWindow", u"Shapiro-Wilk normal test", None))
        self.comboBox_significance_level_chi22.setItemText(0, QCoreApplication.translate("MainWindow", u"0.05", None))
        self.comboBox_significance_level_chi22.setItemText(1, QCoreApplication.translate("MainWindow", u"0.001", None))
        self.comboBox_significance_level_chi22.setItemText(2, QCoreApplication.translate("MainWindow", u"0.002", None))
        self.comboBox_significance_level_chi22.setItemText(3, QCoreApplication.translate("MainWindow", u"0.005", None))
        self.comboBox_significance_level_chi22.setItemText(4, QCoreApplication.translate("MainWindow", u"0.01", None))
        self.comboBox_significance_level_chi22.setItemText(5, QCoreApplication.translate("MainWindow", u"0.02", None))
        self.comboBox_significance_level_chi22.setItemText(6, QCoreApplication.translate("MainWindow", u"0.025", None))
        self.comboBox_significance_level_chi22.setItemText(7, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.comboBox_significance_level_chi22.setItemText(8, QCoreApplication.translate("MainWindow", u"0.2", None))
        self.comboBox_significance_level_chi22.setItemText(9, QCoreApplication.translate("MainWindow", u"0.5", None))
        self.comboBox_significance_level_chi22.setItemText(10, QCoreApplication.translate("MainWindow", u"0.9", None))
        self.comboBox_significance_level_chi22.setItemText(11, QCoreApplication.translate("MainWindow", u"0.95", None))
        self.comboBox_significance_level_chi22.setItemText(12, QCoreApplication.translate("MainWindow", u"0.975", None))
        self.comboBox_significance_level_chi22.setItemText(13, QCoreApplication.translate("MainWindow", u"0.99", None))
        self.comboBox_significance_level_chi22.setItemText(14, QCoreApplication.translate("MainWindow", u"0.995", None))

        self.label_param_significance_level_chi22.setText(QCoreApplication.translate("MainWindow", u"Significance level:", None))
        self.label_param_hypothesis_chi22.setText(QCoreApplication.translate("MainWindow", u"Hypothesis:", None))
        self.label_hypothesis_chi22.setText(QCoreApplication.translate("MainWindow", u"Data is normally distributed", None))
        self.label_param_chi2_value_chi22.setText(QCoreApplication.translate("MainWindow", u"W value:", None))
        self.label_chi2_value_chi22.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_param_verdict_chi22.setText(QCoreApplication.translate("MainWindow", u"Verdict:", None))
        self.label_verdict_chi22.setText(QCoreApplication.translate("MainWindow", u"Not calculated yet.", None))
        self.label_title_chi23.setText(QCoreApplication.translate("MainWindow", u"Wald\u2013Wolfowitz test", None))
        self.comboBox_significance_level_chi23.setItemText(0, QCoreApplication.translate("MainWindow", u"0.05", None))
        self.comboBox_significance_level_chi23.setItemText(1, QCoreApplication.translate("MainWindow", u"0.001", None))
        self.comboBox_significance_level_chi23.setItemText(2, QCoreApplication.translate("MainWindow", u"0.002", None))
        self.comboBox_significance_level_chi23.setItemText(3, QCoreApplication.translate("MainWindow", u"0.005", None))
        self.comboBox_significance_level_chi23.setItemText(4, QCoreApplication.translate("MainWindow", u"0.01", None))
        self.comboBox_significance_level_chi23.setItemText(5, QCoreApplication.translate("MainWindow", u"0.02", None))
        self.comboBox_significance_level_chi23.setItemText(6, QCoreApplication.translate("MainWindow", u"0.025", None))
        self.comboBox_significance_level_chi23.setItemText(7, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.comboBox_significance_level_chi23.setItemText(8, QCoreApplication.translate("MainWindow", u"0.2", None))
        self.comboBox_significance_level_chi23.setItemText(9, QCoreApplication.translate("MainWindow", u"0.5", None))
        self.comboBox_significance_level_chi23.setItemText(10, QCoreApplication.translate("MainWindow", u"0.9", None))
        self.comboBox_significance_level_chi23.setItemText(11, QCoreApplication.translate("MainWindow", u"0.95", None))
        self.comboBox_significance_level_chi23.setItemText(12, QCoreApplication.translate("MainWindow", u"0.975", None))
        self.comboBox_significance_level_chi23.setItemText(13, QCoreApplication.translate("MainWindow", u"0.99", None))
        self.comboBox_significance_level_chi23.setItemText(14, QCoreApplication.translate("MainWindow", u"0.995", None))

        self.label_param_significance_level_chi23.setText(QCoreApplication.translate("MainWindow", u"Significance level:", None))
        self.label_param_hypothesis_chi23.setText(QCoreApplication.translate("MainWindow", u"Hypothesis:", None))
        self.label_hypothesis_chi23.setText(QCoreApplication.translate("MainWindow", u"Data is random", None))
        self.label_param_chi2_value_chi23.setText(QCoreApplication.translate("MainWindow", u"Z value:", None))
        self.label_chi2_value_chi23.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_param_verdict_chi23.setText(QCoreApplication.translate("MainWindow", u"Verdict:", None))
        self.label_verdict_chi23.setText(QCoreApplication.translate("MainWindow", u"Not calculated yet.", None))
        self.label_title_pearson.setText(QCoreApplication.translate("MainWindow", u"Pearson Linear Correlation Coefficient", None))
        self.label_param_coefficient_value_pearson.setText(QCoreApplication.translate("MainWindow", u"Coefficient value:", None))
        self.label_coefficient_value_person.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"Start calculator", None))
        self.label_data_validator.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.label_equation.setText(QCoreApplication.translate("MainWindow", ""))


    def emptyString(self):
        self.loadDataTextEdit.setText("")

    def showAboutDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Statistics IDS 2022\nBarbara Morawska\nExtended by Lukasz Pierscieniewski:\n- Pearson Chi2, Saphiro-Wilk and WaldWolfowits")
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
            self.stackedWidget.setCurrentIndex(5)
        elif it.text(col) == 'Chi2 Independence Test':
            self.stackedWidget.setCurrentIndex(1)
        elif it.text(col) == 'Pearson Chi2 Test':
            self.stackedWidget.setCurrentIndex(2)
        elif it.text(col) == 'Wald-Wolfowitz Test':
            self.stackedWidget.setCurrentIndex(4)
        elif it.text(col) == 'Shapiro-Wilk Test':
            self.stackedWidget.setCurrentIndex(3)

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

        elif page == 5:
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

        elif page == 2:
            significance_level = self.comboBox_significance_level_chi21.currentText()
            try:
                expected, observed = PearsonChi2.load_data_from_csv(filename)
            except Exception as e:
                self.label_data_validator.setText("   Loaded data is not valid.")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
                return

            chi2_value, pvalue = PearsonChi2.pearson_chi2_test(expected, observed)

            print(f"Test value:\t{chi2_value}\n"
                  f"p-value:\t{pvalue}")

            if pvalue > float(significance_level):
                self.label_verdict_chi21.setText("Hypothesis rejected. There is some relationship between data.")
            else:
                self.label_verdict_chi21.setText("Hypothesis not rejected.")
            self.label_chi2_value_chi21.setText(f"{chi2_value:{6}.{4}}")
            self.label_verdict_chi21.adjustSize()
            self.label_verdict_chi21.setEnabled(True)

        elif page == 4:
            significance_level = self.comboBox_significance_level_chi23.currentText()
            try:
                data = pd.read_csv(filename)["data"].tolist()
            except Exception as e:
                self.label_data_validator.setText("   Loaded data is not valid.")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
                return

            z, pvalue = WaldWolfowits.wald_wolfowits_test(data)

            print(f"Test value:\t{z}\n"
                  f"p-value:\t{pvalue}")

            if pvalue > float(significance_level):
                self.label_verdict_chi23.setText("Hypothesis rejected. There is some relationship between data.")
            else:
                self.label_verdict_chi23.setText("Hypothesis not rejected.")
            self.label_chi2_value_chi23.setText(f"{z:{6}.{4}}")
            self.label_verdict_chi23.adjustSize()
            self.label_verdict_chi23.setEnabled(True)

        elif page == 3:
            significance_level = self.comboBox_significance_level_chi22.currentText()
            try:
                data = pd.read_csv(filename)["data"].tolist()
            except Exception as e:
                self.label_data_validator.setText("   Loaded data is not valid.")
                self.label_data_validator.setStyleSheet("color: white;  background-color: red")
                return

            w, pvalue = ShapiroWilk.shapiro_wilk_test(data)

            print(f"Test value:\t{w}\n"
                  f"p-value:\t{pvalue}")

            if pvalue > float(significance_level):
                self.label_verdict_chi22.setText("Hypothesis rejected. Data is not normal.")
            else:
                self.label_verdict_chi22.setText("Hypothesis not rejected.")
            self.label_chi2_value_chi22.setText(f"{w:{6}.{4}}")
            self.label_verdict_chi22.adjustSize()
            self.label_verdict_chi22.setEnabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
