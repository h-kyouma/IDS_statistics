import pandas as pd

def chi_square_independence_test(filename: str):
    assert '.csv' in filename, "csv file should be loaded"
    df = pd.read_csv(filename, delimiter=',', index_col=0)

    (number_of_rows, number_of_cols) = df.shape
    dof = (number_of_rows - 1) * (number_of_cols - 1)  # Degrees of freedom

    df['row_total'] = df.iloc[:, 0:len(df.columns)].sum(axis=1)
    df_sum = df.sum()

    for col in range(number_of_cols):
        expected_col_name = df.columns[col] + '_expected_value'
        df[expected_col_name] = df['row_total'] * df_sum[col] / df_sum[-1]
        df[expected_col_name + '_temp'] = df[expected_col_name]
        df[expected_col_name] = df[expected_col_name] - df.iloc[:, col]
        df[expected_col_name] **= 2
        df[expected_col_name] /= df[expected_col_name + '_temp']
        df.drop([expected_col_name + '_temp'], inplace=True, axis=1)
    test_value = df.iloc[:, number_of_cols + 1:number_of_cols * 2 + 1].sum(axis=0).sum()
    return test_value, dof


possible_significance_levels = [
    '0.995',
    '0.99',
    '0.975',
    '0.95',
    '0.9',
    '0.5',
    '0.2',
    '0.1',
    '0.05',
    '0.025',
    '0.02',
    '0.01',
    '0.005',
    '0.002',
    '0.001'
]

def get_chi_square_distribution_value(dof: int, significance_level: str):
    df_chi2 = pd.read_csv('static/chi2Table.csv', index_col=0, delimiter=',')
    val =df_chi2.loc[dof, significance_level]
    return val


print("Algorithm loaded: Chi2 independence test")

"""
print("Hypothesis: Data are independent.")

significance_level = '0.05'
test_value, dof = chi_square_independence_test('data/chiSquareTestOfIndependence.csv')
chi2_value = get_chi_square_distribution_value(dof, significance_level)
print(f"Test value:\t{test_value}"
      f"\nDOF:\t\t{dof}"
      f"\nα:\t\t\t{significance_level}"
      f"\nchi2 value:\t{chi2_value}")

if test_value > chi2_value:
    print("Hypothesis rejected. There is some relationship between data.")
else:
    print("Hypothesis not rejected.")
plt.show()
"""