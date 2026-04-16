"""Stack and Queue implementations using linked-list internals.

Students: implement every method below. Both Stack and Queue must use
a linked-list structure internally — do NOT use a Python list as the
backing store.

Two approaches are valid:
  1. Build from scratch using the _Node inner class provided in each class.
  2. Import and wrap your LinkedList: from linked_list import LinkedList
Both are fine. Option 2 is a great exercise in composability!
"""

from linked_list import LinkedList

class Stack:
    """Last-In, First-Out (LIFO) collection backed by a singly-linked list."""

    class _Node:
        __slots__ = ("value", "next")

        def __init__(self, value, next_node=None):
            self.value = value
            self.next = next_node

    def __init__(self):
        raise NotImplementedError

    # --- Size / emptiness -------------------------------------------------

    def __len__(self):
        """Return the number of elements. Enables len(s)."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the structure contains no elements."""
        raise NotImplementedError

    # --- Core operations --------------------------------------------------

    def push(self, value):
        """Push *value* onto the top of the stack."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top element.

        Raises IndexError if the stack is empty.
        """
        raise NotImplementedError

    def peek(self):
        """Return the top element without removing it.

        Raises IndexError if the stack is empty.
        """
        raise NotImplementedError

    def clear(self):
        """Remove all elements from the stack."""
        raise NotImplementedError

    # --- Conversion / iteration -------------------------------------------

    def to_list(self):
        """Return a plain Python list of elements, top first."""
        raise NotImplementedError

    def __iter__(self):
        """Iterate from top to bottom."""
        raise NotImplementedError

    def __repr__(self):
        """e.g. Stack([3, 2, 1]) where 3 is the top."""
        raise NotImplementedError

    def __contains__(self, value):
        """Return True if value is in the structure. Enables the `in` operator."""
        raise NotImplementedError

    def __eq__(self, other):
        """Return True if other is a Stack with the same elements in the same order."""
        raise NotImplementedError


class Queue:
    """First-In, First-Out (FIFO) collection backed by a singly-linked list."""

    class _Node:
        __slots__ = ("value", "next")

        def __init__(self, value, next_node=None):
            self.value = value
            self.next = next_node

    def __init__(self):
        raise NotImplementedError

    # --- Size / emptiness -------------------------------------------------

    def __len__(self):
        """Return the number of elements. Enables len(s)."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the structure contains no elements."""
        raise NotImplementedError

    # --- Core operations --------------------------------------------------

    def enqueue(self, value):
        """Add *value* to the back of the queue."""
        raise NotImplementedError

    def dequeue(self):
        """Remove and return the front element.

        Raises IndexError if the queue is empty.
        """
        raise NotImplementedError

    def peek(self):
        """Return the front element without removing it.

        Raises IndexError if the queue is empty.
        """
        raise NotImplementedError

    def clear(self):
        """Remove all elements from the queue."""
        raise NotImplementedError

    # --- Conversion / iteration -------------------------------------------

    def to_list(self):
        """Return a plain Python list of elements, front first."""
        raise NotImplementedError

    def __iter__(self):
        """Iterate from front to back."""
        raise NotImplementedError

    def __repr__(self):
        """e.g. Queue([1, 2, 3]) where 1 is the front."""
        raise NotImplementedError

    def __contains__(self, value):
        """Return True if value is in the structure. Enables the `in` operator."""
        raise NotImplementedError

    def __eq__(self, other):
        """Return True if other is a Queue with the same elements in the same order."""
        raise NotImplementedError
