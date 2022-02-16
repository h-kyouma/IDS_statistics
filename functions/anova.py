#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Bartłomiej Jabłoński
# Created Date: 15/02/2022
# ---------------------------------------------------------------------------
""" Module for comparison of means of populations with one-way ANOVA """
# ---------------------------------------------------------------------------

import math

from PyQt5 import QtWidgets, QtGui, QtCore  # GUI
import pandas as pd  # Parse CSV files

import statistical_hypothesis

# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

import scipy.stats as stats  # F-critical value


class SnedecorsFDistribution:

    def __init__(self, k, N):
        """
        :param int N: number of elements.
        :param int k: number of groups.
        """
        self.dfn = k - 1
        self.dfd = N - k

        self.ppf = self.__instance_ppf

    @staticmethod
    def ppf(alpha, dfn, dfd):
        """
        Percent point function.

        :param float alpha: lower probability tail.
        :param int dfn: degrees of freedom between groups.
        :param int dfd: degrees of freedom within groups.
        """
        # Am I allowed to use this function?
        return stats.f.ppf(alpha, dfn, dfd)

    def __instance_ppf(self, alpha):
        return SnedecorsFDistribution.ppf(alpha, self.dfn, self.dfd)


class Group:

    def __init__(self, elements, label=''):
        assert(elements)

        self.elements = elements
        self.label = label

        self.n, self.mean, self.std = statistical_hypothesis.sample_parameters(
            elements)

        self.sum_of_squares = sum([(element - self.mean) **
                                   2 for element in self.elements])


class Anova:

    def __init__(self, groups):
        assert(groups)

        self.k = len(groups)
        assert(self.k > 1)

        self.N = sum([group.n for group in groups])
        self.F = SnedecorsFDistribution(self.k, self.N)

        self.mean = sum([sum(group.elements) for group in groups]) / self.N

        self.sum_of_squares_between = sum(
            [group.n * (group.mean - self.mean) ** 2 for group in groups])
        self.sum_of_squares_within = sum(
            [group.sum_of_squares for group in groups])

        self.mean_sum_of_squares_between = self.sum_of_squares_between / self.F.dfn
        self.mean_sum_of_squares_within = self.sum_of_squares_within / self.F.dfd

        self.total_df = self.N - 1
        self.total_sum_of_squares = self.sum_of_squares_between + self.sum_of_squares_within

    def f_value(self):
        assert(self.mean_sum_of_squares_within)

        return self.mean_sum_of_squares_between / self.mean_sum_of_squares_within

    def f_alpha(self, alpha):
        return self.F.ppf(1 - alpha)

    def f_test(self, alpha):
        """
        Returns True if H0 is rejected.
        """
        return self.f_value() > self.f_alpha(alpha)

# ---------------------------------------------------------------------------
# Graphical User Interface
# ---------------------------------------------------------------------------


class GroupRow(QtWidgets.QWidget):

    MIN_ELEMENTS = 2

    deleteGroupRow = QtCore.pyqtSignal(object)

    def __init__(self, initial_label, initial_values=[1, 2, 3], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = QtWidgets.QLineEdit(initial_label)

        self.values = QtWidgets.QLineEdit(','.join(map(str, initial_values)))
        self.values.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp(r'^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)*$')))

        self.load = QtWidgets.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_FileIcon), '')
        self.load.setAutoDefault(False)
        self.load.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.load.setToolTip('Load single group values from CSV file')
        self.load.clicked.connect(self.__load_data)

        self.delete = QtWidgets.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_DialogCancelButton), '')
        self.delete.setAutoDefault(False)
        self.delete.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.delete.setToolTip('Delete group')
        self.delete.clicked.connect(lambda: self.deleteGroupRow.emit(self))

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label, 1)
        layout.addWidget(self.values, 3)
        layout.addWidget(self.load)
        layout.addWidget(self.delete)

        self.setLayout(layout)

    def set_deletable(self, status):
        self.delete.setEnabled(status)

    def model(self):
        group_values = list(
            map(float, filter(None, self.values.text().strip().rstrip(',').split(','))))
        group_label = self.label.text()

        if not len(group_values):
            raise ValueError(f'group "{group_label}" is empty')
        if len(group_values) < self.MIN_ELEMENTS:
            raise ValueError(
                f'number of element is smaller than {self.MIN_ELEMENTS} in group "{group_label}"')

        return Group(group_values, group_label)

    def __load_data(self):
        # Handle files that only contains numbers separated by commas in a single row
        file_name, _ = QtGui.QFileDialog.getOpenFileName(
            self, 'Load group', filter='CSV files (*.csv)')
        if not file_name:
            return

        try:
            data_frame = pd.read_csv(
                file_name, dtype=float, header=None, nrows=1, index_col=False, float_precision='high').dropna('columns')
            group_values = data_frame.values[0].tolist()
        except (FileNotFoundError, ValueError) as e:
            QtWidgets.QMessageBox.critical(
                self, 'Error', f'Failed to load {file_name}\nCause: {str(e)}')
            return

        self.values.setText(','.join(map(str, group_values)))


class GroupWidget(QtWidgets.QGroupBox):

    MIN_GROUPS = 2
    MAX_GROUPS = 10

    rowRemoved = QtCore.pyqtSignal(bool)
    calculationRequested = QtCore.pyqtSignal(object, float)

    def __init__(self, *args, **kwargs):
        super().__init__('Groups', *args, **kwargs)

        self.groups = []
        self.widgets = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('α =')
        label.setToolTip('Confidence level')

        self.alpha = QtWidgets.QDoubleSpinBox()
        self.alpha.setValue(0.05)
        self.alpha.setSingleStep(0.005)
        self.alpha.setDecimals(4)
        self.alpha.setRange(0.0001, 0.9999)

        self.calculate = QtWidgets.QPushButton('Calculate')
        self.calculate.setDefault(True)
        self.calculate.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.calculate.clicked.connect(self.__make_calculation)

        self.load = QtWidgets.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_FileIcon), '')
        self.load.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.load.setToolTip('Load all group values from CSV file')
        self.load.clicked.connect(self.__load_data)

        self.add = QtWidgets.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_DialogApplyButton), '')
        self.add.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.add.setToolTip('Add group')
        self.add.clicked.connect(lambda: self.add_group(
            GroupRow(f'Group {len(self.widgets) + 1}')))

        self.add_group(
            GroupRow('Traditional', [4, 1, 3, 1, 2, 4, 2, 3, 0, 3, 3, 4, 5, 6, 5, 2]))
        self.add_group(
            GroupRow('Modern', [6, 2, 3, 5, 3, 4, 1, 4, 2, 4, 5, 3]))
        self.add_group(GroupRow('Reactionist', [6, 5, 7, 6, 7, 9, 8, 8]))

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(self.alpha)
        h_layout.addWidget(self.calculate)
        h_layout.addWidget(self.load)
        h_layout.addWidget(self.add)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.widgets)
        layout.addLayout(h_layout)

        self.setLayout(layout)

    def add_group(self, group):
        self.groups.append(group)
        self.widgets.addWidget(group)

        group.deleteGroupRow.connect(self.remove_group)
        self.rowRemoved.connect(group.set_deletable)

        self.add.setDisabled(len(self.widgets) >= self.MAX_GROUPS)

    def remove_group(self, group):
        self.groups.remove(group)
        self.widgets.removeWidget(group)

        group.deleteLater()
        self.rowRemoved.emit(len(self.groups) > self.MIN_GROUPS)
        self.add.setDisabled(len(self.widgets) >= self.MAX_GROUPS)

    def __make_calculation(self):
        try:
            groups = [group.model() for group in self.groups]
            self.calculationRequested.emit(groups, self.alpha.value())
        except ValueError as e:
            QtWidgets.QMessageBox.critical(
                self, 'Error', f'Invalid configuration: {str(e)}')
        except OverflowError as e:
            QtWidgets.QMessageBox.critical(
                self, 'Error', f'Caclulation overflow')

    def __load_data(self):
        # Handle files that only contains numbers separated by commas in multiple rows
        file_name, _ = QtGui.QFileDialog.getOpenFileName(
            self, 'Load group', filter='CSV files (*.csv)')
        if not file_name:
            return

        try:
            data_frame = pd.read_csv(
                file_name, dtype=float, header=None, nrows=len(self.groups), index_col=False, float_precision='high').dropna('columns')

            values = [row.tolist() for row in data_frame.values]
        except (FileNotFoundError, ValueError) as e:
            QtWidgets.QMessageBox.critical(
                self, 'Error', f'Failed to load {file_name}\nCause: {str(e)}')
            return

        for group, group_values in zip(self.groups, values):
            print(len(group_values))
            group.values.setText(','.join(map(str, group_values)))


class GroupParameters(QtWidgets.QGroupBox):

    class TableView(QtWidgets.QTableWidget):

        def __init__(self, *args, **kwargs):
            QtWidgets.QTableWidget.__init__(self, 0, 4, *args, **kwargs)

            self.setHorizontalHeaderLabels(('n', 'x̄', 'σ', 'Σ(x - x̄)²'))
            self.horizontalHeaderItem(0).setToolTip('Group size')
            self.horizontalHeaderItem(1).setToolTip('Group mean')
            self.horizontalHeaderItem(2).setToolTip('Group standard deviation')
            self.horizontalHeaderItem(3).setToolTip('Group sum of squares')

            self.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)
            self.verticalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)

            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                               QtWidgets.QSizePolicy.Fixed)

        def update_rows(self, rows):
            self.setRowCount(0)
            for index, row in enumerate(rows):
                self.insertRow(index)
                self.setItem(index, 0, QtWidgets.QTableWidgetItem(f'{row.n}'))
                self.setItem(
                    index, 1, QtWidgets.QTableWidgetItem(f'{row.mean:.2f}'))
                self.setItem(
                    index, 2, QtWidgets.QTableWidgetItem(f'{row.std:.2f}'))
                self.setItem(index, 3, QtWidgets.QTableWidgetItem(
                    f'{row.sum_of_squares:.2f}'))

            self.resizeRowsToContents()

    def __init__(self, *args, **kwargs):
        super().__init__('Group Parameters', *args, **kwargs)

        self.table = self.TableView()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update(self, groups):
        self.table.update_rows(groups)


class AnovaParameters(QtWidgets.QGroupBox):

    class TableView(QtWidgets.QTableWidget):

        def __init__(self, *args, **kwargs):
            QtWidgets.QTableWidget.__init__(self, 3, 3, *args, **kwargs)

            self.setHorizontalHeaderLabels(('df', 'SS', 'MS'))
            self.horizontalHeaderItem(0).setToolTip('Degrees of freedom')
            self.horizontalHeaderItem(1).setToolTip('Sum of squares')
            self.horizontalHeaderItem(2).setToolTip('Mean square')

            self.setVerticalHeaderLabels(
                ('Between Groups', 'Within Groups', 'Total'))
            self.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)
            self.verticalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)

            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                               QtWidgets.QSizePolicy.Fixed)

        def update_rows(self, anova):
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(f'{anova.F.dfn}'))
            self.setItem(0, 1, QtWidgets.QTableWidgetItem(
                f'{anova.sum_of_squares_between:.2f}'))
            self.setItem(0, 2, QtWidgets.QTableWidgetItem(
                f'{anova.mean_sum_of_squares_between:.2f}'))

            self.setItem(1, 0, QtWidgets.QTableWidgetItem(f'{anova.F.dfd}'))
            self.setItem(1, 1, QtWidgets.QTableWidgetItem(
                f'{anova.sum_of_squares_within:.2f}'))
            self.setItem(1, 2, QtWidgets.QTableWidgetItem(
                f'{anova.mean_sum_of_squares_within:.2f}'))

            self.setItem(2, 0, QtWidgets.QTableWidgetItem(f'{anova.total_df}'))
            self.setItem(2, 1, QtWidgets.QTableWidgetItem(
                f'{anova.total_sum_of_squares:.2f}'))
            self.setItem(2, 2, QtWidgets.QTableWidgetItem('-'))

            self.resizeRowsToContents()

    def __init__(self, *args, **kwargs):
        super().__init__('Anova', *args, **kwargs)

        self.table = self.TableView()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update(self, anova):
        self.table.update_rows(anova)


class TestResult(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super().__init__('Test', *args, **kwargs)

        self.f_ratio = QtWidgets.QLabel('0')
        self.f_alpha = QtWidgets.QLabel('0')
        self.conclusion = QtWidgets.QLabel('')

        layout = QtWidgets.QVBoxLayout()

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('F-ratio ='))
        h_layout.addWidget(self.f_ratio)
        h_layout.addWidget(QtWidgets.QLabel('F<sub>α</sub> ='))
        h_layout.addWidget(self.f_alpha)

        layout.addLayout(h_layout)
        layout.addWidget(self.conclusion)

        self.setLayout(layout)

    def update(self, alpha, anova):
        f_value, f_alpha = anova.f_value(), anova.f_alpha(alpha)

        self.f_ratio.setText(f'{f_value:.4f}')
        self.f_alpha.setText(f'{f_alpha:.4f}')
        self.conclusion.setText(self.__conclustion_text(anova.f_test(alpha)))

    @staticmethod
    def __conclustion_text(result):
        condition = '>' if result else '≤'
        hypothesis = '<strong>is</strong>' if result else '<strong>cannot</strong> be'
        means = '<font color=\"Maroon\">Means are not equal</font>' if result else '<font color=\"Green\">All means are equal</font>'

        return f'F-ratio {condition} F<sub>α</sub>. H<sub>0</sub> {hypothesis} rejected. {means}.'


class AnovaResult(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super().__init__('Result', *args, **kwargs)

        self.parameters = GroupParameters()
        self.parameters.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.anova = AnovaParameters()
        self.anova.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.test = TestResult()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.parameters)
        layout.addWidget(self.anova)
        layout.addWidget(self.test)

        self.setLayout(layout)

    def calculate(self, groups, alpha):
        anova = Anova(groups)
        if anova.mean_sum_of_squares_within == 0:
            raise ValueError(
                f'mean sum of squares within is 0. There is no variability in any group')

        self.parameters.update(groups)
        self.anova.update(anova)
        self.test.update(alpha, anova)


class Controller:

    def __init__(self):
        self.app = QtWidgets.QApplication([])

        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.C))

        self.window = QtWidgets.QDialog()
        self.window.setWindowTitle('ANOVA')

        self.group_widget = GroupWidget()
        self.anova_result = AnovaResult()
        self.anova_result.setVisible(False)

        self.group_widget.rowRemoved.connect(self.__resize)
        self.group_widget.calculationRequested.connect(self.calculate)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.group_widget)
        layout.addWidget(self.anova_result)

        self.window.setLayout(layout)

    def show(self):
        self.window.show()
        self.app.exec()

    def calculate(self, groups, alpha):
        try:
            self.anova_result.calculate(groups, alpha)
            self.anova_result.setVisible(True)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(
                self.window, 'Error', f'Invalid configuration: {str(e)}')
        except OverflowError as e:
            QtWidgets.QMessageBox.critical(
                self.window, 'Error', f'Caclulation overflow')

    def __resize(self):
        self.window.resize(self.window.sizeHint())

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    # Lecture example
    anova = Anova(
        [Group([4, 1, 3, 1, 2, 4, 2, 3, 0, 3, 3, 4, 5, 6, 5, 2], 'Traditional'),
         Group([6, 2, 3, 5, 3, 4, 1, 4, 2, 4, 5, 3], 'Modern'),
         Group([6, 5, 7, 6, 7, 9, 8, 8], 'Reactionist')])
    assert(math.isclose(anova.f_value(), 19.995, abs_tol=1e-3))
    assert(anova.f_test(0.05))

    # Start GUI
    application = Controller()
    application.show()
