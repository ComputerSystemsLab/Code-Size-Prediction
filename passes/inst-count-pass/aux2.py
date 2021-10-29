import os
import csv
import yaml
import argparse
import numpy as np
from os import listdir
from os.path import isfile, join


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",
                        metavar='p1',
                        nargs='?',
                        const=1,
                        help="prog path", type=str)
    args = parser.parse_args()

    programs = [f for f in listdir(args.path) if isfile(join(args.path, f))]

    values, names = ([] for i in range(2))
    for i in range(len(programs)):
        with open(args.path+programs[i]) as f:
            csv_file = csv.reader(f)
            for num in csv_file:
                fitness = num
                values.append(int(fitness[0]))
                names.append(programs[i][:-4])

    for i in range(len(programs)):
        print(names[i]+': '+str(values[i]))

if __name__ == '__main__':
    Main()
