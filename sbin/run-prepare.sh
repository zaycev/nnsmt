# /usr/bin/env bash

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

