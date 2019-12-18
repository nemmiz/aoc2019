#!/usr/bin/python3

import heapq
from collections import deque


def find_positions(the_map):
    positions = {}
    for y, line in enumerate(the_map):
        for x, c in enumerate(line):
            if c not in '.#':
                positions[c] = (x, y)
    return positions


def split_map(the_map):
    the_map = the_map.copy()

    for y, line in enumerate(the_map):
        x = line.find('@')
        if x != -1:
            break

    the_map[y-1] = the_map[y-1][:x-1] + '@#@' + the_map[y-1][x+2:]
    the_map[y  ] = the_map[y  ][:x-1] + '###' + the_map[y  ][x+2:]
    the_map[y+1] = the_map[y+1][:x-1] + '@#@' + the_map[y+1][x+2:]

    tmp_quadrants = []
    tmp_quadrants.append([line[:x+1] for line in the_map[:y+1]])
    tmp_quadrants.append([line[x:] for line in the_map[:y+1]])
    tmp_quadrants.append([line[:x+1] for line in the_map[y:]])
    tmp_quadrants.append([line[x:] for line in the_map[y:]])

    quadrants = []
    for quadrant in tmp_quadrants:
        positions = find_positions(quadrant)
        keys_in_map = frozenset((x.upper() for x in positions.keys() if x.islower()))
        locks_in_map = frozenset((x for x in positions.keys() if x.isupper()))
        locks_to_remove = locks_in_map - keys_in_map
        
        new_quadrant = []
        for line in quadrant:
            new_line = line
            for lock in locks_to_remove:
                new_line = new_line.replace(lock, '.')
            new_quadrant.append(new_line)
        quadrants.append(new_quadrant)

    return quadrants


def bitmask_from_string(s, offset):
    result = 0
    for c in s:
        result |= 1 << (ord(c) - offset)
    return result


def find_distance_between_keys(the_map):
    positions = {}
    for y, line in enumerate(the_map):
        for x, c in enumerate(line):
            if c not in '.#':
                positions[c] = (x, y)

    locks = {}
    for ent, pos in positions.items():
        if ent.isupper():
            locks[pos] = ent
   
    result = {}
    for ent, pos in positions.items():
        if ent.isupper():
            continue
        open_set = [(0, pos)]
        came_from = {pos: None}
        cost_so_far = {pos: 0}
        while open_set:
            current = heapq.heappop(open_set)[1]
            neighbors = ((current[0], current[1]-1), (current[0], current[1]+1), (current[0]-1, current[1]), (current[0]+1, current[1]))
            for adj in neighbors:
                if the_map[adj[1]][adj[0]] == '#':
                    continue
                new_cost = cost_so_far[current] + 1
                if adj not in cost_so_far or new_cost < cost_so_far[adj]:
                    cost_so_far[adj] = new_cost
                    priority = new_cost
                    heapq.heappush(open_set, (priority, adj))
                    came_from[adj] = current

        for other_ent, other_pos in positions.items():
            if other_ent.isupper() or ent == other_ent:
                continue
            distance = 0
            locks_in_the_way = ''
            if other_pos not in came_from:
                continue
            parent_pos = came_from[other_pos]
            while parent_pos is not None:
                if parent_pos in locks:
                    locks_in_the_way = locks_in_the_way + locks[parent_pos]
                parent_pos = came_from[parent_pos]
                distance += 1
            result[ent+other_ent] = (distance, bitmask_from_string(locks_in_the_way, ord('A')))

    return result


def solve(the_map):
    positions = find_positions(the_map)
    distances = find_distance_between_keys(the_map)

    keys_in_map = [k for k in positions.keys() if k.islower()]
    all_keys_bitmask = bitmask_from_string(keys_in_map, ord('a'))

    q = deque()
    q.append(('@', 0, 0))
    visited = {}
    current_minimum = 9999999999

    while q:
        state = q.popleft()

        tup = (state[0], state[1])
        if tup in visited:
            steps = visited[tup]
            if steps <= state[2]:
                continue

        visited[tup] = state[2]

        if state[1] == all_keys_bitmask:
            current_minimum = min(current_minimum, state[2])
            continue

        for c in keys_in_map:
            if state[0] == c:
                continue
            dist, req = distances[state[0]+c]
            if (state[1] & req) != req:
                continue

            new_owned_keys = state[1] | (1 << (ord(c)-ord('a')))

            q.append((c, new_owned_keys, state[2]+dist))

    return current_minimum


with open('../input/18.txt') as f:
    the_map = [line.strip() for line in f.readlines()]

# Part 1
print(solve(the_map))

# Part 2
print(sum(map(solve, split_map(the_map))))
