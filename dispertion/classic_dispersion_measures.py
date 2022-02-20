# classic methods:
# - variance
# - standard deviation
# - mean absolute deviation

import math


class ClassicDispersionMeasures(object):

    def variance(self, population):
        squared_diff_sum = 0.0
        mean = self.mean(population)
        for current in population:
            squared_diff_sum += math.pow(current - mean, 2)
        return squared_diff_sum / len(population)

    def standard_deviation(self, population):
        return math.sqrt(self.variance(population))

    def coefficient_of_variation(self, population):
        return self.standard_deviation(population) / self.mean(population)

    def mean_absolute_deviation(self, population):
        absolute_deviations_sum = 0.0
        mean = self.mean(population)
        for current in population:
            absolute_deviations_sum += abs(current - mean)
        return absolute_deviations_sum / len(population)

    def mean(self, population):
        return sum(population) / len(population)


# tests

classic_dispersion_measures = ClassicDispersionMeasures()
print('variance \t\t\t\t\t' + str(classic_dispersion_measures.variance([40, 42, 47, 53, 54, 59, 65])))
print('standard deviation \t\t\t' + str(classic_dispersion_measures.standard_deviation([40, 42, 47, 53, 54, 59, 65])))
print('mean absolute deviation \t' + str(classic_dispersion_measures.mean_absolute_deviation([40, 42, 47, 53, 54, 59, 65])))
print('coefficient of variation \t' + str(classic_dispersion_measures.coefficient_of_variation([40, 42, 47, 53, 54, 59, 65])))
