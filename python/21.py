#!/usr/bin/python3

def read_program(s):
    prog = list(map(int, s.split(',')))
    prog.extend([0] * 10000)
    return prog


def getindex(program, ip, mode, relative_base):
    index = 0
    if mode == 0:
        index = program[ip]
    elif mode == 1:
        index = ip
    elif mode == 2:
        index = program[ip] + relative_base
    return index


def make_program(program):
    ip = 0
    relative_base = 0

    while True:
        mode1 = 0
        mode2 = 0
        mode3 = 0
        tmp = program[ip]
        while tmp >= 10000:
            mode3 += 1
            tmp -= 10000
        while tmp >= 1000:
            mode2 += 1
            tmp -= 1000
        while tmp >= 100:
            mode1 += 1
            tmp -= 100
        opcode = tmp

        if opcode == 1:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = a + b
            ip += 4
        elif opcode == 2:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = a * b
            ip += 4
        elif opcode == 3:
            user_input = (yield None)
            program[getindex(program, ip+1, mode1, relative_base)] = user_input
            ip += 2
        elif opcode == 4:
            output = program[getindex(program, ip+1, mode1, relative_base)]
            yield output
            ip += 2
        elif opcode == 5:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            if a != 0:
                b = program[getindex(program, ip+2, mode2, relative_base)]
                ip = b
            else:
                ip += 3
        elif opcode == 6:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            if a == 0:
                b = program[getindex(program, ip+2, mode2, relative_base)]
                ip = b
            else:
                ip += 3
        elif opcode == 7:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = 1 if a < b else 0
            ip += 4
        elif opcode == 8:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            b = program[getindex(program, ip+2, mode2, relative_base)]
            program[getindex(program, ip+3, mode3, relative_base)] = 1 if a == b else 0
            ip += 4
        elif opcode == 9:
            a = program[getindex(program, ip+1, mode1, relative_base)]
            relative_base += a
            ip += 2
        elif opcode == 99:
            break
        else:
            sys.exit('something went wrong')


def run_script(code, script):
    prog = make_program(code.copy())

    # Skip the prompt
    out = next(prog)
    while out is not None:
        out = next(prog)

    # Enter the program
    for c in script:
        prog.send(ord(c))

    # Run the script and print the result (>127) if the droid makes it.
    # If the droid doesn't make it. Print the ascii rendering of its demise.
    for x in prog:
        if x > 127:
            print(x)
        else:
            print(chr(x), end='')


# Script for part 1
# Jump if the landing point is ground and there
# are holes between the droid and the landing point
script_a = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

# Script for part 2
# Same as part 1 with the addition that the ground 1 or 4
# steps past the landing point must also be ground
script_b = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
AND E T
OR H T
AND T J
RUN
"""

with open('../input/21.txt') as f:
    code = read_program(f.read())

run_script(code, script_a)
run_script(code, script_b)


