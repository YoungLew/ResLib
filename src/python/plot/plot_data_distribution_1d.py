#! /usr/bin/env python
#
#     File Name           :     plot_data_distribution_1d.py
#     Created By          :     largelymfs
#     Creation Date       :     [2015-12-23 14:16]
#     Last Modified       :     [2015-12-24 14:36]
#     Description         :     plot the data distribution given multi label 
#

#data format : data label


import matplotlib.pyplot as plt
import numpy as np

def load_data(filename):
    with open(filename) as fin:
        datas = [l.strip().split() for l in fin]
        label = set([item[1] for item in datas]) 
        data_map = {}
        for l in label:
            data_map[l] = []
        for dataitem in datas:
            data_map[dataitem[1]].append(float(dataitem[0]))
    return data_map

def plot(label, data, min_value, max_value, delta, length, norm=False, smooth = 0):

    item_number = np.zeros(length)

    for item in data:
        index = (item - min_value) / delta
        index = int(index)
        item_number[index] += 1
    
    #normalize
    if norm==True:
        for index in range(length):
            item_number[index] /=  float(len(data))
    
    #smooth
    smooth_item_number = np.zeros(length)
    for index in xrange(length):
        start = max(0, index - smooth)
        finish = min(length - 1, index + smooth)
        smooth_item_number[index] = sum(item_number[start:finish + 1]) / float(finish - start + 1)
    item_number = smooth_item_number
    plt.plot(delta * np.array(range(length)) + min_value, item_number, label = label)

def get_extreme(data_lists):
    max_values = [max(item) for item in data_lists]
    min_values = [min(item) for item in data_lists]
    return min(min_values), max(max_values)

def main():
    data_filename, _norm, smooth = parse_arg()
    if _norm == 1:
        norm = True
    else:
        norm = False
    data_map = load_data(data_filename)
    min_value, max_value = get_extreme(data_map.values())
    delta = 0.5
    length = (max_value - min_value) / delta + 1
    length = int(length)
    for k, v in data_map.items():
        plot(k, v, min_value, max_value, delta, length, norm, smooth)
    plt.legend()
    plt.show()

def parse_arg():
    import argparse
    parser = argparse.ArgumentParser(description = 'plot the data distribution with 1-d data')
    parser.add_argument('data_filename', type=str, help = 'data distribution filename')
    parser.add_argument('--norm', '-n', type=int, help = '0=normalize, 1=do not normalize')
    parser.add_argument('--smooth', '-s', type=int, help='smooth parameters : 0 means not smooth')
    args = parser.parse_args()
    return args.data_filename, args.norm, args.smooth 

if __name__=="__main__":
    main()
