import pandas as pd


def pwr_lvl(x, y, grid_serial):
    rack_id = x + 10
    power_level = (rack_id * y + grid_serial) * rack_id
    pwr = int(str(power_level)[-3]) - 5
    return pwr


def grid(s, grid_serial):
    rows = []
    for x in range(1, s + 1):
        for y in range(1, s + 1):
            pwr = pwr_lvl(x, y, grid_serial)
            rows.append([x, y, pwr])
    df = pd.DataFrame(rows, columns=['x', 'y', 'pwr'])
    return rows, df


def grid_sums(s, g, df):
    rows = []
    for x in range(s - (g - 2)):
        for y in range(s - (g - 2)):
            df_filter = df.loc[(df['x'] >= x) &
                               (df['x'] < x + g) &
                               (df['y'] >= y) & 
                               (df['y'] < y + g)]
            pwr_sum = sum(df_filter['pwr'])
            rows.append([x, y, pwr_sum])
    df_grids = pd.DataFrame(rows, columns=['x', 'y', 'pwr_sum'])
    df_grids = df_grids.sort_values(by='pwr_sum', ascending=False)
    top = df_grids.iloc[0]
    return [top['x'], top['y'], top['pwr_sum']]

%%timeit
def grid_sums(s, g, df):
    rows = []
    for x in range(s - (g - 2)):
        for y in range(s - (g - 2)):
            x_r = [i for i in range(x + g) if i >= x]
            y_r = [i for i in range(y + g) if i >= y]
            p_sum = sum(df.loc[(df['x'].isin(x_r)) & (df['y'].isin(y_r))]['pwr'])
            rows.append([x, y, p_sum])
    df_grids = pd.DataFrame(rows, columns=['x', 'y', 'pwr_sum'])
    top = df_grids.sort_values(by='pwr_sum', ascending=False).iloc[0]
    return [top['x'], top['y'], top['pwr_sum'], g]
row = grid_sums(300, 3, df)

s = 300
g = 3
grid_serial = 5093
rows, df = grid(s, grid_serial)
#df_grids = grid_sums(s, g, df)


rows = []
for i in range(2, s + 1):
    g = i
    print(g)
    row = grid_sums(s, g, df)
    rows.append(row)