# Stanisław Zakrzewski 30/01/2022 - t-student distribution

import math
from scipy.integrate import quad


def probability_for_normal_distribution(t_student_distribution, x):
    return quad(t_student_distribution, -math.inf, x)[0]


def z_score(x, mean, standard_deviation):
    return (x - mean) / standard_deviation


def t_student_function(degrees_of_freedom):
    return lambda x: math.gamma((degrees_of_freedom + 1) / 2) / (
            math.gamma(degrees_of_freedom / 2) * math.sqrt(degrees_of_freedom * math.pi)) * (
                             1 + x ** 2 / degrees_of_freedom) ** (-(degrees_of_freedom + 1) / 2)


def t_student_distribution(x, degrees_of_freedom):
    """
    Calculates Percentile, Probability between two values and Probability density function

    Parameters
    -------
        x: Real-number value of x is used to calculate probabilities and probability density function.
        degrees_of_freedom: The number of values in the final calculation of a statistic that are free to vary.

    Returns
    -------
        P( X ≤ x )
        P( X > x )
        P(-|x| ≤ X ≤ |x| )
        Probability density( x )
    """

    ts = t_student_function(degrees_of_freedom)
    p1 = probability_for_normal_distribution(ts, x)
    p2 = 1 - p1
    p3 = abs(abs(p1) - abs(p2))
    pd = ts(x)

    return p1, p2, p3, pd


# Example
print(t_student_distribution(1, 2))
