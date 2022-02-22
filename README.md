# tiny_vm
A tiny virtual machine interpreter for Quack programs

## Usage
After building tiny_vm, run parser.py on any file written in quack.

    python astbuilder.py -f simple.qk

This will build a corresponding .asm file in the unit_tests directory 
called user.asm. In order to run the .asm file on tiny_vm, simply
run the run.sh script with the .qk file's name as an argument.
    
    ./run.sh simple

## TODOs
- finish implementing conditionals and a more elaborate type/var checker
- create helper functions to generate if_block code so that i can reuse for code

