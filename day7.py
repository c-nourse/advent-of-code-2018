import pandas as pd

d = open('input7.csv', 'r').readlines()
data = [s.rstrip() for s in d]


def parse_step(s):
    s_l = s.split(' ')
    parent = s_l[1]
    child = s_l[7]
    return [parent, child]


def combine_steps(data):
    steps = []
    for step in data:
        row = parse_step(step)
        steps.append(row)
    df = pd.DataFrame(steps, columns=['parent', 'child'])
    return df[['child', 'parent']].sort_values(by=['child', 'parent'])


def build(steps):
    staging = []  # Criteria met, just need to check alphabetically
    complete = []  # Order of run

    last_run = None

    while len(complete) < len(set(list(steps['parent'])).union(set(list(steps['child'])))):
            
        if last_run is None:    
            # Find first batch for staging
            without_parents = sorted(list(
                set(list(steps['parent'])).difference(set(list(steps['child'])))
                ))

            # Add column to steps df to track runs of parents
            steps['run'] = 0
        
            last_run = without_parents[0]
            unlocked = without_parents[1:]
            staging += unlocked

        else:

            child_of_last_run = list(steps[steps['parent'] == last_run]['child'])
            test_parents = steps[
                steps['child'].isin(child_of_last_run)
                ].groupby(by='child').agg({'parent': 'size',
                                           'run': 'sum'}).reset_index()

            unlocked = list(
                test_parents.loc[test_parents['parent'] == test_parents['run']]['child']
                )

            staging += list(set(unlocked).difference(set(complete)))
            staging = sorted(staging)
            last_run = staging.pop(0)

        complete.append(last_run)
        steps.loc[steps['parent'] == last_run, 'run'] = 1

    return complete


steps = combine_steps(data)
complete = build(steps)
print(''.join(complete))


# Part 2

def build_w_qs(steps):
    pipeline = []
    complete = []
    seconds = 0
    queues = {}
    
    # Construct times
    times = {}
    all_steps = sorted(
        list(
            set(list(steps['parent'])).union(set(list(steps['child'])))
        )
    )
    for i, letter in enumerate(all_steps):
        times[letter] = 60 + i + 1

    # Run
    while len(complete) < len(all_steps):
            
        if seconds == 0:

            unlocked = sorted(list(
                set(list(steps['parent'])).difference(set(list(steps['child'])))
                ))

            steps['run'] = 0
            pipeline += unlocked

            for i in range(len(pipeline)):
                queues[pipeline[0]] = times[pipeline[0]]
                pipeline.pop(0)

        else:

            child_of_complete = list(steps[steps['parent'].isin(complete)]['child'])
            test_parents = steps[
                steps['child'].isin(child_of_complete)
                ].groupby(by='child').agg({'parent': 'size',
                                           'run': 'sum'}).reset_index()
            unlocked = list(
                test_parents.loc[test_parents['parent'] == test_parents['run']]['child']
                )            
            
            unlocked_new = [u for u in unlocked
                if u not in complete and u not in queues.keys()
            ]
            
            pipeline += unlocked_new
            pipeline = sorted(list(set(pipeline)))

            if len(queues) < 5 and len(pipeline) > 0:
                for i in range(min(5 - len(queues), len(pipeline))):
                    letter = pipeline[0]
                    queues[letter] = times[letter]
                    pipeline.pop(0)

        print("{} <--- {}".format(queues, pipeline))
        # Add to queue
        to_del = []
        for queue in queues:
            queues[queue] -= 1
            if queues[queue] == 0:
                complete.append(queue)
                to_del.append(queue)
        for letter in to_del:
            del queues[letter]
        to_del = []
        
        steps.loc[steps['parent'].isin(complete), 'run'] = 1
        seconds += 1

    return complete, seconds


complete, seconds = build_w_qs(steps)