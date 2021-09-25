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


def statistics(csv_file):
    inst_values = []

    print(type(csv_file))
    with open(csv_file, mode='r') as sq:
        f = csv.DictReader(sq)

    print(f)
    line_count = 0
    for row in f:
        print("oi")

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
