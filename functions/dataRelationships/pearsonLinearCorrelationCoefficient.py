import pandas as pd


def pearson_linear_correlation_coefficient(filename: str):
    df = pd.read_csv(filename, delimiter=',')
    number_of_rows = df.shape[0]
    df_hat = df.sum() / number_of_rows
    x_hat = df_hat[0]
    y_hat = df_hat[1]
    df['xi-x_hat'] = df.iloc[:, 0] - x_hat
    df['yi-y_hat'] = df.iloc[:, 1] - y_hat
    df['(xi-x_hat)2'] = df['xi-x_hat'] ** 2
    df['(yi-y_hat)2'] = df['yi-y_hat'] ** 2
    df['(xi-x_hat)(yi-y_hat)'] = df['xi-x_hat'] * df['yi-y_hat']
    df_sum = df.sum()
    r = df_sum['(xi-x_hat)(yi-y_hat)'] / ((df_sum['(xi-x_hat)2']) ** (1 / 2) * (df_sum['(yi-y_hat)2']) ** (1 / 2))
    return r


print("Algorithm loaded: Pearson linear correlation coefficient.")

"""
r = pearson_linear_correlation_coefficient('data/pearsonLinearCorrelationCoefficient.csv')

print(f"Correlation coefficient: {r}")

state = 'positive'
if r < 0:
    state = 'negative'

if -0.01 <= r < 0.01:
    print("No correlation")
elif 0.01 <= abs(r) < 0.3:
    print(f"Weak {state} correlation")
elif 0.3 <= abs(r) < 0.5:
    print(f"{state} correlation")
elif 0.5 <= abs(r) < 0.7:
    print(f"Strong {state} correlation")
elif 0.7 <= abs(r) <= 1:
    print(f"Very strong {state} correlation")
"""