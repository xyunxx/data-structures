# TDD Challenge: Build Your Own Standard Library

You're given five data structures, each with a fully stubbed-out class and a
massive test suite. Every method raises `NotImplementedError`. Your job:
**make the tests pass.**

## Getting Started

```bash
cd tdd-challenge

# Run one test suite (start here):
uv run --with pytest python -m pytest test_linked_list.py -v

# Run a single test class to focus:
uv run --with pytest python -m pytest test_linked_list.py::TestPushFront -v

# Run the scoreboard to see your progress across all five:
uv run run_score.py
```

Open the stub file (e.g., `linked_list.py`), read the docstrings, and start
implementing. The tests will tell you exactly what's expected.

## Suggested Order

Each data structure builds on the ideas (and optionally the code) of the
previous one:

| # | File | Tests | What you'll build |
|---|---|---|---|
| 1 | `linked_list.py` | 213 | Singly-linked list with 26 methods |
| 2 | `stack_queue.py` | 171 | Stack (LIFO) + Queue (FIFO) |
| 3 | `deque.py` | 155 | Double-ended queue (doubly-linked) |
| 4 | `binary_search_tree.py` | 208 | BST with floor/ceiling/range queries |
| 5 | `hash_map.py` | 165 | Hash table with separate chaining |

**Start with LinkedList.** Once it's solid, you can import it in your Stack,
Queue, and even HashMap implementations instead of building from scratch:

```python
from linked_list import LinkedList

class Stack:
    def __init__(self):
        self._data = LinkedList()

    def push(self, value):
        self._data.push_front(value)

    def pop(self):
        return self._data.pop_front()
    # ...
```

This is composability in action: a well-tested building block that you can
reuse with confidence.

## Rules

- Don't change the method signatures (names, parameters, return types).
- Don't modify the test files.
- Don't use Python's built-in `collections.deque`, `dict`, or `list` as your
  backing store (the whole point is to build these yourself).
- You *can* import and use your own earlier implementations.

## Tips

- **Read the docstrings.** They tell you what to return, what exceptions to
  raise, and what edge cases to handle.
- **Run tests often.** Implement one method, run the tests, watch your count
  climb.
- **Start with the simple methods** (`__len__`, `is_empty`, `push_front`) and
  build up.
- If you're stuck on a test, read it! The test file is not secret — it shows
  you exactly what inputs and outputs are expected.
