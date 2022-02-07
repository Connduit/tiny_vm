.class bigtest:Obj

.method $constructor
.local a,c,b,d
enter
const 3
const 5
const 4
call Int:times
call Int:plus
store a
load a
call Int:print
const "\n"
call String:print
const true
store c
load c
call Bool:print
const "\n"
call String:print
const none
store b
load b
call Nothing:print
const "\n"
store d
load d
call String:print
const "hello world\n"
call String:print
return 0