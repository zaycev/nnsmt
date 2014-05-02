# /usr/bin/env bash

PYTHON=python
THIS=`pwd`
ROOT=$THIS/..
NPLM_ROOT=$ROOT/nplm
DATA_ROOT=$ROOT/contrib

# Training data
TRAIN_SRC_TEXT=$DATA_ROOT/train.de.txt
TRAIN_TRG_TEXT=$DATA_ROOT/train.en.txt
TRAIN_ALIGNMENT=$DATA_ROOT/train.de-en.a3.txt

# Development data
DEV_SRC_TEXT=$DATA_ROOT/dev.de.txt
DEV_TRG_TEXT=$DATA_ROOT/dev.en.txt

# Tests data
TEST_SRC_TEXT=$DATA_ROOT/test.de.txt
TEST_TRG_TEXT=$DATA_ROOT/test.en.txt

# Workdir
WORK_DIR=/Users/zvm/dev/dr-data/workdir