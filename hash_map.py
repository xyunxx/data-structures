"""HashMap implementation using separate chaining.

You must use separate chaining (an array/list of buckets). Use Python's
built-in hash() function for hashing keys. Do NOT use a Python dict
anywhere in your implementation.

Bonus: you can import and use your LinkedList for the bucket chains!
"""


class HashMap:
    """A hash map (associative array) that resolves collisions via separate chaining.

    Each bucket is a linked list (or plain Python list) of [key, value] pairs.
    The table automatically resizes when the load factor exceeds the threshold.
    """

    def __init__(self, capacity=8, load_factor_threshold=0.75):
        """Initialise an empty HashMap.

        Parameters
        ----------
        capacity : int
            Number of buckets in the underlying array.
        load_factor_threshold : float
            When len / capacity exceeds this value, the table doubles in size.
        """
        raise NotImplementedError

    # --- Size / emptiness ---------------------------------------------------

    def __len__(self):
        """Return the number of key-value pairs stored in the map."""
        raise NotImplementedError

    def __bool__(self):
        """Return True if the map is non-empty."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the map contains no key-value pairs."""
        raise NotImplementedError

    # --- Representation -----------------------------------------------------

    def __repr__(self):
        """Return a string like ``HashMap({key1: value1, key2: value2})``."""
        raise NotImplementedError

    # --- Lookup -------------------------------------------------------------

    def __contains__(self, key):
        """Return True if *key* is present in the map."""
        raise NotImplementedError

    def __getitem__(self, key):
        """Return the value associated with *key*.

        Raises KeyError if the key is not found.
        """
        raise NotImplementedError

    def get(self, key, default=None):
        """Return the value for *key* if present, otherwise *default*."""
        raise NotImplementedError

    # --- Mutation -----------------------------------------------------------

    def __setitem__(self, key, value):
        """Set *key* to *value*, inserting or updating as needed.

        If the load factor exceeds the threshold after insertion, the
        table is resized (doubled).
        """
        raise NotImplementedError

    def put(self, key, value):
        """Set *key* to *value* (alias for ``__setitem__``)."""
        raise NotImplementedError

    def __delitem__(self, key):
        """Remove the entry for *key*.

        Raises KeyError if the key is not found.
        """
        raise NotImplementedError

    def remove(self, key):
        """Remove *key* and return its value.

        Raises KeyError if the key is not found.
        """
        raise NotImplementedError

    def clear(self):
        """Remove all key-value pairs, keeping the current capacity."""
        raise NotImplementedError

    def pop(self, key, *args):
        """Remove *key* and return its value.

        If *key* is not found and a default is provided, return the default.
        If *key* is not found and no default is provided, raise KeyError.
        """
        raise NotImplementedError

    def setdefault(self, key, default=None):
        """If *key* is present, return its value.

        Otherwise, set *key* to *default* and return *default*.
        """
        raise NotImplementedError

    def update(self, other):
        """Update the map from *other* (a HashMap or a dict)."""
        raise NotImplementedError

    # --- Equality -----------------------------------------------------------

    def __eq__(self, other):
        """Return True if *other* contains exactly the same key-value pairs.

        Two HashMaps are equal if they have the same pairs, regardless
        of internal capacity or insertion order.
        """
        raise NotImplementedError

    # --- Bulk access --------------------------------------------------------

    def keys(self):
        """Return a list of all keys."""
        raise NotImplementedError

    def values(self):
        """Return a list of all values."""
        raise NotImplementedError

    def items(self):
        """Return a list of ``(key, value)`` tuples."""
        raise NotImplementedError

    def __iter__(self):
        """Iterate over the keys of the map."""
        raise NotImplementedError

    # --- Copying ------------------------------------------------------------

    def copy(self):
        """Return a shallow copy of the map."""
        raise NotImplementedError

    # --- Internal metrics ---------------------------------------------------

    def load_factor(self):
        """Return the current load factor (len / capacity)."""
        raise NotImplementedError

    def capacity(self):
        """Return the current number of buckets."""
        raise NotImplementedError

    # --- Resizing -----------------------------------------------------------

    def resize(self, new_capacity):
        """Resize the table to *new_capacity* buckets, rehashing all entries."""
        raise NotImplementedError
