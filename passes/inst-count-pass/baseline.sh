#!/bin/bash


# apply the pass over all benchmarks.
mkdir -p out_"$3"_"$1"

for filename in /home/andrefz/research/m-project/core-massalin/benchmarks/"$1"/"$2"/*.ll; do
    opt -load=build/lib/libFeatureExtractor.so -cfg-extractor -disable-output "$filename" 2> "$filename".txt
    mv "$filename".txt out_"$3"_"$1"/
done

