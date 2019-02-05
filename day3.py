import pandas as pd

d = open('input3.csv', 'r').readlines()
data = [s.rstrip() for s in d]

# Part 1

def parse_claim(s):
    components = s.split(" ")
    idx_claim = components[0]
    x = int(components[2].split(",")[0])
    y = int(components[2].split(",")[1].replace(":", ""))
    w = int(components[3].split('x')[0])
    h = int(components[3].split('x')[1])
    return [x, y, w, h, idx_claim]


def expand_claim(claim):
    space = []
    for i in range(claim[2]):
        x = claim[0] + i
        for j in range(claim[3]):
            y = claim[1] + j
            space.append([x, y, 1])

    df = pd.DataFrame(space, columns=['x', 'y', 'val'])
    return df


def check_claims(data):
    dfs = []
    for i in range(len(data)):
        claim = parse_claim(data[i])
        df = expand_claim(claim)
        dfs.append(df)
        
    all_claims = pd.concat(dfs)
    grouped = all_claims.groupby(by=['x', 'y']).sum().reset_index()
    grouped = grouped.sort_values(by='val', ascending=False)
    return grouped

grouped = check_claims(data)
len(grouped.loc[grouped['val'] >= 2])

# Part 2

def test_claim(data, grouped):
    single_area = grouped.loc[grouped['val'] == 1]
    
    for i in range(len(data)):
        claim = parse_claim(data[i])
        idx_claim = claim[4]
        df = expand_claim(claim)
        test = single_area.merge(df, on=['x', 'y'], how='inner')
        if len(df) == len(test):
            break

    return idx_claim


idx = test_claim(data, grouped)