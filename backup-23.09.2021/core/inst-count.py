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

# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

#module_level_variable1 = 12345

#module_level_variable2 = 98765
"""int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""


def apply_inst_count(src_path, out_path, src_benchmarks):
    """Function that apply the LLVM inst count Pass

    Args:
        src_path       (str):
        out_path       (str):
        src_benchmarks (obj):
    """
    passe_path = './../tools/inst-count-pass/build/lib/'
    os.system("mkdir -p " + out_path)
    for bench in range(len(src_benchmarks)):
        out_name = src_benchmarks[bench][:-3]
        out_name = out_name + '.txt'
        #: Applying the LLVM pass
        os.system("opt -load=" + passe_path + "libFeatureExtractor.so -cfg-extractor -disable-output " +
              src_path + src_benchmarks[bench] + " 2> " + out_name)
        os.system("mv " + out_name + " " + out_path)


def baselines(bench_name, out_path):
    opt_plans = ['O0/', 'Os/', 'Oz/']
    baselines_path = './../benchmarks/'+bench_name+'/baselines/'

    for i in range(3):
        base_files = [f for f in listdir(baselines_path+opt_plans[i])
                      if isfile(join(baselines_path+opt_plans[i], f))]
        apply_inst_count(baselines_path+opt_plans[i],
                         out_path+bench_name+'-'+opt_plans[i],
                         base_files
                         )

def best(bench_name, out_path, opt_class):

    best_path = './../benchmarks/'+bench_name+'/'+opt_class+'/'
    best_files = [f for f in listdir(best_path) if isfile(join(best_path, f))]
    apply_inst_count(best_path, out_path+bench_name+'-'+opt_class, best_files)

def Main():
    parser = argparse.ArgumentParser()

    parser.add_argument("bench_name",
                        metavar='p0',
                        nargs='?',
                        const=1,
                        help="[Angha15|AnghaW|Angha15-LLVM|LLVM-Suite-Train|Coremark-pro-f-300]",
                        type=str,
                        ) # use '/' in the end of path specification


    parser.add_argument("out_path",
                        metavar='p1',
                        nargs='?',
                        const=2,
                        help="Path of programs directories.",
                        type=str,
                        ) # use '/' in the end of path specification

    parser.add_argument("opt_class",
                        metavar='p2',
                        nargs='?',
                        const=3,
                        help="[baselines|best_10|best_22]",
                        type=str,
                         )


    args = parser.parse_args()

    if (args.opt_class == 'baselines'):
        baselines(args.bench_name, args.out_path)
    if (args.opt_class=='best_10'):
        best(args.bench_name, args.out_path, args.opt_class)
    if (args.opt_class=='best_22'):
        best(args.bench_name, args.out_path, args.opt_class)

if __name__ == '__main__':
    Main()
