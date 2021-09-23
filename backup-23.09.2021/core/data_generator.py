import yaml
import click
import pickle
import argparse
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

from sklearn.manifold import TSNE


class LoadData:

    def __init__(self, name, embedding, fitness_path, keys, objects, normalization):
        self.name = name
        self.embedding = embedding           # caminho comun para as representações
        self.fitness_path = fitness_path     # arquivo com os fitness
        self.objects = objects               # arquivo com as médias dos vetores
        self.keys = keys
        self.normalization = normalization
        self.fitness = [f for f in listdir(self.fitness_path)
                        if isfile(join(self.fitness_path, f))]

    def i2v_matrix(self, word_indices, pre_values):
        # Chamada por programa
        nr = []
        num_index = len(word_indices)

        if(num_index) >= 300:
            for i in range(300):
                embedding_vector = pre_values[word_indices[i]]
                embedding_vector = embedding_vector.astype(np.float32)
                nr.append(embedding_vector)
        else:
            for j in range(num_index):
                embedding_vector = pre_values[word_indices[j]]
                embedding_vector = embedding_vector.astype(np.float32)
                nr.append(embedding_vector)
            remainder = 300 - num_index
            for k in range(num_index, num_index + remainder):
                # Converting to int16 to save memory
                mask_value = np.full((200), -10)
                mask_value = mask_value.astype(np.int8)
                nr.append(mask_value)

        nr = np.array(nr)
        return nr


    def ncc(self):

        i2v_data = ([] for i in range(7))

        ncc_data, goal_data, name_data, keys_data, \
        dense_vectors = ([] for i in range(6))

        [dense_vectors.append(word) for word in self.objects[0]]

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
                    ncc_data.append(np.zeros(dimension))
                    goal_data.append(0.0)
                    name_data.append(name_ncc)
                    keys_data.append(self.keys[k])
                    continue

                # Flatten the vector (Program's dense vector indices)
                flat_values = [item for sublist in df.values for item in sublist]


                i2v_representation = self.i2v_matrix(flat_values,dense_vectors)
                i2v_data.append(i2v_representation)

                elif (self.normalization == 'tSNE'):
                    tsne_representation = self.tSNE(flat_values,dense_vectors)

                goal_data.append(goal)
                name_data.append(name_ncc)
                keys_data.append(self.keys[k])

        goal_data = np.expand_dims(goal_data, axis=1)
        name_data = np.expand_dims(name_data, axis=1)
        keys_data = np.expand_dims(keys_data, axis=1)

        if (self.normalization == 0):
            i2v_data = np.array(i2v_data)
            # Saving binary
            np.savez_compressed(self.name,
                                i2v=i2v_data,
                                goal=goal_data,
                                name=name_data,
                                keys=keys_data)

            print(i2v_data.shape)

        else:
            #avg_words_data   = np.expand_dims(avg_words_data, axis=1)
            avg_prog_data    = np.expand_dims(avg_prog_data, axis=1)
            avg_prog_l1_data = np.expand_dims(avg_prog_l1_data, axis=1)
            sum_data         = np.expand_dims(sum_data, axis=1)
            min_max_data     = np.expand_dims(min_max_data, axis=1)
            # Saving binary
            np.savez_compressed(self.name,
                                #avg_words=avg_words_data,
                                avg_prog=avg_prog_data,
                                avg_prog_l1=avg_prog_l1_data,
                                sum_prog=sum_data,
                                min_max=min_max_data,
                                goal=goal_data,
                                name=name_data,
                                keys=keys_data)

            print(" avg_prog: %s\n avg_prog_l1: %s\n sum_prog: %s\n min_max: %s\n goal: %s\n name: %s\n keys: %s" %
                  (avg_prog_data.shape,
                   avg_prog_l1_data.shape,
                   sum_data.shape,
                   min_max_data.shape,
                   goal_data.shape,
                   name_data.shape,
                   keys_data.shape))

def Main():

    parser = argparse.ArgumentParser()
    parser.add_argument("prog_csv",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help='Loading the inst2vec csv files.',
                        type=str,
                        default='./../../data-massalin/representations/')

    parser.add_argument("prog_label",
                        metavar='p1',
                        nargs='?',
                        const=2,
                        help='Loading fitness yaml file.',
                        type=str,
                        default='./../benchmarks/')

    parser.add_argument("suite",
                        metavar='p2',
                        nargs='?',
                        const= 3,
                        help='[angha_15|angha_w|llvm_300|coremark-pro|mibench]',
                        type=str,
                        default='angha_15_2k_random_llvm_train')

    parser.add_argument("best",
                        metavar='p4',
                        nargs='?',
                        const=4,
                        help='[best22|best10]',
                        type=str,
                        default='best10')

    parser.add_argument("name",
                        metavar='p6',
                        nargs='?',
                        const=6,
                        help='file name',
                        type=str,
                        default='angha_15_2k_random_llvm_train-mask.npz')

    parser.add_argument("normalization",
                        metavar='p7',
                        nargs='?',
                        const=7,
                        help='[1|0|tSNE]',
                        type=str,
                        default=0)

    args = parser.parse_args()

    print("Benchmark: %s \nRepresentation: %s \n>> %s\n" %
          (args.suite, args.normalization, args.name))

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
    with open('./../common/sequences/'+ args.best+'.yaml') as sq:
        sequences = yaml.safe_load(sq)
        for key, value in sequences.items():
            keys_22.append(key)

    #
    # Path of y values
    #
    fitness_path = args.prog_label+args.suite+'/results/goal_'+args.best+'/'

    args.suite = LoadData(args.name,
                        args.prog_csv+args.suite+'/'+args.suite+'-noopt-ncc',
                        fitness_path,
                        keys_22,
                        objects,
                        args.normalization)

    args.suite.ncc()

if __name__ == '__main__':
   Main()
