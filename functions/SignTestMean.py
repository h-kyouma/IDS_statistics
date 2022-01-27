# Jacek Wolski 26/01/2022 - sign test for mean value 


import csv
import math

def sign_test_mean(csv_file='data\SignTestMean.csv'):
    rows = []
    with open(csv_file, 'r',encoding = 'utf-8-sig') as file:
        csvreader = csv.DictReader(file, delimiter =';')
        mean_row = next(csvreader)
        mean = float(mean_row['Data'])
        alpha_row = next(csvreader)
        alpha = float(alpha_row['Data'])
        data_headers_row = next(csvreader)
        for row in csvreader:
            rows.append(row)
    print('Mean: ' + str(mean))
    print('Alpha: ' + str(alpha))
    print('Data headers: ' + data_headers_row['Desc'] + ' ' + data_headers_row['Data'])
    print(rows)

    num_rows = len(rows)
    print('Number of data points: ' + str(num_rows))
    probability = 1
    negative = 0
    positive = 0
    zeros = 0
    for row in rows:
        data_point = float(row['Data'])
        if data_point - mean > 0: 
            positive += 1
            probability *= 0.5
        elif data_point - mean < 0: 
            negative += 1
            probability *= 0.5
        else: zeros += 1

    print("Neg: " + str(negative) + " Pos: " + str(positive) + " Zeros: " + str(zeros));
    result = probability * math.factorial(negative + positive) / (math.factorial(negative) * math.factorial(positive))
    result_list = {'mean': mean, 'alpha': alpha, 'result': result}
    return result_list



if __name__ == '__main__':
    test_result = sign_test_mean()
    print("Sign Test results: " + str(test_result))
    if test_result['result'] < test_result['alpha']:
        print("HO hypothesis rejected")
    else:
        print("HO hypothesis is NOT rejected")

