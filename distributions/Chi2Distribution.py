# Lukasz Pierscieniewski 6/2/2022 - Chi2 distribution
from typing import Callable, Tuple

import math
from scipy.integrate import quad

def _lower_incomplete_gamma_func(s: float, x: float) -> float:
    def _func(t: float) -> float:
        return (t ** (s-1)) * math.exp(-t)
    return quad(_func, 0, x)[0]


def chi2_distribution_function(degree_of_freedom: int) -> Tuple[Callable[[float], float],
                                                                Callable[[float], float]]:
    """ Return a function that calculates probability density for `degree_of_freedom`
        at specified point
    """
    def _pdf(x: float) -> float:
        if x < 0.0:
            return 0.0
        num = (x ** (degree_of_freedom/2 - 1)) * math.exp(-x / 2)
        den = (2 ** (degree_of_freedom/2)) * math.gamma(degree_of_freedom/2)
        return num / den

    def _cdf(x: float) -> float:
        if x < 0.0:
            return 0.0
        return (_lower_incomplete_gamma_func(degree_of_freedom / 2, x / 2) 
                / math.gamma(degree_of_freedom / 2))

    return _pdf, _cdf

def chi2_distribution(x: float, degree_of_freedom: int) -> Tuple[float, float, float, float]:
    pdf, cdf = chi2_distribution_function(degree_of_freedom)
    cdf_x = cdf(x)

    return cdf_x, 1-cdf_x, cdf_x, pdf(x)