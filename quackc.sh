#!/bin/bash
name=${1##*/}
python ./compiler.py -f $1
python ./assemble.py ./tests/src/"${name%.*}".asm ./tests/OBJ/"${name%.*}".json

