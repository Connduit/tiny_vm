.class Sample:Obj

.method $constructor
	enter
	const 4
	const 4
	const 4
	call Int:times
	call Int:minus
	call Int:print
	pop
	const "\n"
	call String:print
	return 0
