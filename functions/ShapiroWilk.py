# Lukasz Pierscieniewski 6/2/2022 - ShapiroWilk normality test
# Based on https://scistatcalc.blogspot.com/2013/10/shapiro-wilk-test-testing-for-normality.html
from typing import List, Tuple

import math

def _norm_dist_cdf(x: float, mean: float, stddev:float) -> float:
        """ Fast, accurate way to calculate cdf"""
        return 0.5 * (1 + math.erf((x - mean) / (math.sqrt(2) * stddev)))


def _inverse_gaussian_cdf(p: float, mean: float, stddev: float) -> float:
    """ CDF is monotonically increasing so using binsearch to find correct value
        :param p float: Value P(X < x) for which we want to find x
        :param mean float: Mean of distribution we calculate
        :param stddev float: Stddev of distribution
        :return float: Value x such as P(X < x) = p
    """
    
    x = mean
    if _norm_dist_cdf(x, mean, stddev) < p:
        range_beg, range_end = x, x
        while _norm_dist_cdf(range_end, mean, stddev) < p:
            range_end += stddev
    else:
        range_beg, range_end = x, x
        while _norm_dist_cdf(range_beg, mean, stddev) >= p:
            range_beg -= stddev

    for _ in range(1000): # That should be way enough iters to estimate accurately
        range_mean = 0.5 * (range_beg + range_end)
        if _norm_dist_cdf(range_mean, mean, stddev) < p:
            range_beg = range_mean
        else:
            range_end = range_mean
    return range_mean


def _shapiro_wilk_test_p_value(w_statistic: float, n_samples: int) -> float:
    c3 = [0.5440e0, -0.39978e0, 0.25054e-1, -0.6714e-3]
    c4 = [0.13822e1, -0.77857e0, 0.62767e-1, -0.20322e-2]
    c5 = [-0.15861e1, -0.31082e0, -0.83751e-1, 0.38915e-2]
    c6 = [-0.4803e0, -0.82676e-1, 0.30302e-2]

    if n_samples == 3:
        return max(0.0, (math.pi / 6) * (math.asin(math.sqrt(w_statistic)) - math.sqrt(0.75)))
    if n_samples <= 11:
        gma = 0.459 * n_samples + -0.2273e-1
        if math.log(1 - w_statistic) > gma:
            return 1e-19
        
        y = -math.log(gma - math.log(1 - w_statistic))
        m = sum((w * n_samples**i for i, w in enumerate(c3)))
        s = math.exp(sum((w * n_samples**i for i, w in enumerate(c4))))
        
        return 1 - _norm_dist_cdf((y - m) / s, 0, 1)
    else:
        y = math.log(1 - w_statistic)
        m = sum((w * n_samples**i for i, w in enumerate(c5)))
        s = math.exp(sum((w * n_samples**i for i, w in enumerate(c6))))

        return 1 - _norm_dist_cdf((y - m) / s, 0, 1)


def shapiro_wilk_test(samples: List[int]) -> Tuple[float, float]:
    n_samples = len(samples)

    avg_samples = sum(samples) / n_samples
    stddev = math.sqrt((1 / (n_samples-1)) * sum(((x-avg_samples)*(x-avg_samples) 
                                                  for x in samples)))

    m = [_inverse_gaussian_cdf((i - (3 / 8)) / (n_samples + 0.25), 0.0, 1.0)
         for i in range(1, n_samples+1)]
    sum_m2 = sum([x*2 for x in m])
    w = [x / math.sqrt(sum_m2) for x in m]

    if n_samples == 3:
        w = [math.sqrt(0.5), 0.0, -math.sqrt(0.5)]
    if n_samples > 3:
        u = 1 / math.sqrt(n_samples)
        y = -2.706056 * u ** 5 + 4.434687 * u ** 4 + -2.071190 * u ** 3 \
            + -0.147981 * u ** 2 + 0.221157 * u + w[n_samples-1]
        w[n_samples-1] = y
        w[0] = -y

        if n_samples == 4 or n_samples == 5:
            phi = (sum_m2 - (2 * m[-1] ** 2)) / (1 - (2 * w[-1] ** 2))

            for i in range(1, n_samples-1):
                w[i] = m[i] / math.sqrt(phi)
        else:
            z = -3.582633 * u**5 + 5.682633 * u**4 + -1.752461 * u**3 \
                + -0.293762 * u**2 + 0.042981 * u + w[n_samples-2]
            w[n_samples-2] = z
            w[1] = -z

            phi = (sum_m2 - (2*m[-1]**2) - (2*m[-2]**2)) / (1-(2*w[-1]**2)-(2*w[-2]**2))
            for i in range(2, n_samples-2):
                w[i] = m[i] / math.sqrt(phi)
    W = sum((wi * x for wi, x in zip(w, sorted(samples))))**2 / (stddev * (n_samples-1))
    return W, _shapiro_wilk_test_p_value(W, n_samples)