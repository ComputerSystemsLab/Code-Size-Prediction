LLVM analysis pass to dump the CFG edges and nodes.

## Building

```sh
export CC=clang
export CXX=clang++
mkdir build
cd build
cmake .. && cmake --build .
```

### Usage

```sh
opt -load=lib/libFeatureExtractor.so -cfg-extractor -disable-output /path/to/ir
```

### Node features
Vector of 67 elements (llvm/IR/Instruction.def), where each element is a counting of an specificy instruction.


baselines.sh: ./baseline.sh llvm_300_train baselines/O0 O0

statistics.py: aplicar no output out/ que são arquivos txt com o nr de instruçoes

apply_pass.sh -> aux.py -> goal.py
