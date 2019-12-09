#!/usr/bin/python3

import sys
from itertools import permutations

def read_program(s):
    return list(map(int, s.split(',')))

def run_program(program, phase_setting, user_input):
    ip = 0
    has_read_phase_setting = False
    #output = None

    while True:
        immediate_1 = False
        immediate_2 = False
        immediate_3 = False
        tmp = program[ip]
        if tmp >= 10000:
            immediate_3 = True
            tmp -= 10000
        if tmp >= 1000:
            immediate_2 = True
            tmp -= 1000
        if tmp >= 100:
            immediate_1 = True
            tmp -= 100
        opcode = tmp

        if opcode == 1:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            b = program[ip+2] if immediate_2 else program[program[ip+2]]
            program[program[ip+3]] = a + b
            ip += 4
        elif opcode == 2:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            b = program[ip+2] if immediate_2 else program[program[ip+2]]
            program[program[ip+3]] = a * b
            ip += 4
        elif opcode == 3:
            program[program[ip+1]] = user_input if has_read_phase_setting else phase_setting
            has_read_phase_setting = True
            ip += 2
        elif opcode == 4:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            user_input = (yield a)
            #output = a
            ip += 2
        elif opcode == 5:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            if a != 0:
                b = program[ip+2] if immediate_2 else program[program[ip+2]]
                ip = b
            else:
                ip += 3
        elif opcode == 6:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            if a == 0:
                b = program[ip+2] if immediate_2 else program[program[ip+2]]
                ip = b
            else:
                ip += 3
        elif opcode == 7:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            b = program[ip+2] if immediate_2 else program[program[ip+2]]
            program[program[ip+3]] = 1 if a < b else 0
            ip += 4
        elif opcode == 8:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            b = program[ip+2] if immediate_2 else program[program[ip+2]]
            program[program[ip+3]] = 1 if a == b else 0
            ip += 4
        elif opcode == 99:
            break
        else:
            sys.exit('something went wrong')
    
    #return output

#original_program = read_program('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')

#original_program = read_program('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')

#original_program = read_program('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')

with open('../input/07.txt') as f:
    original_program = read_program(f.read())

# program = original_program.copy()

# #for 
# run_program(program, 4, 0)

# run_program(program, 3, 4)

# run_program(program, 2, 43)

# run_program(program, 1, 432)

# run_program(program, 0, 4321)

best_result = 0

for p in permutations([0, 1, 2, 3, 4]):
    result = next(run_program(original_program.copy(), p[0], 0))
    result = next(run_program(original_program.copy(), p[1], result))
    result = next(run_program(original_program.copy(), p[2], result))
    result = next(run_program(original_program.copy(), p[3], result))
    result = next(run_program(original_program.copy(), p[4], result))
    best_result = max(result, best_result)
    
print(best_result)


for p in permutations([5, 6, 7, 8, 9]):
    amp_a = run_program(original_program.copy(), p[0], 0)
    amp_b = run_program(original_program.copy(), p[1], next(amp_a))
    amp_c = run_program(original_program.copy(), p[2], next(amp_b))
    amp_d = run_program(original_program.copy(), p[3], next(amp_c))
    amp_e = run_program(original_program.copy(), p[4], next(amp_d))

    while result in amp_e:
        

    
    #result = next(run_program(original_program.copy(), p[4], result))
    #best_result = max(result, best_result)

#def mygen():
#    yield 1
#    yield 2
#    yield 3

#g = mygen()

#for x in g:
#    print(x)

# run_program(program, 3, 4)

# run_program(program, 2, 43)

# run_program(program, 1, 432)

# run_program(program, 0, 4321)

# with open('../input/05.txt') as f:
#     original_program = read_program(f.read())

#     program = original_program.copy()
#     run_program(program, 1)

#     program = original_program.copy()
#     run_program(program, 5)
