#!/usr/bin/python3


def wire_points(wire_def):
    x, y, dx, dy = 0, 0, 0, 0
    points = []
    steps = wire_def.split(',')
    for step in steps:
        direction = step[0]
        amount = int(step[1:])
        if direction == 'U':
            dx, dy = 0, -1
        elif direction == 'D':
            dx, dy = 0, 1
        elif direction == 'L':
            dx, dy = -1, 0
        elif direction == 'R':
            dx, dy = 1, 0
        for _ in range(amount):
            x += dx
            y += dy
            points.append(((x, y), len(points)+1))
    return points


def manhattan_distance(pt):
    return abs(pt[0]) + abs(pt[1])


def find_intersections(wire1, wire2):
    # Create a dict of wire2's points as:
    #    { point: min_steps_to_get_there }
    pts = {}
    for pt, steps in wire2:
        if pt not in pts:
            pts[pt] = steps
        elif pts[pt] > steps:
            pts[pt] = steps

    # Find all point that exist in both wires and record:
    #    * the collision point
    #    * the manhattan distance between the point and origo
    #    * the sum of steps to get there for both wires
    intersections = []
    for pt, steps in wire1:
        if pt in pts:
            intersections.append((pt, manhattan_distance(pt), steps + pts[pt]))

    return intersections


def print_closest_and_first_intersections(wire1, wire2):
    points1 = wire_points(wire1)
    points2 = wire_points(wire2)
    intersections = find_intersections(points1, points2)

    closest = min((intersection[1] for intersection in intersections))
    first = min((intersection[2] for intersection in intersections))
    
    print('Closest intersection:', closest)
    print('First intersection:', first)


with open('../input/03.txt') as f:
    wire1 = f.readline()
    wire2 = f.readline()
    print_closest_and_first_intersections(wire1, wire2)
