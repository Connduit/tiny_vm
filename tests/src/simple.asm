.class simple:Obj

.method $constructor
.local i,j
enter
const 14
const 40
call Int:plus
store i
load i
call Int:string
store j
load j
call Int:print
return 0