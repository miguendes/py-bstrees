import unittest

from pybstrees import BinarySearchTree


class BinarySearchTreeTest(unittest.TestCase):
    def test_empty_tree(self):
        tree = BinarySearchTree()
        self.assertFalse(tree)
