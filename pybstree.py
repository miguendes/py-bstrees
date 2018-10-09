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
from collections import deque


class EmptyBSTNode:
    def __init__(self):
        self.height = 0

    def insert(self, entry):
        return BSTNode(entry)

    def delete(self, entry):
        """Cannot delete a entry from a EmptyNode"""
        raise KeyError(f"KeyError: {entry}")

    def __str__(self):
        return ""

    def __bool__(self):
        return False

    def __len__(self):
        """The lenght of a empty node is always 0."""
        return 0

    def __eq__(self, other):
        """Checks if a EmptyNode is equal to other"""
        return isinstance(other, self.__class__)

    def clear(self):
        """Clears the whole subtree"""
        return EMPTY_NODE

    def pred(self, pred, entry):
        raise KeyError(f'Predecessor of {entry} not found.')

    def succ(self, pred, entry):
        raise KeyError(f'Successor of {entry} not found.')


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

    def delete(self, entry):
        """Deletes a entry from subtree."""
        if entry > self.entry:
            self.right = self.right.delete(entry)
        elif entry < self.entry:
            self.left = self.left.delete(entry)
        else:
            if self.is_leaf():
                return EMPTY_NODE

            if self.left:
                new_entry = self.left.max()
                self.entry = new_entry
                self.left = self.left.delete(new_entry)
            else:
                return self.right

        self._update_height()

        return self

    def is_leaf(self):
        """Checks if the node is a leaf node, i. e, if its siblings are empty."""
        return not (bool(self.left) or bool(self.right))

    def max(self):
        """Returns the max element in the subtree."""
        max_entry = self.entry
        right_node = self.right
        while right_node:
            max_entry = right_node.entry
            right_node = right_node.right

        return max_entry

    def min(self):
        """Returns the min element in the subtree."""
        min_entry = self.entry
        left_node = self.left
        while left_node:
            min_entry = left_node.entry
            left_node = left_node.left

        return min_entry

    def __str__(self):
        return f"{self.entry} ({str(self.left)}) ({str(self.right)})"

    def __bool__(self):
        return True

    def __len__(self) -> int:
        """Return the number of elements in this subtree."""
        return 1 + len(self.left) + len(self.right)

    def __eq__(self, other) -> bool:
        """Checks if two nodes are equal."""
        return self.entry == other.entry and self.left == other.left and self.right == other.right

    def clear(self):
        """Clears the whole subtree"""
        if self.is_leaf():
            return EMPTY_NODE
        self.left = self.left.clear()
        self.right = self.right.clear()

        return EMPTY_NODE

    def search(self, entry):
        """Returns node.k if T has a entry k, else raise KeyError"""
        root = self

        while root:
            if entry > root.entry:
                root = root.right
            elif entry < root.entry:
                root = root.left
            else:
                return root

        raise KeyError(f'Entry {entry} not found.')

    def pred(self, pred, entry):
        if entry > self.entry:
            return self.right.pred(self, entry)
        elif entry < self.entry:
            return self.left.pred(pred, entry)
        else:
            if self.left:
                return self.left.max()
            if pred:
                return pred.entry

            raise KeyError(f'Predecessor of {entry} not found.')

    def succ(self, succ, entry):
        if entry > self.entry:
            return self.right.succ(succ, entry)
        elif entry < self.entry:
            return self.left.succ(self, entry)
        else:
            if self.right:
                return self.right.min()
            if succ:
                return succ.entry

            raise KeyError(f'Successor of {entry} not found.')

    def _update_height(self):
        self.height = 1 + max(self.left.height, self.right.height)


class BinarySearchTree:

    def __init__(self, args=None):
        """Initialize the tree according to the arguments passed. """
        self.root = EMPTY_NODE

        self._init_tree(args)

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

    def pred(self, entry):
        return self.root.pred(EMPTY_NODE, entry)

    def succ(self, entry):
        return self.root.succ(EMPTY_NODE, entry)

    def traverse(self, order='inorder'):
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

    def _init_tree(self, args):
        """Initialize the tree according to the arguments passed. """
        self.root = EMPTY_NODE

        if args is not None:
            if isinstance(args, self.__class__):
                args = args.traverse('bfs')

            try:
                for entry in args:
                    self.insert(entry)
            except (ValueError, TypeError) as e:
                raise TypeError(f'{self.__class__.__name__} constructor called with '
                                f'incompatible data type: {e}')

    def __str__(self):
        return f"({str(self.root)})"

    @property
    def height(self) -> int:
        """Returns the height of the tree. When the tree is empty its height is zero."""
        return self.root.height

    def __eq__(self, other) -> bool:
        """Checks if two trees are equal. """
        if isinstance(other, self.__class__):
            if self.height == other.height and len(self) == len(other):
                return self.root == other.root
        return False

    def __copy__(self):
        """Returns a shallow copy of the tree."""
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def max(self):
        """T.max() -> get the maximum entry of T."""
        return self.root.max()

    def min(self):
        """T.min() -> get the minimum entry of T."""
        return self.root.min()

    def delete(self, entry):
        """T.remove(entry) remove item <entry> from tree."""
        self.root = self.root.delete(entry)

    def clear(self):
        """T.clear() -> Removes all entries of T leaving it empty."""
        self.root = self.root.clear()

    def search(self, entry):
        """Returns k if T has a entry k, else raise KeyError"""
        return self.root.search(entry).entry