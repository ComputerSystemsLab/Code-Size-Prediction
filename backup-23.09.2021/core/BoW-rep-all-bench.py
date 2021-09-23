import yaml
import click
import pickle
import argparse
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join


class LoadData:

    def __init__(self, keys, all_data_aux, fitness_best, fitness_path, yaml_path, embedding_path, suite):
        self.keys = keys
        self.all_data_aux = all_data_aux
        self.fitness_best = fitness_best
        self.fitness_path = fitness_path
        self.yaml_path = yaml_path
        self.embedding_path = embedding_path
        self.suite = suite


    def complete_array(self, array_bag, max_len):
        array_size = len(array_bag)

        if(array_size < max_len):
            for i in range(array_size, max_len):
                mask_value = np.full((67), -10)
                mask_value = mask_value.astype(np.int16)
                array_bag = np.append(array_bag, [mask_value], axis=0)

        elif(array_size > max_len):
            n = array_size - max_len
            array_bag = array_bag[:-n, :].astype(np.int16)

        return array_bag


    def bag_of_inst(self, sum_or_not):

        bag_insts, goal_data, name_data, keys_data = ([] for i in range(4))

        for prog in range(len(self.all_data_aux)):
            print(self.yaml_path + '/' + self.all_data_aux[prog])
            summ = []
            # Carregando o arquivo contendo
            # os vetores
            with open(self.yaml_path + '/' + self.all_data_aux[prog]) as f:
                insts = yaml.safe_load(f)
                for key, value in insts.items():
                    summ.append(value)

            summ = np.array(summ)

            if (sum_or_not == 1):
                summ = sum(summ)
            else:
                summ = self.complete_array(summ, 300)

            # Carregando o arquivo contento
            # os valores y
            print(self.fitness_path + self.all_data_aux[prog]+'\n')
            with open(self.fitness_path + self.all_data_aux[prog]) as fl:
                label_yaml = yaml.safe_load(fl)

            for k in range(len(self.keys)):
                # y
                goal = label_yaml[self.keys[k]]['goal']
                # benchmark
                name_ncc = self.fitness_best[prog][:-5]
                try:
                    # Se o programa possui
                    # uma representação inst2vec
                    # inserir a o input auxiliar
                    # /home/andrefz/research/m-project/data-massalin/representations/llvm-suite-train//llvm-suite-train/-noopt-ncc/CAPBenchmarks.RT_seq.csv
                    df = pd.read_csv(self.embedding_path + self.suite + '/' + self.suite + '-noopt-ncc/' + name_ncc + '_seq.csv')

                    bag_insts.append(summ)
                    goal_data.append(goal)
                    name_data.append(name_ncc)
                    keys_data.append(self.keys[k])

                except IOError:
                    # If missing file, fill with zeros
                    #bag_insts.append(np.zeros((300,67)).astype(np.int16))
                    bag_insts.append(np.zeros((67)).astype(np.int16))
                    goal_data.append(0.0)
                    name_data.append(name_ncc)
                    keys_data.append(self.keys[k])
                    continue

        bag_insts = np.array((bag_insts), dtype='int16')
        goal_data = np.expand_dims(goal_data, axis=1)
        name_data = np.expand_dims(name_data, axis=1)
        keys_data = np.expand_dims(keys_data, axis=1)

        np.savez_compressed('BoW-Nodes-best22-'+self.suite,
                            bag_insts=bag_insts,
                            goal=goal_data,
                            name=name_data,
                            keys=keys_data)

        return bag_insts

def Main():

    parser = argparse.ArgumentParser()
    parser.add_argument("prog_yaml",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help='Loading the inst2vec csv files.',
                        type=str,
                        default='/home/andrefz/research/m-project/data-massalin/representations')

    parser.add_argument("best",
                        metavar='p4',
                        nargs='?',
                        const=4,
                        help='[best22|best10]',
                        type=str,
                        default='best22')


    args = parser.parse_args()
    keys = []

    """
    benchmarks_noopt = ['Coremark-pro',
                       'Coremark-pro-f-300',
                       'Mibench',
                       'Mibench-f-300',
                       'LLVM-Suite-Train',
                       'LLVM-Suite-Test',
                       'Angha15',
                       'Angha15-LLVM',
                       'AnghaW',
                       'AnghaW-LLVM']
    """

    benchmarks_noopt = ['LLVM-Suite-Train',
                        'LLVM-Suite-Test',
                        'Mibench',
                        'Mibench-f-300',
                        'Coremark-pro-f-300',
                        'Coremark-pro']

    # Sequence keys
    with open('./../common/sequences/'+ args.best+'.yaml') as sq:
        sequences = yaml.safe_load(sq)
        for key, value in sequences.items():
            keys.append(key)

    # Absolute paths
    benchmarks_path = '/home/andrefz/research/m-project/core-massalin/benchmarks/'
    embedding_path = '/home/andrefz/research/m-project/data-massalin/representations/'

    ########################################################
    all_bow_vectors = []
    for b in range(len(benchmarks_noopt)):
        yaml_path = args.prog_yaml + '/' + benchmarks_noopt[b] + '/' + benchmarks_noopt[b] + '-bag-inst'
        fitness_path = benchmarks_path + benchmarks_noopt[b] + '/results/goal_' + args.best + '/'
        all_data_aux = [f for f in listdir(yaml_path) if isfile(join(yaml_path, f))]
        fitness_best = [g for g in listdir(fitness_path) if isfile(join(fitness_path, g))]

        model = LoadData(keys, all_data_aux, fitness_best, fitness_path, yaml_path, embedding_path, benchmarks_noopt[b])
        bow_vector = model.bag_of_inst(0)
        #all_bow_vectors.append(bow_vector)

    #all_bow_vectors = np.array(all_bow_vectors)
    #np.savez_compressed('all_bow_vectors',bag_insts=all_bow_vectors)

if __name__ == '__main__':
   Main()
