#!/usr/bin/python3


def pattern(pos):
    repeats = pos + 1
    for _ in range(1, repeats):
        yield 0
    while True:
        for _ in range(repeats):
            yield 1
        for _ in range(repeats):
            yield 0
        for _ in range(repeats):
            yield -1
        for _ in range(repeats):
            yield 0


def fft(numbers):
    result = []

    for i in range(len(numbers)):
        tmp = 0
        for n, p in zip(numbers, pattern(i)):
            if p == 1:
                tmp += n
            elif p == -1:
                tmp -= n
        result.append(abs(tmp) % 10)
    
    return result


def part1(data, iterations):
    numbers = [int(c) for c in data]
    
    for _ in range(iterations):
        numbers = fft(numbers)
        
    print(''.join((str(n) for n in numbers[:8])))


def part2(data, repeats, iterations, offset):
    
    data = data * (repeats // 2)
    offset -= len(data)
    data = data[offset:]
    numbers = [int(c) for c in data]

    for _ in range(iterations):
        for i in range(len(numbers)-2, -1, -1):
            a = numbers[i]
            b = numbers[i+1]
            c = abs(a + b) % 10
            numbers[i] = c

    print(''.join((str(n) for n in numbers[:8])))


with open('../input/16.txt') as f:
    signal = f.read()

part1(signal, 100)
part2(signal, 10000, 100, int(signal[:7]))
