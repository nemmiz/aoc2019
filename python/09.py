#!/usr/bin/python3

import sys
from itertools import permutations

def read_program(s):
    prog = list(map(int, s.split(',')))
    prog.extend([0] * 1000)
    return prog

def getindex(program, ip, mode, relative_base):
    index = 0
    if mode == 0:
        index = program[ip]
    elif mode == 1:
        index = ip
    elif mode == 2:
        index = program[ip] + relative_base
    return index

def run_program(program, user_input):
    ip = 0
    relative_base = 0

    while True:
        mode1 = 0
        mode2 = 0
        mode3 = 0
        tmp = program[ip]
        while tmp >= 10000:
            mode3 += 1
            tmp -= 10000
        while tmp >= 1000:
            mode2 += 1
            tmp -= 1000
        while tmp >= 100:
            mode1 += 1
            tmp -= 100
        opcode = tmp

        if opcode == 1:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = a + b
            ip += 4
        elif opcode == 2:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = a * b
            ip += 4
        elif opcode == 3:
            program[getindex(program, ip+1, mode1, relative_base)] = user_input
            ip += 2
        elif opcode == 4:
            output = program[getindex(program, ip+1, mode1, relative_base)]
            print(output)
            ip += 2
        elif opcode == 5:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            if a != 0:
                b = program[getindex(program, ip+2, mode2, relative_base)]
                ip = b
            else:
                ip += 3
        elif opcode == 6:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            if a == 0:
                b = program[getindex(program, ip+2, mode2, relative_base)]
                ip = b
            else:
                ip += 3
        elif opcode == 7:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = 1 if a < b else 0
            ip += 4
        elif opcode == 8:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = 1 if a == b else 0
            ip += 4
        elif opcode == 9:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            relative_base += a
            ip += 2
        elif opcode == 99:
            break
        else:
            sys.exit('something went wrong')

with open('../input/09.txt') as f:
    original_program = read_program(f.read())

run_program(original_program.copy(), 1)
run_program(original_program.copy(), 2)

