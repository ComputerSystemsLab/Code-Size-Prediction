benchmark='MiBench.telecomm-FFT.ll'
output='MiBench.telecomm-FFT.txt'

opt -load=lib/libFeatureExtractor.so -cfg-extractor -disable-output /home/andrefz/research/m-project/core-massalin/benchmarks/mibench/no_opt/"$benchmark" 2> "$output"
#awk '/-----/{n++}{print >"FFT-f" n ".ll" }' "$output".ll
