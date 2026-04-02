"""
Singly Linked List — Student Stub File

Implement each method so that the test suite in test_linked_list.py passes.
Every method currently raises NotImplementedError; replace each one with
your implementation. Do NOT change the method signatures.
"""


class Node:
    """A node in a singly linked list."""

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def __repr__(self):
        return f"Node({self.value!r})"


class LinkedList:
    """A singly linked list."""

    def __init__(self, iterable=None):
        """Initialize the list, optionally from an iterable.

        Hint: store the first node as self.head (some tests access it directly).
        """
        self.head = Node(None)
        self.tail = self.head
        self.len = 0

        if iterable:
            for i in iterable:
                self.push_back(i)

    def __len__(self):
        """Return the number of elements in the list."""
        return self.len

    def __iter__(self):
        """Iterate over the values in the list."""
        n = self.head.next
        while n:
            yield n.value
            n = n.next

    def __repr__(self):
        """Return a string like LinkedList([1, 2, 3])."""
        string = 'LinkedList('
        string += str([item for item in self])
        string += ')'
        return string

    def __contains__(self, value):
        """Return True if value is in the list."""
        for i in self:
            if i == value:
                return True
        return False

    def __eq__(self, other):
        """Return True if other is a LinkedList with the same values in the same order."""
        if type(self) != type(other):
            return False
        try:
            for i in range(max(len(self), len(other))):
                if self[i] != other[i]:
                    return False
            return True
        except:
            return False

    def __getitem__(self, index):
        """Return the value at the given index. Support negative indices.
        Raise IndexError if the index is out of range."""
        if index >= 0:
            if index >= len(self):
                raise IndexError
            cursor = self.head.next
            for _ in range(index):
                cursor = cursor.next
            return cursor.value
        else:
            if abs(index) > len(self):
                raise IndexError
            # do the reverse on the spot first maybe

    def __setitem__(self, index, value):
        """Set the value at the given index. Support negative indices.
        Raise IndexError if the index is out of range."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the list has no elements."""
        return True if len(self) == 0 else False

    def push_front(self, value):
        """Add a value to the front of the list. O(1)."""
        n = Node(value, self.head.next)
        self.head.next = n
        self.len += 1

    def push_back(self, value):
        """Add a value to the end of the list."""
        n = Node(value)
        self.tail.next = n
        self.tail = n
        self.len += 1

    def pop_front(self):
        """Remove and return the front value. Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError
        val = self.head.next.value
        self.head.next = self.head.next.next
        return val

    def pop_back(self):
        """Remove and return the last value. Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError
        raise NotImplementedError

    def insert(self, index, value):
        """Insert value at the given index. Raise IndexError if out of range.
        Inserting at index == len(self) is allowed (appends).
        Negative indices are supported (converted to positive, clamped to 0)."""
        raise NotImplementedError

    def remove(self, value):
        """Remove the first occurrence of value. Raise ValueError if not found."""
        raise NotImplementedError

    def clear(self):
        """Remove all elements from the list."""
        raise NotImplementedError

    def copy(self):
        """Return a new LinkedList that is a shallow copy of this list."""
        return LinkedList(self)

    def count(self, value):
        """Return the number of occurrences of value."""
        c = 0
        for i in self:
            if i == value:
                c += 1
        return c

    def index(self, value):
        """Return the index of the first occurrence of value.
        Raise ValueError if not found."""
        for i in range(len(self)):
            if self[i] == value:
                return i
        raise ValueError

    def reverse(self):
        """Reverse the list in-place. Modifies the list in-place. Returns None."""
        raise NotImplementedError

    def to_list(self):
        """Return a Python list of the values."""
        return [item for item in self]

    def sorted(self):
        """Return a new LinkedList with elements in sorted order.
        Do not mutate the original list."""
        l = [item for item in self]
        return LinkedList(sorted(l))

    def merge(self, other):
        """Return a new sorted LinkedList from two already-sorted LinkedLists.
        Do not mutate either original list."""
        l = [item for item in self] + [item for item in other]
        return LinkedList(sorted(l))

    def has_cycle(self):
        """Return True if there is a cycle in the list.
        Hint: look up Floyd's tortoise and hare algorithm."""
        raise NotImplementedError

    def midpoint(self):
        """Return the value at the middle node.
        For even length, return the earlier middle.
        Raise IndexError if the list is empty."""
        raise NotImplementedError

    def remove_duplicates(self):
        """Remove duplicate values in-place, keeping the first occurrence.
        Modifies the list in-place. Returns None."""
        raise NotImplementedError
