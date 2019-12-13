#!/usr/bin/python3

import sys


EMPTY_TILE = 0
WALL_TILE = 1
BLOCK_TILE = 2
PADDLE_TILE = 3
BALL_TILE = 4

print_char = {
    EMPTY_TILE: ' ',
    WALL_TILE: '#',
    BLOCK_TILE: '*',
    PADDLE_TILE: '-',
    BALL_TILE: 'O',
}


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


def print_tiles(tiles):
    minx, miny = 100000, 100000
    maxx, maxy = -100000, -100000

    for x, y in tiles.keys():
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)

    image = [[' ']*(maxx-minx+1) for _ in range(miny, maxy+1)]

    for pos, tile in tiles.items():
        x = pos[0]-minx
        y = pos[1]-miny
        image[y][x] = print_char[tile]

    for row in image:
        print(''.join(row))


def part1(code):
    tiles = {}
    prog = make_program(code.copy())

    try:
        while True:
            x = next(prog)
            y = next(prog)
            t = next(prog)
            tiles[(x, y)] = t
    except StopIteration:
        pass

    print('Blocks:', list(tiles.values()).count(BLOCK_TILE))


def part2(code):
    code = code.copy()

    # Set free play
    code[0] = 2

    tiles = {}
    prog = make_program(code)

    score = 0
    ball_x = 0
    paddle_x = 0

    try:
        while True:
            tmp = next(prog)

            # Handle input by moving the paddle towards the ball
            while tmp is None:
                if ball_x > paddle_x:
                    tmp = prog.send(1)
                elif ball_x < paddle_x:
                    tmp = prog.send(-1)
                else:
                    tmp = prog.send(0)
            
            x = tmp
            y = next(prog)
            t = next(prog)

            if x == -1 and y == 0:
                score = t
            else:
                if t == BALL_TILE:
                    ball_x = x
                elif t == PADDLE_TILE:
                    paddle_x = x
                tiles[(x, y)] = t

    except StopIteration:
        pass

    print('End score:', score)


with open('../input/13.txt') as f:
    code = read_program(f.read())

part1(code)
part2(code)