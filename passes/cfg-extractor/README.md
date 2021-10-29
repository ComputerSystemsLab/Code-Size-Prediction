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
Direcionar saída com `2>` e aplicar `/script/preprocess.sh` em seguida.

### Node features
Vector of 67 elements (llvm/IR/Instruction.def), where each element is a counting of an specificy instruction.
