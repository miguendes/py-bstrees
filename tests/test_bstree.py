from pybstrees import BinarySearchTree


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
