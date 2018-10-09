"""
Copyright (c) 2018 Miguel Mendes, http://miguendes.me/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import functools

import pytest

from pybstree import BinarySearchTree


@functools.total_ordering
class Entry:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __lt__(self, other):
        if self.a == other.a:
            return self.b < other.b
        return self.a < other.a

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __repr__(self):
        return f"{self.__class__.__name__}({self.a}, {self.b})"


def test_empty_tree():
    tree = BinarySearchTree()
    assert not tree


def test_insert_on_empty_tree():
    tree = BinarySearchTree()
    tree.insert(9)
    tree.insert(4)
    tree.insert(14)
    tree.insert(17)
    tree.insert(7)

    root = tree.root
    assert root.entry == 9
    assert root.left.entry == 4
    assert root.right.entry == 14
    assert root.right.right.entry == 17
    assert root.left.right.entry == 7
    assert tree


def test_insert_duplicated_entry():
    tree = BinarySearchTree()
    tree.insert(9)
    tree.insert(10)
    tree.insert(9)

    assert tree.root.entry == 9
    assert tree.root.right.entry == 10
    assert not tree.root.left
    assert tree


def test_height():
    tree = BinarySearchTree()
    tree.insert(9)
    root = tree.root
    assert root.height == 1

    tree.insert(4)
    root = tree.root
    assert root.height == 2
    assert root.left.height == 1

    tree.insert(14)
    root = tree.root
    assert root.height == 2
    assert root.left.height == 1
    assert root.right.height == 1

    tree.insert(17)
    root = tree.root
    assert root.height == 3
    assert root.left.height == 1
    assert root.right.height == 2
    assert root.right.right.height == 1

    tree.insert(7)
    root = tree.root
    assert root.height == 3
    assert root.left.height == 2
    assert root.left.right.height == 1


def test_length():
    tree = BinarySearchTree()

    entries = range(150)
    for entry in entries:
        tree.insert(entry)

    assert len(tree) == len(entries)
    assert len(BinarySearchTree()) == 0


def test_empty_tree_contains_no_key():
    """test empty tree should not contain any entry"""
    assert 10 not in BinarySearchTree()


def test_all_inserted_elements_must_be_in_tree():
    """test element must be in tree"""
    import random
    entries = list(range(128))
    random.shuffle(entries)

    tree = BinarySearchTree()

    for entry in entries:
        tree.insert(entry)

    for entry in entries:
        assert entry in tree


@pytest.mark.parametrize("order,expected", [
    ('preorder', (20, 10, 25, 23, 29, 30)),
    ('inorder', (10, 20, 23, 25, 29, 30)),
    ('postorder', (10, 23, 30, 29, 25, 20)),
    ('bfs', (20, 10, 25, 23, 29, 30)),
])
def test_traversal(order, expected):
    tree = BinarySearchTree()

    tree.insert(20)
    tree.insert(10)
    tree.insert(25)
    tree.insert(23)
    tree.insert(29)
    tree.insert(30)

    assert tuple(tree.traverse(order)) == expected


@pytest.mark.parametrize("order,expected", [
    ('preorder', ()),
    ('inorder', ()),
    ('postorder', ()),
    ('bfs', ()),
])
def test_empty_traversal(order, expected):
    tree = BinarySearchTree()

    assert tuple(tree.traverse(order)) == expected


def test_constructor_not_properly_called():
    with pytest.raises(TypeError) as context:
        BinarySearchTree(4)
    assert ("BinarySearchTree constructor called with incompatible data type: "
            "'int' object is not iterable" in str(context.value))


def test_initialize_tree_from_sequence():
    entries = [5, 3, 8, 9, 1, 2]
    tree = BinarySearchTree(entries)

    assert tuple(tree.traverse('bfs')) == (5, 3, 8, 1, 9, 2)


def test_find_max():
    entries = get_random_entries()
    tree = BinarySearchTree(entries)
    assert tree.max() == max(entries)


def test_find_min():
    entries = get_random_entries()
    tree = BinarySearchTree(entries)
    assert tree.min() == min(entries)


@pytest.mark.parametrize("entries,expected", [
    ([2, 1, 4, 3, 5], '(2 (1 () ()) (4 (3 () ()) (5 () ())))'),
    ([1, 2, 3, 4, 5], '(1 () (2 () (3 () (4 () (5 () ())))))'),
    ([], '()')
])
def test_str_repr(entries, expected):
    tree = BinarySearchTree(entries)
    assert str(tree) == expected


def test_delete_single_element():
    tree = BinarySearchTree([1])

    tree.delete(1)

    assert 1 not in tree
    assert not tree
    assert len(tree) == 0


def test_delete_leaf_node():
    tree = BinarySearchTree([1, 2])

    tree.delete(2)

    assert 1 in tree
    assert 2 not in tree
    assert tree
    assert len(tree) == 1


@pytest.mark.parametrize("entries,entry_to_be_deleted", [
    ([1, 2, 3], 10),
    (None, 10)
])
def test_delete_not_existent_entry(entries, entry_to_be_deleted):
    with pytest.raises(KeyError) as context:
        tree = BinarySearchTree(entries)
        tree.delete(entry_to_be_deleted)
    assert f"KeyError: {entry_to_be_deleted}" in str(context.value)


def test_delete_entries_in_a_row():
    entries = [20, 10, 5, 7, 40, 30, 50]
    tree = BinarySearchTree(entries)
    assert str(tree) == '(20 (10 (5 () (7 () ())) ()) (40 (30 () ()) (50 () ())))'

    tree.delete(10)
    assert 10 not in tree
    assert str(tree) == '(20 (7 (5 () ()) ()) (40 (30 () ()) (50 () ())))'

    tree.delete(5)
    assert 5 not in tree
    assert str(tree) == '(20 (7 () ()) (40 (30 () ()) (50 () ())))'

    tree.delete(7)
    assert 7 not in tree
    assert str(tree) == '(20 () (40 (30 () ()) (50 () ())))'

    tree.delete(20)
    assert 20 not in tree
    assert str(tree) == '(40 (30 () ()) (50 () ()))'

    tree.delete(40)
    assert 40 not in tree
    assert str(tree) == '(30 () (50 () ()))'

    tree.delete(30)
    assert 30 not in tree
    assert str(tree) == '(50 () ())'

    tree.delete(50)
    assert 50 not in tree
    assert str(tree) == '()'

    assert not tree


def test_equals():
    tree1 = BinarySearchTree([2, 4, 1, 5, 3])
    tree2 = BinarySearchTree([2, 1, 4, 3, 5])
    tree3 = BinarySearchTree([1, 2, 3, 4, 5, 6])

    assert tree1 == tree2
    assert tree1 is not tree2

    assert tree1 != tree3
    assert tree1 is not tree3
    assert tree2 != tree3
    assert tree2 is not tree3

    assert tree1 != int(9)

    assert tree1 != BinarySearchTree()


def test_clear():
    tree = BinarySearchTree([1, 2, 3, 4, 5])
    tree.clear()

    assert not tree


def test_search():
    tree = BinarySearchTree([1, 2, 3, 4, 5])
    entry = tree.search(4)

    assert 4 == entry


def test_search_complex_data_type():
    tree = BinarySearchTree([Entry(1, 'a'),
                             Entry(4, 'b'),
                             Entry(3, 'c'),
                             Entry(3, 'd'), ])
    entry = tree.search(Entry(3, 'd'))

    Entry(3, 'd') == entry

    entry = Entry(3113, 'd')
    with pytest.raises(KeyError) as context:
        tree.search(entry)

    assert f"Entry {entry} not found." in str(context.value)


def test_build_tree_from_other():
    original = BinarySearchTree([1, 2, 3, 4, 5])
    copy = BinarySearchTree(original)

    assert copy == BinarySearchTree([1, 2, 3, 4, 5])


def test_copy():
    import copy
    single_entry = Entry(1, ['a'])
    tree1 = BinarySearchTree([single_entry,
                              Entry(2, 'b'),
                              Entry(3, 'c'),
                              Entry(3, 'd'), ])
    tree2 = copy.copy(tree1)
    assert tree1 == tree2
    single_entry.b = 'a'
    assert tree1 == tree2


def test_pred():
    import random
    random.seed(7477)
    entries = get_random_entries()
    tree = BinarySearchTree(entries)

    pred, prev = None, None
    for entry in tree.traverse():
        try:
            pred = tree.pred(entry)
        except KeyError:
            assert prev is None
        assert prev == pred
        prev = entry

    with pytest.raises(KeyError) as context:
        tree.pred(1000000)
    assert "Predecessor of 1000000 not found." in str(context.value)


def test_succ():
    import random
    random.seed(7477)
    entries = get_random_entries()
    tree = BinarySearchTree(entries)
    rev_entries = sorted(entries, reverse=True)

    succ, prev = None, None
    for entry in rev_entries:
        try:
            succ = tree.succ(entry)
        except KeyError:
            assert prev is None
        assert prev == succ
        prev = entry

    with pytest.raises(KeyError) as context:
        tree.succ(1000000)
    assert "Successor of 1000000 not found." in str(context.value)


def get_random_entries():
    from random import randint, shuffle, seed
    seed(7477)
    a = randint(1, 500)
    b = randint(1, 500)
    lower, upper = min(a, b), max(a, b)
    entries = list(range(lower, upper + 1))
    shuffle(entries)
    return entries
