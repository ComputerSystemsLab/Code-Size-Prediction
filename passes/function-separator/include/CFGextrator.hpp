#include <llvm/IR/Module.h>
#include <ostream>

using namespace llvm;

namespace cfg_extractor {

class CFGExtractor {
public:
  CFGExtractor(Module &);
  friend std::ostream &operator<<(std::ostream &, const CFGExtractor &);
};

} // namespace cfg_extractor

