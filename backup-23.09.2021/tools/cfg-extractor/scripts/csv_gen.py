import yaml
import numpy as np
from os import listdir
from os.path import isfile, join

"""
    Arguments:
"""


def edges_file(bench_path, yaml_graphs):
    print("graph_id,src,dst")
    for i in range(len(yaml_graphs)):
        #print(yaml_graphs[i])
        with open(bench_path + yaml_graphs[i]) as f:
            graph = yaml.safe_load(f)

        for key, value in graph['nodes'].items():
            for dest in range(len(value)):
                print("{},{},{}".format(i, key, value[dest]))

def nodes_file(bench_path, yaml_graphs, labels_path, keys):
    print("graph_id,num_nodes")
    for i in range(len(yaml_graphs)):
        #
        # Reading the Graph
        #
        with open(bench_path + yaml_graphs[i]) as f:
            graph = yaml.safe_load(f)

        num_nodes = len(graph['nodes_features'].keys())
        print("{},{}".format(i, num_nodes))

def nodes_features_labels(bench_path, yaml_graphs, labels_path, keys):
    #
    # Loop per program
    #
    nodes_features = []
    labels_graphs = []
    for i in range(len(yaml_graphs)):
        bag_insts = []
        labels = []
        #
        # Reading the labels
        #
        with open(labels_path + yaml_graphs[i]) as l:
            labels_file = yaml.safe_load(l)

        for k in range(len(keys)):
            labels.append(labels_file[keys[k]]['goal'])
        #
        # Loading the nodes features
        #
        with open(bench_path + yaml_graphs[i]) as f:
            graph = yaml.safe_load(f)
            for key, values in graph['nodes_features'].items():
                bag_insts.append(values)

        labels_graphs.append(labels)
        bag_insts = np.array(bag_insts)
        nodes_features.append(bag_insts)
        print(i)

    labels_graphs = np.array(labels_graphs)
    nodes_features = np.array((nodes_features))

    np.savez_compressed('file',
                        feat=nodes_features,
                        y=labels_graphs)


def Main():
    bench_path = './Coremark-pro-f-300/'
    labels_path = '/home/andrefz/research/m-project/core-massalin/benchmarks/Coremark-pro-f-300/results/goal_best10/'

    #
    # It's necessary to read the files from Graphs and
    # NOT from the Labels, because there are files with
    # zero edges.
    #
    yaml_graphs = [f for f in listdir(bench_path) if isfile(join(bench_path, f))]

    keys_best = []
    with open('/home/andrefz/research/m-project/core-massalin/common/sequences/best10.yaml') as sq:
        sequences = yaml.safe_load(sq)
        for key, value in sequences.items():
            keys_best.append(key)

    #edges_file(bench_path, yaml_graphs)
    #nodes_file(bench_path, yaml_graphs, labels_path, keys_best)
    nodes_features_labels(bench_path, yaml_graphs, labels_path, keys_best)


if __name__ == '__main__':
    Main()
