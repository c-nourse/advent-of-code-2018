import pandas as pd
import matplotlib.pyplot as plt

d = open('input6.csv', 'r').readlines()
coords = [[int(el) for el in s.rstrip().split(', ')] for s in d]
df_c = pd.DataFrame(coords, columns=['x', 'y'])

def taxicab(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Max vals for x and y are 355 and 359 so let's use a 400x400 canvas
def construct_canvas(width, height, coords):
    dfs = []

    # Perform distance calculations for every point on canvas
    for i in range(width):
        for j in range(height):
            distances = []
            for k, coord in enumerate(coords):
                a = [i, j]
                b = coord
                dist = taxicab(a, b)
                distances.append([i, j, k, dist])
            df = pd.DataFrame(distances, columns=['x', 'y', 'label', 'dist'])
            dfs.append(df)

    # Get a canvas with the labels for the min dist
    point_calcs = pd.concat(dfs)
    min_x_point = point_calcs.groupby(by=['x', 'y']).min().reset_index()
    filter_x_min = point_calcs.merge(min_x_point, on=['x', 'y', 'dist'], how='inner')

    # Relabel the points with two or more labels for a single min
    two_or_more = filter_x_min.groupby(by=['x', 'y']).size().reset_index()
    canvas = filter_x_min.merge(two_or_more, on=['x', 'y'], how='left')
    canvas = canvas[['x', 'y', 'label_x', 'dist', 0]]
    canvas.columns = ['x', 'y', 'label', 'dist', 'calc']

    # Clean
    canvas = canvas.loc[canvas['calc'] == 1]

    return point_calcs, canvas


def plot(df, label=None, data='df'):
    fig, ax = plt.subplots()
    if label is not None:
        df = df[df['label'] == label]
    if data == 'df':
        ax.scatter(df['x'], df['y'], c=df['label'])
    else:
        ax.scatter(df['x'], df['y'])
    plt.show()


point_calcs, canvas = construct_canvas(500, 500, coords)
biggest_spread = canvas.groupby(by='label').size().reset_index()
biggest_spread.sort_values(by=0, ascending=False)

plot(canvas)
# Answer is label 1

# Part 2
dist_to_all = point_calcs[['x', 'y', 'dist']].groupby(by=['x', 'y']).sum().reset_index()
dist_filter = dist_to_all[dist_to_all['dist'] < 10000]