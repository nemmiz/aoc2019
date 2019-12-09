#!/usr/bin/python3

with open('../input/06.txt') as f:
    lines = f.readlines()

orbits = {}
for line in lines:
    a, b = line.strip().split(')')
    orbits[b] = a

total = 0

for obj in orbits:
    n = 1
    parent = orbits[obj]
    while parent in orbits:
        parent = orbits[parent]
        n += 1
    total += n

print(total)

santa_orbits = {}
parent = orbits['SAN']
while parent in orbits:
    santa_orbits[parent] = len(santa_orbits)
    parent = orbits[parent]

parent = orbits['YOU']
jumps = 0
while parent in orbits:
    if parent in santa_orbits:
        print(jumps + santa_orbits[parent])
        break
    parent = orbits[parent]
    jumps += 1
