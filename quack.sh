#!/bin/bash
name=${1##*/}
./quackc.sh $1

cd tests/
../bin/tiny_vm "${name%.*}"


