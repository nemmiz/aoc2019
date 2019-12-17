#!/usr/bin/python3

import sys
import io


NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3


def read_program(s):
    prog = list(map(int, s.split(',')))
    prog.extend([0] * 10000)
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


def make_program(program):
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
            user_input = (yield None)
            program[getindex(program, ip+1, mode1, relative_base)] = user_input
            ip += 2
        elif opcode == 4:
            output = program[getindex(program, ip+1, mode1, relative_base)]
            yield output
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


def read_scaffolding(code, print_map=False):
    prog = make_program(code.copy())
    scaffolding = set()
    stream = io.StringIO()
    x, y, rx, ry, rdir = 0, 0, 0, 0, None

    for output in prog:
        if output == 35:
            print('#', end='', file=stream)
            scaffolding.add((x, y))
            x += 1
        elif output == 46:
            print(' ', end='', file=stream)
            x += 1
        elif output == 10:
            print('', file=stream)
            x, y = 0, y+1
        elif chr(output) in '^v<>':
            print(chr(output), end='', file=stream)
            scaffolding.add((x, y))
            rx, ry = x, y
            rdir = '^v<>'.index(chr(output))
            x += 1

    if print_map:
        print(stream.getvalue())

    return scaffolding, rx, ry, rdir


def subsequences(s, start=0, end=20):
    while True:
        end = s.rfind('|', start, end)
        if end == -1:
            break
        substr = s[start:end]
        remstr = s.replace(substr, '').replace('||', '|').strip('|')
        yield substr, remstr


def partition_program(moves):
    str_a = '|'.join(moves)

    for fun_a, rem_a in subsequences(str_a):
        for fun_b, rem_b in subsequences(rem_a):
            for fun_c, rem_c in subsequences(rem_b):
                if not rem_c:
                    fun_a = fun_a.replace('|', ',')
                    fun_b = fun_b.replace('|', ',')
                    fun_c = fun_c.replace('|', ',')
                    main_routine = ','.join(moves)
                    main_routine = main_routine.replace(fun_a, 'A')
                    main_routine = main_routine.replace(fun_b, 'B')
                    main_routine = main_routine.replace(fun_c, 'C')
                    return main_routine, fun_a, fun_b, fun_c
    else:
        sys.exit('failed to partition program')


def next_input(prog):
    for output in prog:
        if output is None:
            return


def part1(scaffolding):
    result = 0
    for x, y in scaffolding:
        if (x, y-1) in scaffolding and (x, y+1) in scaffolding and (x-1, y) in scaffolding and (x+1, y) in scaffolding:
            result += x * y
    print(result)    


def part2(scaffolding, x, y, direction, code):
    moves = []

    while True:
        # Find direction to travel
        if direction == NORTH:
            if (x-1, y) in scaffolding:
                turn, direction = 'L', WEST
            elif (x+1, y) in scaffolding:
                turn, direction = 'R', EAST
            else:
                break
        elif direction == SOUTH:
            if (x-1, y) in scaffolding:
                turn, direction = 'R', WEST
            elif (x+1, y) in scaffolding:
                turn, direction = 'L', EAST
            else:
                break
        elif direction == WEST:
            if (x, y-1) in scaffolding:
                turn, direction = 'R', NORTH
            elif (x, y+1) in scaffolding:
                turn, direction = 'L', SOUTH
            else:
                break
        elif direction == EAST:
            if (x, y+1) in scaffolding:
                turn, direction = 'R', SOUTH
            elif (x, y-1) in scaffolding:
                turn, direction = 'L', NORTH
            else:
                break

        # Move in this direction
        steps = 0
        if direction == NORTH:
            while (x, y-1) in scaffolding:
                y -= 1
                steps += 1
        elif direction == SOUTH:
            while (x, y+1) in scaffolding:
                y += 1
                steps += 1
        elif direction == WEST:
            while (x-1, y) in scaffolding:
                x -= 1
                steps += 1
        elif direction == EAST:
            while (x+1, y) in scaffolding:
                x += 1
                steps += 1

        moves.append('{},{}'.format(turn, steps))

    main_routine, function_a, function_b, function_c = partition_program(moves)

    code = code.copy()
    code[0] = 2
    prog = make_program(code)

    # Send main routine
    next_input(prog)
    for i in (ord(c) for c in main_routine + '\n'):
        prog.send(i)

    # Send function A
    next_input(prog)
    for i in (ord(c) for c in function_a + '\n'):
        prog.send(i)

    # Send function B
    next_input(prog)
    for i in (ord(c) for c in function_b + '\n'):
        prog.send(i)

    # Send function C
    next_input(prog)
    for i in (ord(c) for c in function_c + '\n'):
        prog.send(i)
        
    next_input(prog)
    prog.send(ord('n'))
    prog.send(10)

    for output in prog:
        if chr(output) not in '#.^v<>\n':
            print(output)    


with open('../input/17.txt') as f:
    code = read_program(f.read())

scaffolding, robot_x, robot_y, robot_dir = read_scaffolding(code)

part1(scaffolding)
part2(scaffolding, robot_x, robot_y, robot_dir, code)
