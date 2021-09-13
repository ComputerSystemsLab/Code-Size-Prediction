import os
import csv
import yaml
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


def Main():
    parser = argparse.ArgumentParser()

    parser.add_argument("output",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help="Path of programs directories.",
                        type=str,
                        ) # --> '/'

    args = parser.parse_args()

    absolute = '/home/andrefz/research/m-project/core-massalin/tools/inst-count-pass/'+args.output+'/'
    programs = [f for f in listdir(absolute) if isfile(join(absolute, f))]

    vetor = []
    for i in range(len(programs)):
        with open(absolute+programs[i]) as f:
            csv_file = csv.reader(f)
            for num in csv_file:
                fit = num
                fit = fit[0]
                vetor.append(int(fit))

    vetor = np.array(vetor)
    print(len(vetor))
    print('max value: ', max(vetor))
    print('min value: ', min(vetor))
    print('mean value: ', np.mean(vetor))
    print('std value: ', std(vetor))

    #plt.plot(vetor)
    #plt.show()

if __name__ == '__main__':
    Main()
