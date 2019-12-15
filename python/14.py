#!/usr/bin/python3

import sys
import re


def produce(chemical, amount, spares, requirements, produced):
    if chemical == 'ORE':
        return amount

    amount_in_spares = spares.get(chemical, 0)
    amount_to_take = min(amount_in_spares, amount)
    spares[chemical] = amount_in_spares - amount_to_take
    amount -= amount_to_take

    ore_required = 0

    if amount > 0:
        produced_per_reaction = produced[chemical]
        amount_produced = (amount // produced_per_reaction) * produced_per_reaction

        if amount_produced < amount:
            amount_produced += produced_per_reaction

        multiplier = amount_produced // produced_per_reaction
        
        for req_name, req_amount in requirements[chemical].items():
            ore_required += produce(req_name, req_amount * multiplier, spares, requirements, produced)

        if amount_produced > amount:
            spares[chemical] = spares.get(chemical, 0) + (amount_produced - amount)

    return ore_required


def part1(requirements, produced):
    print(produce('FUEL', 1, {}, requirements, produced))


def part2(requirements, produced):
    n = 1000000000000

    a = 1
    b = n
    req_a = produce('FUEL', a, {}, requirements, produced)
    req_b = produce('FUEL', b, {}, requirements, produced)

    while True:
        m = (a + b) // 2
        req_m = produce('FUEL', m, {}, requirements, produced)

        if req_m <= n:
            a = m
            req_a = req_m
        elif req_m > n:
            b = m
            req_b = req_m

        if (a + 1) == b:
            break

    print(a)


with open('../input/14.txt') as f:
    requirements = {}
    produced = {}
    for line in f.readlines():
        tokens = line.split()
        name = tokens[-1]
        requirements[name] = {tokens[i+1].rstrip(','): int(tokens[i]) for i in range(0, len(tokens)-3, 2)}
        produced[name] = int(tokens[-2])
        
part1(requirements, produced)
part2(requirements, produced)