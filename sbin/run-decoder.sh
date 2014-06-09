# /usr/bin/env bash

source run-env.sh

export PYTHONPATH=$ROOT/build/python:$PYTHONPATH

<<<<<<< HEAD
$PYTHON $ROOT/nnsmt/vocabtest.py                    \
    --i-vocab-fl $WORK_DIR/input.vocab.txt          \
    --o-vocab-fl $WORK_DIR/output.vocab.txt         \
    --new-i-vocab-fl $WORK_DIR/new.input.vocab.txt  \
    --new-o-vocab-fl $WORK_DIR/new.output.vocab.txt \
    --train-file $WORK_DIR/nplm.train.txt           \
    --train-w-file $WORK_DIR/nplm.w.train.txt       \
    --source-vector-size 3                          \
    --target-vector-size 3

MODEL=$ROOT/models/3t.3s.6j.3f.europarl.50ks.50kw


$PYTHON $ROOT/nnsmt/zdec.py                     \
    --t-model-fl $MODEL/t.nplm                  \
    --d-model-fl $MODEL/d.nplm                  \
    --f-model-fl $MODEL/f.nplm                  \
    --i-vocab-fl $MODEL/input.vocab.txt         \
    --o-t-vocab-fl $MODEL/output.t.vocab.txt    \
    --o-d-vocab-fl $MODEL/output.d.vocab.txt    \
    --o-f-vocab-fl $MODEL/output.f.vocab.txt    \
    --source-vector-size 3                      \
    --target-vector-size 3                      \
    --observed-data $MODEL/observed.txt         \
    --max-jump 3                                \
    --max-fert 3                                \
    --train-file  $MODEL/t.train.txt            \
    --t-cache-size 16                           \
    < $TEST_SRC_TEXT > /dev/stdout
=======
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
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
