#!/bin/bash


# apply the pass over all benchmarks.

for filename in /home/andrefz/research/m-project/core-massalin/benchmarks/"$1"/best_10/*.ll; do
    opt -load=build/lib/libFeatureExtractor.so -cfg-extractor -disable-output "$filename" 2> "$filename".txt
    mv "$filename".txt out/
done

python3 aux.py /home/andrefz/research/m-project/core-massalin/benchmarks/"$1"/no_opt/
