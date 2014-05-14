# /usr/bin/env bash

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