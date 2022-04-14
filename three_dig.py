import math

class Node:
    def __init__(self, digit, parent=None):
        self.value = digit
        self.parent = parent
        self.children = []
    # Custom equality check:
    # - 2 nodes are same if they same 3 digits AND same child nodes
    def __eq__(self, other):
        return set(self.children) == set(other.children) and self.value == other.value

# Helper method used to subtract/add at char i
def change_single_digit(node_value, i):
    dig_add = dig_subtract = None
    ith_digit = int(str(node_value)[i])
    if ith_digit != 9:
        dig_add = ith_digit + 1
    if ith_digit != 0:
        dig_subtract = ith_digit - 1
    return dig_add, dig_subtract

# generates 0-2 children of the ith index/digit
def gen_ith_children(node, i):
    dig_add, dig_sub = change_single_digit(node.value, i)
    
    # --?? should i use "or"...  --
    if dig_add is None and dig_sub is None:
        return []

    if dig_add and dig_sub:
        if i == 0:
            list_a = [str(dig_add), str(node.value)[1], str(node.value)[2]]
            list_b = [str(dig_sub), str(node.value)[1], str(node.value)[2]]
        elif i == 1:
            list_a = [str(node.value)[0], str(dig_add), str(node.value)[2]]
            list_b = [str(node.value)[0], str(dig_sub), str(node.value)[2]] 
        else:
            list_a = [str(node.value)[0], str(node.value)[1], str(dig_add)]
            list_b = [str(node.value)[0], str(node.value)[1], str(dig_sub)]
        
        str_a = str_b = ""
        for c in list_a: str_a += c
        for c in list_b: str_b += c
        return [Node(int(str_a), parent=node), Node(int(str_b), parent=node)]

    elif dif_add: 
        if i == 0:
            list_a = [str(dig_add), str(node.value)[1], str(node.value)[2]]
        elif i == 1:
            list_a = [str(node.value)[0], str(dig_add), str(node.value)[2]]
        else:
            list_a = [str(node.value)[0], str(node.value)[1], str(dig_add)]

        str_a = ""
        for c in list_a: str_a += c
        return [Node(int(str_a), parent=node)]
    else:
        if i == 0:
            list_b = [str(dig_sub), str(node.value)[1], str(node.value)[2]]
        elif i == 1:
            list_b = [str(node.value)[0], str(dig_sub), str(node.value)[2]] 
        else:
            list_b = [str(node.value)[0], str(node.value)[1], str(dig_sub)]

        str_b = "" 
        for c in list_b: str_b += c
        return [Node(int(str_b), parent=node)]

def gen_children(node, forbidden):
    if node.parent is None:
        # generate all children since no parent to depend on
        for i in range(0, 3):
            node_li += gen_ith_children(node, i)
        
        # children added as raw values - for easier comparisons of equality
        #  using set/dict
        for n in node_li:
            node.children.append(n.value)
        return node_li
    else:
        diff = math.fabs(node.parent.value - node.value)

    if diff == 100:
        node_li = gen_ith_children(node, 1) + gen_ith_children(node, 2)
        for n in node_li:
            node.children.append(n.value)
        return node_li

    elif diff == 10:
        node_li = gen_ith_children(node, 0) + gen_ith_children(node, 2)
        for n in node_li:
            node.children.append(n.value)
        return node_li

    else:
        # assume 3rd digit was changed (good assumption if valid input)
        node_li = gen_ith_children(node, 0) + gen_ith_children(node, 1)
        for n in node_li:
            node.children.append(n.value)
        return node_li

def get_path(node):
    n = node
    path = []
    path.append(n.value)
    while n.parent is not None:
        path.appent(n.parent.value)
        # Trace back through the parents for path
        n = n.parent
    return path[::-1] # Return the reverse of the list since we tracked back

# Can implement bfs and dfs in the same method, since the only
# difference is the way the children are added to the fringe.
def bfs_dfs(start, goal, forbidden=None, bfs=True):
    visited_nodes = []
    fringe = []
    expanded = []
    current = start
    visited_nodes.append(current)

    while curent.value != goal.value and len(expanded) < 1000:
        expanded.append(current) # then we generate its children bc expanded
        if bfs:
            fringe += gen_children(current, forbidden)
        else:
            # else must be dfs; children are added at the front
            fringe += gen_children(current, forbidden) + fringe

        tmp = fringe.pop(0) # O(n)
        # To avoid cycles, we implement our own __eq__ method
        while tmp in visited_nodes:
            # Keep discarding from fringe till u find a digit that
            # hasn't been visited
            tmp = fringe.pop(0)

        # If we reach here means we found an unvisited node;
        # can mark it as visited for next iteration
        visited_nodes.append(tmp)
        current = tmp

    if len(expanded) == 1000 return "No solution found, limit reached."

    # If we're here, means goal has been found
    expanded.append(current)
    
    final_expanded = []
    for n in expanded: final_expanded.append(n.value)
    
    
