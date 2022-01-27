# Jacek Wolski 27/01/2022 - Wilcoxon test for pairs


import csv
import math

def Wilcoxon_test_pairs(csv_file='data\WilcoxonTestPairs.csv'):
    rows = []
    with open(csv_file, 'r',encoding = 'utf-8-sig') as file:
        csvreader = csv.DictReader(file, delimiter =';')
        mean_row = next(csvreader)
        mean = float(mean_row['Before'])
        alpha_row = next(csvreader)
        alpha = float(alpha_row['Before'])
        data_headers_row = next(csvreader)
        for row in csvreader:
            rows.append(row)
    print('Mean: ' + str(mean))
    print('Alpha: ' + str(alpha))
    print('Data headers: ' + data_headers_row['Desc'] + '; ' + data_headers_row['Before'] + '; ' + data_headers_row['After'])
    #print(rows)

    num_rows = len(rows)
    print('Number of data points: ' + str(num_rows))
    negative = 0
    positive = 0
    zeros = 0
    increases = []
    for row in rows:
        seq_no = int(row['Desc'])
        before_classes = float(row['Before'])
        after_classes = float(row['After'])
        increase = after_classes - before_classes
        if increase > 0: 
            positive += 1
            sign = 1
        elif increase < 0: 
            negative += 1
            sign = -1
        else: 
            zeros += 1
            sign = 0
        increases.append([abs(increase),sign,0.0])
        #print(str(seq_no) + ' ' + str(increases[seq_no-1]))

    sorted_increases = sorted(increases)
    rank = 0
    W_plus = 0
    W_minus = 0

    series_end = 0
    for incr in sorted_increases:
        count_equal = 1
        rank_equal = rank
        # correct ranks
        i = 1
        for incr2 in sorted_increases:
            if i > rank:
                break
            i += 1
            if incr[0] < incr2[0]:
                continue
            if incr[0] > incr2[0]:
                continue
            if incr[0] == incr2[0]:
                count_equal += 1
                incr[2] = (2*rank - 1)/2
                incr2[2] = incr[2]

        if rank + 1 < num_rows and sorted_increases[rank+1][0] > incr[0]:
            series_end = 1
        else:
            series_end = 0
        if rank + 1 == num_rows: # last row
            series_end = 1

        if count_equal > 2 and series_end == 1:
            for j in range (0, count_equal, 1):
                sorted_increases[rank - j][2] -= (count_equal - 2) / 2.0

        if incr[2] == 0.0:
            incr[2] = rank

        rank += 1

    for incr in sorted_increases:
        if incr[1] > 0: # sign
            W_plus += incr[2] # rank
        elif incr[1] < 0: 
            W_minus += incr[2] 

    print("Neg: " + str(negative) + " Pos: " + str(positive) + " Zeros: " + str(zeros));
    print("W+: " + str(W_plus) + " W-: " + str(W_minus));
    result_list = {'mean': mean, 'alpha': alpha, 'W+': W_plus, 'W-': W_minus, 'n': positive+negative, 'increases': sorted_increases}
    return result_list



if __name__ == '__main__':
    test_result = Wilcoxon_test_pairs()
    print("Wilcoxon Test results: " + str(test_result))
    # read Wilcoxon Signed Rank Test Critical Values Table
    wilcoxon = []
    with open('data\WilcoxonTable.csv', 'r',encoding = 'utf-8-sig') as file:
        csvreader = csv.DictReader(file, delimiter =';')
        #data_headers_row = next(csvreader)
        for row in csvreader:
            wilcoxon.append(row)
    # get alpha index
    alpha_index = str('alpha_0' + str(int(test_result['alpha']*100)).rjust(2,'0'))
    print(wilcoxon[test_result['n']])
    if min(test_result['W-'],test_result['W+']) < int(wilcoxon[test_result['n']][alpha_index]):
        print("HO hypothesis rejected")
    else:
        print("HO hypothesis is NOT rejected")

