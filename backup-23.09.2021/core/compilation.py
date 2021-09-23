import os
import yaml
import argparse
from os import listdir
from os.path import isfile, join

'''
Script: compilador de programas
'''


class Compilation:

    def __init__(self, sequences, programs, num_progs, in_path, out_path):
        self.sequences = sequences
        self.programs = programs
        self.num_progs = num_progs
        self.in_path = in_path
        self.out_path = out_path

        self.CMD_optone = 'clang -Xclang -disable-O0-optnone -S -w -emit-llvm -c '
        self.CMD_baseline_O0 = 'opt -O0 -S ' + self.in_path
        self.CMD_baseline_Os = 'opt -Os -S ' + self.in_path
        self.CMD_baseline_Oz = 'opt -Oz -S ' + self.in_path

    def optone(self):
        for i in range(self.num_progs):
            name = self.programs[i]

            print(self.CMD_optone + self.in_path + name)
            os.system(self.CMD_optone + self.in_path + name)
            print('mv *.ll ' + self.out_path)
            os.system('mv *.ll ' + self.out_path)


    def baseline(self):
        os.system('mkdir -p ' + self.out_path + 'O0')
        os.system('mkdir -p ' + self.out_path + 'Os')
        os.system('mkdir -p ' + self.out_path + 'Oz')
        for i in range(self.num_progs):
            name = self.programs[i]

            print(self.CMD_baseline_O0 + name + ' -o ' + name[:-3] + '.O0.ll')
            os.system(self.CMD_baseline_O0 + name + ' -o ' + name[:-3] + '.O0.ll')
            print('mv *.O0.ll ' + self.out_path + 'O0')
            os.system('mv *.O0.ll ' + self.out_path + 'O0')

            print(self.CMD_baseline_Os + name + ' -o ' + name[:-3] + '.Os.ll')
            os.system(self.CMD_baseline_Os + name + ' -o ' + name[:-3] + '.Os.ll')
            print('mv *.Os.ll ' + self.out_path + 'Os')
            os.system('mv *.Os.ll ' + self.out_path + 'Os')

            print(self.CMD_baseline_Oz + name + ' -o ' + name[:-3] + '.Oz.ll')
            os.system(self.CMD_baseline_Oz + name + ' -o ' + name[:-3] + '.Oz.ll')
            print('mv *.Oz.ll ' + self.out_path + 'Oz')
            os.system('mv *.Oz.ll ' + self.out_path + 'Oz')

    def best(self):
        #os.system('mkdir ' + self.out_path + 'best')
        keys = list(self.sequences.keys())
        for i in range(self.num_progs):
            for k in range(len(keys)):
                sq = ' '.join(self.sequences[keys[k]]['seq'])
                name = self.programs[i]
                name_out = name[:-3]+'.0.'+str(keys[k])+'.ll'
                print('opt ' + sq + ' -S ' + self.in_path + name + ' -o ' + name_out)
                os.system('opt ' + sq + ' -S ' + self.in_path + name + ' -o ' + name_out)
                print('mv ' + name_out + ' ' + self.out_path)
                os.system('mv ' + name_out + ' ' + self.out_path)


def Main():
    parser = argparse.ArgumentParser()

    parser.add_argument("in_path",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help="Path of programs directories.",
                        type=str) # use '/' in the end of path specification

    parser.add_argument("out_path",
                        metavar='p1',
                        nargs='?',
                        const=2,
                        help="Path to save.",
                        type=str) # use '/' in the end of path specification

    parser.add_argument("seq_path",
                        metavar='p2',
                        nargs='?',
                        const=3,
                        help="Path of sequences.",
                        type=str,
                        default='./../common/sequences/best22.yaml')

    parser.add_argument("compilation_class",
                        metavar='p3',
                        nargs='?',
                        const=4,
                        help="[optone|baseline|best]",
                        type=str,
                        default='baseline')

    args = parser.parse_args()

    with open(args.seq_path, "r") as seqs:
        sequences = yaml.safe_load(seqs)

    programs = [f for f in listdir(
        args.in_path) if isfile(join(args.in_path, f))]
    num_progs = len(programs)

    comp = Compilation(sequences,
                       programs,
                       num_progs,
                       args.in_path,
                       args.out_path)

    print('Benchmark:   ', args.in_path)
    print('Compilation: ', args.compilation_class)
    print('Sequence:    ', args.seq_path)
    print('Output:      ', args.out_path)

    if (args.compilation_class == 'optone'):
        comp.optone()
    elif(args.compilation_class == 'baseline'):
        comp.baseline()
    elif(args.compilation_class == 'best'):
        comp.best()
    else:
        print('Incomplete')

if __name__ == '__main__':
    Main()
