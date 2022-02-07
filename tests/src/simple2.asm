.class simple2:Obj

.method $constructor
.local i,j
enter
const 5
call Int:negate
store i
const 8
store j
const "\n"
call String:print
load i
load j
call Int:plus
call Int:print
const "\n"
call String:print
return 0