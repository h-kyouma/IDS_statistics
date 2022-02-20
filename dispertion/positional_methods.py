# positional methods
# - interquartile range (IQR, midspread, H-spread)


class PositionalMethods(object):

    def iqr(self, population):
        middle_index = (len(population) - 1) // 2

        if len(population) % 2 == 0:
            q1 = self.median_from_to(population, 0, middle_index)
            q3 = self.median_from_to(population, middle_index + 1, len(population) - 1)
        else:
            q1 = self.median_from_to(population, 0, middle_index - 1)
            q3 = self.median_from_to(population, middle_index + 1, len(population) - 1)

        return q3 - q1

    def median(self, population):
        return self.median_from_to(population, 0, len(population) - 1)

    def median_from_to(self, population, index_from, index_to):
        size = index_to - index_from
        middle_index = size // 2
        if size % 2 == 0:
            return population[index_from + middle_index]
        else:
            return (population[index_from + middle_index] + population[index_from + middle_index + 1]) / 2.0


# tests

positional_methods = PositionalMethods()
print('q1 \t\t' + str(positional_methods.median_from_to([7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177], 0, 5)))
print('q2 \t\t' + str(positional_methods.median([7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177])))
print('q3 \t\t' + str(positional_methods.median_from_to([7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177], 7, 12)))
print('iqr \t' + str(positional_methods.iqr([7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177])))

positional_methods = PositionalMethods()
print('q1 \t\t' + str(positional_methods.median_from_to([1, 3, 7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177, 198], 0, 7)))
print('q2 \t\t' + str(positional_methods.median([1, 3, 7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177, 198])))
print('q3 \t\t' + str(positional_methods.median_from_to([1, 3, 7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177, 198], 8, 15)))
print('iqr \t' + str(positional_methods.iqr([1, 3, 7, 7, 31, 31, 47, 75, 87, 115, 116, 119, 119, 155, 177, 198])))
