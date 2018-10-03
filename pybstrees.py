class EmptyBSTNode:
    def __init__(self):
        self.height = 0

    def insert(self, entry):
        return BSTNode(entry)

    def __bool__(self):
        return False

    def __len__(self):
        """The lenght of a empty node is always 0."""
        return 0


EMPTY_NODE = EmptyBSTNode()


class BSTNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = EMPTY_NODE
        self.right = EMPTY_NODE
        self.height = 1

    def insert(self, entry):
        if entry > self.entry:
            self.right = self.right.insert(entry)
        elif entry < self.entry:
            self.left = self.left.insert(entry)

        self._update_height()

        return self

    def __bool__(self):
        return True

    def __len__(self) -> int:
        """Return the number of elements in this subtree."""
        return 1 + len(self.left) + len(self.right)

    def _update_height(self):
        self.height = 1 + max(self.left.height, self.right.height)


class BinarySearchTree:

    def __init__(self):
        self.root = EMPTY_NODE

    def insert(self, entry):
        self.root = self.root.insert(entry)

    def __bool__(self):
        return bool(self.root)

    def __len__(self):
        """T.__len__() <==> len(x). Retuns the number of elements in the tree."""
        return len(self.root)

    def _search(self, entry):
        """Returns node.k if T has a entry k, else raise KeyError"""
        root = self.root

        while root:
            if entry > root.entry:
                root = root.right
            elif entry < root.entry:
                root = root.left
            else:
                return root

        raise KeyError(f'Entry {entry} not found.')

    def __contains__(self, entry):
        """k in T -> True if T has a entry k, else False"""
        try:
            self._search(entry)
            return True
        except KeyError:
            return False
