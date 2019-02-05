import pandas as pd
import math
import copy
from matplotlib import pyplot as plt
from matplotlib import animation

d = open('input10.csv', 'r').readlines()
instructions = [s.rstrip() for s in d]


def construct_df(instructions):
    rows = []
    for instruction in instructions:
        split_up = [d.split('<') for d in instruction.split('>')]
        x = int(split_up[0][1].split(', ')[0].strip())
        y = int(split_up[0][1].split(', ')[1].strip())
        x_delta = int(split_up[1][1].split(', ')[0].strip())
        y_delta = int(split_up[1][1].split(', ')[1].strip())
        rows.append([x, y, x_delta, y_delta])
    return rows


def calc_distance(rows):
    total_distance = 0
    for i in range(len(rows)):
        this_x = rows[i][0]
        this_y = rows[i][1]
        other_x = [r[0] for idx, r in enumerate(rows) if idx != i] 
        other_y = [r[1] for idx, r in enumerate(rows) if idx != i]
        for j in range(len(other_x)):
            distance = math.sqrt((this_x - other_x[j]) ** 2 +
                                 (this_y - other_y[j]) ** 2)
            total_distance += distance
    return total_distance


def test(rows, iterations):
    new_rows = copy.deepcopy(rows)
    for row in new_rows:
        row[0] += iterations * row[2]
        row[1] += iterations * row[3]
    d = calc_distance(new_rows)
    return new_rows, d
    

def dist_x_time(rows, start, end):
    distance_over_time = []
    for i in range(end-start):
        new_rows = copy.deepcopy(rows)
        for row in new_rows:
            row[0] += ((start + i) * row[2])
            row[1] += ((start + i) * row[3])
        dist = calc_distance(new_rows)
        distance_over_time.append([i, dist])

    df_d = pd.DataFrame(distance_over_time, columns=['i', 'distance'])
    return df_d


rows = construct_df(instructions)

# Perform some initial evaluation
rows_10k, d1 = test(rows, 10000)
rows_105k, d2 = test(rows, 10500)
rows_11k, d3 = test(rows, 11000)
rows_115k, d4 = test(rows, 11500)
rows_12k, d5 = test(rows, 12000)

print(d1, '-->', d2, '-->', d3, '-->', d4, '-->', d5)

# Now we've narrowed down, iterate and calc distances
start = 10600
end = 11400
df_d = dist_x_time(rows, start, end)
min_d = min(df_d['distance'])
min_idx = df_d.loc[df_d['distance'] == min_d].index

#fig, ax = plt.subplots()
#for i in range(10850, 10900):
#    to_vis, d = test(rows, i)
#    df = pd.DataFrame(to_vis, columns=['x', 'y', 'x_delta', 'y_delta'])
#    plt.axis([min(df['x']), max(df['x']), min(df['y']), max(df['y'])])
#    plt.clf()
#    plt.scatter(df['x'], df['y'])
#    plt.pause(0.5)

fig, ax = plt.subplots()
to_vis, d = test(rows, 10880)
df = pd.DataFrame(to_vis, columns=['x', 'y', 'x_delta', 'y_delta'])
plt.axis([min(df['x']), max(df['x']), max(df['y']), min(df['y'])])
plt.clf()
plt.scatter(df['x'], df['y'])

plt.show()
#ax = plt.axes(xlim=(-55000,), ylim=())