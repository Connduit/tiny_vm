#!/bin/bash

python ./assemble.py ./tests/src/$1.asm ./tests/OBJ/$1.json
cd tests/
../bin/tiny_vm $1


