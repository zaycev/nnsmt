# /usr/bin/env bash

source run-env.sh

<<<<<<< HEAD
$PYTHON $ROOT/nnsmt/aligner.py          \
    --source-text $TRAIN_SRC_TEXT       \
    --target-text $TRAIN_TRG_TEXT       \
    --alignment   $TRAIN_ALIGNMENT      \
    --giza-source-vocab $GIZA_SRC_VC    \
    --giza-target-vocab $GIZA_TRG_VC    \
    --heuristic "affiliation-pp"        \
    --verbosity-level 1                 \
=======
$PYTHON $ROOT/nnsmt/aligner.py     \
    --source-text $TRAIN_SRC_TEXT  \
    --target-text $TRAIN_TRG_TEXT  \
    --alignment   $TRAIN_ALIGNMENT \
    --verbosity-level 1            \
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
    > $WORK_DIR/pp-alignment.txt