import pandas as pd

d = open('input2.csv', 'r').readlines()
data = [s.rstrip() for s in d]

# Part 1

def check(s):
    counts = []
    letters = list(s)
    for i, letter in enumerate(letters):
        counts.append([letter, 1])

    df = pd.DataFrame(counts, columns=['letter', 'val'])
    df = df.groupby(by='letter').sum().reset_index()
    
    two = False
    three = False
    
    if len(df.loc[df['val'] == 2]) > 0:
        two = True

    if len(df.loc[df['val'] == 3]) > 0:
        three = True
    
    return [two, three]


def check_sum(data):
    two = 0
    three = 0
    for i in range(len(data)):
        test = check(data[i])

        if test[0] == True:
            two += 1
        
        if test[1] == True:
            three += 1
    return two * three


check_sum = check_sum(data)
check_sum

        
# Part 2

def compare(s1, s2):
    score = 0
    one = list(s1)
    two = list(s2)
    for i in range(len(one)):
        if one[i] == two[i]:
            score += 1
    row = [s1, s2, score]
    return row


def search(data):
    comparisons = []
    for i in range(len(data)):
        if i == len(data) - 1:
            pass
        else:
            for j in range(i + 1, len(data)):
                s1 = data[i]
                s2 = data[j]
                row = compare(s1, s2)
                comparisons.append(row)
    df = pd.DataFrame(comparisons, columns=['s1', 's2', 'score'])
    return df


df = search(data)
df = df.sort_values(by='score', ascending=False)

prtkqyluiusocwvaezjmhmfgx
prtkqyluiusocwvaezjmhmfgx