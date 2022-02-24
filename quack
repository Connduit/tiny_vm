#!/bin/bash
name=$1
python ./astbuilder.py -f $1
python ./assemble.py ./tests/src/"${name%%.*}.asm" ./tests/OBJ/"${name%%.*}.json"


cd tests/
../bin/tiny_vm ${name%%.*}


