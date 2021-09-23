#!/bin/bash

arg1=$1
arg2=$2
arg3=$3

export CC=clang
export CXX=clang++

if [ ! -d ../tools/cfg-pass/build/ ]; then
    mkdir -p ../tools/cfg-pass/build/
    (cd ../tools/cfg-pass/build/ && cmake .. && make)
fi

if [ ! -d ../tools/msf-pass/build/ ]; then
    mkdir -p ../tools/msf-pass/build/
    (cd ../tools/msf-pass/build/ && cmake .. && make)
fi

if [ ! -d ../tools/cfg-emb-pass/build/ ]; then
    mkdir -p ../tools/cfg-emb-pass/build/
    (cd ../tools/cfg-emb-pass/build && cmake .. && make)
fi


if [[ "$arg1" == "cfg" ]]; then
    if [ ! -d ../benchmarks/"$arg3"/"$arg2"_"$arg1" ]; then
        mkdir -p ../benchmarks/"$arg3"/"$arg2"_"$arg1"
    fi
    for filename in ../benchmarks/"$arg3"/"$arg2"/*.ll; do
        opt -load=../tools/cfg-pass/build/lib/libFeatureExtractor.so -cfg-extractor -disable-output "$filename" 2> "$filename".cfg
        mv "$filename".cfg ../benchmarks/"$arg3"/"$arg2"_"$arg1"
    done

elif [[ "$arg1" == "cfge" ]]; then
    if [ ! -d ../benchmarks/"$arg3"/"$arg2"_"$arg1" ]; then
        mkdir -p ../benchmarks/"$arg3"/"$arg2"_"$arg1"
    fi
    for filename in ../benchmarks/"$arg3"/"$arg2"/*.ll; do
        opt -load=../tools/cfg-emb-pass/build/lib/libFeatureExtractor.so -cfg-extractor -disable-output "$filename" 2> "$filename".cfge
        mv "$filename".cfge ../benchmarks/"$arg3"/"$arg2"_"$arg1"
    done

elif [[ "$arg1" == "msf" ]]; then
    if [ ! -d ../benchmarks/"$arg3"/"$arg2"_"$arg1" ]; then
        mkdir -p ../benchmarks/"$arg3"/"$arg2"_"$arg1"
    fi
    for filename in ../benchmarks/"$arg3"/"$arg2"/*.ll; do
        opt -load=../tools/msf-pass/lib/libMilepostStaticFeatures.so -msf -disable-output "$filename" 2> "$filename".yaml
        mv "$filename".yaml ../benchmarks/"$arg3"/"$arg2"_"$arg1"
    done
else
    echo "must specify ./apply-pass.sh [msf|cfg|cfge] [base_Ox|no_opt] [angha_1k|angh_15k|angha_whole]"
fi

