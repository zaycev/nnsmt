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
<<<<<<< HEAD
<<<<<<< HEAD
mv $NPLM_ROOT/src/python/nplm.so       $ROOT/build/python/
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
mv $NPLM_ROOT/src/python/nplm.so       $ROOT/build/python/

cd $ROOT/nnsmt
$PYTHON alignmentsetup.py build_ext --inplace
<<<<<<< HEAD
$PYTHON decodingsetup.py build_ext --inplace
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
$PYTHON decodingsetup.py build_ext --inplace
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
