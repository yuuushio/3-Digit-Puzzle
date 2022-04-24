import math
import sys
from queue import PriorityQueue

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

def mh_heuristic(a, b):
    res = 0
    for x,y in zip(str(a), str(b)):
        res += math.fabs(int(x)-int(y))
    return res

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
    if dig_add is not None and dig_sub is not None:
        if i == 0:
            str_a = f"{str(dig_add)}{str(node.value)[1]}{str(node.value)[2]}"
            str_b = f"{str(dig_sub)}{str(node.value)[1]}{str(node.value)[2]}"
        elif i == 1:
            str_a = f"{str(node.value)[0]}{str(dig_add)}{str(node.value)[2]}"
            str_b = f"{str(node.value)[0]}{str(dig_sub)}{str(node.value)[2]}"
        else:
            str_a = f"{str(node.value)[0]}{str(node.value)[1]}{str(dig_add)}"
            str_b = f"{str(node.value)[0]}{str(node.value)[1]}{str(dig_sub)}"
        
        return [Node(int(str_a), parent=node), Node(int(str_b), parent=node)]

    elif dig_add: 
        if i == 0:
            str_a = f"{str(dig_add)}{str(node.value)[1]}{str(node.value)[2]}"
        elif i == 1:
            str_a = f"{str(node.value)[0]}{str(dig_add)}{str(node.value)[2]}"
        else:
            str_a = f"{str(node.value)[0]}{str(node.value)[1]}{str(dig_add)}"

        return [Node(int(str_a), parent=node)]
    else:
        if i == 0:
            str_b = f"{str(dig_sub)}{str(node.value)[1]}{str(node.value)[2]}"
        elif i == 1:
            str_b = f"{str(node.value)[0]}{str(dig_sub)}{str(node.value)[2]}"
        else:
            str_b = f"{str(node.value)[0]}{str(node.value)[1]}{str(dig_sub)}"

        return [Node(int(str_b), parent=node)]

# Returns a new list that doesnt consist of forbidden nodes
def renew_list(node_li, f):
    new_list = []
    if f is not None and len(f) != 0:
        for n in node_li:
            if n.value not in f:
                new_list.append(n)
        return new_list
    else:
        return node_li

# Generates the nodes' children
def node_children_list_helper(node, renewed_li):
    # Children added as raw values - easier for comparisons
    for n in renewed_li: node.children.append(n.value)

def gen_children(node, forbidden):
    node_li = []
    if node.parent is None:
        # generate all children since no parent to depend on
        for i in range(0, 3):
            node_li += gen_ith_children(node, i) 
    else:
        diff = math.fabs(node.parent.value - node.value)
        if diff == 100:
            node_li = gen_ith_children(node, 1) + gen_ith_children(node, 2)
        elif diff == 10:
            node_li = gen_ith_children(node, 0) + gen_ith_children(node, 2)
        else:
            # assume 3rd digit was changed (good assumption if valid input)
            node_li = gen_ith_children(node, 0) + gen_ith_children(node, 1)
    
    renewed_li = renew_list(node_li, forbidden)
    node_children_list_helper(node, renewed_li)
    return renewed_li 

def get_path(node):
    n = node
    path = []
    path.append(n.value)
    while n.parent is not None:
        path.append(n.parent.value)
        # Trace back through the parents for path
        n = n.parent
    return path[::-1] # Return the reverse of the list since we tracked back

# Generates the output path and expanded list
def generate_return_val(expanded):
    final_expanded = [n.value for n in expanded]
    # [-1] bc we appended the goal node in the end
    # and then use it to trace back
    path = get_path(expanded[-1])
    return path, final_expanded

# Can implement bfs and dfs in the same method, since the only
# difference is the way the children are added to the fringe.
def bfs_dfs(start, goal, forbidden=None, bfs=True):
    visited_nodes = []
    visited_nodes_values = []
    fringe = []
    expanded = []
    current = start
    visited_nodes.append(current)
    visited_nodes_values.append(current.value)

    while current.value != goal.value and len(expanded) <= 1000:
        expanded.append(current) # then we generate its children bc expanded
        if bfs:
            fringe += gen_children(current, forbidden)
        else:
            # else must be dfs; children are added at the front
            fringe = gen_children(current, forbidden) + fringe

        if len(fringe) != 0:
            tmp = fringe.pop(0) # O(n)
        # To avoid cycles, we implement our own __eq__ method for node equality check
        while tmp.value in visited_nodes_values and len(fringe) != 0:
            ind = visited_nodes_values.index(tmp.value)
            # Keep discarding from fringe till u find a digit that
            # hasn't been visited
            if tmp.children == visited_nodes[ind].children:
                tmp = fringe.pop(0)
            else: break
        # If we reach here means we found an unvisited node;
        # can mark it as visited for next iteration
        visited_nodes.append(tmp)
        visited_nodes_values.append(tmp.value)
        current = tmp

    if len(expanded) == 1000: return "No solution found, limit reached."
    # If we're here, means goal has been found
    expanded.append(current)
    return generate_return_val(expanded)

# DFS that only gets expanded up to a certain depth
# Return: [] -> expanded nodes, true if goal found, else false
def ids_helper(s, g, f, d, expanded):
    visited_nodes = []
    visited_nodes_values = []
    fringe = []
    current = s
    visited_nodes.append(current)
    visited_nodes_values.append(current.value)

    while current.value != g.value and len(expanded) <= 1000:
        expanded.append(current)
        # Dont generate children of depth greater than current d
        if current.depth < d: 
            fringe = gen_children(current, f) + fringe
        #print([a.value for a in fringe])
        # To avoid popping from empty fringe list
        if len(fringe) == 0:
            return expanded, False
        else:
            # Keep popping till you find an un-visited noed
            tmp = fringe.pop(0)
            while tmp.value in visited_nodes_values and len(fringe) != 0:
                ind = visited_nodes_values.index(tmp.value)
                if tmp.children == visited_nodes[ind].children:
                    tmp = fringe.pop(0)
                else:
                    break
                if len(fringe) == 0:
                    return expanded, False

            visited_nodes.append(tmp)
            visited_nodes.append(tmp.value)
            if tmp is not None:
                current = tmp
    if len(expanded) == 1000: return expanded, False
    expanded.append(current)
    return expanded, True

def ids(start, goal, forbidden=None):
    expanded = []
    depth = 0
    dls = ids_helper(start, goal, forbidden, depth, expanded)
    goal_found = False
    if dls[1]:
        # if goal is found at depth 0 
        return [dls[0].value]
    else:
        # Iteratively call dfs till goal found/limit reached
        while goal_found == False and len(expanded) <= 1000:
            # Increase depth after each dfs call
            depth += 1
            dls = ids_helper(start, goal, forbidden, depth, expanded)
            goal_found = dls[1]
            expanded = dls[0]
        if dls[1] == False and len(expanded) >= 1000:
            return "No solution found. Limit Reached"

        return generate_return_val(expanded)

# Returns f; f = g + h
# where g = cost so far to reach node
# h = heuristic of the node
def astar_cost_func(node, g):
    # Since the edge weights are virtually 1,
    # we can use the node's depth as cost to get to that node
    return node.depth + mh_heuristic(node.value, g.value)

# Greedy & a_star combined into 1 since the only difference in this case
# is the heuristic/f(n) calculation:
#  if a_star = False, evaluate Greedy, i.e., evaluate greedy by default
def heuristic_based(s, g, f=None, a_star=False):
    expanded = []
    visited = []
    visited_values = []
    # Pq to get node with lowest cost function in lg(n) time
    fringe = PriorityQueue()
    current = s
    visited.append(current)
    visited_values.append(current.value)
    i = 0 # To differentiate when nodes have same h
    while current.value != g.value and len(expanded) <= 1000:
        expanded.append(current)
        # Expand node and add its children to fringe
        for c in gen_children(current, f):
            h = astar_cost_func(c, g) if a_star else mh_heuristic(c.value, g.value)
            fringe.put((h, i, c))
            i -= 1
        # Get next node to expand from fringe
        if not fringe.empty() != 0:
            tmp = fringe.get()[2]
        while tmp.value in visited_values and not fringe.empty() != 0:
            ind = visited_values.index(tmp.value)
            if tmp.children == visited[ind].children:
                # Keep popping from fringe till an un-visited node is found
                tmp = fringe.get()[2]
            else: break
        visited.append(tmp)
        visited_values.append(tmp.value)
        current = tmp

    if len(expanded) == 1000: return "No solution found."
    # Goal has been found: get path and the list of expanded nodes
    expanded.append(current)
    return generate_return_val(expanded)

def print_output(path, expanded):
    for i in range(len(path)):
        print(path[i], end="")
        if i != len(path)-1:
            print(",", end="")
    print("")
    for i in range(len(expanded)):
        print(expanded[i], end="")
        if i != len(expanded)-1:
            print(",", end="")
    print("")

def read_input():
    algo = sys.argv[1]
    file_name = sys.argv[2]
    with open(file_name, 'r') as f:
        contents = f.readlines()
    s = Node(int(contents[0]))
    g = Node(int(contents[1])) 
    # Prase forbidden if file has a 3rd line
    if len(contents) > 2:
        forbidden_list_str = contents[2].split(",")
        f = [Node(int(dig)) for dig in forbidden_list_str]
    else:
        f = None
    return algo, s, g, f

def main():
    algo, s, g, f = read_input()
    if algo == "B":
        p, e = bfs_dfs(s,g,f)
        print_output(p,e)
    if algo == "D":
        p, e = bfs_dfs(s,g,f,bfs=False)
        print_output(p, e)
    if algo == "I":
        p, e = ids(s,g,f)
        print_output(p, e)
    if algo == "G":
        p, e = heuristic_based(s,g,f)
        print_output(p, e)
    if algo == "A":
        p, e = heuristic_based(s,g,f,a_star=True)
        print_output(p, e)

if __name__ == "__main__":
    main()
