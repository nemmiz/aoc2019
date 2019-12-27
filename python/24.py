#!/usr/bin/python3


def part1(state):
    # For each of the 25 tiles, create a bitmask of its neighbors
    masks = []
    for i in range(25):
        y, x = divmod(i, 5)
        mask = 0
        if x > 0:
            mask |= (1 << (i-1))
        if x < 4:
            mask |= (1 << (i+1))
        if y > 0:
            mask |= (1 << (i-5))
        if y < 4:
            mask |= (1 << (i+5))
        masks.append(mask)

    states = set([state])
    while True:
        new_state = 0

        # For each tile, AND the current state with that tile's
        # bitmask and count how many bits were set
        for i in range(25):
            bits = state & masks[i]
            n = bin(bits).count('1')
            if (state & (1 << i)) != 0:
                if n == 1:
                    new_state |= (1 << i)
            else:
                if n == 1 or n == 2:
                    new_state |= (1 << i)

        # Break if the new state has been seen before
        if new_state in states:
            print(new_state)
            break

        states.add(new_state)
        state = new_state


def part2(state):
    masks = []
    inner_masks = []
    outer_masks = []
    top_mask = sum((1 << i for i in range(5)))
    bottom_mask = sum((1 << i for i in range(20, 25)))
    left_mask = sum((1 << i for i in range(0, 25, 5)))
    right_mask = sum((1 << i for i in range(4, 25, 5)))

    # Same idea as for part 1, only with a much more complicated bitmask
    # as well as additional bitmasks for the outer and inner levels
    for i in range(25):
        y, x = divmod(i, 5)
        mask, inner_mask, outer_mask = 0, 0, 0

        if x == 0:
            mask |= (1 << (i+1))
            outer_mask |= (1 << 11)
        elif x == 4:
            mask |= (1 << (i-1))
            outer_mask |= (1 << 13)
        elif y == 2:
            if x == 1:
                mask |= (1 << 10)
                inner_mask |= left_mask
            elif x == 2:
                pass
            elif x == 3:
                mask |= (1 << 14)
                inner_mask |= right_mask
        else:
            mask |= (1 << (i-1))
            mask |= (1 << (i+1))

        if y == 0:
            mask |= (1 << (i+5))
            outer_mask |= (1 << 7)
        elif y == 4:
            mask |= (1 << (i-5))
            outer_mask |= (1 << 17)
        elif x == 2:
            if y == 1:
                mask |= (1 << 2)
                inner_mask |= top_mask
            elif y == 2:
                pass
            elif y == 3:
                mask |= (1 << 22)
                inner_mask |= bottom_mask
        else:
            mask |= (1 << (i-5))
            mask |= (1 << (i+5))
            
        masks.append(mask)
        inner_masks.append(inner_mask)
        outer_masks.append(outer_mask)

    states = {0: state}
    bitcount_cache = {}

    # Run the simulation
    # Cache the bitcounts for a nice speedup
    for _ in range(200):
        new_states = {}
        levels = sorted(states.keys())

        for level in range(min(levels)-1, max(levels)+2):
            state = states.get(level, 0)
            inner_state = states.get(level+1, 0)
            outer_state = states.get(level-1, 0)
            new_state = 0

            for i in range(25):
                # Skip the center tile
                if i == 12:
                    continue

                # Check current level
                bits = state & masks[i]
                count = bitcount_cache.get(bits, None)
                if count is None:
                    count = bin(bits).count('1')
                    bitcount_cache[bits] = count
                n = count

                # Check outer level
                bits = outer_state & outer_masks[i]
                if bits != 0:
                    count = bitcount_cache.get(bits, None)
                    if count is None:
                        count = bin(bits).count('1')
                        bitcount_cache[bits] = count
                    n += count

                # Check inner level
                bits = inner_state & inner_masks[i]
                if bits != 0:
                    count = bitcount_cache.get(bits, None)
                    if count is None:
                        count = bin(bits).count('1')
                        bitcount_cache[bits] = count
                    n += count

                if (state & (1 << i)) != 0:
                    if n == 1:
                        new_state |= (1 << i)
                else:
                    if n == 1 or n == 2:
                        new_state |= (1 << i)

            if new_state != 0:
                new_states[level] = new_state

        states = new_states

    print(sum((bin(state).count('1') for state in states.values())))


with open('../input/24.txt') as f:
    # Represent the 5x5 tile state as a 25-bit number
    state = int(f.read().replace('\n', '').replace('.', '0').replace('#', '1')[::-1], 2)

part1(state)
part2(state)
