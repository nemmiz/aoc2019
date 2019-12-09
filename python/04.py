#!/usr/bin/python3

def check_number(n):
    s = str(n)
    if len(s) != 6:
        return False
    for i in range(1, 6):
        if s[i-1] == s[i]:
            break
    else:
        return False
    digits = [int(c) for c in s]
    for i in range(1, 6):
        if digits[i-1] > digits[i]:
            return False
    return True

def check_number2(n):
    s = str(n)
    if len(s) != 6:
        return False
    found_adjacent = False
    if s[0] == s[1] and s[2] != s[1]:
        found_adjacent = True
    elif s[1] == s[2] and s[1] != s[0] and s[2] != s[3]:
        found_adjacent = True
    elif s[2] == s[3] and s[2] != s[1] and s[3] != s[4]:
        found_adjacent = True
    elif s[3] == s[4] and s[3] != s[2] and s[4] != s[5]:
        found_adjacent = True
    elif s[4] == s[5] and s[4] != s[3]:
        found_adjacent = True
    if not found_adjacent:
        return False
    digits = [int(c) for c in s]
    for i in range(1, 6):
        if digits[i-1] > digits[i]:
            return False
    return True

meets_criteria1 = 0
meets_criteria2 = 0

for i in range(248345, 746315 + 1):
    if check_number(i):
        meets_criteria1 += 1
    if check_number2(i):
        meets_criteria2 += 1

print(meets_criteria1)
print(meets_criteria2)
