#!/usr/bin/python3

def fuel_required(mass):
    return mass // 3 - 2

def fuel_required2(mass):
    req = 0
    while mass > 0:
        mass = fuel_required(mass)
        req += max(0, mass)
    return req

with open('../input/01.txt') as f:
    numbers = [int(line) for line in f.readlines()]

print(sum(map(fuel_required, numbers)))
print(sum(map(fuel_required2, numbers)))
