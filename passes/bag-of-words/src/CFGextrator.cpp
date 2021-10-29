#include <llvm/IR/Instructions.h>
#include <llvm/Support/raw_ostream.h>
#include "../include/CFGextrator.hpp"

using namespace llvm;

namespace cfg_extractor {

//------------------------------------------------------------------------------
// CFGextractor Implementation
//------------------------------------------------------------------------------

CFGExtractor::CFGExtractor(Module &module) {
    unsigned block_counting = 0;

    std::map<unsigned, std::vector<unsigned>> nodes;
    std::map<unsigned, std::vector<Value *>> edges;
    std::map<unsigned, StringRef> names;
    std::map<StringRef, std::vector<std::tuple<unsigned,StringRef>>> names_calls;

    std::vector<Value *> blocks;

    for (Function &function : module) {
        StringRef fname = function.getName();
        if (function.isDeclaration() == 0) {
            std::vector<std::tuple<unsigned, StringRef>> called_functions;

            // All function names with respective first block
            names[block_counting] = fname;

            for (BasicBlock &block : function) {
                std::vector<Value *> predAddres;
                std::vector<unsigned> score(67, 0);
                const Instruction *terminalInstruction = block.getTerminator();

                for (unsigned I = 0, NSucc = terminalInstruction->getNumSuccessors(); I < NSucc; I++) {
                    BasicBlock *Succ = terminalInstruction->getSuccessor(I);
                    predAddres.push_back(Succ);
                }

                edges[block_counting] = predAddres;
                blocks.push_back(&block);

                for (Instruction &instruction : block) {

                    // 56 is the opcode of Call / CallInst
                    if (CallInst *callInst = dyn_cast<CallInst>(&instruction)) {
                        if (Function *calledFunction = callInst->getCalledFunction()) {
                            StringRef cname = cast<CallInst>(&instruction)->getCalledFunction()->getName();
                            called_functions.push_back({block_counting,cname});
                        }
                    }
                    score[instruction.getOpcode() - 1] = score[instruction.getOpcode() -1] + 1;
                }
                ++block_counting;
                nodes[block_counting] = score;
            }
            // The function Y called by Function X in block Z
            names_calls[fname] = called_functions;
        }
    }

    // Add call function edge
    std::map<unsigned, std::vector<unsigned>> temporario;
    for (std::map<StringRef, std::vector<std::tuple<unsigned,StringRef>>>::const_iterator it = names_calls.begin(); it != names_calls.end(); ++it) {
        for (std::vector<std::tuple<unsigned,StringRef>>::const_iterator it2 = it->second.begin(); it2 != it->second.end(); ++it2) {

            //(func_original_index: func_source_index)
            StringRef func_dest = std::get<1>(*it2);
            for ( const auto &names : names ) {
                if (func_dest == names.second) {
                    unsigned func_source_index = names.first; // Indíce da função values
                    temporario[std::get<0>(*it2)].push_back(func_source_index);
                }
            }
        }
    }


    unsigned vector_count = 0;
    for (std::map<unsigned, std::vector<unsigned>>::const_iterator it = nodes.begin(); it != nodes.end(); ++it) {
        bool zeros = std::all_of(it->second.begin(), it->second.end(), [](int i){ return i==0; });
        if (!zeros) {
            errs() << vector_count << ": [ ";
            for (std::vector<unsigned>::const_iterator it2 = it->second.begin(); it2 != it->second.end(); ++it2) {
                errs() << *it2 << " ";
            }
            errs() << "]" << "\n";
            ++vector_count;
        }
    }
}

} // namespace feature_extractor
