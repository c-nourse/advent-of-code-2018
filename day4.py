import pandas as pd
from datetime import datetime, timedelta
import itertools

d = open('input4.csv', 'r').readlines()
data = [s.rstrip() for s in d]


def parse_record(record):
    dt_time = record.split('] ')[0]
    msg = record.split('] ')[1]
    
    dt_time = dt_time.replace('[', '')
    dt = [int(d) for d in dt_time.split(' ')[0].split('-')]
    t = [int(ts) for ts in dt_time.split(' ')[1].split(':')]
    
    return [datetime(dt[0], dt[1], dt[2]), datetime(dt[0], dt[1], dt[2], t[0], t[1]), msg]


def compile_df(data):
    rows = []
    for i in range(len(data)):
        row = parse_record(data[i])
        rows.append(row)
    df = pd.DataFrame(rows, columns=['dt', 'time', 'msg'])
    df = df.sort_values(by=['time'])
    return df.reset_index()[['dt', 'time', 'msg']]


def one_by_one(df):
    expanded = []

    for i in range(len(df)):
      
        if i == len(df) - 1:
            t0 = df.loc[i, 'time']
            tN = datetime(t0.year, t0.month, t0.day, 0, 59)
            dt = df.loc[i, 'dt']
            if df.loc[i, 'msg'].split(' ')[0] in ['Guard', 'wakes']:
                m = 0
            else:
                m = 1
        else:
            if df.loc[i, 'msg'].split(' ')[0] == 'Guard':
            # Get Guard ID
                guard = df.loc[i, 'msg'].split(' ')[1]
            
            if df.loc[i, 'time'].hour == 11:
                t = df.loc[i, 'time']
                t0 = datetime(t.year, t.month, t.day + 1, 0, 0)
            else:
                t0 = df.loc[i, 'time']
            # Get dt
            dt = datetime(t0.year, t0.month, t0.day)
            # Get tN
            if df.loc[i + 1, 'msg'].find('Guard') == 0:
                tN = datetime(t0.year, t0.month, t0.day, 0, 59)
            else:
                tN = df.loc[i + 1, 'time']
            # Get awake or asleep
            if df.loc[i, 'msg'].split(' ')[0] in ['Guard', 'wakes']:
                m = 0
                print(df.loc[i, 'msg'].split(' ')[0])
            else:
                m = 1
                print(m)

        # Generator for the minutes between falling asleep and waking up
        min_generator = (t0 + timedelta(minutes=i) for i in itertools.count())
        gap = int((tN - t0).total_seconds()/60)
        try:
            all_mins = list(itertools.islice(min_generator, gap))
        except:
            print(gap)
            print(df.loc[i])
            print(df.loc[i + 1])
        for k, minute in enumerate(all_mins):
            expanded.append([guard, dt, minute, m])

    df_exp = pd.DataFrame(expanded, columns=['idx', 'dt', 'minute', 'asleep'])

    return df_exp


df = compile_df(data)
df_exp = one_by_one(df)
#df_exp = expand_df(df)

most_sleep = df_exp.groupby(by=['idx']).sum().reset_index()
most_sleep.sort_values(by='asleep', ascending=False)

df_exp['minute_int'] = df_exp['minute'].apply(lambda x: x.minute)
guards_x_min = df_exp.groupby(by=['idx', 'minute_int']).sum().reset_index()
guards_x_min.loc[guards_x_min['idx'] == '#1601'].sort_values(by='asleep')
