import yaml
import pickle
import argparse
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join


class LoadData:

    def __init__(self, name, embedding, fitness_path, keys, objects):
        self.name = name
        self.embedding = embedding           # caminho comun para as representações
        self.fitness_path = fitness_path     # arquivo com os fitness
        self.objects = objects               # arquivo com as médias dos vetores
        self.keys = keys
        self.fitness = [f for f in listdir(self.fitness_path)
                        if isfile(join(self.fitness_path, f))]

    def non_normalization(self, word_indices, pre_values):
        nr = []
        for i in range(len(word_indices)):
            nr.append(pre_values[word_indices[i]])
        nr = np.array(nr)
        return nr

    def normalization_1(self, word_indices, pre_values):
        #
        # Parameters
        # ----------
        # - word_indices: list with instruction indices
        # - objetcs: dense vector mean for each instruction
        #            according to their indice
        #
        r1 = word_indices
        for i in range(len(word_indices)):
            r1[i] = pre_values[word_indices[i]]
        return r1


    def normalization_2(self, word_indices, pre_values):
        #
        # Parameters
        # ----------
        #
        #
        r2 = np.zeros(200)
        for i in range(len(word_indices)):
            r2 = r2 + pre_values[word_indices[i]]
        r2 = r2/len(word_indices)
        return r2


    def normalization_3(self, word_indices, pre_values):
        #
        # Parameters
        # ----------
        #
        #
        r3 = np.zeros(200)
        for i in range(len(word_indices)):
            r3 = r3 + pre_values[word_indices[i]]
        return r3


    def ncc(self):
        ncc_data_r1, ncc_data_r2, \
        ncc_data_r3, goal_data,  \
        name_data, keys_data, \
        dense_vectors_r1, dense_vectors_r2 = ([] for i in range(8))

        [dense_vectors_r1.append(np.mean(word)) for word in self.objects[0]]
        [dense_vectors_r2.append(word) for word in self.objects[0]]

        #
        # Loop through goal files
        #
        for prog_l in range(len(self.fitness)):
            print(self.fitness_path + self.fitness[prog_l])

            with open(self.fitness_path + self.fitness[prog_l]) as fl:
                label_yaml = yaml.safe_load(fl)

            # Loop over 22
            for k in range(len(self.keys)):
                goal = label_yaml[self.keys[k]]['goal']
                name_ncc = self.fitness[prog_l][:-5]

                #
                # Loading correspondent inst2vec embedding
                #
                try:
                    df = pd.read_csv(self.embedding + '/' + name_ncc + '_seq.csv')
                except IOError:
                    # If missing file, fill with zeros
                    ncc_data_r1.append(np.zeros(300))
                    ncc_data_r2.append(np.zeros(200))
                    ncc_data_r3.append(np.zeros(200))
                    goal_data.append(0.0)
                    name_data.append(name_ncc)
                    keys_data.append(self.keys[k])
                    continue

                # Flatten the vector
                flat_values_1 = [item for sublist in df.values for item in sublist]
                flat_values_2 = [item for sublist in df.values for item in sublist]
                flat_values_3 = [item for sublist in df.values for item in sublist]

                # Normalizing
                r1_vector = self.normalization_1(flat_values_1,dense_vectors_r1)
                r2_vector = self.normalization_2(flat_values_2,dense_vectors_r2)
                r3_vector = self.normalization_3(flat_values_3,dense_vectors_r2)

                ncc_data_r1.append(r1_vector)
                ncc_data_r2.append(r2_vector)
                ncc_data_r3.append(r3_vector)

                goal_data.append(goal)
                name_data.append(name_ncc)
                keys_data.append(self.keys[k])

        # 
        # Expanding dimentions
        #
        ncc_data_r1 = np.array(ncc_data_r1)
        ncc_data_r1 = np.expand_dims(ncc_data_r1, axis=1)
        ncc_data_r2 = np.expand_dims(ncc_data_r2, axis=1)
        ncc_data_r3 = np.expand_dims(ncc_data_r3, axis=1)

        goal_data = np.array(goal_data)
        goal_data = np.expand_dims(goal_data, axis=1)

        name_data = np.array(name_data)
        name_data = np.expand_dims(name_data, axis=1)

        keys_data = np.array(keys_data)
        keys_data = np.expand_dims(keys_data, axis=1)

        np.savez_compressed(self.name,
                            ncc_r1=ncc_data_r1,
                            ncc_r2=ncc_data_r2,
                            ncc_r3=ncc_data_r3,
                            goal=goal_data,
                            name=name_data,
                            keys=keys_data)


def Main():

    parser = argparse.ArgumentParser()
    parser.add_argument("prog_csv",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help='Loading the inst2vec csv files.',
                        type=str,
                        default = './../../data-massalin/representations/')

    parser.add_argument("prog_label",
                        metavar='p1',
                        nargs='?',
                        const=2,
                        help='Loading fitness yaml file.',
                        type=str,
                        default = './../benchmarks/')

    parser.add_argument("suite",
                        metavar='p2',
                        nargs='?',
                        const= 3,
                        help='[angha_15|angha_w|llvm_300|coremark-pro|mibench]',
                        type=str,
                        default='SAMPLE-02-angha-300')


    parser.add_argument("best",
                        metavar='p4',
                        nargs='?',
                        const=4,
                        help='[best22|best10]',
                        type=str,
                        default = 'best10')

    parser.add_argument("name",
                        metavar='p6',
                        nargs='?',
                        const=6,
                        help='file name',
                        type=str,
                        default='SAMPLE-02.npz')
    args = parser.parse_args()

    print("Benchmark: %s \n>> %s" % (args.suite, args.name))

    keys_22, objects = ([] for i in range(2))

    #
    # Loading inst2vec vocabulary
    #
    with open('./../common/sequences/vocabulary/emb.p', 'rb') as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    #
    # Loading sequences
    #
    print('./../common/sequences/'+ args.best+'.yaml')
    with open('./../common/sequences/'+ args.best+'.yaml') as sq:
        sequences = yaml.safe_load(sq)
        for key, value in sequences.items():
            keys_22.append(key)

    #
    # Path of y values
    #
    fitness_path = args.prog_label+args.suite+'/results/goal_'+args.best+'/'
    print(fitness_path)

    args.suite = LoadData(args.name,
                        args.prog_csv+args.suite+'/'+args.suite+'-noopt-ncc',
                        fitness_path,
                        keys_22,
                        objects)

    args.suite.ncc()

if __name__ == '__main__':
   Main()
