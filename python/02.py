#!/usr/bin/python3

import sys
from itertools import product

def read_program(s):
    return list(map(int, s.split(',')))

def run_program(program):
    pc = 0

    while True:
        if program[pc] == 1:
            program[program[pc+3]] = program[program[pc+1]] + program[program[pc+2]]
        elif program[pc] == 2:
            program[program[pc+3]] = program[program[pc+1]] * program[program[pc+2]]
        elif program[pc] == 99:
            break
        else:
            sys.exit('something went wrong')
        pc += 4
    
    return program[0]

with open('../input/02.txt') as f:
    original_program = read_program(f.read())
    
    program = original_program.copy()
    program[1] = 12
    program[2] = 2
    print(run_program(program))

    for noun, verb in product(range(100), range(100)):
        program = original_program.copy()
        program[1] = noun
        program[2] = verb
        if run_program(program) == 19690720:
            print(100 * noun + verb)
            break
