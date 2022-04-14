import math

class Node:
    def __init__(self, digit, parent=None):
        self.value = digit
        self.parent = parent
        self.children = []

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
def generate_ith_children(node, i):
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
