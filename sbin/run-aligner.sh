# /usr/bin/env bash

source run-env.sh

$PYTHON $ROOT/nnsmt/aligner.py     \
    --source-text $TRAIN_SRC_TEXT  \
    --target-text $TRAIN_TRG_TEXT  \
    --alignment   $TRAIN_ALIGNMENT \
    --verbosity-level 1            \
    > $WORK_DIR/pp-alignment.txt