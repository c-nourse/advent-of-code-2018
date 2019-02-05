d = open('input8.csv', 'r').readlines()
data = [int(i) for i in d[0].split(' ')]

alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def add_node(current_node, position, level):
    
    chld_count = data[position]
    meta_count = data[position + 1]

    if level == 0:
        pass
    else:
        nodes[current_node[:-1]]['chld_loads'] += 1
    
    nodes[current_node] = {
        'parent': current_node[:-1],
        'chld_count': chld_count,
        'chld_loads': 0,
        'meta_count': meta_count,
        'meta': [],
        'position': position,
        'level': level
    }
    return 'Done'


def get_meta(current_node, position):
    meta_count = nodes[current_node]['meta_count']
    meta = data[position: position + meta_count]
    nodes[current_node]['meta'] += meta
    position += meta_count
    return position


def down(current_node, position, level):
    position += 2
    level += 1
    new_node = current_node + alpha[0]
    return new_node, position, level


def up(current_node, level):
    new_node = current_node[:-1]
    level -=1
    return new_node, level


def along(current_node):
    new_node = current_node[:-1] + alpha[nodes[current_node[:-1]]['chld_loads']]
    return new_node


# Set initial values
nodes = {}
level = 0
position = 0
current_node = 'A'
chld_count = 1  # Set a value above zero to get the ball rolling
status = 'head'  # head or meta


while position < len(data):

    if status == 'head':
        add_node(current_node, position, level)
        if nodes[current_node]['chld_count'] > nodes[current_node]['chld_loads']:
            current_node, position, level = down(current_node, position, level)
        elif nodes[current_node]['chld_count'] == 0:
            status = 'meta'

    elif status == 'meta':

        # We've just hit a node with no children
        if nodes[current_node]['chld_count'] == 0:
            position += 2
            position = get_meta(current_node, position)
            current_node, level = up(current_node, level)

        # We're at the end
        elif current_node == 'A':
            position = get_meta(current_node, position)
            position += 1000
        
        # We've visited all of the children in this node and this node is the
        # last child for its parent (no siblings left)
        elif nodes[current_node]['chld_count'] == nodes[current_node]['chld_loads'] and \
            nodes[current_node[:-1]]['chld_count'] == nodes[current_node[:-1]]['chld_loads']:
            position = get_meta(current_node, position)
            current_node, level = up(current_node, level)

        # We're done with this node and next we'll head to its sibling
        else:
            position = get_meta(current_node, position)
            current_node = along(current_node)
    
        # Check if we're at a node with children to visit or if we're at a new node
        try:
            if nodes[current_node]['chld_count'] > nodes[current_node]['chld_loads']:
                print('helo')
                status = 'head'
        except KeyError:
            status = 'head'


meta = 0
for node in nodes:
    node_meta = nodes[node]['meta']
    sum_meta = sum(node_meta)
    meta += sum_meta


# Part 2

val = 0

def walk_and_sum(node, all_nodes):
    global val

    # Check for children
    children = [c for c in all_nodes if c.find(node) > -1]

    if len(children) == 0:
        val += 0
    
    elif len(children) == 1:
        val += sum(nodes[node]['meta'])
    
    elif len(children) > 1:
        refs = nodes[node]['meta']
        refs = [node + alpha[r-1] for r in refs]
        for child in refs:
            walk_and_sum(child, all_nodes)

    else:
        print('Issues have arisen.')
    

