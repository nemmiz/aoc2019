#!/usr/bin/python3

import sys
import heapq
from string import ascii_uppercase


def find_portals(maze):
    rows = len(maze)
    cols = len(maze[0])
    all_portals = []

    # Scan the upper and lower outer edges
    for x in range(2, cols-1):
        upper, lower = 1, rows-2
        if maze[upper][x] in ascii_uppercase:
            all_portals.append((maze[upper-1][x]+maze[upper][x], (x, upper), (x, upper+1)))
        if maze[lower][x] in ascii_uppercase:
            all_portals.append((maze[lower][x]+maze[lower+1][x], (x, lower), (x, lower-1)))

    # Scane the left and right outer edges
    for y in range(2, rows-1):
        left, right = 1, cols-2
        if maze[y][left] in ascii_uppercase:
            all_portals.append((maze[y][left-1]+maze[y][left], (left, y), (left+1, y)))
        if maze[y][right] in ascii_uppercase:
            all_portals.append((maze[y][right]+maze[y][right+1], (right, y), (right-1, y)))

    # Find the bounds of the inner hole
    min_x, min_y = cols // 2, rows // 2
    max_x, max_y = min_x, min_y
    while maze[min_y][min_x-1] not in '.#':
        min_x -= 1
    while maze[min_y-1][min_x] not in '.#':
        min_y -= 1
    while maze[max_y][max_x] not in '.#':
        max_x += 1
    while maze[max_y][max_x-1] not in '.#':
        max_y += 1

    # Scan the upper and lower inner edges
    for x in range(min_x+1, max_x-1):
        upper, lower = min_y, max_y-1
        if maze[upper][x] in ascii_uppercase:
            all_portals.append((maze[upper][x]+maze[upper+1][x], (x, upper), (x, upper-1)))
        if maze[lower][x] in ascii_uppercase:
            all_portals.append((maze[lower-1][x]+maze[lower][x], (x, lower), (x, lower+1)))

    # Scane the left and right inner edges
    for y in range(min_y+1, max_y-1):
        left, right = min_x, max_x-1
        if maze[y][left] in ascii_uppercase:
            all_portals.append((maze[y][left]+maze[y][left+1], (left, y), (left-1, y)))
        if maze[y][right] in ascii_uppercase:
            all_portals.append((maze[y][right-1]+maze[y][right], (right, y), (right+1, y)))

    start, goal = None, None
    previous_portals = {}
    portals = {}
    for portal, ent, ext in all_portals:
        if portal == 'AA':
            start = ext
        elif portal == 'ZZ':
            goal = ext
        else:
            if portal not in previous_portals:
                previous_portals[portal] = (ent, ext)
            else:
                portals[ent] = (*previous_portals[portal][1], 1)
                portals[previous_portals[portal][0]] = (*ext, -1)

    return start, goal, portals


def find_path(maze, recurse):
    start, goal, portals = find_portals(maze)

    start = (*start, 0)
    goal = (*goal, 0)
    open_set = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    found_goal = False

    while open_set and not found_goal:
        current = heapq.heappop(open_set)[1]
        neighbors = (
            (current[0], current[1]-1, current[2]),
            (current[0], current[1]+1, current[2]),
            (current[0]-1, current[1], current[2]),
            (current[0]+1, current[1], current[2])
        )
        for neighbor in neighbors:
            position = (neighbor[0], neighbor[1])
            if position in portals:
                portal = portals[position]
                new_depth = neighbor[2] + (portal[2] if recurse else 0)
                if new_depth < 0:
                    continue
                neighbor = (portal[0], portal[1], new_depth)
            if maze[neighbor[1]][neighbor[0]] != '.':
                continue
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current
                if neighbor == goal:
                    found_goal = True
                    break

    steps = 0
    goal = came_from[goal]
    while goal is not None:
        goal = came_from[goal]
        steps += 1

    print(steps)


with open('../input/20.txt') as f:
    the_maze = [line.rstrip('\n') for line in f.readlines()]

find_path(the_maze, recurse=False)
find_path(the_maze, recurse=True)
