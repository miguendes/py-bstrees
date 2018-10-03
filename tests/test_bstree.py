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


def test_contains():
    import random
    """test empty tree should not contain any entry"""
    assert 10 not in BinarySearchTree()

    """test single element must be in tree"""
    tree = BinarySearchTree()
    tree.insert(10)

    assert 10 in tree

    """test element must be in tree"""
    entries = list(range(128))

    tree = BinarySearchTree()

    for entry in entries:
        tree.insert(entry)

    random.shuffle(entries)

    for entry in entries:
        assert entry in tree
