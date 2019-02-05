import pandas as pd

d = open('input5.csv', 'r').readlines()
data = [s.rstrip() for s in d]

polymer = list(data[0])


def check(a, b):
    # Check units
    if a.upper() == b.upper() and a != b:
        return True
    else:
        return False


def reaction(polymer):
    s = polymer
    reacted = False
    while reacted == False:
        for i in range(len(s) - 1):
            react = check(s[i], s[i + 1])
            if react == True:
                s.pop(i)
                s.pop(i)
                break
            elif i == len(s) - 2:
                reacted = True
    return s


#reacted = reaction(polymer)

# Part 2

s = [i.upper() for i in polymer]
s = list(set(s))

results = {}
for unit in s:
    new_poly = [u for u in polymer if u not in [unit, unit.lower()]]
    reacted = reaction(new_poly)
    print('{}: {}'.format(unit, len(reacted)))
    results[unit] = len(reacted)
