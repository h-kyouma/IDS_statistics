# Kacper Kubicki 23.02.2022

from math import sqrt
from typing import List, Tuple


def nonparametric_skew(data: List[float]) -> Tuple[float, str]:
    """
    Measure of the skewness of a random variable's distribution.

    Parameters
    ----------
    data

    Returns
    -------
        S: Calculated nonparametric skewness
        info: Additional information about the skewness direction
    """
    arth_mean = sum(data) / len(data)
    std_deviation = sqrt(sum([(sample - arth_mean) ** 2 for sample in data]) / len(data))
    median = sorted(data)[(len(data)-1)//2] if len(data) % 2 else ((sorted(data)[(len(data)-1)//2] + sorted(data)[((len(data)-1)//2)+1]) / 2.0)
    S = (arth_mean - median) / std_deviation

    if S > 0:
        info = "right skewed"
    elif S == 0:
        info = "symmetric"
    else:
        info = "left skewed"

    return S, info


def standardized_central_moment(data: List[float], r: int) -> Tuple[float, str]:
    """
    Parameters
    ----------
    data
    r: which central moment we want to calculate, has to be between 1 and 4

    Returns
    -------
    standardized_moment: Calculated standardized central moment.
    info: Additional information about the distribution in case of third and fourth moments.
    """
    assert (1 <= r <= 4)

    arth_mean = sum(data) / len(data)
    std_deviation = sqrt(sum([(sample - arth_mean) ** 2 for sample in data]) / len(data))
    arth_mean_of_deviations_from_mean = sum([(sample - arth_mean) ** r for sample in data]) / len(data)
    standardized_moment = arth_mean_of_deviations_from_mean / (std_deviation ** r)
    info = ""

    if r == 3:
        if standardized_moment > 0:
            info = "right skewed"
        elif standardized_moment == 0:
            info = "symmetric"
        else:
            info = "left skewed"

    if r == 4:
        if standardized_moment < 3:
            info = "platykurtic"
        elif standardized_moment == 3:
            info = "normal distribution"
        else:
            info = "leptokurtic"

    return standardized_moment, info
