"""
Binary Search Tree — Student Stub File

Implement each method so that the test suite in test_binary_search_tree.py
passes. Every method currently raises NotImplementedError; replace each one
with your implementation. Do NOT change the method signatures.

BST invariant: for every node, all values in its left subtree are strictly
less than the node's value, and all values in its right subtree are strictly
greater. Duplicate values are ignored on insert.
"""


class BSTNode:
    """A node in a binary search tree."""

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BSTNode({self.value!r})"


class BinarySearchTree:
    """A binary search tree that stores unique, comparable values."""

    def __init__(self, iterable=None):
        """Initialize the BST, optionally inserting each element of *iterable*.

        Hint: store the root node as self._root (some tests access it directly).
        """
        raise NotImplementedError

    # --- Size / emptiness ----------------------------------------------------

    def __len__(self):
        """Return the number of nodes in the tree."""
        raise NotImplementedError

    def __bool__(self):
        """Return True if the tree is non-empty."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the tree has no nodes."""
        raise NotImplementedError

    def size(self):
        """Return the number of nodes (same as __len__)."""
        raise NotImplementedError

    # --- Representation ------------------------------------------------------

    def __repr__(self):
        """Return a string like BinarySearchTree([1, 2, 3])."""
        raise NotImplementedError

    # --- Membership ----------------------------------------------------------

    def __contains__(self, value):
        """Return True if *value* is in the tree (uses BST search)."""
        raise NotImplementedError

    def search(self, value):
        """Return True if *value* is in the tree, False otherwise."""
        raise NotImplementedError

    # --- Equality ------------------------------------------------------------

    def __eq__(self, other):
        """Two BSTs are equal iff they have the same structure AND values."""
        raise NotImplementedError

    # --- Insertion / removal -------------------------------------------------

    def insert(self, value):
        """Insert *value* into the tree. Ignore duplicates."""
        raise NotImplementedError

    def remove(self, value):
        """Remove *value* from the tree.

        Raises ValueError if *value* is not found.
        For a node with two children, replace with its in-order successor.
        """
        raise NotImplementedError

    def clear(self):
        """Remove all nodes from the tree."""
        raise NotImplementedError

    # --- Min / Max -----------------------------------------------------------

    def min(self):
        """Return the minimum value.

        Raises ValueError if the tree is empty.
        """
        raise NotImplementedError

    def max(self):
        """Return the maximum value.

        Raises ValueError if the tree is empty.
        """
        raise NotImplementedError

    # --- Height --------------------------------------------------------------

    def height(self):
        """Return the height of the tree.

        Empty tree: -1.  Single node: 0.
        """
        raise NotImplementedError

    # --- Traversals ----------------------------------------------------------

    def inorder(self):
        """Return a list of values in in-order (left, root, right)."""
        raise NotImplementedError

    def preorder(self):
        """Return a list of values in pre-order (root, left, right)."""
        raise NotImplementedError

    def postorder(self):
        """Return a list of values in post-order (left, right, root)."""
        raise NotImplementedError

    def levelorder(self):
        """Return a list of values in level-order (breadth-first)."""
        raise NotImplementedError

    def __iter__(self):
        """Yield values in in-order (sorted order)."""
        raise NotImplementedError

    # --- Validation ----------------------------------------------------------

    def is_valid_bst(self):
        """Return True if the BST property holds for every node."""
        raise NotImplementedError

    # --- Successor / predecessor ---------------------------------------------

    def successor(self, value):
        """Return the in-order successor of *value*.

        Raises ValueError if *value* is not in the tree or has no successor.
        """
        raise NotImplementedError

    def predecessor(self, value):
        """Return the in-order predecessor of *value*.

        Raises ValueError if *value* is not in the tree or has no predecessor.
        """
        raise NotImplementedError

    # --- Floor / ceiling -----------------------------------------------------

    def floor(self, value):
        """Return the largest value in the tree that is <= *value*.

        The *value* itself does NOT need to be in the tree.
        Raises ValueError if no such value exists.
        """
        raise NotImplementedError

    def ceiling(self, value):
        """Return the smallest value in the tree that is >= *value*.

        The *value* itself does NOT need to be in the tree.
        Raises ValueError if no such value exists.
        """
        raise NotImplementedError

    # --- Range queries -------------------------------------------------------

    def range_query(self, low, high):
        """Return a sorted list of all values v where low <= v <= high."""
        raise NotImplementedError

    def kth_smallest(self, k):
        """Return the k-th smallest value (1-indexed).

        Raises ValueError if k is out of range or tree is empty.
        """
        raise NotImplementedError

    # --- Conversion ----------------------------------------------------------

    def to_sorted_list(self):
        """Return a sorted list of all values in the tree."""
        raise NotImplementedError
