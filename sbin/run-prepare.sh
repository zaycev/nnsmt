# /usr/bin/env bash

source run-env.sh


$ROOT/build/bin/prepareNeuralLM                     \
    --numberize 1                                   \
    --train_text $TRAIN_SRC_TEXT                    \
    --ngram_size 1                                  \
    --vocab_size 5000                               \
    --validation_size 0                             \
    --write_words_file $WORK_DIR/source.vocab.txt   \
    --add_start_stop 0                              \
    --train_file /dev/null


$ROOT/build/bin/prepareNeuralLM                     \
    --numberize 1                                   \
    --train_text $TRAIN_TRG_TEXT                    \
    --ngram_size 1                                  \
    --vocab_size 5000                               \
    --validation_size 0                             \
    --write_words_file $WORK_DIR/target.vocab.txt   \
    --add_start_stop 0                              \
    --train_file /dev/null

$PYTHON $ROOT/nnsmt/preparenplm.py                          \
    --input-data $WORK_DIR/pp-alignment.txt                 \
    --target-vector-size 2                                  \
    --source-vector-size 3                                  \
    --source-vocab $WORK_DIR/source.vocab.txt               \
    --target-vocab $WORK_DIR/target.vocab.txt               \
    --write-input-vocab-file $WORK_DIR/input.vocab.txt      \
    --write-output-vocab-file $WORK_DIR/output.vocab.txt    \
    --write-train-file $WORK_DIR/nplm.train.txt             \
    --write-valid-file $WORK_DIR/nplm.valid.txt             \
    --write-train-w-file $WORK_DIR/nplm.w.train.txt         \
    --write-valid-w-file $WORK_DIR/nplm.w.valid.txt         \
    --valid-data-size 0

