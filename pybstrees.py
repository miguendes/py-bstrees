class EmptyBSTNode:
    def __init__(self):
        self.height = 0

    def __bool__(self):
        return False


EMPTY_NODE = EmptyBSTNode()


class BSTNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = EMPTY_NODE
        self.right = EMPTY_NODE

    def __bool__(self):
        return True


class BinarySearchTree:

    def __init__(self):
        self.root = EMPTY_NODE

    def __bool__(self):
        return bool(self.root)
