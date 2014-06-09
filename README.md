Word Bases MT System with NN
============================

#### Generative Story

```
1. i <- 1, j <- 0
2. Choose \delta j from [-h, h] with the following probability:
	 P_d(\delta j | f_{j - h}, ..., f_{j+h}, e_{i-g}, ..., e_{i + j})
3. Let j <- j + \delta j
4. Generate e_i with probability:
    P_t(e_i | f_{j - h}, ..., f_{j+h}, e_{i-g}, ..., e_{i + j})
5. If e_i = </s>, stop; otherwise go to 2.
```

### 0. Data Preparation

Input data is Target-Source parallel corpus, word-aligned using GIZA++. You can test this MT pipeline with a sample dataset stored in contrib `directory`.

Before run the training pipeline, first open `sbin/run-env.sh` and change environment variables `WORK_DIR` to make it point to your working directory path.


### 1. Word Alignment

Word alignments are given (generated by GIZA++ or any other tool), but our model requires that every target word has to be aligned with exactly one not null source word. The algorithm of PP rules is explained in [4,3], here is a brief idea:

**Affiliation Heuristic**
* If `t_i` aligns to exactly one source word, `A_i` is the index of the word it aligns to.
* If `t_i` align to multiple source words, `A_i` is the index of the aligned word in the middle (round
down).
* If `t_i` is unaligned, we inherit its affiliation from the closest aligned word, starting with the right.

**Run word aligner**

* Use script `./sbin/run-align.sh`.

Or:

```
cd ./sbin/
source run-env.sh
$PYTHON $ROOT/nnsmt/aligner.py          \
    --source-text $TRAIN_SRC_TEXT       \
    --target-text $TRAIN_TRG_TEXT       \
    --alignment   $TRAIN_ALIGNMENT      \
    --giza-source-vocab $GIZA_SRC_VC    \
    --giza-target-vocab $GIZA_TRG_VC    \
    --heuristic "affiliation-pp"        \
    --verbosity-level 1                 \
    > $WORK_DIR/pp-alignment.txt
```

The result file will contain target sentence, source sentence and new alignment on every line, separated by ` ||| ` . For example:
```
wiederaufnahme der sitzungsperiode ||| resumption of the session ||| 0-0 1-1 1-2 2-3
die aussprache ist geschlossen . ||| the debate is closed . ||| 0-0 1-1 2-2 3-3 4-4
...
```


### 2. Generating data for NPLM

We use [NPLM](http://nlg.isi.edu/software/nplm/) toolkit for trainig NN translation, fertility and distortion models.

In order to use NPLM, first build the toolkit and place NPLM binary files inside `./build/bin/` directory. In should contain the following files:
```
neuralLM.a
neuralLM.so
prepareNeuralLM
prepareNeuralTM
testNeuralLM
testNeuralNetwork
trainNeuralNetwork
```

To generate input data in NPLM format, run the following script:

```
./sbin/run-prepare.sh
```

Or:

```
cd ./sbin/
source run-env.sh
$ROOT/build/bin/prepareNeuralLM                     \
    --numberize 1                                   \
    --train_text $TRAIN_SRC_TEXT                    \
    --ngram_size 1                                  \
    --vocab_size 50000                              \
    --validation_size 0                             \
    --write_words_file $WORK_DIR/source.vocab.txt   \
    --add_start_stop 0                              \
    --train_file /dev/null

$ROOT/build/bin/prepareNeuralLM                     \
    --numberize 1                                   \
    --train_text $TRAIN_TRG_TEXT                    \
    --ngram_size 1                                  \
    --vocab_size 50000                              \
    --validation_size 0                             \
    --write_words_file $WORK_DIR/target.vocab.txt   \
    --add_start_stop 0                              \
    --train_file /dev/null
    
pypy $ROOT/nnsmt/preparenplm.py                                 \
    --input-data $WORK_DIR/pp-alignment.txt                     \
    --target-vector-size 3                                      \
    --source-vector-size 3                                      \
    --source-vocab $WORK_DIR/source.vocab.txt                   \
    --target-vocab $WORK_DIR/target.vocab.txt                   \
    --write-input-vocab-file $WORK_DIR/input.vocab.txt          \
    --write-output-vocab-file $WORK_DIR/output.t.vocab.txt      \
    --write-output-j-vocab-file $WORK_DIR/output.j.vocab.txt    \
    --write-output-f-vocab-file $WORK_DIR/output.f.vocab.txt    \
    --write-t-train-file $WORK_DIR/nplm/t.train.txt             \
    --write-t-valid-file $WORK_DIR/nplm/t.valid.txt             \
    --write-t-train-w-file $WORK_DIR/nplm/t.w.train.txt         \
    --write-t-valid-w-file $WORK_DIR/nplm/t.w.valid.txt         \
    --write-d-train-file $WORK_DIR/nplm/d.train.txt             \
    --write-d-valid-file $WORK_DIR/nplm/d.valid.txt             \
    --write-d-train-w-file $WORK_DIR/nplm/d.w.train.txt         \
    --write-d-valid-w-file $WORK_DIR/nplm/d.w.valid.txt         \
    --write-f-train-file $WORK_DIR/nplm/f.train.txt             \
    --write-f-valid-file $WORK_DIR/nplm/f.valid.txt             \
    --write-f-train-w-file $WORK_DIR/nplm/f.w.train.txt         \
    --write-f-valid-w-file $WORK_DIR/nplm/f.w.valid.txt         \
    --max-jump-size 6                                           \
    --max-fertility 3                                           \
    --valid-data-size 5000
```

Here we use `prepareNeuralLM` application to extract vocabularies of needed size and then use `preparenplm.py` to create train and validation data for NPLM (12 files in total, 2 train and 2 validation files for every model).

* `source.vocab.txt` and `target.vocab.txt` - original target and source vocabularies.
* `input.vocab.txt` and `output.vocab.txt` - NPLM input and output vocabularies. Input is a union of the original target and source files and output is just target vocabulary (plus some special null/start/end/...etc words).
* `write-[t,d,f]-train-file` - train files for translation, distortion and fertlity model. They contain training examples consisting of word IDs. 
* `write-[t,d,f]-train-w-file` - the same as the previous files, but contain words instead of their IDs (for debugging purposes only).

### 3. Train NPLMs

Use NPLM to train models:

```
./sbin/run-train.sh
```

Or:

```
cd ./sbin/
source run-env.sh
# Train T-model
M=t
$ROOT/build/bin/trainNeuralNetwork                      \
    --train_file $WORK_DIR/nplm/$M.train.txt            \
    --validation_file $WORK_DIR/nplm/$M.valid.txt       \
    --num_epochs 32                                     \
    --input_words_file $WORK_DIR/input.vocab.txt        \
    --output_words_file $WORK_DIR/output.$M.vocab.txt   \
    --model_prefix  $WORK_DIR/nplm/$M.model/model       \
    --learning_rate 1                                   \
    --num_hidden 750                                    \
    --input_embedding_dimension 150                     \
    --output_embedding_dimension 150                    \
    --embedding_dimension 150                           \
    --num_threads 4                                     \
    --num_noise_samples 100                             \
    --minibatch_size 1000                               \
    --validation_minibatch_size 1000&


# Train D-model
M=d
$ROOT/build/bin/trainNeuralNetwork                      \
    --train_file $WORK_DIR/nplm/$M.train.txt            \
    --validation_file $WORK_DIR/nplm/$M.valid.txt       \
    --num_epochs 32                                     \
    --input_words_file $WORK_DIR/input.vocab.txt        \
    --output_words_file $WORK_DIR/output.$M.vocab.txt   \
    --model_prefix  $WORK_DIR/nplm/$M.model/model       \
    --learning_rate 1                                   \
    --num_hidden 750                                    \
    --input_embedding_dimension 150                     \
    --output_embedding_dimension 150                    \
    --embedding_dimension 150                           \
    --num_threads 4                                     \
    --num_noise_samples 100                             \
    --minibatch_size 1000                               \
    --validation_minibatch_size 1000&


# Train F-model
M=f
$ROOT/build/bin/trainNeuralNetwork                      \
    --train_file $WORK_DIR/nplm/$M.train.txt            \
    --validation_file $WORK_DIR/nplm/$M.valid.txt       \
    --num_epochs 32                                     \
    --input_words_file $WORK_DIR/input.vocab.txt        \
    --output_words_file $WORK_DIR/output.$M.vocab.txt   \
    --model_prefix  $WORK_DIR/nplm/$M.model/model       \
    --learning_rate 1                                   \
    --num_hidden 750                                    \
    --input_embedding_dimension 150                     \
    --output_embedding_dimension 150                    \
    --embedding_dimension 150                           \
    --num_threads 4                                     \
    --num_noise_samples 100                             \
    --minibatch_size 1000                               \
    --validation_minibatch_size 1000&
```

### 4. Try Decoder

First, compile NPLM Python package (see instructions in NPLM readme file). Place compiled files in `./build/python`:

```
nplm.pxd
nplm.pyx
nplm.so
```

Run Z-decoder:

```
cd ./sbin
source run-env.sh
export PYTHONPATH=$ROOT/build/python:$PYTHONPATH
$PYTHON $ROOT/nnsmt/zdec.py                             \
    --t-model-fl $WORK_DIR/nplm/t.model/model.32        \
    --d-model-fl $WORK_DIR/nplm/d.model/model.32        \
    --f-model-fl $WORK_DIR/nplm/f.model/model.32        \
    --i-vocab-fl $WORK_DIR/input.vocab.txt              \
    --o-t-vocab-fl $WORK_DIR/output.t.vocab.txt         \
    --o-d-vocab-fl $WORK_DIR/output.d.vocab.txt         \
    --o-f-vocab-fl $WORK_DIR/output.f.vocab.txt         \
    --source-vector-size 3                              \
    --target-vector-size 3                              \
    --observed-data $WORK_DIR/pp-alignment.txt          \
    --max-jump 6                                        \
    --max-fert 3                                        \
    --train-file  $WORK_DIR/nplm/t.train.txt            \
    --t-cache-size 100                                  \
    < $TEST_SRC_TEXT

```

### Related Links

1. N. Durrani, A. Fraser, H. Schmid. 2013. [Model With Minimal Translation Units, But DecodeWith Phrases](http://www.cis.uni-muenchen.de/~fraser/pubs/durrani_naacl2013.pdf)
2. H. Zhang, K. Toutanova, C. Quirk, J. Gao. 2013. [Beyond Left-to-Right: Multiple Decomposition Structures for SMT](http://research.microsoft.com/en-us/um/people/jfgao/paper/2013/mtu.pdf)
3. N. Durrani, H. Schmid, A. Fraser. 2011. [A Joint Sequence Translation Model with Integrated Reordering](http://aclweb.org/anthology//P/P11/P11-1105.pdf)
4. J. Devlin, R. Zbib, Z. Huang, T. Lamar, R. Schwartz, J. Makhoul. 2014. Fast and Robust Neural Network Joint Models for Statistical Machine Translation.

