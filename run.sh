#!/bin/bash

python ./assemble.py ./unit_tests/user.asm ./cmake-build-debug-wsl/sample.json
cd cmake-build-debug-wsl/
./tiny_vm


