.class sample:Obj

.method $constructor
.local i,j,cat,other
enter
const 42
const 13
roll 1
call Int:plus
store i
load i
const 32
roll 1
call Int:minus
store j
load j
call Int:print
const "\n"
call String:print
const "Nora"
store cat
const " can solve puzzles"
store other
load cat
load other
roll 1
call String:plus
call String:print
const "\n"
call String:print
return 0