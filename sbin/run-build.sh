# /usr/bin/env bash

source run-env.sh

mkdir -p $ROOT/build/bin/
mkdir -p $ROOT/build/python/

cd $NPLM_ROOT/src

make
make python/nplm.so

mv $NPLM_ROOT/src/neuralLM.so          $ROOT/build/bin/
mv $NPLM_ROOT/src/neuralLM.a           $ROOT/build/bin/
mv $NPLM_ROOT/src/prepareNeuralLM      $ROOT/build/bin/
mv $NPLM_ROOT/src/prepareNeuralTM      $ROOT/build/bin/
mv $NPLM_ROOT/src/testNeuralLM         $ROOT/build/bin/
mv $NPLM_ROOT/src/testNeuralNetwork    $ROOT/build/bin/
mv $NPLM_ROOT/src/trainNeuralNetwork   $ROOT/build/bin/

mv $NPLM_ROOT/src/python/nplm.pxd      $ROOT/build/python/
mv $NPLM_ROOT/src/python/nplm.pyx      $ROOT/build/python/
mv $NPLM_ROOT/src/python/nplm.so       $ROOT/build/python/
