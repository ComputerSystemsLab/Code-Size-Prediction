import yaml as yl
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences


def sequence_encoding(seqs, passes):
  '''
  Encoding compilation plans in integers.
  - Arguments:
                - number_samples: Integer
                - seqs: Optimizaton sequences
                - passes: LLVM flags
  '''
  sequences, sequences_map_final = ([] for i in range(2))
  for key, value in seqs.items():
    sequences.append(seqs[key]['seq'])

  # Listing passes
  passes = passes['flags']
  singlePasses = list(set(passes))
  pass_list = sorted(set(singlePasses))
  print('  -Vocabulary size (Passes): ',len(pass_list),'\n')
  print(pass_list)

  # Converting passes to Integers
  pass2idx = {word:idx for idx, word in enumerate(pass_list, 1)}
  idx2word = {idx:word for idx, word in enumerate(pass_list, 1)}
  print(idx2word)

  # Encoding sequences
  sequences_map = list(map(lambda sequences: [pass2idx.get(token) for token in sequences], sequences))
  sequences_map = pad_sequences(sequences_map, maxlen=19, padding='post')
  sequences_map = sequences_map.astype(np.float32)
  print(sequences_map)

  return sequences_map


def Main():

    with open('./best22.yaml', "r") as sq:
        seqs = yl.safe_load(sq)

    with open('./flags-best22.yaml', "r") as ps:
        passes = yl.safe_load(ps)

    sequence_encoding(seqs, passes)

if __name__ == '__main__':
    Main()
