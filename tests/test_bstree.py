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

from pybstree import BinarySearchTree, AVLTree


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


class TestBinarySearchTree:
    @pytest.fixture
    def tree(self):
        return BinarySearchTree()

    def test_empty_tree(self, tree):
        assert not tree

    def test_insert_on_empty_tree(self, tree):
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

    def test_insert_duplicated_entry(self, tree):
        tree.insert(9)
        tree.insert(10)
        tree.insert(9)

        assert tree.root.entry == 9
        assert tree.root.right.entry == 10
        assert not tree.root.left
        assert tree

    def test_height(self, tree):
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

    def test_empty_tree_contains_no_key(self, tree):
        """test empty tree should not contain any entry"""
        assert 10 not in tree

    def test_all_inserted_elements_must_be_in_tree(self, tree):
        """test element must be in tree"""
        import random
        entries = list(range(128))
        random.shuffle(entries)

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
    def test_traversal(self, order, expected, tree):
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
    def test_empty_traversal(self, order, expected, tree):
        assert tuple(tree.traverse(order)) == expected

    def test_constructor_not_properly_called(self):
        with pytest.raises(TypeError) as context:
            BinarySearchTree(4)
        assert ("BinarySearchTree constructor called with incompatible data type: "
                "'int' object is not iterable" in str(context.value))

    def test_initialize_tree_from_sequence(self):
        entries = [5, 3, 8, 9, 1, 2]
        tree = BinarySearchTree(entries)

        assert tuple(tree.traverse('bfs')) == (5, 3, 8, 1, 9, 2)

    def test_find_max(self):
        entries = get_random_entries()
        tree = BinarySearchTree(entries)
        assert tree.max() == max(entries)

    def test_find_min(self):
        entries = get_random_entries()
        tree = BinarySearchTree(entries)
        assert tree.min() == min(entries)

    @pytest.mark.parametrize("entries,expected", [
        ([2, 1, 4, 3, 5], '(2 (1 () ()) (4 (3 () ()) (5 () ())))'),
        ([1, 2, 3, 4, 5], '(1 () (2 () (3 () (4 () (5 () ())))))'),
        ([], '()')
    ])
    def test_str_repr(self, entries, expected):
        tree = BinarySearchTree(entries)
        assert str(tree) == expected

    def test_delete_single_element(self):
        tree = BinarySearchTree([1])

        tree.delete(1)

        assert 1 not in tree
        assert not tree
        assert len(tree) == 0

    def test_delete_leaf_node(self):
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
    def test_delete_not_existent_entry(self, entries, entry_to_be_deleted):
        with pytest.raises(KeyError) as context:
            tree = BinarySearchTree(entries)
            tree.delete(entry_to_be_deleted)
        assert f"KeyError: {entry_to_be_deleted}" in str(context.value)

    def test_delete_entries_in_a_row(self):
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

    def test_equals(self):
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

    def test_clear(self):
        tree = BinarySearchTree([1, 2, 3, 4, 5])
        tree.clear()

        assert not tree

    def test_search(self):
        tree = BinarySearchTree([1, 2, 3, 4, 5])
        entry = tree.search(4)

        assert 4 == entry

    def test_search_complex_data_type(self):
        tree = BinarySearchTree([Entry(1, 'a'),
                                 Entry(4, 'b'),
                                 Entry(3, 'c'),
                                 Entry(3, 'd'), ])
        entry = tree.search(Entry(3, 'd'))

        assert Entry(3, 'd') == entry

        entry = Entry(3113, 'd')
        with pytest.raises(KeyError) as context:
            tree.search(entry)

        assert f"Entry {entry} not found." in str(context.value)

    def test_build_tree_from_other(self):
        original = BinarySearchTree([1, 2, 3, 4, 5])
        copy = BinarySearchTree(original)

        assert copy == BinarySearchTree([1, 2, 3, 4, 5])

    def test_copy(self):
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

    def test_length(self, tree):
        entries = sorted(list(range(150)))
        for entry in entries:
            tree.insert(entry)

        assert len(tree) == len(entries)

        assert len(BinarySearchTree()) == 0

    def test_pred(self):
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

    def test_succ(self):
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


class TestAVLTree:
    @pytest.fixture
    def tree(self):
        return AVLTree()

    def test_empty_tree(self, tree):
        assert not tree

    def test_insert_on_empty_tree(self, tree):
        tree.insert(9)

        assert tree.root.entry == 9
        assert tree.root.left.balance_factor == 0
        assert tree.root.right.balance_factor == 0
        assert tree

    def test_insert_duplicated_entry(self, tree):
        tree.insert(9)
        tree.insert(10)
        tree.insert(9)

        assert tree.root.entry == 9
        assert tree.root.right.entry == 10
        assert tree.height == 2
        assert tree

    def test_smaller_entry_on_the_left_of_root(self, tree):
        tree.insert(9)
        tree.insert(4)

        assert tree.root.entry == 9
        assert tree.root.left.entry == 4

    def test_greater_entry_on_the_right_of_root(self, tree):
        tree.insert(9)
        tree.insert(14)

        assert tree.root.entry == 9
        assert tree.root.right.entry == 14

    def test_recursive_insertion(self, tree):
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

    def test_height(self, tree):
        tree.insert(9)
        root = tree.root
        assert root.height == 1

        tree.insert(4)
        assert root.height == 2
        assert root.left.height == 1

        tree.insert(14)
        assert root.height == 2
        assert root.left.height == 1
        assert root.right.height == 1

        tree.insert(17)
        assert root.height == 3
        assert root.left.height == 1
        assert root.right.height == 2
        assert root.right.right.height == 1

        tree.insert(7)
        assert root.height == 3
        assert root.left.height == 2
        assert root.left.right.height == 1

    def test_balance_factor(self, tree):
        tree.insert(9)
        root = tree.root
        assert root.balance_factor == 0

        tree.insert(4)
        assert root.balance_factor == 1
        assert root.left.balance_factor == 0

        tree.insert(14)
        assert root.balance_factor == 0
        assert root.left.balance_factor == 0
        assert root.right.balance_factor == 0

        tree.insert(17)
        assert root.balance_factor == -1
        assert root.left.balance_factor == 0
        assert root.right.balance_factor == -1
        assert root.right.right.balance_factor == 0

        tree.insert(7)
        assert root.balance_factor == 0
        assert root.left.balance_factor == -1
        assert root.left.right.balance_factor == 0

    def test_single_left_rotation(self, tree):
        tree.insert(1)
        root = tree.root
        assert root.balance_factor == 0
        assert root.height == 1
        assert root.entry == 1

        tree.insert(2)
        root = tree.root
        assert root.balance_factor == -1
        assert root.height == 2
        assert root.entry == 1
        assert root.right.entry == 2

        tree.insert(3)
        root = tree.root
        assert root.balance_factor == 0
        assert root.left.balance_factor == 0
        assert root.right.balance_factor == 0
        assert root.height == 2

        assert root.entry == 2
        assert root.left.entry == 1
        assert root.right.entry == 3

    def test_single_right_rotation(self, tree):
        tree.insert(3)
        root = tree.root
        assert root.balance_factor == 0
        assert root.height == 1
        assert root.entry == 3

        tree.insert(2)
        root = tree.root
        assert root.balance_factor == 1
        assert root.height == 2
        assert root.entry == 3
        assert root.left.entry == 2

        tree.insert(1)
        root = tree.root
        assert root.balance_factor == 0
        assert root.left.balance_factor == 0
        assert root.right.balance_factor == 0
        assert root.height == 2

        assert root.entry == 2
        assert root.left.entry == 1
        assert root.right.entry == 3

    def test_left_right_rotation(self, tree):
        tree.insert(3)
        root = tree.root
        assert root.balance_factor == 0
        assert root.height == 1
        assert root.entry == 3

        tree.insert(1)
        root = tree.root
        assert root.balance_factor == 1
        assert root.height == 2
        assert root.entry == 3
        assert root.left.entry == 1

        tree.insert(2)
        root = tree.root
        assert root.balance_factor == 0
        assert root.left.balance_factor == 0
        assert root.right.balance_factor == 0
        assert root.height == 2

        assert root.entry == 2
        assert root.left.entry == 1
        assert root.right.entry == 3

    def test_right_left_rotation(self):
        tree = AVLTree()
        tree.insert(1)
        root = tree.root
        assert root.balance_factor == 0
        assert root.height == 1
        assert root.entry == 1

        tree.insert(3)
        root = tree.root
        assert root.balance_factor == -1
        assert root.height == 2
        assert root.entry == 1
        assert root.right.entry == 3

        tree.insert(2)
        root = tree.root
        assert root.balance_factor == 0
        assert root.left.balance_factor == 0
        assert root.right.balance_factor == 0
        assert root.height == 2

        assert root.entry == 2
        assert root.left.entry == 1
        assert root.right.entry == 3

    def test_advanced_right_rotation(self):
        tree = AVLTree()
        tree.insert(8)
        root = tree.root
        assert root.balance_factor == 0
        assert root.height == 1
        assert root.entry == 8

        tree.insert(5)
        root = tree.root

        assert root.balance_factor == 1
        assert root.height == 2
        assert root.entry == 8
        assert root.left.entry == 5

        tree.insert(11)
        root = tree.root

        assert root.balance_factor == 0
        assert root.height == 2
        assert root.entry == 8
        assert root.right.entry == 11

        tree.insert(4)
        root = tree.root

        assert root.balance_factor == 1
        assert root.height == 3
        assert root.entry == 8
        assert root.left.left.entry == 4

        tree.insert(7)
        root = tree.root

        assert root.balance_factor == 1
        assert root.height == 3
        assert root.entry == 8
        assert root.left.right.entry == 7

        tree.insert(2)
        root = tree.root

        assert root.balance_factor == 0
        assert root.height == 3
        assert root.entry == 5
        assert root.left.entry == 4
        assert root.right.entry == 8
        assert root.left.left.entry == 2
        assert root.right.right.entry == 11
        assert root.right.left.entry == 7

    def test_advanced_left_rotation(self):
        tree = AVLTree()
        tree.insert(20)
        root = tree.root
        assert root.balance_factor == 0
        assert root.height == 1
        assert root.entry == 20

        tree.insert(10)
        root = tree.root

        assert root.balance_factor == 1
        assert root.height == 2
        assert root.entry == 20
        assert root.left.entry == 10

        tree.insert(25)
        root = tree.root

        assert root.balance_factor == 0
        assert root.height == 2
        assert root.entry == 20
        assert root.right.entry == 25

        tree.insert(23)
        root = tree.root

        assert root.balance_factor == -1
        assert root.height == 3
        assert root.entry == 20
        assert root.right.left.entry == 23

        tree.insert(29)
        root = tree.root

        assert root.balance_factor == -1
        assert root.height == 3
        assert root.entry == 20
        assert root.right.right.entry == 29

        tree.insert(30)
        root = tree.root

        assert root.balance_factor == 0
        assert root.height == 3
        assert root.entry == 25
        assert root.left.entry == 20
        assert root.right.entry == 29
        assert root.left.left.entry == 10
        assert root.right.right.entry == 30
        assert root.left.right.entry == 23

    def test_traversal(self, tree):
        tree.insert(20)
        tree.insert(10)
        tree.insert(25)
        tree.insert(23)
        tree.insert(29)
        tree.insert(30)

        d = {
            'preorder': (25, 20, 10, 23, 29, 30),
            'inorder': (10, 20, 23, 25, 29, 30),
            'postorder': (10, 23, 20, 30, 29, 25),
            'bfs': (25, 20, 29, 10, 23, 30),
        }

        for order, expected_value in d.items():
            assert tuple(tree.traverse(order)) == expected_value

    def test_empty_traversal(self, tree):
        d = {
            'preorder': (),
            'inorder': (),
            'postorder': (),
            'bfs': (),
        }

        for order, expected_value in d.items():
            assert tuple(tree.traverse(order)) == expected_value

    def test_length(self, tree):
        entries = range(150)
        for entry in entries:
            tree.insert(entry)
        assert len(tree) == len(entries)
        assert len(AVLTree()) == 0

    def test_contains(self):
        assert 10 not in AVLTree()

        tree = AVLTree()
        tree.insert(10)

        assert 10 in tree

        entries = range(128)

        tree = AVLTree()

        for entry in entries:
            tree.insert(entry)

        for entry in entries:
            assert entry in tree

    def test_balanced_tree_must_have_height_of_log2(self):
        import math
        base = 2

        for exp in range(2, 13):
            tree1 = AVLTree()
            tree2 = AVLTree()
            tree3 = AVLTree()

            entries = [i for i in range(base ** exp)]
            for entry in entries:
                tree1.insert(entry)
                if entry == 0:
                    continue
                tree2.insert(entry)
                if entry == 1:
                    continue
                tree3.insert(entry)

            assert tree1.height == int(math.log2(len(entries))) + 1
            assert len(tree1) == len(entries)
            assert tree2.height == int(math.log2(len(entries)))
            assert len(tree2) == len(entries) - 1
            assert tree3.height == int(math.log2(len(entries)))
            assert len(tree3) == len(entries) - 2

    def test_initialize_tree_from_sequence(self):
        import math
        entries = [1, 2, 3, 4, 5, 6, 7]
        tree = AVLTree(entries)

        expected_order = (4, 2, 6, 1, 3, 5, 7)
        assert tuple(tree.traverse('bfs')) == expected_order
        assert len(tree) == len(entries)
        assert tree.height == math.ceil(math.log2(len(entries)))

    def test_constructor_not_properly_called(self):
        with pytest.raises(TypeError) as context:
            AVLTree(4)
        assert ("AVLTree constructor called with incompatible data type: "
                "'int' object is not iterable" in str(context.value))

    def test_find_max(self):
        entries = get_random_entries()
        tree = AVLTree(entries)
        assert tree.max() == max(entries)

    def test_find_min(self):
        entries = get_random_entries()
        tree = AVLTree(entries)
        assert tree.min() == min(entries)

    def test_delete_single_element(self):
        tree = AVLTree([1])

        tree.delete(1)

        assert 1 not in tree
        assert not tree
        assert len(tree) == 0

    def test_delete_leaf_node(self):
        tree = AVLTree([1, 2])

        tree.delete(2)

        assert 1 in tree
        assert 2 not in tree
        assert tree
        assert len(tree) == 1

    def test_delete_not_existent_entry(self):
        self.assert_entry_error([1, 2, 3], 10)
        self.assert_entry_error(None, 10)

    def assert_entry_error(self, entries, entry_to_be_deleted):
        with pytest.raises(KeyError) as context:
            tree = AVLTree(entries)
            tree.delete(entry_to_be_deleted)
            assert f"entryError: {entry_to_be_deleted}" in str(context.value)

    def test_delete_entry_but_tree_remains_balanced(self):
        entries = [10, 5, 11, 3, 7, 15]
        tree = AVLTree(entries)
        entry_to_be_deleted = 10

        tree.delete(entry_to_be_deleted)

        expected_order = (7, 5, 11, 3, 15)
        assert entry_to_be_deleted not in tree
        assert tuple(tree.traverse('bfs')) == expected_order

    def test_delete_entry_make_tree_unbalanced(self):
        entries = [5, 3, 8, 2, 4, 7, 11, 1, 6, 10, 12, 9]
        tree = AVLTree(entries)
        entry_to_be_deleted = 4

        tree.delete(entry_to_be_deleted)

        expected_order = (8, 5, 11, 2, 7, 10, 12, 1, 3, 6, 9)
        assert entry_to_be_deleted not in tree
        assert tuple(tree.traverse('bfs')) == expected_order

    def test_delete_entries_in_a_row(self):
        entries = [2, 1, 4, 3, 5]
        tree = AVLTree(entries)

        tree.delete(1)
        assert 1 not in tree
        assert tuple(tree.traverse('bfs')), (4, 2, 5 == 3)

        tree.delete(2)
        assert 2 not in tree
        assert tuple(tree.traverse('bfs')), (4, 3 == 5)

        tree.delete(3)
        assert 3 not in tree
        assert tuple(tree.traverse('bfs')), (4 == 5)

        tree.delete(4)
        assert 4 not in tree
        assert tuple(tree.traverse('bfs')) == (5,)

        tree.delete(5)
        assert 5 not in tree
        assert tuple(tree.traverse('bfs')) == ()
        assert not tree

    def test_str_repr(self):
        tree = AVLTree([1, 2, 3, 4, 5])
        assert repr(tree), 'AVLTree([2, 1, 4, 3 == 5])'
        assert str(tree), 'AVLTree([2, 1, 4, 3 == 5])'

    def test_equals(self):
        tree1 = AVLTree([1, 2, 3, 4, 5])
        tree2 = AVLTree([2, 1, 4, 3, 5])
        tree3 = AVLTree([1, 2, 3, 4, 5, 6])

        assert tree1 == tree2
        assert tree1 is not tree2
        assert tree1 != tree3
        assert tree1 is not tree3
        assert tree2 != tree3
        assert tree2 is not tree3
        assert tree1 != int(9)
        assert tree1 != AVLTree()

    def test_clear(self):
        tree = AVLTree([1, 2, 3, 4, 5])
        tree.clear()

        assert not tree

    def test_build_tree_from_other(self):
        original = AVLTree([1, 2, 3, 4, 5])
        copy = AVLTree(original)

        assert copy == AVLTree([2, 1, 4, 3, 5])

    def test_search(self):
        tree = AVLTree([1, 2, 3, 4, 5])
        entry = tree.search(4)

        assert 4 == entry

    def test_search_complex_data_type(self):
        tree = AVLTree([Entry(1, 'a'),
                        Entry(2, 'b'),
                        Entry(3, 'c'),
                        Entry(3, 'd'), ])
        entry = tree.search(Entry(3, 'd'))

        assert Entry(3, 'd') == entry

        entry = Entry(3113, 'd')
        with pytest.raises(KeyError) as context:
            tree.search(entry)
        assert f"Entry {entry} not found." in str(context.value)

    def test_copy(self):
        import copy
        single_entry = Entry(1, ['a'])
        tree1 = AVLTree([single_entry,
                         Entry(2, 'b'),
                         Entry(3, 'c'),
                         Entry(3, 'd'), ])
        tree2 = copy.copy(tree1)
        assert tree1 == tree2
        single_entry.b = 'a'
        assert tree1 == tree2

    def test_pred(self):
        import random
        random.seed(7477)
        entries = get_random_entries()
        tree = AVLTree(entries)

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

    def test_succ(self):
        import random
        random.seed(7477)
        entries = get_random_entries()
        tree = AVLTree(entries)
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
