#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Bartłomiej Jabłoński
# Created Date: 27/01/2022
# ---------------------------------------------------------------------------
""" Module for statistical hypothesis testing with Z-test"""
# ---------------------------------------------------------------------------


import itertools
import math
import enum
import operator

from PyQt5 import QtWidgets, QtGui, QtCore  # GUI
import pyqtgraph as pg  # Plot distribution function
import pandas as pd  # Parse CSV files

# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

import scipy.stats as stats  # Z-critical value


class NormalDistribution:
    def __init__(self, mean, var):
        self.mean = mean
        self.var = var
        self.std = math.sqrt(var)

    @staticmethod
    def ppf(alpha):
        """
        Percent point function.
        """
        # Am I allowed to use this function?
        return stats.norm.ppf(alpha)

    @staticmethod
    def pdf(x, mean=0, std=1):
        """
        Probability density function.
        """
        variance = std ** 2
        return math.exp(-(x - mean) ** 2 / (2 * variance)) / math.sqrt(2 * math.pi * variance)

    @staticmethod
    def symbol():
        return 'z'

    @staticmethod
    def scale_symbol():
        return 'σ'


class StudentsTDistribution:
    def __init__(self, mean, var, n):
        self.mean = mean
        self.var = var
        self.std = math.sqrt(var)
        self.df = n - 1

        self.ppf = self.__instance_ppf
        self.pdf = self.__instance_pdf

    @staticmethod
    def ppf(alpha, df):
        """
        Percent point function.
        """
        # Am I allowed to use this function?
        return stats.t.ppf(alpha, df)

    @staticmethod
    def pdf(x, df):
        """
        Probability density function.
        """
        return math.gamma((df + 1) / 2) / (math.sqrt(math.pi * df) * math.gamma(df / 2) * (1 + x ** 2 / df) ** ((df + 1) / 2))

    @staticmethod
    def symbol():
        return 't'

    @staticmethod
    def scale_symbol():
        return 's'

    def __instance_ppf(self, alpha):
        return StudentsTDistribution.ppf(alpha, self.df)

    def __instance_pdf(self, x):
        return StudentsTDistribution.pdf(x, self.df)


class TailTest(enum.Enum):
    class __Test():
        def __init__(self, condition, get_alpha, name, rule):
            self.get_alpha = lambda alpha: get_alpha(alpha)
            self.condition = lambda z, z_alpha: condition(z, z_alpha)
            self.name = name
            self.rule = rule

    LEFT = __Test(operator.lt,
                  lambda alpha: alpha,
                  'left tailed',
                  lambda symbol: f'{symbol} &#60; {symbol}<sub>α</sub>')
    RIGHT = __Test(operator.gt,
                   lambda alpha: 1 - alpha,
                   'right tailed',
                   lambda symbol: f'{symbol} &#62; {symbol}<sub>α</sub>')
    TWO = __Test(lambda z, z_alpha: abs(z) > z_alpha,
                 lambda alpha: 1 - alpha / 2,
                 'two tailed',
                 lambda symbol: f'|{symbol}| &#62; {symbol}<sub>α</sub>')

    def z_alpha(self, distribution, alpha):
        """
        Z-critical value.
        """
        return distribution.ppf(self.value.get_alpha(alpha))

    def __call__(self, distribution, alpha, z):
        return self.value.condition(z, self.z_alpha(distribution, alpha))

    def name(self):
        return self.value.name

    def rule(self, symbol):
        return self.value.rule(symbol)


def z_value(N, mean, n):
    """
    Transform to standard normal distribution.
    """
    assert(N.std > 0)
    assert(n > 0)

    return (mean - N.mean) * math.sqrt(n) / N.std


def margin_of_error(z_alpha, std, n):
    assert(std >= 0)
    assert(n > 0)

    return z_alpha * std / math.sqrt(n)


def confidence_interval(test, z_alpha, mean, std, n):
    """
    Returns an interval, which with a high, a priori assumed, probability contains the value of the
    estimated parameter Q, i.e. 𝑃(𝑢 < 𝑄 < 𝑣) = 1 − α
    """
    offset = margin_of_error(z_alpha, std, n)
    result = (mean - offset, mean + offset)
    if test == TailTest.LEFT:
        return (-math.inf, result[0])
    if test == TailTest.RIGHT:
        return (result[0], math.inf)

    return result


def minimal_sample_count(z_alpha, margin, std):
    assert(std >= 0)
    assert(margin != 0)

    return (z_alpha * std / margin) ** 2


def sample_parameters(sample):
    """
    Returns number of elements, mean and standard deviation of a sample.
    """
    assert(sample)

    n = len(sample)
    mean = sum(sample) / n
    std = math.sqrt(sum([(x - mean) ** 2 for x in sample])) / n

    return n, mean, std


def check_mean_greater(alpha, N, mean, n):
    """
    H0: m <= m_0
    H1: m >  m_0,
    where m_0 = N.mean

    Returns True if H0 is rejected in favor of H1, and False if cannot reject H0.
    """
    assert(0 < alpha < 1.0)  # significance level
    assert(n > 0)  # sample size

    return TailTest.RIGHT(N, alpha, z_value(N, mean, n))


def check_mean_lesser(alpha, N, mean, n):
    """
    H0: m >= m_0
    H1: m <  m_0,
    where m_0 = N.mean

    Returns True if H0 is rejected in favor of H1, and False if cannot reject H0.
    """
    assert(0 < alpha < 1.0)  # significance level
    assert(n > 0)  # sample size

    return TailTest.LEFT(N, alpha, z_value(N, mean, n))


def check_mean_different(alpha, N, mean, n):
    """
    H0: m  = m_0
    H1: m != m_0,
    where m_0 = N.mean

    Returns True if H0 is rejected in favor of H1, and False if cannot reject H0.
    """
    assert(0 < alpha < 1.0)  # significance level
    assert(n > 0)  # sample size

    return TailTest.TWO(N, alpha, z_value(N, mean, n))

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class HypothesisModel:

    def __init__(self, test, mean):
        self.test = test
        self.mean = mean


class SampleModel:

    def __init__(self, n, mean, std):
        self.n = n
        self.mean = mean
        self.std = std


class CalculationModel:

    def __init__(self, alpha, distribution_factory, margin, include_sample_count):
        self.alpha = alpha
        self.distribution_factory = distribution_factory
        self.margin = margin
        self.include_sample_count = include_sample_count


class Calculator:

    def __init__(self, hypothesis_model, sample_model, calculation_model):
        self.hypothesis_mean = hypothesis_model.mean
        self.hypothesis_test = hypothesis_model.test

        self.is_left_test = self.hypothesis_test in (
            TailTest.LEFT, TailTest.TWO)
        self.is_right_test = self.hypothesis_test in (
            TailTest.RIGHT, TailTest.TWO)

        self.sample_mean = sample_model.mean
        self.sample_std = sample_model.std
        self.sample_n = sample_model.n

        self.confidence_level = calculation_model.alpha

        self.N = calculation_model.distribution_factory(
            self.hypothesis_mean, self.sample_std ** 2, self.sample_n)
        self.z = z_value(self.N, self.sample_mean, self.sample_n)
        self.z_alpha = self.hypothesis_test.z_alpha(
            self.N, self.confidence_level)

        self.rejected = self.hypothesis_test(
            self.N, self.confidence_level, self.z)

        self.confidence_interval = confidence_interval(
            self.hypothesis_test, self.z_alpha, self.sample_mean, self.sample_std, self.sample_n)

        self.margin_of_error = calculation_model.margin
        self.include_sample_count = calculation_model.include_sample_count
        self.minimal_sample_count = minimal_sample_count(
            self.z_alpha, self.margin_of_error, self.sample_std)

# ---------------------------------------------------------------------------
# Graphical User Interface
# ---------------------------------------------------------------------------


NUMBER_LIMIT = 9999999

pg.setConfigOptions(antialias=True)


class HypothesisWidget(QtWidgets.QWidget):

    OPERATORS = ('≤', '=', '≥')
    INVERSE_OPERATORS = ('>', '!=', '<')
    TESTS = (TailTest.RIGHT, TailTest.TWO, TailTest.LEFT)

    valueChanged = QtCore.pyqtSignal(float)
    operatorChanged = QtCore.pyqtSignal(int)

    def __init__(self, label, operators, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = QtWidgets.QDoubleSpinBox()
        self.value.setRange(-NUMBER_LIMIT, NUMBER_LIMIT)
        self.value.setValue(1000)
        self.value.valueChanged.connect(
            lambda text: self.valueChanged.emit(text))

        self.operator = QtWidgets.QComboBox()
        self.operator.addItems(operators)
        self.operator.setCurrentIndex(0)
        self.operator.setMinimumWidth(40)
        self.operator.currentIndexChanged.connect(
            lambda index: self.operatorChanged.emit(index))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel(label))
        layout.addWidget(QtWidgets.QLabel('μ'))
        layout.addWidget(self.operator)
        layout.addWidget(self.value)

        self.setLayout(layout)

    def update_value(self, mean):
        self.blockSignals(True)
        self.value.setValue(mean)
        self.blockSignals(False)

    def update_operator(self, operator_index):
        self.blockSignals(True)
        self.operator.setCurrentIndex(operator_index)
        self.blockSignals(False)

    def connect_to(self, other_hypothesis):
        self.valueChanged.connect(other_hypothesis.update_value)
        self.operatorChanged.connect(other_hypothesis.update_operator)

    def get_model(self):
        return HypothesisModel(self.TESTS[self.operator.currentIndex()], self.value.value())

    def activate_minimal_sample_count_configuration(self, activate):
        self.value.setDisabled(activate)


class SampleParameters(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.n = QtWidgets.QSpinBox()
        self.n.setRange(1, NUMBER_LIMIT)
        self.n.setValue(196)

        self.mean = QtWidgets.QDoubleSpinBox()
        self.mean.setRange(-NUMBER_LIMIT, NUMBER_LIMIT)
        self.mean.setValue(1005)

        self.std = QtWidgets.QDoubleSpinBox()
        self.std.setRange(0.01, NUMBER_LIMIT)
        self.std.setValue(20)

        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('n =')
        label.setToolTip('Sample size')
        layout.addWidget(label)
        layout.addWidget(self.n)
        label = QtWidgets.QLabel('μ<sub>0</sub> =')
        label.setToolTip('Sample mean')
        layout.addWidget(label)
        layout.addWidget(self.mean)
        self.std_label = QtWidgets.QLabel('σ =')
        layout.addWidget(self.std_label)
        layout.addWidget(self.std)

        self.setLayout(layout)

    def apply_sample(self, sample):
        n, mean, std = sample_parameters(sample)
        self.n.setValue(n)
        self.mean.setValue(mean)
        self.std.setValue(std)

    def apply_distribution(self, distribution):
        self.std_label.setText(f'{distribution.scale_symbol()} =')

    def get_model(self):
        return SampleModel(self.n.value(), self.mean.value(), self.std.value())


class SampleValues(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.values = QtWidgets.QLineEdit('1.4,2.1,3.7')
        self.values.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp(r'^(\s*-?\d+(\.\d+)?)(\s*,\s*-?\d+(\.\d+)?)*$')))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel('Values = ['))
        layout.addWidget(self.values)
        layout.addWidget(QtWidgets.QLabel(']'))

        self.setLayout(layout)

    def apply_sample(self, sample):
        self.values.setText(','.join(map(str, sample)))

    def get_model(self):
        n, mean, std = sample_parameters(self.__get_sample())
        if std == 0:
            raise ValueError('sample standard deviation is 0')

        return SampleModel(n, mean, std)

    def __get_sample(self):
        values = tuple(
            filter(None, self.values.text().strip().rstrip(',').split(',')))
        if not values:
            raise ValueError('empty sample')

        return list(map(float, values))


class SampleConfiguration(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super().__init__('Sample', *args, **kwargs)

        self.button_group = QtWidgets.QButtonGroup()

        self.parameters = self.Method(SampleParameters())
        self.parameters.methodActivated.connect(self.change_method)
        self.parameters.insert_to_group(self.button_group)
        self.parameters.select()

        self.values = self.Method(SampleValues())
        self.values.methodActivated.connect(self.change_method)
        self.values.insert_to_group(self.button_group)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.parameters)
        layout.addWidget(QtWidgets.QLabel('--OR--'))
        layout.addWidget(self.values)
        self.setLayout(layout)

    def change_method(self, method):
        self.method = method

    class Method(QtWidgets.QWidget):

        methodActivated = QtCore.pyqtSignal(object)

        def __init__(self, widget, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.widget = widget

            self.button = QtWidgets.QRadioButton()
            self.button.toggled.connect(self.enable_method)
            self.button.toggled.connect(self.activated)

            self.load = QtWidgets.QPushButton(
                self.style().standardIcon(QtGui.QStyle.SP_FileIcon), '')
            self.load.setSizePolicy(
                QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            self.load.setToolTip('Load from CSV file')
            self.load.clicked.connect(self.load_data)

            self.enable_method(False)

            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(self.button)
            layout.addWidget(self.widget)
            layout.addWidget(self.load)

            self.setLayout(layout)

        def select(self):
            self.button.setChecked(True)

        def activated(self, value):
            if value:
                self.methodActivated.emit(self.widget)

        def insert_to_group(self, group):
            group.addButton(self.button)

        def enable_method(self, value):
            self.widget.setEnabled(value)
            self.load.setEnabled(value)

        def load_data(self):
            # Handle files that only contains numbers separated by commas in a single row
            file_name, _ = QtGui.QFileDialog.getOpenFileName(
                self, 'Load sample', filter='CSV files (*.csv)')
            if not file_name:
                return

            try:
                data_frame = pd.read_csv(
                    file_name, dtype=float, header=None, nrows=1, index_col=False, float_precision='high').dropna('columns')
                sample = data_frame.values[0].tolist()

                if not len(sample):
                    raise ValueError('empty sample')
            except (FileNotFoundError, ValueError) as e:
                QtWidgets.QMessageBox.critical(
                    self, 'Error', f'Failed to load {file_name}\nCause: {str(e)}')

                return

            self.widget.apply_sample(sample)

    def apply_distribution(self, distribution):
        self.parameters.widget.apply_distribution(distribution)

    def get_model(self):
        return self.method.get_model()

    def activate_minimal_sample_count_configuration(self, activate):
        if activate:
            self.parameters.select()

        self.parameters.widget.n.setDisabled(activate)
        self.values.setDisabled(activate)


class CalculationConfiguration(QtWidgets.QGroupBox):

    distributionActivated = QtCore.pyqtSignal(object)
    minimalSampleCountEnabled = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__('Calculation', *args, **kwargs)

        self.alpha = QtWidgets.QDoubleSpinBox()
        self.alpha.setValue(0.01)
        self.alpha.setSingleStep(0.005)
        self.alpha.setDecimals(4)
        self.alpha.setRange(0.0001, 0.9999)

        label = QtWidgets.QLabel('α =')
        label.setToolTip('Confidence level')

        minimal_sample_count_group = QtWidgets.QGroupBox('Margin of error')
        minimal_sample_count_group.setToolTip(
            'Enable to calculate minimal sample count. It determines <i>n</i> that results in μ<sub>0</sub> ± <i>margin of error</i>')

        self.margin_of_error = QtWidgets.QDoubleSpinBox()
        self.margin_of_error.setValue(1)
        self.margin_of_error.setSingleStep(0.5)
        self.margin_of_error.setDecimals(4)
        self.margin_of_error.setRange(0.0001, NUMBER_LIMIT)
        self.margin_of_error.setDisabled(True)

        enable_minimal_sample_count = QtWidgets.QCheckBox()
        enable_minimal_sample_count.stateChanged.connect(
            self.margin_of_error.setEnabled)
        enable_minimal_sample_count.stateChanged.connect(
            lambda state: self.minimalSampleCountEnabled.emit(state))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(enable_minimal_sample_count)
        layout.addWidget(self.margin_of_error)
        minimal_sample_count_group.setLayout(layout)

        distribution = QtWidgets.QGroupBox('Distribution')
        self.normal = QtWidgets.QRadioButton('Normal')
        self.normal.toggled.connect(
            lambda value: self.activated(value, (NormalDistribution, lambda mean, var, _: NormalDistribution(mean, var))))
        self.normal.setChecked(True)

        self.students_t = QtWidgets.QRadioButton("Student's t")
        self.students_t.toggled.connect(
            lambda value: self.activated(value, (StudentsTDistribution, lambda mean, var, n: StudentsTDistribution(mean, var, n))))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.normal)
        layout.addWidget(self.students_t)
        distribution.setLayout(layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.alpha)
        layout.addWidget(minimal_sample_count_group)
        layout.addWidget(distribution)

        self.setLayout(layout)

    def activated(self, value, distribution):
        distribution_class, distribution_factory = distribution
        if value:
            self.distribution_factory = distribution_factory
            self.distributionActivated.emit(distribution_class)

    def get_model(self):
        return CalculationModel(self.alpha.value(),
                                self.distribution_factory,
                                self.margin_of_error.value(),
                                self.margin_of_error.isEnabled())


class DistributionPlot(pg.PlotWidget):

    def __init__(self, width=4, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert(width > 0)
        self.width = width

        self.setMinimumHeight(300)
        self.setMouseEnabled(False, False)

        self.setRange(xRange=(-self.width, self.width),
                      yRange=(0, .4), padding=0)
        self.getPlotItem().hideAxis('left')
        self.hideButtons()

        self.x_axis = self.getAxis('bottom')

    def update(self, z, distribution, z_alpha, left, right):
        self.clear()

        ticks = [(0, 0), (z_alpha, f'{z_alpha:.3f}')]

        area_range = (min(z_alpha, self.width),
                      self.width) if right else (-self.width, max(-self.width, z_alpha))
        self.__draw_critical_value(distribution, z_alpha, area_range)
        if left and right:
            ticks.append((-z_alpha, f'{-z_alpha:.3f}'))
            self.__draw_critical_value(distribution, -z_alpha,
                                       [-i for i in area_range[::-1]])

        self.addLine(x=z, pen=(50, 50, 150), markers=[
                     ('^', 0, 10)], label=f'{z:.3f}')

        self.x_axis.setTicks([ticks])

        self.plot(*self.generate_range(distribution, -
                  self.width, self.width, .05))

    def __draw_critical_value(self, distribution, z_alpha, area_range):
        self.addLine(x=z_alpha, pen=(50, 150, 50), markers=[('^', 0, 10)])

        self.addItem(pg.FillBetweenItem(self.plot(*self.generate_range(distribution, *area_range, min(abs(z_alpha), .1))),
                                        self.plot(area_range, (0, 0)),
                                        brush=(255, 0, 0, 100)))

    @staticmethod
    def generate_range(distribution, start, end, step):
        def linspace(start, end, step):
            return list(itertools.islice(itertools.count(start, step), int(abs(end - start) / step) + 1)) + [end]

        X = linspace(start, end, step)
        y = [distribution.pdf(x) for x in X]
        return X, y


class SolutionDescription(QtWidgets.QGroupBox):

    CONCLUSION_TYPE = {
        True: 'H<sub>0</sub> <strong>rejected</strong><br>Accepted H<sub>1</sub>',
        False: '<strong>Cannot reject</strong> H<sub>0</sub><br>Cannot accept H<sub>1</sub>'
    }

    def __init__(self, *args, **kwargs):
        super().__init__('Solution', *args, **kwargs)

        self.test_type = QtWidgets.QLabel('')
        self.rule_type = QtWidgets.QLabel('')
        self.z_value = QtWidgets.QLabel('')
        self.z_alpha_value = QtWidgets.QLabel('')
        self.conclusion = QtWidgets.QLabel('')
        self.interval = QtWidgets.QLabel('')
        self.minimal_sample_count = QtWidgets.QLabel('')

        layout = QtWidgets.QVBoxLayout()

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('Test:'))
        h_layout.addStretch()
        h_layout.addWidget(self.test_type)
        layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('Rule: Reject H<sub>0</sub> if'))
        h_layout.addStretch()
        h_layout.addWidget(self.rule_type)
        layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        self.condition_label_lhs = QtWidgets.QLabel('z =')
        h_layout.addWidget(self.condition_label_lhs)
        h_layout.addWidget(self.z_value)
        h_layout.addStretch()
        self.condition_label_rhs = QtWidgets.QLabel('z<sub>α</sub> =')
        h_layout.addWidget(self.condition_label_rhs)
        h_layout.addWidget(self.z_alpha_value)
        layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('Conclusion:'))
        h_layout.addStretch()
        h_layout.addWidget(self.conclusion)
        layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('Interval:'))
        h_layout.addStretch()
        h_layout.addWidget(self.interval)
        layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('Min. sample count:'))
        h_layout.addStretch()
        h_layout.addWidget(self.minimal_sample_count)
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.minimal_sample_count_widget = QtWidgets.QWidget()
        self.minimal_sample_count_widget.setLayout(h_layout)
        layout.addWidget(self.minimal_sample_count_widget)

        self.setLayout(layout)

    def update(self, symbol, test, z, z_alpha, interval, result, minimal_sample_count_result):
        self.condition_label_lhs.setText(f'{symbol} =')
        self.condition_label_rhs.setText(f'{symbol}<sub>α</sub> =')

        self.test_type.setText(test.name())
        self.rule_type.setText(test.rule(symbol))

        self.z_value.setText(f'{z:.3f}')
        self.z_alpha_value.setText(f'{z_alpha:.3f}')

        self.conclusion.setText(self.CONCLUSION_TYPE[result])

        self.interval.setText(f'({interval[0]:.4f} — {interval[1]:.4f})')

        self.minimal_sample_count.setText(
            f'{minimal_sample_count_result[1]:.3f} ≈ {math.ceil(minimal_sample_count_result[1])}')
        self.minimal_sample_count_widget.setVisible(
            minimal_sample_count_result[0])


class ResultPanel(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super().__init__('Result', *args, **kwargs)

        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(self.__build_normal_plot())
        layout.addWidget(self.__build_solution_description())

        self.setLayout(layout)

    def update(self, calculator):
        self.plot.update(calculator.z, calculator.N, calculator.z_alpha,
                         calculator.is_left_test, calculator.is_right_test)
        self.solution.update(calculator.N.symbol(), calculator.hypothesis_test, calculator.z, calculator.z_alpha,
                             calculator.confidence_interval, calculator.rejected, (calculator.include_sample_count, calculator.minimal_sample_count))

    def __build_normal_plot(self):
        self.plot = DistributionPlot()
        return self.plot

    def __build_solution_description(self):
        self.solution = SolutionDescription()
        return self.solution


class Controller:

    def __init__(self):
        self.app = QtWidgets.QApplication([])

        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.C))

        self.window = QtWidgets.QDialog()
        self.window.setWindowTitle('Statistical Hypothesis Testing')

        self.calculate_button = QtWidgets.QPushButton('Calculate')
        self.calculate_button.setDefault(True)
        self.calculate_button.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.calculate_button.clicked.connect(self.calculate)

        h1_layout = QtWidgets.QHBoxLayout()
        h1_layout.addWidget(self.__create_hypotheses())
        h1_layout.addWidget(self.__create_sample_configuration())

        h2_layout = QtWidgets.QHBoxLayout()
        h2_layout.addWidget(self.__create_calculation_configuration())
        h2_layout.addWidget(self.calculate_button)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addLayout(h1_layout)
        v_layout.addLayout(h2_layout)
        v_layout.addWidget(self.__create_result_panel())

        self.window.setLayout(v_layout)

        self.calculation_configuration.distributionActivated.connect(
            self.sample_configuration.apply_distribution)

        self.calculation_configuration.minimalSampleCountEnabled.connect(
            self.__activate_minimal_sample_count_configuration)

    def show(self):
        self.window.show()
        self.app.exec()

    def calculate(self):
        try:
            self.result_panel.update(Calculator(
                self.H0.get_model(),
                self.sample_configuration.get_model(),
                self.calculation_configuration.get_model()))

            self.result_panel.show()
        except ValueError as e:
            QtWidgets.QMessageBox.critical(
                self.window, 'Error', f'Invalid configuration: {str(e)}')

    def __create_hypotheses(self):
        self.H0 = HypothesisWidget(
            'H<sub>0</sub>:', HypothesisWidget.OPERATORS)
        self.H0.setToolTip('Null hypothesis')
        self.H1 = HypothesisWidget(
            'H<sub>1</sub>:', HypothesisWidget.INVERSE_OPERATORS)
        self.H1.setToolTip('Alternative hypothesis')

        self.H0.connect_to(self.H1)
        self.H1.connect_to(self.H0)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.H0)
        layout.addWidget(self.H1)

        hypotheses = QtWidgets.QGroupBox('Hypotheses')
        hypotheses.setLayout(layout)

        return hypotheses

    def __create_sample_configuration(self):
        self.sample_configuration = SampleConfiguration()
        return self.sample_configuration

    def __create_calculation_configuration(self):
        self.calculation_configuration = CalculationConfiguration()
        return self.calculation_configuration

    def __create_result_panel(self):
        self.result_panel = ResultPanel()
        self.result_panel.setHidden(True)
        return self.result_panel

    def __activate_minimal_sample_count_configuration(self, activate):
        self.H0.activate_minimal_sample_count_configuration(activate)
        self.H1.activate_minimal_sample_count_configuration(activate)
        self.sample_configuration.activate_minimal_sample_count_configuration(
            activate)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    # Lecture examples with dust emission

    # Z-test
    assert(check_mean_greater(
        0.01, NormalDistribution(1000, 400), 1005, 196) == True)
    assert(check_mean_different(
        0.01, NormalDistribution(1000, 400), 1005, 196) == True)
    assert(check_mean_different(
        0.0002, NormalDistribution(1000, 400), 1005, 196) == False)
    assert(check_mean_lesser(0.01, NormalDistribution(1000, 400),
           1005, 196) == False)  # Inverse of the first case

    # Confidence interval
    assert(all([math.isclose(actual, expected, abs_tol=2e-2) for actual, expected in zip(confidence_interval(
        TailTest.TWO, TailTest.TWO.z_alpha(NormalDistribution, 0.01), 1005, 20, 196), (1001.31, 1008.69))]))

    # Minimal sample count
    assert(math.isclose(minimal_sample_count(TailTest.TWO.z_alpha(
        NormalDistribution, 0.05), 0.45, 2.3), 100.4, abs_tol=2e-1))

    # Start GUI
    application = Controller()
    application.show()
