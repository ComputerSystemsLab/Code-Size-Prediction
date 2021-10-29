import os
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

    for i in range(len(programs)):
        name = programs[i][:-3]
        os.system("python3 goal.py "+programs[i]+" > "+name+'.yaml')
        #break

if __name__ == '__main__':
    Main()
