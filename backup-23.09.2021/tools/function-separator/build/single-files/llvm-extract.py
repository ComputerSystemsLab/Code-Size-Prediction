import os
import csv
import yaml
import argparse
from os import listdir
from os.path import isfile, join

'''
Script: compilador de programas
'''


def llvm_extract(mibench_path, prog_path, program, num_progs, mibench, output):
    for i in range(num_progs):
        name_out = mibench[i][:-3]
        name_out = name_out+'.txt'
        with open(prog_path+name_out) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        print(content)
        for j in range(len(content)):
            os.system("llvm-extract --func=" + content[j] + ' ' + mibench_path+mibench[i] + ' -S -o ' + name_out+'_'+content[j]+'.ll')
            os.system("mv *.ll " + output)

def Main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dir_path", metavar='p0', nargs='?', const=1,
                        help="Path of programs directories.", type=str,
                        default='./names-mibench/')

    parser.add_argument("output", metavar='p1', nargs='?', const=2,
                        help="Path to save.", type=str,
                        default='./mibench-functions')


    parser.add_argument("prog_path", metavar='p4', nargs='?', const=4,
                        help="Path of IR programs.", type=str,
                        default='/home/andrefz/research/m-project/core-massalin/benchmarks/Mibench/no_opt/')

    args = parser.parse_args()

    programs = [f for f in listdir(
        args.dir_path) if isfile(join(args.dir_path, f))]
    num_progs = len(programs)

    print(num_progs)
    print(programs)

    mibench = [
        'MiBench.automotive-basicmath-large.ll',
        'MiBench.automotive-basicmath-small.ll',
        'MiBench.automotive-bitcount.ll',
        'MiBench.automotive-qsort-small.ll',
        'MiBench.automotive-susan-c.ll',
        'MiBench.automotive-susan-e.ll',
        'MiBench.automotive-susan-s.ll',
        'MiBench.consumer-jpeg-c.ll',
        'MiBench.consumer-jpeg-d.ll',
        'MiBench.consumer-lame.ll',
        'MiBench.network-dijkstra.ll',
        'MiBench.network-patricia.ll',
        'MiBench.office-stringsearch-large.ll',
        'MiBench.office-stringsearch-small.ll',
        'MiBench.security-rijndael-d.ll',
        'MiBench.security-rijndael-e.ll',
        'MiBench.security-sha.ll',
        'MiBench.telecomm-CRC32.ll',
        'MiBench.telecomm-FFT.ll']

    llvm_extract(args.prog_path, args.dir_path, programs, num_progs, mibench, args.output)

if __name__ == '__main__':
    Main()
