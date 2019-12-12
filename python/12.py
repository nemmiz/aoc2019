#!/usr/bin/python3

import sys
import re
from itertools import permutations, chain
from math import gcd
from copy import deepcopy


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def __str__(self):
        return ("pos=<x={: >{width}}, y={: >{width}}, z={: >{width}}>, "
                "vel=<x={: >{width}}, y={: >{width}}, z={: >{width}}>").format(
            self.x, self.y, self.z, self.vx, self.vy, self.vz, width=3)

    def __repr__(self):
        return str(self)

    def apply_gravity(self, other):
        self.vx += sign(other.x - self.x)
        self.vy += sign(other.y - self.y)
        self.vz += sign(other.z - self.z)

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


def read_moons(filename):
    moons = []
    with open(filename) as f:
        for line in f.readlines():
            m = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
            if m:
                moons.append(Moon(int(m.group(1)), int(m.group(2)), int(m.group(3))))
            else:
                sys.exit('failed to read moons')
    return moons


def get_x_state(moons):
    return tuple(chain.from_iterable((moon.x, moon.vx) for moon in moons))


def get_y_state(moons):
    return tuple(chain.from_iterable((moon.y, moon.vy) for moon in moons))


def get_z_state(moons):
    return tuple(chain.from_iterable((moon.z, moon.vz) for moon in moons))


def simulate(moons, num_steps):
    moons = deepcopy(moons)

    for _ in range(num_steps):
        for i, j in permutations(range(len(moons)), 2):
            moons[i].apply_gravity(moons[j])

        for moon in moons:
            moon.apply_velocity()

    print('Sum of total energy:', sum((moon.total_energy() for moon in moons)))


def calculate_state_loop(moons):
    moons = deepcopy(moons)
    x_states = set()
    y_states = set()
    z_states = set()
    steps = 0

    # Calculate how many different states there are for each axis
    while True:
        for a, b in permutations(range(len(moons)), 2):
            moons[a].apply_gravity(moons[b])

        for moon in moons:
            moon.apply_velocity()
    
        if len(x_states) < steps:
            x_states.add(get_x_state(moons))
        if len(y_states) < steps:
            y_states.add(get_y_state(moons))
        if len(z_states) < steps:
            z_states.add(get_z_state(moons))

        if len(x_states) < steps and len(y_states) < steps and len(z_states) < steps:
            break

        steps += 1

    lxs, lys, lzs = len(x_states), len(y_states), len(z_states)
    x, y, z = 0, 0, 0
    steps = 0

    # Calculate the optimal number of steps to take each iteration
    d = gcd(gcd(lxs, lys), lzs)
    tmp = sorted([lxs, lys, lzs])
    step_amount = (tmp[1] // d) * (tmp[2] // d)

    # Step through the states until we reach state 0,0,0 again
    # and keep track of how many steps it took to get there
    while True:
        x = (x + step_amount) % lxs
        y = (y + step_amount) % lys
        z = (z + step_amount) % lzs
        steps += step_amount
        if x == 0 and y == 0 and z == 0:
            break
    
    print('Steps until repetition:', steps)


moons = read_moons('../input/12.txt')
simulate(moons, 1000)
calculate_state_loop(moons)
