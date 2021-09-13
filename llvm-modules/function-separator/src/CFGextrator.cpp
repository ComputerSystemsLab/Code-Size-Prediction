#include <llvm/IR/Instructions.h>
#include <llvm/Support/raw_ostream.h>
#include "../include/CFGextrator.hpp"

using namespace llvm;

namespace cfg_extractor {

//------------------------------------------------------------------------------
// CFGextractor Implementation
//------------------------------------------------------------------------------

CFGExtractor::CFGExtractor(Module &module) {
    unsigned int count = 0;
    std::map<unsigned, StringRef> names;
    
    for (Function &function : module) {
        if (function.isDeclaration() == 0) {
            StringRef fname = function.getName();
            names[count] = fname;
            count = count + 1;
            //errs() << function << "\n";
            //errs() << "-----" << "\n";
            //for (BasicBlock &block : function) {        
            //    for (Instruction &instruction : block) {
            //        ++num_inst;
            //    }
            }
        }
        for (std::map<unsigned,StringRef>::const_iterator it = names.begin(); it != names.end(); ++it) {
            StringRef func_name = std::get<1>(*it);
            errs() << func_name << "\n";
        }
    }
    //errs() << num_inst << "\n";

} // namespace feature_extractor
