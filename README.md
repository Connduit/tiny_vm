# tiny_vm
A tiny virtual machine interpreter for Quack programs

## Usage
After building tiny_vm, run quack.sh or quackc.sh on any file written in quack. 


quack.sh: compiles, builds, and runs the provided .qk file on tiny_vm

    ./quack.sh simple.qk

quackc.sh: compiles and builds the provided .qk file

    ./quackc.sh simple.qk

The .asm and .json files produced are stored in tests/src and tests/OBJ 
respectively. 

Example .qk files can be found in the qktests directory.

## What Works
- if/while loops
- type checking
- var checking
- conditionals
- integer and string arithmetic
- ast tree

## What Doesn't Work
- type checking for user defined classes
- var checking for user defined classes
- class fields 
