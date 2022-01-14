# tiny_vm
A tiny virtual machine interpreter for Quack programs

## Work in progress

This is intended to become the core of an interpreter for the Winter 2022
offering of CIS 461/561 compiler construction course at University of Oregon, 
if I can ready it in time. 

## Usage
After building tiny_vm, run parser.py and enter a mathematical expression
that you wish to compute.

    python parser.py

This will build a corresponding .asm file in the unit_tests directory 
called user.asm. In order to run the .asm file on tiny_vm, simply
run the run.sh script.
    
    ./run.sh

## TODOs
- fix tacky implementation of minus and divide in builtins.c
  - the best way to do this is probably how Lack traverses the
    parse tree in parser.py

