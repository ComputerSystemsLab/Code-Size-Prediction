#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

#include "../include/CFGextrator.hpp"

using namespace cfg_extractor;
using namespace llvm;

namespace {

void visitor(Module &M) { CFGExtractor msf(M); }

struct CFGExtractorPass : PassInfoMixin<CFGExtractorPass> {
  PreservedAnalyses run(Module &M, ModuleAnalysisManager &) {
    visitor(M);
    return PreservedAnalyses::all();
  }
};

struct LegacyCFGExtractorPass : public ModulePass {
  static char ID;
  LegacyCFGExtractorPass() : ModulePass(ID) {}
  bool runOnModule(Module &M) override {
    visitor(M);
    return false;
  }
};

} // namespace

llvm::PassPluginLibraryInfo getCFGExtractorPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "CFGExtractor", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, ModulePassManager &MPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "cfg-extractor") {
                    MPM.addPass(CFGExtractorPass());
                    return true;
                  }
                  return false;
                });
          }};
}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return getCFGExtractorPassPluginInfo();
}

char LegacyCFGExtractorPass::ID = 0;
static RegisterPass<LegacyCFGExtractorPass>
    X("cfg-extractor",
      "cfg-extractor Pass",
      true,
      false);

#ifdef LT_OPT_PIPELINE_REG

static llvm::RegisterStandardPasses
    RegisterCFGExtractorPass(llvm::PassManagerBuilder::EP_EarlyAsPossible,
                                 [](const llvm::PassManagerBuilder &Builder,
                                    llvm::legacy::PassManagerBase &PM) {
                                   PM.add(new LegacyCFGExtractorPass());
                                 });
#endif
