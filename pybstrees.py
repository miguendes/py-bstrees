from collections import deque


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

    def traverse(self, order):
        """Traverse the tree based on a given strategy.
        order : 'preorder' | 'postorder' | 'bfs' | default 'inorder'
            The traversal of the tree.
            Use 'preorder' to print the root first, then left and right subtree, respectively.
            Use 'postorder' to print the left and right subree first, then the root.
            Use 'bfs' to visit the tree in a breadth-first manner.
            The default is 'inorder' which prints the left subtree, the root and the right subtree.
        """
        if order == 'preorder':
            return self._preorder(self.root)
        elif order == 'postorder':
            return self._postorder(self.root)
        elif order == 'bfs':
            return self._bfs()
        else:
            return self._inorder(self.root)

    def _inorder(self, root):
        """Performs an in-order traversal. """
        if root:
            yield from self._inorder(root.left)
            yield root.entry
            yield from self._inorder(root.right)

    def _preorder(self, root):
        """Performs an pre-order traversal."""
        if root:
            yield root.entry
            yield from self._preorder(root.left)
            yield from self._preorder(root.right)

    def _postorder(self, root):
        """Performs an post-order traversal."""
        if root:
            yield from self._postorder(root.left)
            yield from self._postorder(root.right)
            yield root.entry

    def _bfs(self):
        """Performs an Breadth first traversal."""
        root = self.root

        if root:
            q = deque()
            q.append(root)

            while q:
                root = q.popleft()
                if not root:
                    continue

                yield root.entry
                left = root.left
                right = root.right

                q.append(left)
                q.append(right)
