#!/usr/bin/python3

from math import gcd, atan2, degrees
from copy import deepcopy


def mark(m, x, y):
    m[y][x] = 'x'


def remove_asteroids(m, points):
    for point in points:
        m[point[1]][point[0]] = '.'


def visible_asteroids(m, ax, ay):
    m = deepcopy(m)
    mark(m, ax, ay)
    for y, line in enumerate(m):
        for x, c in enumerate(line):
            if c == '#':
                ox, oy = x, y
                dx = ox - ax
                dy = oy - ay
                if dx == 0:
                    dy = 1 if dy > 0 else -1
                if dy == 0:
                    dx = 1 if dx > 0 else -1
                if abs(dx) == abs(dy):
                    dx = 1 if dx > 0 else -1
                    dy = 1 if dy > 0 else -1
                tmp = gcd(dx, dy)
                if tmp != 1:
                    dx //= tmp
                    dy //= tmp
                while True:
                    ox += dx
                    oy += dy
                    if ox < 0 or ox >= len(line) or oy < 0 or oy >= len(m):
                        break
                    mark(m, ox, oy)
    
    visible = []
    for y, line in enumerate(m):
        for x, c in enumerate(line):
            if c == '#':
                visible.append((x, y))
    return visible


def find_best_asteroid(m):
    m = deepcopy(m)
    best_result = 0
    best_x = None
    best_y = None
    for y, line in enumerate(m):
        for x, c in enumerate(line):
            if c == '#':
                visible = visible_asteroids(m, x, y)
                if len(visible) > best_result:
                    best_result = len(visible)
                    best_x = x
                    best_y = y
    return best_result, best_x, best_y


def angle(pt1, pt2):
    x = degrees(atan2(pt2[1]-pt1[1], pt2[0]-pt1[0])) + 90
    if x < 0:
        x += 360
    return x


def vaporization_order(m, x, y):
    m = deepcopy(m)
    order = []

    while True:
        visible = visible_asteroids(m, x, y)
        if not visible:
            break

        remove_asteroids(m, visible)

        tmp_list = []
        for i, v in enumerate(visible):
            a = angle((x, y), v)
            tmp_list.append((i, a))
        tmp_list.sort(key=lambda x: x[1])
        for i, a in tmp_list:
            order.append(visible[i])
            
    return order


with open('../input/10.txt') as f:
    parsed_map = [list(line.strip()) for line in f.readlines()]

best_result, best_x, best_y = find_best_asteroid(parsed_map)
order = vaporization_order(parsed_map, best_x, best_y)

print(best_result, 'asteroids are visible at', best_x, best_y)
print(order[199], 'is the 200th asteroid to be vaporized')

