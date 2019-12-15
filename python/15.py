#!/usr/bin/python3

import sys
import time

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST,
}

EMPTY_TILE = 0
WALL_TILE = 1
OXYGEN_TILE = 2
START_TILE = 3

print_char = {
    EMPTY_TILE: '.',
    WALL_TILE: '#',
    OXYGEN_TILE: 'O',
    START_TILE: 'S',
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
    tiles[(0,0)] = START_TILE

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

    tiles[(0,0)] = EMPTY_TILE


def next_position(pos, direction):
    if direction == NORTH:
        return (pos[0], pos[1]-1)
    elif direction == SOUTH:
        return (pos[0], pos[1]+1)
    if direction == WEST:
        return (pos[0]-1, pos[1])
    if direction == EAST:
        return (pos[0]+1, pos[1])


def part1(code):
    pos = (0, 0)
    area_map = {pos: EMPTY_TILE}
    prog = make_program(code.copy())
    directions = (NORTH, SOUTH, WEST, EAST)
    history = []
    distances = {}
    oxygen_tile = None

    while True:
        # Update the distance to this position
        distance = distances.get(pos, 99999999999999)
        if len(history) < distance:
            distances[pos] = len(history)

        # Pick the next position to go to
        for direction in directions:
            next_pos = next_position(pos, direction)
            if next_pos not in area_map:
                break
        else:
            if history:
                # At a dead end. Go back the way we came.
                direction = OPPOSITE[history.pop()]
                next(prog)
                result = prog.send(direction)
                pos = next_position(pos, direction)
                assert result == 1
                continue
            else:
                break

        next(prog)
        result = prog.send(direction)

        if result == 0:
            area_map[next_pos] = WALL_TILE
        elif result == 1:
            area_map[next_pos] = EMPTY_TILE
            history.append(direction)
            pos = next_pos
        elif result == 2:
            area_map[next_pos] = OXYGEN_TILE
            history.append(direction)
            oxygen_tile = next_pos
            pos = next_pos
            
    print('Distance to oxygen system:', distances[oxygen_tile])
    return area_map


def part2(area_map):
    area_map = area_map.copy()
    directions = (NORTH, SOUTH, WEST, EAST)

    for pos, tile in area_map.items():
        if tile == OXYGEN_TILE:
            oxygen_tile = pos
            break

    oxygen_tiles = set()
    oxygen_tiles.add(oxygen_tile)
    minutes = 0

    while True:
        next_oxygen_tiles = set()
        for tile in oxygen_tiles:
            for direction in directions:
                next_pos = next_position(tile, direction)
                if area_map[next_pos] == EMPTY_TILE:
                    area_map[next_pos] = OXYGEN_TILE
                    next_oxygen_tiles.add(next_pos)

        if next_oxygen_tiles:
            oxygen_tiles = next_oxygen_tiles
            minutes += 1
        else:
            break

    print('Minutes to fill with oxygen', minutes)


with open('../input/15.txt') as f:
    code = read_program(f.read())

area_map = part1(code)
part2(area_map)