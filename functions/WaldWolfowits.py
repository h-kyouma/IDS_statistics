# Lukasz Pierscieniewski 6/2/2022
from typing import Tuple, List
from functions.ShapiroWilk import _norm_dist_cdf

import math

def wald_wolfowits_test(sample: List[int]) -> Tuple[float, float]:
    sample_sorted = [x for x in sorted(sample)]
    if len(sample) % 2 == 1:
        median = sample_sorted[len(sample) // 2]
    else:
        median = sample_sorted[len(sample) // 2 - 1] + sample_sorted[len(sample) // 2]
        median /= 2
    NA = sum((1 for x in sample if x < median))
    NB = sum((1 for x in sample if x > median))

    k = 0
    last = None
    for x in sample:
        current = x < median
        if last is None or last != current:
            k += 1
            last = current

    N = NA + NB
    m = 2 * NA * NB / N + 1

    s = math.sqrt(2 * NA * NB * (2 * NA * NB - NA - NB) / (N * N) * (N - 1))
    z = (k - m) / s

    return z, 1 - _norm_dist_cdf(z, 0.0, 1.0)

