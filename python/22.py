#!/usr/bin/python3

import sys
import re
from enum import Enum


class Command(Enum):
    DEAL_WITH = 0
    REVERSE = 1
    CUT = 2


def deal_into_new_stack(cards):
    return list(reversed(cards))


def cut_n_cards(cards, n):
    return cards[n:] + cards[:n]


def deal_with_increment_n(cards, n):
    new_cards = [0] * len(cards)
    for i, card in enumerate(cards):
        new_cards[(i*n)%len(cards)] = card
    return new_cards


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def parse_commands(lines):
    commands = []
    for line in lines:
        m = re.match(r'^deal with increment (\d+)', line)
        if m:
            commands.append((Command.DEAL_WITH, int(m.group(1))))
            continue
        m = re.match(r'^deal into new stack', line)
        if m:
            commands.append((Command.REVERSE, None))
            continue
        m = re.match(r'^cut (-?\d+)', line)
        if m:
            commands.append((Command.CUT, int(m.group(1))))
            continue
        print('no match for', line.strip())
    return commands


def simplify_commands(commands, deck_size):
    while True:
        new_commands = []
        i, n = 0, len(commands)

        while i < n:
            if i == n-1:
                new_commands.append(commands[-1])
                break

            cmd1, arg1 = commands[i]
            cmd2, arg2 = commands[i+1]

            if cmd1 == Command.REVERSE and cmd2 == Command.REVERSE:
                i += 2
            elif cmd1 == Command.CUT and cmd2 == Command.CUT:
                new_commands.append((Command.CUT, (arg1+arg2)%deck_size))
                i += 2
            elif cmd1 == Command.DEAL_WITH and cmd2 == Command.DEAL_WITH:
                new_commands.append((Command.DEAL_WITH, (arg1*arg2)%deck_size))
                i += 2
            elif cmd1 == Command.CUT and cmd2 == Command.DEAL_WITH:
                new_commands.append((cmd2, arg2))
                new_commands.append((Command.CUT, (arg1*arg2)%deck_size))
                i += 2
            elif cmd1 == Command.REVERSE and cmd2 == Command.CUT:
                new_commands.append((Command.CUT, -arg2))
                new_commands.append((Command.REVERSE, None))
                i += 2
            elif cmd1 == Command.REVERSE and cmd2 == Command.DEAL_WITH:
                new_commands.append((Command.DEAL_WITH, arg2))
                new_commands.append((Command.CUT, -arg2+1))
                new_commands.append((Command.REVERSE, None))
                i += 2
            else:
                new_commands.append((cmd1, arg1))
                i += 1

        if commands == new_commands:
            break

        commands = new_commands

    return commands

def get_simplified_commands(commands, deck_size, iterations):
    power = 1
    commands_per_power = {}
    while power <= iterations:
        commands = simplify_commands(commands, deck_size)
        commands_per_power[power] = commands
        power <<= 1
        commands = commands * 2
    
    remaining = iterations
    combined_commands = []
    for power in sorted(commands_per_power.keys(), reverse=True):
        if remaining >= power:
            remaining -= power
            combined_commands += commands_per_power[power]

    return simplify_commands(combined_commands, deck_size)


def part1(commands):
    deck = list(range(10007))
    for cmd, arg in commands:
        if cmd == Command.DEAL_WITH:
            deck = deal_with_increment_n(deck, arg)
        elif cmd == Command.REVERSE:
            deck = deal_into_new_stack(deck)
        elif cmd == Command.CUT:
            deck = cut_n_cards(deck, arg)
    print(deck.index(2019))


def part2(commands):
    deck_size = 119315717514047
    iterations = 101741582076661
    pos = 2020
    commands = get_simplified_commands(commands, deck_size, iterations)
    for i in range(1):
        for cmd, arg in reversed(commands):
            if cmd == Command.DEAL_WITH:
                pos = (pos * modinv(arg, deck_size)) % deck_size
            elif cmd == Command.REVERSE:
                pos = deck_size - 1 - pos
            elif cmd == Command.CUT:
                pos = (pos + arg) % deck_size
    print(pos)


with open('../input/22.txt') as f:
    commands = parse_commands(f.readlines())

part1(commands)
part2(commands)
