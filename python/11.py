#!/usr/bin/python3

import sys

BLACK = 0
WHITE = 1

TURN_LEFT = 0
TURN_RIGHT = 1

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


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


def calc_direction(current_direction, turn):
    if current_direction == UP:
        return LEFT if turn == TURN_LEFT else RIGHT
    elif current_direction == DOWN:
        return RIGHT if turn == TURN_LEFT else LEFT
    elif current_direction == LEFT:
        return DOWN if turn == TURN_LEFT else UP
    elif current_direction == RIGHT:
        return UP if turn == TURN_LEFT else DOWN


def move_forward(position, direction):
    if direction == UP:
        return (position[0], position[1]-1)
    elif direction == DOWN:
        return (position[0], position[1]+1)
    elif direction == LEFT:
        return (position[0]-1, position[1])
    elif direction == RIGHT:
        return (position[0]+1, position[1])


def paint(panels, code):
    prog = make_program(code.copy())
    position = (0,0)
    direction = UP
    next(prog)

    try:
        while True:
            old_color = panels.get(position, BLACK)
            new_color = prog.send(old_color)
            turn = next(prog)
            next(prog)

            panels[position] = new_color

            direction = calc_direction(direction, turn)
            position = move_forward(position, direction)
    except StopIteration:
        pass

    return panels


def print_panels(panels):
    minx, miny = 100000, 100000
    maxx, maxy = -100000, -100000

    for x, y in panels.keys():
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)

    image = [[' ']*(maxx-minx+1) for _ in range(miny, maxy+1)]

    for pos, color in panels.items():
        x = pos[0]-minx
        y = pos[1]-miny
        image[y][x] = ' ' if color == BLACK else '#' 

    for row in image:
        print(''.join(row))


with open('../input/11.txt') as f:
    code = read_program(f.read())

panels = paint({(0,0): BLACK}, code)
print(len(panels))

panels = paint({(0,0): WHITE}, code)
print_panels(panels)
