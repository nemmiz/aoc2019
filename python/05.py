#!/usr/bin/python3

import sys

def read_program(s):
    return list(map(int, s.split(',')))

def run_program(program, user_input):
    ip = 0

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
            program[program[ip+1]] = user_input
            ip += 2
        elif opcode == 4:
            a = program[ip+1] if immediate_1 else program[program[ip+1]]
            print(a)
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
    
    return program[0]

with open('../input/05.txt') as f:
    original_program = read_program(f.read())

    program = original_program.copy()
    run_program(program, 1)

    program = original_program.copy()
    run_program(program, 5)
