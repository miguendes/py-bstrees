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
