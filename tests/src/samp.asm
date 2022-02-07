.class samp:Obj

.method $constructor
.local i,j,s,t
enter
const 14
const 40
call Int:plus
store i
load i
const 9
roll 1
call Int:divide
store j
load j
call Int:print
load j
call Int:string
store s
load s
const "is cool\n"
call Int:plus
store t
load t
call Int:print
return 0