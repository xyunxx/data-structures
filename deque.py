"""
Double-Ended Queue (Deque) -- Student Stub File

Implement each method so that the test suite in test_deque.py passes.
Every method currently raises NotImplementedError; replace each one with
your implementation. Do NOT change the method signatures.

Your Deque MUST use a doubly-linked list internally (a _Node inner class
is provided). Do NOT use a Python list as the backing store.
"""


class Deque:
    """A double-ended queue backed by a doubly-linked list."""

    class _Node:
        __slots__ = ("value", "prev", "next")

        def __init__(self, value, prev=None, next_node=None):
            self.value = value
            self.prev = prev
            self.next = next_node

    def __init__(self, iterable=None):
        """Initialize the deque, optionally from an iterable."""
        raise NotImplementedError

    # --- Size / emptiness -------------------------------------------------

    def __len__(self):
        """Return the number of elements in the deque."""
        raise NotImplementedError

    def __bool__(self):
        """Return True if the deque is non-empty."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the deque has no elements."""
        raise NotImplementedError

    # --- Representation ---------------------------------------------------

    def __repr__(self):
        """Return a string like Deque([1, 2, 3]) where 1 is front."""
        raise NotImplementedError

    # --- Membership / equality --------------------------------------------

    def __contains__(self, value):
        """Return True if value is in the deque."""
        raise NotImplementedError

    def __eq__(self, other):
        """Return True if other is a Deque with the same values in order."""
        raise NotImplementedError

    # --- Indexing ----------------------------------------------------------

    def __getitem__(self, index):
        """Return the value at the given index. Support negative indices.

        Raises IndexError if the index is out of range.
        """
        raise NotImplementedError

    # --- Adding elements ---------------------------------------------------

    def append(self, value):
        """Add value to the back of the deque. O(1)."""
        raise NotImplementedError

    def appendleft(self, value):
        """Add value to the front of the deque. O(1)."""
        raise NotImplementedError

    def extend(self, iterable):
        """Add all elements from iterable to the back."""
        raise NotImplementedError

    def extendleft(self, iterable):
        """Add all elements from iterable to the front.

        Note: the order of elements from the iterable is reversed in the
        deque, matching collections.deque behavior. For example,
        extendleft([1, 2, 3]) on an empty deque gives Deque([3, 2, 1]).
        """
        raise NotImplementedError

    # --- Removing elements -------------------------------------------------

    def pop(self):
        """Remove and return the back element.

        Raises IndexError if the deque is empty.
        """
        raise NotImplementedError

    def popleft(self):
        """Remove and return the front element.

        Raises IndexError if the deque is empty.
        """
        raise NotImplementedError

    def remove(self, value):
        """Remove the first occurrence of value (searching front to back).

        Raises ValueError if value is not found.
        """
        raise NotImplementedError

    def clear(self):
        """Remove all elements from the deque."""
        raise NotImplementedError

    # --- Peeking -----------------------------------------------------------

    def peek_front(self):
        """Return the front element without removing it.

        Raises IndexError if the deque is empty.
        """
        raise NotImplementedError

    def peek_back(self):
        """Return the back element without removing it.

        Raises IndexError if the deque is empty.
        """
        raise NotImplementedError

    # --- Searching / counting ----------------------------------------------

    def count(self, value):
        """Return the number of occurrences of value."""
        raise NotImplementedError

    # --- Copying / conversion ----------------------------------------------

    def copy(self):
        """Return a shallow copy of the deque."""
        raise NotImplementedError

    def to_list(self):
        """Return a Python list of the values, front first."""
        raise NotImplementedError

    # --- Reordering --------------------------------------------------------

    def reverse(self):
        """Reverse the deque in-place."""
        raise NotImplementedError

    def rotate(self, n=1):
        """Rotate the deque n steps to the right.

        Positive n: the back element moves to the front.
        Negative n: the front element moves to the back.
        """
        raise NotImplementedError

    # --- Iteration ---------------------------------------------------------

    def __iter__(self):
        """Iterate from front to back."""
        raise NotImplementedError

    def __reversed__(self):
        """Iterate from back to front."""
        raise NotImplementedError
