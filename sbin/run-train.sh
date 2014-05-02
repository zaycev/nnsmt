# /usr/bin/env bash

source run-env.sh

$ROOT/build/bin/trainNeuralNetwork                  \
    --train_file $WORK_DIR/nplm.train.txt           \
    --num_epochs 32                                 \
    --input_words_file $WORK_DIR/input.vocab.txt    \
    --output_words_file $WORK_DIR/output.vocab.txt  \
    --model_prefix  $WORK_DIR/nplm/model            \
    --learning_rate 1                               \
    --num_hidden 750                                \
    --input_embedding_dimension 150                 \
    --output_embedding_dimension 150                \
    --embedding_dimension 150                       \
    --num_threads 4                                 \
    --num_noise_samples 100                         \
    --minibatch_size 1000