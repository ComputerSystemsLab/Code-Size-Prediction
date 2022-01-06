import os
import csv
import yaml as yl
import statistics
import os.path
import argparse
import numpy as np
from numpy import std
from os import listdir
from os.path import isfile, join
from numpy.random import seed
from numpy.random import randn
from numpy import percentile
import matplotlib.pyplot as plt


def statistics(yaml_file):
    inst_values = []

    with open(yaml_file, "r") as sq:
        f = yl.safe_load(sq)

    for key, value in f.items():
        inst_values.append(value)

 

    inst_values = np.array(inst_values)
    quartiles = percentile(inst_values, [25, 75])

    print('- num_of_samples: ', len(inst_values))
    print('- max_value: ', max(inst_values))
    print('- min_value: ', min(inst_values))
    print('- mean_value: %.3f' % np.mean(inst_values))
    print('- Q1_value: %.3f' % quartiles[0])
    print('- median_value: %.3f' % np.median(inst_values))
    print('- Q3_value: %.3f' % quartiles[1])
    print('- std_value: %.3f' % std(inst_values))

def Main():
    parser = argparse.ArgumentParser()

    parser.add_argument("yaml_file",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help="Path to .yaml file",
                        type=str,
                        )

    args = parser.parse_args()

    statistics(args.yaml_file)

if __name__ == '__main__':
    Main()
