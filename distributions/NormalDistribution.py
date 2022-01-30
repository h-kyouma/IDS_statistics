# Stanisław Zakrzewski 29/01/2022 - normal distribution

import math
from scipy.integrate import quad


def probability_for_normal_distribution(normal_distribution, z):
    return quad(normal_distribution, -math.inf, z)[0]


def z_score(x, mean, standard_deviation):
    return (x - mean) / standard_deviation


def normal_distribution_function(mean, standard_deviation):
    return lambda x: 1 / math.sqrt(2 * math.pi * standard_deviation ** 2) * math.exp(
        -0.5 * ((x - mean) / standard_deviation) ** 2)


def normal_distribution(x, mean, standard_deviation):
    """
    Calculates Percentile, Probability between two values and Probability density function

    Parameters
    -------
        x: Real-number value of x is used to calculate probabilities and probability density function.
        mean: The mean is a value that represents the middle of a set of numbers.
            Usually, the mean refers to to the arithmetic mean or arithmetic average.
        standard_deviation: The standard deviation is a statistic that measures
            the data variability. It is derived from the square root of the distances
            between each value in the population and the population's mean squared.

    Returns
    -------
        P( X ≤ x )
        P( X > x )
        P(-|x| ≤ X ≤ |x| )
        Probability density( x )
    """

    nd = normal_distribution_function(mean, standard_deviation)
    zs = z_score(x, mean, standard_deviation)
    p1 = probability_for_normal_distribution(nd, zs)
    p2 = 1 - p1
    p3 = abs(abs(p1) - abs(p2))
    pd = nd(x)

    return p1, p2, p3, pd


# Example
print(normal_distribution(1, 0, 1))
