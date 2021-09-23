import os
import csv
import yaml
import os.path
import argparse
import numpy as np
from os import listdir
from os.path import isfile, join


def goals(file):
    goal = []
    name = file[:-3]

    best_10 = ['435','1577','1606','2659',
               '5288','5624','6955','7399',
               '7672','9965']

    """ Best_22
            Investigar origem deste Best_22
    """
    #best_22 = ['324','435','453','500','1491',
    #           '1577','1606','2214','2659',
    #           '3360','3801','3845','5288',
    #           '5624','6955','7399','7672',
    #           '7774','8048','8712','9934',
    #           '9965']
    best_22 = ['200','310','460','470','512',
               '549','715','722','736','745',
               '835','902','929','957','976',
               '991','1014','1099','1167',
               '1177','1225','1253']

    wich_best = best_22

    for s in range(len(wich_best)):
        if (os.path.isfile('./out/'+name+'.0.'+wich_best[s]+'.ll.txt') == True):
            with open('./out/'+name+'.0.'+wich_best[s]+'.ll.txt') as f:
                csv_file = csv.reader(f)
                for num in csv_file:
                    fitness = num
                    goal.append(int(fitness[0]))
        else:
            goal.append(0)

    if (all(v==0 for v in goal)):
        pass
    else:
        for i in range(len(wich_best)):
            print(wich_best[i]+':')
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
