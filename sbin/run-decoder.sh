# /usr/bin/env bash

source run-env.sh

export PYTHONPATH=$ROOT/build/python:$PYTHONPATH

# $PYTHON $ROOT/nnsmt/vocabtest.py                    \
#     --i-vocab-fl $WORK_DIR/input.vocab.txt          \
#     --o-vocab-fl $WORK_DIR/output.vocab.txt         \
#     --new-i-vocab-fl $WORK_DIR/new.input.vocab.txt  \
#     --new-o-vocab-fl $WORK_DIR/new.output.vocab.txt \
#     --train-file $WORK_DIR/nplm.train.txt           \
#     --train-w-file $WORK_DIR/nplm.w.train.txt       \
#     --source-vector-size 3                          \
#     --target-vector-size 3

$PYTHON $ROOT/nnsmt/zdec.py                     \
    --t-model-fl $WORK_DIR/nplm.t/model.32      \
    --d-model-fl $WORK_DIR/nplm.d/model.32      \
    --i-vocab-fl $WORK_DIR/new.input.vocab.txt      \
    --o-vocab-fl $WORK_DIR/new.output.vocab.txt     \
    --source-vector-size 3                      \
    --target-vector-size 3                      \
    --observed-data $WORK_DIR/nplm.train.txt    \
    < $TRAIN_SRC_TEXT
