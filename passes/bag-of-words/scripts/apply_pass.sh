#!/bin/bash

# apply the pass over all benchmarks.
# $1: absolute benchmarks directory
# $2: output directory

arg1=$1
arg2=$2

mkdir -p "$arg2"

for filename in "$arg1"/*.ll; do
    opt -load=../build/lib/libFeatureExtractor.so -cfg-extractor -disable-output "$filename" 2> "$filename".yaml
    # remove empty [ ] fazer isso no passe
    sed -i '/\[ \]/d' "$filename".yaml
    # replace space with comma
    sed -i 's/\s\+/,/g' "$filename".yaml
    # remove first charactere
    sed -i 's/,//' "$filename".yaml
    # remove first ocurrence of ,
    sed -i 's/,//' "$filename".yaml
    # remove second ocurrence of ,
    #sed -i 's/,//' "$filename"
    # substituindo
    sed -i 's/:/: /' "$filename".yaml
    sed -i 's/,]/]/' "$filename".yaml
    # adding white spaces
    sed -i -e 's/^/  /' "$filename".yaml
    # removing spacelines from nodes
    sed -i '/nodes/s/^.\{2\}//' "$filename".yaml
    # add white space after comma
    sed -i 's/, */, /g' "$filename".yaml
    mv "$filename".yaml "$arg2"
done
