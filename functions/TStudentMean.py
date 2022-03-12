# Jacek Wolski 12/03/2022 - T-Student test for equality of mean values


import csv
import math
from scipy.stats import t

def t_student_test_mean(csv_file='data\TStudentMean.csv'):
    print("T-Student test for equality of mean values.\nData file: " + csv_file)
    rows = []
    with open(csv_file, 'r',encoding = 'utf-8-sig') as file:
        csvreader = csv.DictReader(file, delimiter =';')
        alpha_row = next(csvreader)
        alpha = float(alpha_row['Col2'])
        sample_size_row = next(csvreader)
        sample1_size = int(sample_size_row['Col1'])
        sample2_size = int(sample_size_row['Col2'])
        data_headers_row = next(csvreader)
        for row in csvreader:
            rows.append(row)
    print('Alpha: ' + str(alpha))
    print('Data headers: ' + data_headers_row['Col1'] + ' ' + data_headers_row['Col2'])
    print(rows)

    print('Sample size of: ' + data_headers_row['Col1'] + ' is ' + str(sample1_size))
    print('Sample size of: ' + data_headers_row['Col2'] + ' is ' + str(sample2_size))
    # compute means
    sum1 = 0.0
    sum2 = 0.0
    for row in rows:
        sample1 = row['Col1']
        sample2 = row['Col2']
        if sample1 != '':
          sum1 = sum1 + float(sample1)
        if sample2 != '':
          sum2 = sum2 + float(sample2)

    mean1 = sum1 / sample1_size 
    mean2 = sum2 / sample2_size

    # compute variances
    var1 = 0.0
    var2 = 0.0
    for row in rows:
        sample1 = row['Col1']
        sample2 = row['Col2']
        if sample1 != '':
          var1 = var1 + abs(float(sample1) - mean1)**2
        if sample2 != '':
          var2 = var2 + abs(float(sample2) - mean2)**2
    variance1 = var1 / (sample1_size - 1)
    variance2 = var2 / (sample2_size - 1) 
    result = (mean1 - mean2) / math.sqrt((var1 + var2)/(sample1_size + sample2_size - 2)*(1.0/sample1_size + 1.0/sample2_size))
    print('Sample ' + data_headers_row['Col1'] + ' mean is ' + str(mean1) + ' and variance is ' + str(variance1))
    print('Sample ' + data_headers_row['Col2'] + ' mean is ' + str(mean2) + ' and variance is ' + str(variance2))
    # look up T-Student table
    t_student = t.ppf(1 - alpha/2, sample1_size + sample2_size - 2)
    result_list = {'alpha': alpha, 'result': result, 'T-Student': t_student}
    return result_list



if __name__ == '__main__':
    test_result = t_student_test_mean()
    print("T-Student Test results: " + str(test_result))
    if abs(test_result['result']) < test_result['T-Student']:
        print("HO hypothesis NOT rejected (result is abs(" + str(test_result['result']) + "), which is smaller than T-Student value = " + str(test_result['T-Student']) + ")")
    else:
        print("HO hypothesis is rejected (result is abs(" + str(test_result['result']) + "(, which is greater of equal to T-Student value = " + str(test_result['T-Student']) + ")")

