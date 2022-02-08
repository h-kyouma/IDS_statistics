# Lukasz Pierscieniewski 6/2/2022 - Pearson Chi2 Test
from distributions.Chi2Distribution import chi2_distribution
from typing import List, Tuple

def pearson_chi2_test(theoretical_dist: List[int],
                      empirical_dist: List[int]) -> Tuple[float, float]:
    assert len(theoretical_dist) == len(empirical_dist), \
        "Lenght of class intervals for both theoretical and empirical data must be the same."

    chi2_sum = 0.0
    theoretical_population = sum(theoretical_dist)
    empirical_population = sum(empirical_dist)
    for theoretical, empirical in zip(theoretical_dist, 
                                      empirical_dist):
        probability_of_theoretical = theoretical / theoretical_population
        chi2_sum += ((empirical - empirical_population * probability_of_theoretical) 
                     / (empirical_population * probability_of_theoretical))
    p_value = chi2_distribution(chi2_sum, len(theoretical_dist) - 2)[1]

    return chi2_sum, p_value
