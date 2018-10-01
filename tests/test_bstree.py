import unittest

from pybstrees import BinarySearchTree


class BinarySearchTreeTest(unittest.TestCase):
    def test_empty_tree(self):
        tree = BinarySearchTree()
        self.assertFalse(tree)

    def test_insert_on_empty_tree(self):
        tree = BinarySearchTree()
        tree.insert(9)
        tree.insert(10)
        tree.insert(8)

        self.assertEqual(tree.root.entry, 9)
        self.assertEqual(tree.root.left.entry, 8)
        self.assertEqual(tree.root.right.entry, 10)
        self.assertTrue(tree)
