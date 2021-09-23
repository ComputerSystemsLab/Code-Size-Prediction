import os
import csv
import yaml
import argparse
import numpy as np
from operator import itemgetter
from os import listdir
from os.path import isfile, join

""" Find the biggest files
"""

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help='datasetname',
                        type=str,
                        default='Mibench-f-complete.yaml')

    parser.add_argument("max_hot_function",
                        metavar='p1',
                        nargs='?',
                        const=2,
                        help='The first n hot functions',
                        type=int,
                        default=300)

    args = parser.parse_args()

    statistics_path = '/home/andrefz/research/m-project/core-massalin/tools/inst-count-pass/'
    with open(statistics_path + args.dataset) as f:
        insts = yaml.safe_load(f)
        res = dict(sorted(insts.items(), key=itemgetter(1), reverse = True) [:args.max_hot_function])
        for key, value in res.items():
            #key = key[:-5]
            #key = key + 'yaml'
            key = key+'.ll'
            print(key)
            #print(key + ': '+str(value))

if __name__ == '__main__':
    Main()
