import sys
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtWidgets import (QApplication, QComboBox, QCheckBox,QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton,
                QVBoxLayout, QFileDialog, QDialogButtonBox, QMessageBox)

import time
import struct
from scipy.stats.mstats import gmean
import statistics
import os
import numpy as np
from oob_parser_mongo import uartParserSDK
from datetime import datetime
from gui_threads_txt import *
from graphUtilities_new import *
from gl_classes import GLTextItem
compileGui = 0
import queue
#only when compiling
if (compileGui):
    from fbs_runtime.application_context.PyQt5 import ApplicationContext

class Window(QDialog):
    def __init__(self, parent=None, size=[]):
        super(Window, self).__init__(parent)
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowCloseButtonHint
        )
        self.setWindowTitle("Statistical Calculator")

        
        #add connect options
        self.setConnectionLayout()
        self.setSensorPositionControls()
   
        self.setFixedWidth(400)
        self.setFixedHeight(600)
        gridlay = QGridLayout()
        gridlay.addWidget(self.comBox)
        gridlay.addWidget(self.spBox)
        self.setLayout(gridlay)
        
    
		
    def btnstate(self,b):
      if b.text() == "Sample":
         if b.isChecked() == True:
            print(b.text() + " is selected")
         else:
            print(b.text()+" is deselected")
				
      if b.text() == "Population":
         if b.isChecked() == True:
            print(b.text()+" is selected")
         else:
            print(b.text()+" is deselected")
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit?",
            QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Close)

        if reply == QMessageBox.Close:
            event.accept()
        else:
            event.ignore()
    def setConnectionLayout(self):
        self.comBox = QGroupBox('')
        self.sample = QLineEdit('')    #deb_gp

        self.input = QLabel('Input Sample:')
        self.connectButton = QPushButton('Calculate')
        self.connectButton.clicked.connect(self.calculate)
        
        self.b1 = QRadioButton("Sample")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        
		
        self.b2 = QRadioButton("Population")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))

        
        self.comLayout = QGridLayout()
        self.comLayout.addWidget(self.input,0,0)
        self.comLayout.addWidget(self.sample,0,1)
        self.comLayout.addWidget(self.b1,2,0)
        self.comLayout.addWidget(self.b2,2,1)
        self.comLayout.addWidget(self.connectButton,3,0)
        self.comBox.setLayout(self.comLayout)

   
        
    def setSensorPositionControls(self):
        self.minimum1 = QLineEdit('0')
        self.minimum1L = QLabel('Minimum')
        self.maximum1 = QLineEdit('0')
        self.maximum1L = QLabel('Maximum')
        self.range1 = QLineEdit('0')
        self.range1L = QLabel('Range')
        self.count1 = QLineEdit('0')
        self.count1L = QLabel('Count')
        self.sum1 = QLineEdit('0')
        self.sum1L = QLabel('Sum')
        self.Average1 = QLineEdit('0')
        self.Average1L = QLabel('Average')
        self.median1 = QLineEdit('0')
        self.median1L = QLabel('Median')
        self.mode1 = QLineEdit('0')
        self.mode1L = QLabel('Mode')
        self.SD1 = QLineEdit('0')
        self.SD1L = QLabel('Standard Deviation')
        self.variance1 = QLineEdit('0')
        self.variance1L = QLabel('Variance')
        self.geo_mean1 = QLineEdit('0')
        self.geo_mean1L = QLabel('Geometric Mean')
        self.har_mean1 = QLineEdit('0')
        self.har_mean1L = QLabel('Harmonic Mean')
        
        self.spLayout = QGridLayout()
        
        self.spLayout.addWidget(self.minimum1,0,1,1,1)
        self.spLayout.addWidget(self.minimum1L,0,0,1,1)
        self.spLayout.addWidget(self.maximum1,1,1,1,1)
        self.spLayout.addWidget(self.maximum1L,1,0,1,1)
        self.spLayout.addWidget(self.range1,2,1,1,1)
        self.spLayout.addWidget(self.range1L,2,0,1,1)
        self.spLayout.addWidget(self.count1,3,1,1,1)
        self.spLayout.addWidget(self.count1L,3,0,1,1)
        self.spLayout.addWidget(self.sum1,4,1,1,1)
        self.spLayout.addWidget(self.sum1L,4,0,1,1)
        self.spLayout.addWidget(self.Average1,5,1,1,1)
        self.spLayout.addWidget(self.Average1L,5,0,1,1)
        self.spLayout.addWidget(self.median1,6,1,1,1)
        self.spLayout.addWidget(self.median1L,6,0,1,1)
        self.spLayout.addWidget(self.mode1,7,1,1,1)
        self.spLayout.addWidget(self.mode1L,7,0,1,1)
        self.spLayout.addWidget(self.SD1,8,1,1,1)
        self.spLayout.addWidget(self.SD1L,8,0,1,1)
        self.spLayout.addWidget(self.variance1,9,1,1,1)
        self.spLayout.addWidget(self.variance1L,9,0,1,1)
        self.spLayout.addWidget(self.geo_mean1,10,1,1,1)
        self.spLayout.addWidget(self.geo_mean1L,10,0,1,1)
        self.spLayout.addWidget(self.har_mean1,11,1,1,1)
        self.spLayout.addWidget(self.har_mean1L,11,0,1,1)
        self.spBox = QGroupBox('Statistics')
        self.spBox.setLayout(self.spLayout)
        
        
    def calculate(self):
        #rint(int(self.sample.text()))
        x = list(map(float,self.sample.text().split(',')))
        self.minimum = min(x)
        self.maximum = max(x)
        self.range = max(x)-min(x)
        self.count = len(x)
        self.sum = sum(x)
        self.Average = statistics.mean(x)
        self.median = statistics.median(x)
        try:
            self.mode = statistics.mode(x)
        except:
                self.mode = str(x)
        self.SD = statistics.stdev(x)
        self.variance = statistics.variance(x)
        self.geo_mean = gmean(x)
        self.geo_mean = self.geo_mean.item()
        #self.geo_mean = str(self.geo_mean)
        self.har_mean = statistics.harmonic_mean(x)
        self.minimum1.setText(str(self.minimum))
        self.maximum1.setText(str(self.maximum))
        self.range1.setText(str(self.range))
        self.count1.setText(str(self.count))
        self.sum1.setText(str(self.sum))
        self.Average1.setText(str(self.Average))
        self.median1.setText(str(self.median))
        self.mode1.setText(str(self.mode))
        self.SD1.setText(str(self.SD))
        self.variance1.setText(str(self.variance))
        self.geo_mean1.setText(str(self.geo_mean))
        self.har_mean1.setText(str(self.har_mean))
        

if __name__ == '__main__':
    
    if (compileGui):
        appctxt = ApplicationContext()
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        size = screen.size()
        main = Window(size=size)
        main.show()
        exit_code = appctxt.app.exec_()
        sys.exit(exit_code)
    else:
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        size = screen.size()
        main = Window(size=size)
        main.show()
        sys.exit(app.exec_())
