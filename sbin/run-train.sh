# /usr/bin/env bash

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

sleep 100h
