#!/usr/bin/python3

import sys
from collections import deque


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
            #print('expect input')
            user_input = (yield None)
            #print('got', user_input)
            program[getindex(program, ip+1, mode1, relative_base)] = user_input
            ip += 2
        elif opcode == 4:
            output = program[getindex(program, ip+1, mode1, relative_base)]
            #print(output)
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


class Computer:
    def __init__(self, code, address):
        self.prog = make_program(code.copy())
        self.address = address
        self.queue = deque()
        next(self.prog)
        self.ret = self.prog.send(address)

    def run(self):
        if self.ret is None:
            if self.queue:
                _, x, y = self.queue.popleft()
                self.ret = self.prog.send(x)
                self.ret = self.prog.send(y)
            else:
                self.ret = self.prog.send(-1)
            return None
        else:
            dest = self.ret
            x = next(self.prog)
            y = next(self.prog)
            self.ret = next(self.prog)
            return (dest, x, y)

    def recv(self, packet):
        self.queue.append(packet)

    def idle(self):
        return (self.ret == None) and (len(self.queue) == 0)



with open('../input/23.txt') as f:
    code = read_program(f.read())

nat_x, nat_y, nat_prev_y = None, None, None
computers = [Computer(code, i) for i in range(50)]

while True:
    # Simulate computers one by one, handling packets as they come
    for computer in computers:
        packet = computer.run()
        if packet is not None:
            if packet[0] == 255:
                if nat_x is None and nat_y is None:
                    print('Y value of first packet sent to 255:', packet[2])
                nat_x = packet[1]
                nat_y = packet[2]
            else:
                computers[packet[0]].recv(packet)

    # If the network is idle, wake it up again by sending the
    # last recieved NAT message to computer 0
    if all((computer.idle() for computer in computers)):
        if nat_y == nat_prev_y:
            print('First Y to be delivered by the NAT twice:', nat_y)
            break
        computers[0].recv((0, nat_x, nat_y))
        nat_prev_y = nat_y
