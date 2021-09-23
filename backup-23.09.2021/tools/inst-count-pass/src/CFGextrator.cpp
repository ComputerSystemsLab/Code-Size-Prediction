#include <llvm/IR/Instructions.h>
#include <llvm/Support/raw_ostream.h>
#include "../include/CFGextrator.hpp"

using namespace llvm;

namespace cfg_extractor {

//------------------------------------------------------------------------------
// CFGextractor Implementation
//------------------------------------------------------------------------------

CFGExtractor::CFGExtractor(Module &module) {
    unsigned int num_inst = 0;
    for (Function &function : module) {
        if (function.isDeclaration() == 0) {
            for (BasicBlock &block : function) {        
                for (Instruction &instruction : block) {
                    ++num_inst;
                }
            }
        }
    }
    errs() << num_inst << "\n";
}

} // namespace feature_extractor
