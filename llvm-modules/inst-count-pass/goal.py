import os
import csv
import yaml
import os.path
import argparse
import numpy as np
from os import listdir
from os.path import isfile, join


def goals(file):
    name = file[:-3]

    best_10 = ['435','1577','1606','2659',
               '5288','5624','6955','7399',
               '7672','9965']

    best_22 = ['324','435','453','500','1491',
               '1577','1606','2214','2659',
               '3360','3801','3845','5288',
               '5624','6955','7399','7672',
               '7774','8048','8712','9934',
               '9965']

    goal = []
    for s in range(len(best_10)):
        if (os.path.isfile('./out/'+name+'.0.'+best_10[s]+'.ll.txt') == True):
            with open('./out/'+name+'.0.'+best_10[s]+'.ll.txt') as f:
                csv_file = csv.reader(f)
                for num in csv_file:
                    fitness = num
                    goal.append(int(fitness[0]))
        else:
            goal.append(0)

    if (all(v==0 for v in goal)):
        pass
    else:
        for i in range(len(best_10)):
            print(best_10[i]+':')
            print('  goal:', goal[i])

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help="prog name.", type=str)
    args = parser.parse_args()

    goals(args.file)

if __name__ == '__main__':
    Main()
