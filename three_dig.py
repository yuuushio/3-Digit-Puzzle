import math

class Node:
    def __init__(self, digit, parent=None):
        self.value = digit
        self.parent = parent
        self.children = []
        if parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
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
    return dig_subtract, dig_add

# generates 0-2 children of the ith index/digit
def gen_ith_children(node, i):
    dig_add, dig_sub = change_single_digit(node.value, i)
    
    # error check 
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

    elif dig_add: 
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
        node_li = []
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
        path.append(n.parent.value)
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

    while current.value != goal.value and len(expanded) <= 1000:
        expanded.append(current) # then we generate its children bc expanded
        if bfs:
            fringe += gen_children(current, forbidden)
        else:
            # else must be dfs; children are added at the front
            fringe = gen_children(current, forbidden) + fringe

        tmp = fringe.pop(0) # O(n)
        # To avoid cycles, we implement our own __eq__ method for node equality check
        while tmp in visited_nodes:
            # Keep discarding from fringe till u find a digit that
            # hasn't been visited
            tmp = fringe.pop(0)
        print(len(expanded))
        # If we reach here means we found an unvisited node;
        # can mark it as visited for next iteration
        visited_nodes.append(tmp)
        current = tmp

    if len(expanded) == 1000: return "No solution found, limit reached."

    # If we're here, means goal has been found
    expanded.append(current)
    final_expanded = []
    for n in expanded: final_expanded.append(n.value)
    path = get_path(current)

    return path, final_expanded

def ids_helper(s, g, f, d, expanded):
    visited_nodes = []
    fringe = []
    current = s
    visited_nodes.append(current)
    children_generated = []

    while current.value != g.value and len(expanded) <= 1000:
        expanded.append(current)
        if current.depth < d and current not in children_generated:
            fringe = gen_children(current, f) + fringe
            children_generated.append(current)
        if len(fringe) == 0:
            return None, expanded, False
        else:
            tmp = fringe.pop(0)
            while tmp in visited_nodes and len(fringe) != 0:
                tmp = fringe.pop(0)
                if len(fringe) == 0:
                    return None, expanded, False

            visited_nodes.append(tmp)
            if tmp is not None:
                current = tmp
    if len(expanded) == 1000:
        return None, expanded, False

    expanded.append(current)
    return None, expanded, True

def ids(start, goal, forbidden=None):
    expanded = []
    depth = 0
    dls = ids_helper(start, goal, forbidden, depth, expanded)
    goal_found = False
    if dls[2]:
        # if goal is found at depth 0 
        return [dls[1].value]
    else:
        #expanded += dls[1]
        while goal_found == False and len(expanded) <= 1000:
            depth += 1
            dls = ids_helper(start, goal, forbidden, depth, expanded)
            goal_found = dls[2]
            # TODO: implement logic for when 1000 states are reached
            # and the output from the method is the string
            expanded = dls[1]
        final_expanded = []
        for n in expanded:
            final_expanded.append(n.value)
        return final_expanded
            
# infinite loop when start = 310
print(ids(Node(310), Node(110)))

#print(bfs_dfs(Node(310), Node(110), bfs=False))

# def id(start, goal, forbidden=None, d):
    # each time you expand a node, increase current depth by 1
    # final list should be 1000 nodes max
    # iterate till current_depth == d
