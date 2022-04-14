import pytest
import three_dig.py as t

def test_gen_first():
    node = t.Node(320)
    zero_i_c = t.gen_ith_children(node, 0)
    assert zero_i_c[0].value == 820

