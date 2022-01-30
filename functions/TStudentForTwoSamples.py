# Stanisław Zakrzewski 30/01/2022 - t-test paired and unpaired tests

import math
# Only using this function for getting p_value from table
from scipy.stats import t


def paired_t_test(x_mean, standard_deviation, degrees_of_freedom):
    """
    The paired t test provides an hypothesis test of the difference
    between population means for a pair of random samples whose
    differences are approximately normally distributed.

    Parameters
    -------
        x_mean: Mean value of differences between pair.
        standard_deviation: The standard deviation is a statistic that measures the data variability.
            It is derived from the square root of the distances between each
            value in the population and the population's mean squared.
        degrees_of_freedom: The number of values in the final calculation of a statistic that are free to vary.

    Returns
    -------
        t_score: Calculated value of paired t-test
        p_value: Probability value for hypothesis.
    """
    t_score = x_mean / standard_deviation * math.sqrt(degrees_of_freedom)
    p_value = 2*(t.cdf(-abs(t_score), degrees_of_freedom))
    return t_score, p_value


def unpaired_t_test(x1_mean, x2_mean, x1_standard_deviation, x2_standard_deviation, x1_degrees_of_freedom,
                    x2_degrees_of_freedom):
    """
    An unpaired t-test (also known as an independent t-test) is a statistical procedure that
    compares the averages/means of two independent or unrelated groups
    to determine if there is a significant difference between the two.

    Parameters
    -------
        x1_mean: Mean value of samples from first element tested in unpaired t-test test.
        x2_mean: Mean value of samples from second element tested in unpaired t-test test.
        x1_standard_deviation: The standard deviation is a statistic that measures the data variability.
            It is derived from the square root of the distances between each
            value in the population and the population's mean squared.
        x2_standard_deviation: The standard deviation is a statistic that measures the data variability.
            It is derived from the square root of the distances between each
            value in the population and the population's mean squared.
        x1_degrees_of_freedom: The number of values in the final calculation of a statistic that are free to vary.
        x2_degrees_of_freedom: The number of values in the final calculation of a statistic that are free to vary.

    Returns
    -------
        t_score: Calculated value of paired t-test
        p_value: Probability value for hypothesis.
    """
    t_score = (x1_mean - x2_mean) / math.sqrt(
        x1_standard_deviation ** 2 / x1_degrees_of_freedom + x2_standard_deviation ** 2 / x2_degrees_of_freedom)
    p_value = 2 * (t.cdf(-abs(t_score), [x1_degrees_of_freedom, x2_degrees_of_freedom]))
    return t_score, p_value


# Example
print(paired_t_test(-4, 1.78, 6))
print(unpaired_t_test(77, 81, 13.14, 11.71, 6, 6))
