import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pearsonLinearCorrelationCoefficient import pearson_linear_correlation_coefficient

def linear_regression(filename: str):
    df = pd.read_csv(filename, delimiter=',')
    number_of_rows = df.shape[0]
    df_hat = df.sum() / number_of_rows
    x_hat = df_hat[0]
    y_hat = df_hat[1]
    df['xi-x_hat'] = df.iloc[:, 0] - x_hat
    df['yi(xi-x_hat)'] = df['xi-x_hat'] * df.iloc[:, 1]
    df['(xi-x_hat)2'] = df['xi-x_hat'] ** 2
    df_sum = df.sum()
    a = df_sum['yi(xi-x_hat)'] / df_sum['(xi-x_hat)2']
    b = y_hat - x_hat * a
    return a, b

def draw_linear_regression(a: float, b: float, filename: str):
    df = pd.read_csv(filename, delimiter=',')
    column_names = df.columns
    df.plot(x=column_names[0], y=column_names[1], style='o', color='k')
    minX = df.iloc[:, 0].min()
    minX -= 0.1 * minX
    maxX = df.iloc[:, 0].max()
    maxX += 0.1 * maxX
    step = (maxX - minX) / 10
    regressionX = np.arange(minX, maxX, step)
    regressionY = a * regressionX + b
    plt.grid()
    plt.plot(regressionX, regressionY, 'r', linewidth=2)
    plt.xlabel(column_names[0])
    plt.ylabel(column_names[1])
    plt.legend(['y=f(x)', 'regression line'])
    fig = plt.gcf()
    fig.set_size_inches(5, 3.8)
    fig.tight_layout()
    plt.savefig('temp_regression_chart.png',  dpi=100)
    # plt.show()


print("Algorithm loaded: Linear regression")

"""
filename = '../data/pearsonLinearCorrelationCoefficient.csv'
r = pearson_linear_correlation_coefficient(filename)
print(f"Correlation coefficient: {r}")

if abs(r) < 0.5:
    print("Correlation coefficient should be less than |0.5|")
    exit(0)

a, b = linear_regression(filename)
print(f"a: {a}")
print(f"b: {b}")
draw_linear_regression(a, b, filename)
"""