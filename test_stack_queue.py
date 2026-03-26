"""Comprehensive test suite for Stack and Queue (linked-list backed).

Run with:  pytest test_stack_queue.py -v
"""

import time
from collections import deque

import pytest

from stack_queue import Queue, Stack


# ======================================================================
#  STACK TESTS
# ======================================================================


class TestStackConstruction:
    def test_new_stack_is_empty(self):
        s = Stack()
        assert s.is_empty()

    def test_new_stack_has_length_zero(self):
        s = Stack()
        assert len(s) == 0

    def test_new_stack_to_list_is_empty(self):
        s = Stack()
        assert s.to_list() == []

    def test_new_stack_repr(self):
        s = Stack()
        assert repr(s) == "Stack([])"


class TestStackPush:
    def test_push_single(self):
        s = Stack()
        s.push(1)
        assert len(s) == 1
        assert s.peek() == 1

    def test_push_multiple_maintains_lifo(self):
        s = Stack()
        for v in [1, 2, 3]:
            s.push(v)
        assert s.peek() == 3
        assert s.to_list() == [3, 2, 1]

    def test_push_returns_none(self):
        s = Stack()
        assert s.push(42) is None

    def test_push_various_types(self):
        s = Stack()
        s.push(1)
        s.push("hello")
        s.push([1, 2])
        s.push(None)
        assert len(s) == 4
        assert s.peek() is None

    def test_push_after_pop(self):
        s = Stack()
        s.push(1)
        s.pop()
        s.push(2)
        assert s.peek() == 2
        assert len(s) == 1

    def test_push_many(self):
        s = Stack()
        for i in range(100):
            s.push(i)
        assert len(s) == 100
        assert s.peek() == 99


class TestStackPop:
    def test_pop_single(self):
        s = Stack()
        s.push(42)
        assert s.pop() == 42
        assert s.is_empty()

    def test_pop_returns_lifo_order(self):
        s = Stack()
        for v in [1, 2, 3]:
            s.push(v)
        assert s.pop() == 3
        assert s.pop() == 2
        assert s.pop() == 1

    def test_pop_empty_raises_index_error(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_pop_until_empty_then_raises(self):
        s = Stack()
        s.push(1)
        s.pop()
        with pytest.raises(IndexError):
            s.pop()

    def test_push_pop_interleaving(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        s.push(3)
        assert s.pop() == 3
        assert s.pop() == 1

    def test_pop_decrements_length(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.pop()
        assert len(s) == 1

    def test_pop_all_then_push_again(self):
        s = Stack()
        s.push(10)
        s.push(20)
        s.pop()
        s.pop()
        s.push(30)
        assert s.peek() == 30
        assert len(s) == 1


class TestStackPeek:
    def test_peek_returns_top(self):
        s = Stack()
        s.push(5)
        assert s.peek() == 5

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(5)
        s.peek()
        assert len(s) == 1

    def test_peek_empty_raises_index_error(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.peek()

    def test_peek_after_push(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.peek() == 2

    def test_peek_after_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.pop()
        assert s.peek() == 1

    def test_peek_multiple_times_same_value(self):
        s = Stack()
        s.push(99)
        assert s.peek() == 99
        assert s.peek() == 99
        assert s.peek() == 99
        assert len(s) == 1


class TestStackLen:
    def test_empty(self):
        assert len(Stack()) == 0

    def test_after_pushes(self):
        s = Stack()
        for i in range(5):
            s.push(i)
        assert len(s) == 5

    def test_after_pops(self):
        s = Stack()
        for i in range(5):
            s.push(i)
        s.pop()
        s.pop()
        assert len(s) == 3

    def test_after_clear(self):
        s = Stack()
        s.push(1)
        s.clear()
        assert len(s) == 0


class TestStackIsEmpty:
    def test_new_stack(self):
        assert Stack().is_empty()

    def test_after_push(self):
        s = Stack()
        s.push(1)
        assert not s.is_empty()

    def test_after_push_and_pop(self):
        s = Stack()
        s.push(1)
        s.pop()
        assert s.is_empty()

    def test_after_clear(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.clear()
        assert s.is_empty()


class TestStackContains:
    def test_present(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert 2 in s

    def test_absent(self):
        s = Stack()
        s.push(1)
        assert 99 not in s

    def test_empty(self):
        assert 1 not in Stack()

    def test_contains_none(self):
        s = Stack()
        s.push(None)
        assert None in s

    def test_contains_after_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.pop()
        assert 2 not in s
        assert 1 in s


class TestStackEquality:
    def test_equal_stacks(self):
        a = Stack()
        b = Stack()
        for v in [1, 2, 3]:
            a.push(v)
            b.push(v)
        assert a == b

    def test_different_values(self):
        a = Stack()
        b = Stack()
        a.push(1)
        b.push(2)
        assert a != b

    def test_different_lengths(self):
        a = Stack()
        b = Stack()
        a.push(1)
        a.push(2)
        b.push(1)
        assert a != b

    def test_empty_stacks_equal(self):
        assert Stack() == Stack()

    def test_same_values_different_order(self):
        a = Stack()
        b = Stack()
        a.push(1)
        a.push(2)
        b.push(2)
        b.push(1)
        assert a != b

    def test_not_equal_to_non_stack(self):
        s = Stack()
        s.push(1)
        assert s != [1]
        assert s != "not a stack"

    def test_equality_is_symmetric(self):
        a = Stack()
        b = Stack()
        a.push(1)
        b.push(1)
        assert a == b
        assert b == a


class TestStackIter:
    def test_top_to_bottom_order(self):
        s = Stack()
        for v in [1, 2, 3]:
            s.push(v)
        assert list(s) == [3, 2, 1]

    def test_multiple_iterations(self):
        s = Stack()
        s.push(1)
        s.push(2)
        first = list(s)
        second = list(s)
        assert first == second == [2, 1]

    def test_empty_iter(self):
        assert list(Stack()) == []

    def test_iter_does_not_modify(self):
        s = Stack()
        s.push(10)
        s.push(20)
        _ = list(s)
        assert len(s) == 2
        assert s.peek() == 20

    def test_for_loop(self):
        s = Stack()
        for v in [5, 10, 15]:
            s.push(v)
        total = 0
        for v in s:
            total += v
        assert total == 30


class TestStackRepr:
    def test_empty(self):
        assert repr(Stack()) == "Stack([])"

    def test_one_element(self):
        s = Stack()
        s.push(42)
        assert repr(s) == "Stack([42])"

    def test_multiple_elements_top_first(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert repr(s) == "Stack([3, 2, 1])"

    def test_string_elements(self):
        s = Stack()
        s.push("a")
        s.push("b")
        assert repr(s) == "Stack(['b', 'a'])"


class TestStackClear:
    def test_clear_non_empty(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.clear()
        assert s.is_empty()
        assert len(s) == 0

    def test_clear_already_empty(self):
        s = Stack()
        s.clear()
        assert s.is_empty()

    def test_usable_after_clear(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.clear()
        s.push(3)
        assert s.peek() == 3
        assert len(s) == 1

    def test_clear_resets_to_list(self):
        s = Stack()
        s.push(1)
        s.clear()
        assert s.to_list() == []


class TestStackToList:
    def test_empty(self):
        assert Stack().to_list() == []

    def test_one_element(self):
        s = Stack()
        s.push(7)
        assert s.to_list() == [7]

    def test_multiple_top_first(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert s.to_list() == [3, 2, 1]

    def test_to_list_returns_new_list(self):
        s = Stack()
        s.push(1)
        lst = s.to_list()
        lst.append(999)
        assert s.to_list() == [1]

    def test_to_list_does_not_modify_stack(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.to_list()
        assert len(s) == 2
        assert s.peek() == 2


class TestStackStress:
    def test_push_pop_100k(self):
        s = Stack()
        n = 100_000
        for i in range(n):
            s.push(i)
        assert len(s) == n
        for i in range(n - 1, -1, -1):
            assert s.pop() == i
        assert s.is_empty()

    def test_push_o1_time(self):
        s = Stack()
        n = 100_000
        start = time.perf_counter()
        for i in range(n):
            s.push(i)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"100k pushes took {elapsed:.2f}s (expected < 1s)"

    def test_pop_o1_time(self):
        s = Stack()
        n = 100_000
        for i in range(n):
            s.push(i)
        start = time.perf_counter()
        for _ in range(n):
            s.pop()
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"100k pops took {elapsed:.2f}s (expected < 1s)"

    def test_interleaved_push_pop_at_scale(self):
        s = Stack()
        n = 100_000
        for i in range(n):
            s.push(i)
            if i % 2 == 1:
                s.pop()
        assert len(s) == n // 2


class TestStackIntegration:
    """Real-world algorithms implemented with a Stack."""

    def _balanced_parentheses(self, expr):
        """Return True if parentheses/brackets/braces are balanced."""
        s = Stack()
        matching = {")": "(", "]": "[", "}": "{"}
        for ch in expr:
            if ch in "([{":
                s.push(ch)
            elif ch in ")]}":
                if s.is_empty():
                    return False
                if s.pop() != matching[ch]:
                    return False
        return s.is_empty()

    def test_balanced_simple(self):
        assert self._balanced_parentheses("()")

    def test_balanced_nested(self):
        assert self._balanced_parentheses("({[]})")

    def test_balanced_sequential(self):
        assert self._balanced_parentheses("()[]{}()")

    def test_balanced_empty(self):
        assert self._balanced_parentheses("")

    def test_unbalanced_open(self):
        assert not self._balanced_parentheses("(")

    def test_unbalanced_close(self):
        assert not self._balanced_parentheses(")")

    def test_unbalanced_mismatch(self):
        assert not self._balanced_parentheses("(]")

    def test_unbalanced_complex(self):
        assert not self._balanced_parentheses("({)}")

    def test_balanced_with_other_chars(self):
        assert self._balanced_parentheses("a * (b + c) - {d / [e]}")

    def _postfix_eval(self, expression):
        """Evaluate a postfix expression string. Tokens separated by spaces."""
        s = Stack()
        ops = {"+", "-", "*", "/"}
        for token in expression.split():
            if token in ops:
                b = s.pop()
                a = s.pop()
                if token == "+":
                    s.push(a + b)
                elif token == "-":
                    s.push(a - b)
                elif token == "*":
                    s.push(a * b)
                elif token == "/":
                    s.push(a / b)
            else:
                s.push(float(token))
        return s.pop()

    def test_postfix_simple_add(self):
        assert self._postfix_eval("3 4 +") == 7.0

    def test_postfix_complex(self):
        # 3 4 + 2 * = (3 + 4) * 2 = 14
        assert self._postfix_eval("3 4 + 2 *") == 14.0

    def test_postfix_subtract(self):
        # 10 3 - = 7
        assert self._postfix_eval("10 3 -") == 7.0

    def test_postfix_divide(self):
        # 8 2 / = 4
        assert self._postfix_eval("8 2 /") == 4.0

    def test_postfix_multi_operator(self):
        # 5 1 2 + 4 * + 3 - = 5 + (1+2)*4 - 3 = 5 + 12 - 3 = 14
        assert self._postfix_eval("5 1 2 + 4 * + 3 -") == 14.0

    def _reverse_string(self, text):
        """Reverse a string using a stack."""
        s = Stack()
        for ch in text:
            s.push(ch)
        return "".join(s)

    def test_reverse_string(self):
        assert self._reverse_string("hello") == "olleh"

    def test_reverse_empty(self):
        assert self._reverse_string("") == ""

    def test_reverse_single(self):
        assert self._reverse_string("a") == "a"

    def test_reverse_palindrome(self):
        assert self._reverse_string("racecar") == "racecar"

    def _decimal_to_binary(self, n):
        """Convert a non-negative integer to its binary string using a stack."""
        s = Stack()
        if n == 0:
            s.push("0")
        else:
            while n > 0:
                s.push(str(n % 2))
                n //= 2
        return "".join(s)

    def test_dec_to_bin_zero(self):
        assert self._decimal_to_binary(0) == "0"

    def test_dec_to_bin_one(self):
        assert self._decimal_to_binary(1) == "1"

    def test_dec_to_bin_ten(self):
        assert self._decimal_to_binary(10) == "1010"

    def test_dec_to_bin_255(self):
        assert self._decimal_to_binary(255) == "11111111"

    def test_dec_to_bin_power_of_two(self):
        assert self._decimal_to_binary(64) == "1000000"


# ======================================================================
#  QUEUE TESTS
# ======================================================================


class TestQueueConstruction:
    def test_new_queue_is_empty(self):
        q = Queue()
        assert q.is_empty()

    def test_new_queue_has_length_zero(self):
        q = Queue()
        assert len(q) == 0

    def test_new_queue_to_list_is_empty(self):
        q = Queue()
        assert q.to_list() == []

    def test_new_queue_repr(self):
        q = Queue()
        assert repr(q) == "Queue([])"


class TestQueueEnqueue:
    def test_enqueue_single(self):
        q = Queue()
        q.enqueue(1)
        assert len(q) == 1
        assert q.peek() == 1

    def test_enqueue_multiple_maintains_fifo(self):
        q = Queue()
        for v in [1, 2, 3]:
            q.enqueue(v)
        assert q.peek() == 1
        assert q.to_list() == [1, 2, 3]

    def test_enqueue_returns_none(self):
        q = Queue()
        assert q.enqueue(42) is None

    def test_enqueue_various_types(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue("hello")
        q.enqueue([1, 2])
        q.enqueue(None)
        assert len(q) == 4
        assert q.peek() == 1

    def test_enqueue_after_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        q.enqueue(2)
        assert q.peek() == 2
        assert len(q) == 1

    def test_enqueue_many(self):
        q = Queue()
        for i in range(100):
            q.enqueue(i)
        assert len(q) == 100
        assert q.peek() == 0


class TestQueueDequeue:
    def test_dequeue_single(self):
        q = Queue()
        q.enqueue(42)
        assert q.dequeue() == 42
        assert q.is_empty()

    def test_dequeue_returns_fifo_order(self):
        q = Queue()
        for v in [1, 2, 3]:
            q.enqueue(v)
        assert q.dequeue() == 1
        assert q.dequeue() == 2
        assert q.dequeue() == 3

    def test_dequeue_empty_raises_index_error(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.dequeue()

    def test_dequeue_until_empty_then_raises(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        with pytest.raises(IndexError):
            q.dequeue()

    def test_enqueue_dequeue_interleaving(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        q.enqueue(3)
        assert q.dequeue() == 2
        assert q.dequeue() == 3

    def test_dequeue_decrements_length(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        assert len(q) == 1

    def test_dequeue_all_then_enqueue_again(self):
        q = Queue()
        q.enqueue(10)
        q.enqueue(20)
        q.dequeue()
        q.dequeue()
        q.enqueue(30)
        assert q.peek() == 30
        assert len(q) == 1


class TestQueuePeek:
    def test_peek_returns_front(self):
        q = Queue()
        q.enqueue(5)
        assert q.peek() == 5

    def test_peek_does_not_remove(self):
        q = Queue()
        q.enqueue(5)
        q.peek()
        assert len(q) == 1

    def test_peek_empty_raises_index_error(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.peek()

    def test_peek_after_enqueue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.peek() == 1

    def test_peek_after_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        assert q.peek() == 2

    def test_peek_multiple_times_same_value(self):
        q = Queue()
        q.enqueue(99)
        assert q.peek() == 99
        assert q.peek() == 99
        assert q.peek() == 99
        assert len(q) == 1


class TestQueueLen:
    def test_empty(self):
        assert len(Queue()) == 0

    def test_after_enqueues(self):
        q = Queue()
        for i in range(5):
            q.enqueue(i)
        assert len(q) == 5

    def test_after_dequeues(self):
        q = Queue()
        for i in range(5):
            q.enqueue(i)
        q.dequeue()
        q.dequeue()
        assert len(q) == 3

    def test_after_clear(self):
        q = Queue()
        q.enqueue(1)
        q.clear()
        assert len(q) == 0


class TestQueueIsEmpty:
    def test_new_queue(self):
        assert Queue().is_empty()

    def test_after_enqueue(self):
        q = Queue()
        q.enqueue(1)
        assert not q.is_empty()

    def test_after_enqueue_and_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        assert q.is_empty()

    def test_after_clear(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.clear()
        assert q.is_empty()


class TestQueueContains:
    def test_present(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert 2 in q

    def test_absent(self):
        q = Queue()
        q.enqueue(1)
        assert 99 not in q

    def test_empty(self):
        assert 1 not in Queue()

    def test_contains_none(self):
        q = Queue()
        q.enqueue(None)
        assert None in q

    def test_contains_after_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        assert 1 not in q
        assert 2 in q


class TestQueueEquality:
    def test_equal_queues(self):
        a = Queue()
        b = Queue()
        for v in [1, 2, 3]:
            a.enqueue(v)
            b.enqueue(v)
        assert a == b

    def test_different_values(self):
        a = Queue()
        b = Queue()
        a.enqueue(1)
        b.enqueue(2)
        assert a != b

    def test_different_lengths(self):
        a = Queue()
        b = Queue()
        a.enqueue(1)
        a.enqueue(2)
        b.enqueue(1)
        assert a != b

    def test_empty_queues_equal(self):
        assert Queue() == Queue()

    def test_same_values_different_order(self):
        a = Queue()
        b = Queue()
        a.enqueue(1)
        a.enqueue(2)
        b.enqueue(2)
        b.enqueue(1)
        assert a != b

    def test_not_equal_to_non_queue(self):
        q = Queue()
        q.enqueue(1)
        assert q != [1]
        assert q != "not a queue"

    def test_equality_is_symmetric(self):
        a = Queue()
        b = Queue()
        a.enqueue(1)
        b.enqueue(1)
        assert a == b
        assert b == a


class TestQueueIter:
    def test_front_to_back_order(self):
        q = Queue()
        for v in [1, 2, 3]:
            q.enqueue(v)
        assert list(q) == [1, 2, 3]

    def test_multiple_iterations(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        first = list(q)
        second = list(q)
        assert first == second == [1, 2]

    def test_empty_iter(self):
        assert list(Queue()) == []

    def test_iter_does_not_modify(self):
        q = Queue()
        q.enqueue(10)
        q.enqueue(20)
        _ = list(q)
        assert len(q) == 2
        assert q.peek() == 10

    def test_for_loop(self):
        q = Queue()
        for v in [5, 10, 15]:
            q.enqueue(v)
        total = 0
        for v in q:
            total += v
        assert total == 30


class TestQueueRepr:
    def test_empty(self):
        assert repr(Queue()) == "Queue([])"

    def test_one_element(self):
        q = Queue()
        q.enqueue(42)
        assert repr(q) == "Queue([42])"

    def test_multiple_elements_front_first(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert repr(q) == "Queue([1, 2, 3])"

    def test_string_elements(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        assert repr(q) == "Queue(['a', 'b'])"


class TestQueueClear:
    def test_clear_non_empty(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.clear()
        assert q.is_empty()
        assert len(q) == 0

    def test_clear_already_empty(self):
        q = Queue()
        q.clear()
        assert q.is_empty()

    def test_usable_after_clear(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.clear()
        q.enqueue(3)
        assert q.peek() == 3
        assert len(q) == 1

    def test_clear_resets_to_list(self):
        q = Queue()
        q.enqueue(1)
        q.clear()
        assert q.to_list() == []


class TestQueueToList:
    def test_empty(self):
        assert Queue().to_list() == []

    def test_one_element(self):
        q = Queue()
        q.enqueue(7)
        assert q.to_list() == [7]

    def test_multiple_front_first(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert q.to_list() == [1, 2, 3]

    def test_to_list_returns_new_list(self):
        q = Queue()
        q.enqueue(1)
        lst = q.to_list()
        lst.append(999)
        assert q.to_list() == [1]

    def test_to_list_does_not_modify_queue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.to_list()
        assert len(q) == 2
        assert q.peek() == 1


class TestQueueStress:
    def test_enqueue_dequeue_100k(self):
        q = Queue()
        n = 100_000
        for i in range(n):
            q.enqueue(i)
        assert len(q) == n
        for i in range(n):
            assert q.dequeue() == i
        assert q.is_empty()

    def test_enqueue_o1_time(self):
        q = Queue()
        n = 100_000
        start = time.perf_counter()
        for i in range(n):
            q.enqueue(i)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"100k enqueues took {elapsed:.2f}s (expected < 1s)"

    def test_dequeue_o1_time(self):
        q = Queue()
        n = 100_000
        for i in range(n):
            q.enqueue(i)
        start = time.perf_counter()
        for _ in range(n):
            q.dequeue()
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"100k dequeues took {elapsed:.2f}s (expected < 1s)"

    def test_alternating_enqueue_dequeue_at_scale(self):
        q = Queue()
        n = 100_000
        for i in range(n):
            q.enqueue(i)
            if i % 2 == 1:
                q.dequeue()
        assert len(q) == n // 2

    def test_alternating_preserves_fifo(self):
        """Enqueue 0..9, dequeue 5, enqueue 10..14, drain. Verify FIFO."""
        q = Queue()
        for i in range(10):
            q.enqueue(i)
        for _ in range(5):
            q.dequeue()
        for i in range(10, 15):
            q.enqueue(i)
        result = []
        while not q.is_empty():
            result.append(q.dequeue())
        assert result == list(range(5, 15))


class TestQueueIntegration:
    """Real-world algorithms implemented with a Queue."""

    def _hot_potato(self, names, k):
        """Simulate hot-potato: n people in a circle, remove every k-th.

        Return the last person remaining.
        """
        q = Queue()
        for name in names:
            q.enqueue(name)
        while len(q) > 1:
            for _ in range(k - 1):
                q.enqueue(q.dequeue())
            q.dequeue()
        return q.dequeue()

    def test_hot_potato_basic(self):
        names = ["A", "B", "C", "D", "E"]
        survivor = self._hot_potato(names, 3)
        # Simulate: queue starts [A, B, C, D, E], remove every 3rd
        # Round 1: rotate A, B to back -> [C, D, E, A, B], remove C -> [D, E, A, B]
        # Round 2: rotate D, E to back -> [A, B, D, E], remove A -> [B, D, E]
        # Round 3: rotate B, D to back -> [E, B, D], remove E -> [B, D]
        # Round 4: rotate B, D to back -> [B, D], remove B -> [D]
        assert survivor == "D"

    def test_hot_potato_two_people(self):
        assert self._hot_potato(["X", "Y"], 1) == "Y"

    def test_hot_potato_one_person(self):
        assert self._hot_potato(["Solo"], 5) == "Solo"

    def test_hot_potato_k_equals_1(self):
        # Remove front each time: last person enqueued order
        names = ["A", "B", "C", "D"]
        survivor = self._hot_potato(names, 1)
        assert survivor == "D"

    def test_hot_potato_large(self):
        names = [str(i) for i in range(100)]
        survivor = self._hot_potato(names, 7)
        # Verify against independent deque-based Josephus simulation
        d = deque(names)
        while len(d) > 1:
            for _ in range(6):
                d.append(d.popleft())
            d.popleft()
        assert survivor == d.popleft()

    def _priority_scheduler(self, jobs):
        """Process jobs with priorities using multiple queues (FIFO within priority).

        jobs: list of (priority, task_name) tuples.  Lower number = higher priority.
        Returns list of task names in processing order.
        """
        # Feed all jobs through a Queue first to prove the Queue works,
        # then distribute by priority.
        intake = Queue()
        for job in jobs:
            intake.enqueue(job)

        queues = {}
        while not intake.is_empty():
            priority, task = intake.dequeue()
            if priority not in queues:
                queues[priority] = Queue()
            queues[priority].enqueue(task)

        result = []
        for priority in sorted(queues.keys()):
            q = queues[priority]
            while not q.is_empty():
                result.append(q.dequeue())
        return result

    def test_scheduler_single_priority(self):
        jobs = [(1, "A"), (1, "B"), (1, "C")]
        assert self._priority_scheduler(jobs) == ["A", "B", "C"]

    def test_scheduler_multiple_priorities(self):
        jobs = [(2, "Low1"), (1, "High1"), (2, "Low2"), (1, "High2")]
        assert self._priority_scheduler(jobs) == ["High1", "High2", "Low1", "Low2"]

    def test_scheduler_already_sorted(self):
        jobs = [(1, "A"), (1, "B"), (2, "C"), (3, "D")]
        assert self._priority_scheduler(jobs) == ["A", "B", "C", "D"]

    def test_scheduler_reverse_priority(self):
        jobs = [(3, "C"), (2, "B"), (1, "A")]
        assert self._priority_scheduler(jobs) == ["A", "B", "C"]

    def test_scheduler_empty(self):
        assert self._priority_scheduler([]) == []

    def _bfs_shortest_path(self, graph, start, end):
        """BFS on adjacency-list graph. Return shortest path as list of nodes,
        or None if unreachable.

        graph: dict mapping node -> list of neighbors
        """
        if start == end:
            # Still exercise the Queue even for trivial case
            q = Queue()
            q.enqueue(start)
            q.dequeue()
            return [start]
        visited = {start}
        q = Queue()
        q.enqueue([start])
        while not q.is_empty():
            path = q.dequeue()
            node = path[-1]
            for neighbor in graph.get(node, []):
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.enqueue(path + [neighbor])
        return None

    def test_bfs_direct_edge(self):
        graph = {"A": ["B"], "B": []}
        assert self._bfs_shortest_path(graph, "A", "B") == ["A", "B"]

    def test_bfs_two_hops(self):
        graph = {"A": ["B"], "B": ["C"], "C": []}
        assert self._bfs_shortest_path(graph, "A", "C") == ["A", "B", "C"]

    def test_bfs_shortest_among_multiple(self):
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        path = self._bfs_shortest_path(graph, "A", "D")
        assert len(path) == 3  # A -> B -> D or A -> C -> D

    def test_bfs_unreachable(self):
        graph = {"A": ["B"], "B": [], "C": []}
        assert self._bfs_shortest_path(graph, "A", "C") is None

    def test_bfs_same_start_end(self):
        graph = {"A": ["B"], "B": ["A"]}
        assert self._bfs_shortest_path(graph, "A", "A") == ["A"]

    def test_bfs_cycle(self):
        graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A", "D"],
            "D": [],
        }
        assert self._bfs_shortest_path(graph, "A", "D") == ["A", "B", "C", "D"]

    def test_bfs_larger_graph(self):
        # Grid-like graph:
        #  1 - 2 - 3
        #  |       |
        #  4 - 5 - 6
        graph = {
            1: [2, 4],
            2: [1, 3],
            3: [2, 6],
            4: [1, 5],
            5: [4, 6],
            6: [3, 5],
        }
        path = self._bfs_shortest_path(graph, 1, 6)
        # Shortest paths: 1->2->3->6 or 1->4->5->6, both length 4
        assert len(path) == 4
        assert path[0] == 1
        assert path[-1] == 6
