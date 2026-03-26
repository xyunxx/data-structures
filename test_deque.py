"""
Comprehensive test suite for the Deque (double-ended queue) implementation.

Run with: pytest test_deque.py -v
"""

import time

import pytest

from deque import Deque


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty(self):
        d = Deque()
        assert len(d) == 0

    def test_from_list(self):
        d = Deque([1, 2, 3])
        assert d.to_list() == [1, 2, 3]

    def test_from_tuple(self):
        d = Deque((4, 5, 6))
        assert d.to_list() == [4, 5, 6]

    def test_from_generator(self):
        d = Deque(x * x for x in range(5))
        assert d.to_list() == [0, 1, 4, 9, 16]

    def test_from_string(self):
        d = Deque("abc")
        assert d.to_list() == ["a", "b", "c"]

    def test_from_range(self):
        d = Deque(range(4))
        assert d.to_list() == [0, 1, 2, 3]

    def test_single_element(self):
        d = Deque([42])
        assert len(d) == 1
        assert d.to_list() == [42]

    def test_none_iterable(self):
        d = Deque(None)
        assert len(d) == 0

    def test_from_another_deque(self):
        d1 = Deque([1, 2, 3])
        d2 = Deque(d1)
        assert d2.to_list() == [1, 2, 3]

    def test_from_set(self):
        d = Deque({1})
        assert len(d) == 1


# ---------------------------------------------------------------------------
# __len__
# ---------------------------------------------------------------------------


class TestLen:
    def test_empty(self):
        assert len(Deque()) == 0

    def test_one(self):
        assert len(Deque([7])) == 1

    def test_many(self):
        assert len(Deque(range(100))) == 100

    def test_after_append(self):
        d = Deque()
        d.append(1)
        assert len(d) == 1

    def test_after_pop(self):
        d = Deque([1, 2, 3])
        d.pop()
        assert len(d) == 2

    def test_after_clear(self):
        d = Deque([1, 2, 3])
        d.clear()
        assert len(d) == 0


# ---------------------------------------------------------------------------
# __bool__
# ---------------------------------------------------------------------------


class TestBool:
    def test_empty_is_falsy(self):
        assert not Deque()

    def test_nonempty_is_truthy(self):
        assert Deque([1])

    def test_after_clear(self):
        d = Deque([1, 2])
        d.clear()
        assert not d

    def test_after_adding_to_empty(self):
        d = Deque()
        d.append(5)
        assert d


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------


class TestRepr:
    def test_empty(self):
        assert repr(Deque()) == "Deque([])"

    def test_single(self):
        assert repr(Deque([42])) == "Deque([42])"

    def test_multiple(self):
        assert repr(Deque([1, 2, 3])) == "Deque([1, 2, 3])"

    def test_strings(self):
        assert repr(Deque(["a", "b"])) == "Deque(['a', 'b'])"


# ---------------------------------------------------------------------------
# __contains__
# ---------------------------------------------------------------------------


class TestContains:
    def test_present(self):
        assert 2 in Deque([1, 2, 3])

    def test_absent(self):
        assert 5 not in Deque([1, 2, 3])

    def test_empty(self):
        assert 1 not in Deque()

    def test_none_value(self):
        assert None in Deque([None, 1, 2])

    def test_none_absent(self):
        assert None not in Deque([1, 2, 3])


# ---------------------------------------------------------------------------
# __eq__
# ---------------------------------------------------------------------------


class TestEquality:
    def test_equal(self):
        assert Deque([1, 2, 3]) == Deque([1, 2, 3])

    def test_different_lengths(self):
        assert Deque([1, 2]) != Deque([1, 2, 3])

    def test_different_values(self):
        assert Deque([1, 2, 3]) != Deque([1, 2, 4])

    def test_empty_deques(self):
        assert Deque() == Deque()

    def test_not_a_deque(self):
        assert Deque([1, 2, 3]) != [1, 2, 3]

    def test_same_object(self):
        d = Deque([1, 2])
        assert d == d

    def test_different_order(self):
        assert Deque([1, 2, 3]) != Deque([3, 2, 1])


# ---------------------------------------------------------------------------
# __getitem__
# ---------------------------------------------------------------------------


class TestIndexing:
    def test_positive_index(self):
        d = Deque([10, 20, 30])
        assert d[0] == 10
        assert d[1] == 20
        assert d[2] == 30

    def test_negative_index(self):
        d = Deque([10, 20, 30])
        assert d[-1] == 30
        assert d[-2] == 20
        assert d[-3] == 10

    def test_out_of_range_positive(self):
        d = Deque([1, 2])
        with pytest.raises(IndexError):
            d[5]

    def test_out_of_range_negative(self):
        d = Deque([1, 2])
        with pytest.raises(IndexError):
            d[-3]

    def test_single_element(self):
        d = Deque([99])
        assert d[0] == 99
        assert d[-1] == 99

    def test_after_modifications(self):
        d = Deque([1, 2, 3])
        d.pop()
        assert d[0] == 1
        assert d[-1] == 2

    def test_empty_raises(self):
        with pytest.raises(IndexError):
            Deque()[0]


# ---------------------------------------------------------------------------
# is_empty
# ---------------------------------------------------------------------------


class TestIsEmpty:
    def test_empty(self):
        assert Deque().is_empty()

    def test_nonempty(self):
        assert not Deque([1]).is_empty()

    def test_after_clear(self):
        d = Deque([1, 2])
        d.clear()
        assert d.is_empty()

    def test_after_removing_all(self):
        d = Deque([5])
        d.pop()
        assert d.is_empty()

    def test_after_popleft_all(self):
        d = Deque([5])
        d.popleft()
        assert d.is_empty()


# ---------------------------------------------------------------------------
# append
# ---------------------------------------------------------------------------


class TestAppend:
    def test_single(self):
        d = Deque()
        d.append(1)
        assert d.to_list() == [1]

    def test_multiple(self):
        d = Deque()
        d.append(1)
        d.append(2)
        d.append(3)
        assert d.to_list() == [1, 2, 3]

    def test_maintains_order(self):
        d = Deque([10, 20])
        d.append(30)
        assert d.to_list() == [10, 20, 30]

    def test_return_value_is_none(self):
        d = Deque()
        result = d.append(1)
        assert result is None

    def test_len_updates(self):
        d = Deque()
        d.append("a")
        d.append("b")
        assert len(d) == 2


# ---------------------------------------------------------------------------
# appendleft
# ---------------------------------------------------------------------------


class TestAppendLeft:
    def test_single(self):
        d = Deque()
        d.appendleft(1)
        assert d.to_list() == [1]

    def test_multiple(self):
        d = Deque()
        d.appendleft(1)
        d.appendleft(2)
        d.appendleft(3)
        assert d.to_list() == [3, 2, 1]

    def test_maintains_front_insertion(self):
        d = Deque([10, 20])
        d.appendleft(5)
        assert d.to_list() == [5, 10, 20]

    def test_return_value_is_none(self):
        d = Deque()
        result = d.appendleft(1)
        assert result is None

    def test_len_updates(self):
        d = Deque()
        d.appendleft("x")
        d.appendleft("y")
        assert len(d) == 2


# ---------------------------------------------------------------------------
# pop
# ---------------------------------------------------------------------------


class TestPop:
    def test_single(self):
        d = Deque([42])
        assert d.pop() == 42
        assert len(d) == 0

    def test_multiple(self):
        d = Deque([1, 2, 3])
        assert d.pop() == 3
        assert d.pop() == 2
        assert d.pop() == 1

    def test_empty_raises(self):
        with pytest.raises(IndexError):
            Deque().pop()

    def test_pop_all(self):
        d = Deque([1, 2])
        d.pop()
        d.pop()
        assert d.is_empty()

    def test_pop_then_append(self):
        d = Deque([1, 2])
        d.pop()
        d.append(3)
        assert d.to_list() == [1, 3]


# ---------------------------------------------------------------------------
# popleft
# ---------------------------------------------------------------------------


class TestPopLeft:
    def test_single(self):
        d = Deque([42])
        assert d.popleft() == 42
        assert len(d) == 0

    def test_multiple(self):
        d = Deque([1, 2, 3])
        assert d.popleft() == 1
        assert d.popleft() == 2
        assert d.popleft() == 3

    def test_empty_raises(self):
        with pytest.raises(IndexError):
            Deque().popleft()

    def test_popleft_all(self):
        d = Deque([1, 2])
        d.popleft()
        d.popleft()
        assert d.is_empty()

    def test_popleft_then_appendleft(self):
        d = Deque([1, 2])
        d.popleft()
        d.appendleft(0)
        assert d.to_list() == [0, 2]


# ---------------------------------------------------------------------------
# peek_front
# ---------------------------------------------------------------------------


class TestPeekFront:
    def test_nonempty(self):
        d = Deque([10, 20, 30])
        assert d.peek_front() == 10

    def test_empty_raises(self):
        with pytest.raises(IndexError):
            Deque().peek_front()

    def test_does_not_remove(self):
        d = Deque([5, 6])
        d.peek_front()
        assert len(d) == 2

    def test_single_element(self):
        d = Deque([99])
        assert d.peek_front() == 99


# ---------------------------------------------------------------------------
# peek_back
# ---------------------------------------------------------------------------


class TestPeekBack:
    def test_nonempty(self):
        d = Deque([10, 20, 30])
        assert d.peek_back() == 30

    def test_empty_raises(self):
        with pytest.raises(IndexError):
            Deque().peek_back()

    def test_does_not_remove(self):
        d = Deque([5, 6])
        d.peek_back()
        assert len(d) == 2

    def test_single_element(self):
        d = Deque([99])
        assert d.peek_back() == 99

    def test_front_and_back_same_for_single(self):
        d = Deque([7])
        assert d.peek_front() == d.peek_back()


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_nonempty(self):
        d = Deque([1, 2, 3])
        d.clear()
        assert len(d) == 0
        assert d.to_list() == []

    def test_empty(self):
        d = Deque()
        d.clear()
        assert len(d) == 0

    def test_usable_after(self):
        d = Deque([1, 2])
        d.clear()
        d.append(10)
        assert d.to_list() == [10]

    def test_appendleft_after_clear(self):
        d = Deque([1, 2])
        d.clear()
        d.appendleft(10)
        assert d.to_list() == [10]


# ---------------------------------------------------------------------------
# copy
# ---------------------------------------------------------------------------


class TestCopy:
    def test_independence(self):
        d = Deque([1, 2, 3])
        c = d.copy()
        c.append(4)
        assert d.to_list() == [1, 2, 3]
        assert c.to_list() == [1, 2, 3, 4]

    def test_same_values(self):
        d = Deque([1, 2, 3])
        c = d.copy()
        assert d == c

    def test_empty_copy(self):
        d = Deque()
        c = d.copy()
        assert c == Deque()

    def test_modify_original_not_copy(self):
        d = Deque([1, 2])
        c = d.copy()
        d.popleft()
        assert d.to_list() == [2]
        assert c.to_list() == [1, 2]

    def test_copy_is_deque(self):
        d = Deque([1])
        c = d.copy()
        assert isinstance(c, Deque)


# ---------------------------------------------------------------------------
# count
# ---------------------------------------------------------------------------


class TestCount:
    def test_zero(self):
        assert Deque([1, 2, 3]).count(5) == 0

    def test_one(self):
        assert Deque([1, 2, 3]).count(2) == 1

    def test_many(self):
        assert Deque([1, 2, 2, 3, 2]).count(2) == 3

    def test_empty(self):
        assert Deque().count(1) == 0

    def test_after_removal(self):
        d = Deque([1, 1, 1])
        d.remove(1)
        assert d.count(1) == 2

    def test_none_values(self):
        assert Deque([None, None, 1]).count(None) == 2


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------


class TestRemove:
    def test_present(self):
        d = Deque([1, 2, 3])
        d.remove(2)
        assert d.to_list() == [1, 3]

    def test_absent_raises(self):
        with pytest.raises(ValueError):
            Deque([1, 2, 3]).remove(5)

    def test_first_occurrence(self):
        d = Deque([1, 2, 2, 3])
        d.remove(2)
        assert d.to_list() == [1, 2, 3]

    def test_remove_from_front(self):
        d = Deque([1, 2, 3])
        d.remove(1)
        assert d.to_list() == [2, 3]
        assert d.peek_front() == 2

    def test_remove_from_back(self):
        d = Deque([1, 2, 3])
        d.remove(3)
        assert d.to_list() == [1, 2]
        assert d.peek_back() == 2

    def test_remove_from_middle(self):
        d = Deque([1, 2, 3, 4, 5])
        d.remove(3)
        assert d.to_list() == [1, 2, 4, 5]

    def test_remove_only_element(self):
        d = Deque([7])
        d.remove(7)
        assert d.is_empty()

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            Deque().remove(1)

    def test_len_decreases(self):
        d = Deque([1, 2, 3])
        d.remove(2)
        assert len(d) == 2

    def test_remove_none_value(self):
        d = Deque([1, None, 3])
        d.remove(None)
        assert d.to_list() == [1, 3]
        assert len(d) == 2


# ---------------------------------------------------------------------------
# rotate
# ---------------------------------------------------------------------------


class TestRotate:
    def test_right_by_1(self):
        d = Deque([1, 2, 3, 4])
        d.rotate(1)
        assert d.to_list() == [4, 1, 2, 3]

    def test_right_by_n(self):
        d = Deque([1, 2, 3, 4, 5])
        d.rotate(2)
        assert d.to_list() == [4, 5, 1, 2, 3]

    def test_left_negative(self):
        d = Deque([1, 2, 3, 4])
        d.rotate(-1)
        assert d.to_list() == [2, 3, 4, 1]

    def test_left_by_n(self):
        d = Deque([1, 2, 3, 4, 5])
        d.rotate(-2)
        assert d.to_list() == [3, 4, 5, 1, 2]

    def test_by_zero(self):
        d = Deque([1, 2, 3])
        d.rotate(0)
        assert d.to_list() == [1, 2, 3]

    def test_by_length(self):
        d = Deque([1, 2, 3])
        d.rotate(3)
        assert d.to_list() == [1, 2, 3]

    def test_by_negative_length(self):
        d = Deque([1, 2, 3])
        d.rotate(-3)
        assert d.to_list() == [1, 2, 3]

    def test_more_than_length(self):
        d = Deque([1, 2, 3])
        d.rotate(5)  # 5 % 3 == 2
        assert d.to_list() == [2, 3, 1]

    def test_negative_more_than_length(self):
        d = Deque([1, 2, 3])
        d.rotate(-5)  # -5 % 3 == 1 (effectively rotate right by 1)
        assert d.to_list() == [3, 1, 2]

    def test_empty_deque(self):
        d = Deque()
        d.rotate(5)
        assert d.to_list() == []

    def test_single_element(self):
        d = Deque([42])
        d.rotate(100)
        assert d.to_list() == [42]

    def test_default_argument(self):
        d = Deque([1, 2, 3])
        d.rotate()
        assert d.to_list() == [3, 1, 2]


# ---------------------------------------------------------------------------
# extend
# ---------------------------------------------------------------------------


class TestExtend:
    def test_from_list(self):
        d = Deque([1])
        d.extend([2, 3, 4])
        assert d.to_list() == [1, 2, 3, 4]

    def test_from_generator(self):
        d = Deque()
        d.extend(x for x in range(3))
        assert d.to_list() == [0, 1, 2]

    def test_empty_iterable(self):
        d = Deque([1, 2])
        d.extend([])
        assert d.to_list() == [1, 2]

    def test_extend_empty_deque(self):
        d = Deque()
        d.extend([10, 20])
        assert d.to_list() == [10, 20]

    def test_len_updates(self):
        d = Deque([1])
        d.extend([2, 3])
        assert len(d) == 3


# ---------------------------------------------------------------------------
# extendleft
# ---------------------------------------------------------------------------


class TestExtendLeft:
    def test_from_list_reverses(self):
        d = Deque([4])
        d.extendleft([1, 2, 3])
        assert d.to_list() == [3, 2, 1, 4]

    def test_from_generator(self):
        d = Deque()
        d.extendleft(x for x in range(3))
        assert d.to_list() == [2, 1, 0]

    def test_empty_iterable(self):
        d = Deque([1, 2])
        d.extendleft([])
        assert d.to_list() == [1, 2]

    def test_extend_empty_deque(self):
        d = Deque()
        d.extendleft([10, 20])
        assert d.to_list() == [20, 10]

    def test_len_updates(self):
        d = Deque()
        d.extendleft([1, 2, 3])
        assert len(d) == 3


# ---------------------------------------------------------------------------
# to_list
# ---------------------------------------------------------------------------


class TestToList:
    def test_empty(self):
        assert Deque().to_list() == []

    def test_single(self):
        assert Deque([7]).to_list() == [7]

    def test_multiple(self):
        assert Deque([1, 2, 3]).to_list() == [1, 2, 3]

    def test_returns_plain_list(self):
        result = Deque([1]).to_list()
        assert type(result) is list


# ---------------------------------------------------------------------------
# reverse
# ---------------------------------------------------------------------------


class TestReverse:
    def test_empty(self):
        d = Deque()
        d.reverse()
        assert d.to_list() == []

    def test_single(self):
        d = Deque([1])
        d.reverse()
        assert d.to_list() == [1]

    def test_multiple(self):
        d = Deque([1, 2, 3, 4])
        d.reverse()
        assert d.to_list() == [4, 3, 2, 1]

    def test_is_in_place(self):
        d = Deque([1, 2, 3])
        result = d.reverse()
        assert result is None  # should not return a new deque

    def test_preserves_all_elements(self):
        d = Deque([5, 3, 1, 4, 2])
        d.reverse()
        assert sorted(d.to_list()) == [1, 2, 3, 4, 5]

    def test_double_reverse(self):
        d = Deque([1, 2, 3])
        d.reverse()
        d.reverse()
        assert d.to_list() == [1, 2, 3]

    def test_peek_after_reverse(self):
        d = Deque([1, 2, 3])
        d.reverse()
        assert d.peek_front() == 3
        assert d.peek_back() == 1


# ---------------------------------------------------------------------------
# __iter__ and __reversed__
# ---------------------------------------------------------------------------


class TestIteration:
    def test_forward(self):
        d = Deque([1, 2, 3])
        assert list(d) == [1, 2, 3]

    def test_reversed(self):
        d = Deque([1, 2, 3])
        assert list(reversed(d)) == [3, 2, 1]

    def test_multiple_iterations(self):
        d = Deque([1, 2])
        assert list(d) == [1, 2]
        assert list(d) == [1, 2]

    def test_empty_forward(self):
        assert list(Deque()) == []

    def test_empty_reversed(self):
        assert list(reversed(Deque())) == []

    def test_forward_single(self):
        assert list(Deque([42])) == [42]

    def test_reversed_single(self):
        assert list(reversed(Deque([42]))) == [42]

    def test_for_loop(self):
        d = Deque([10, 20, 30])
        total = 0
        for v in d:
            total += v
        assert total == 60


# ---------------------------------------------------------------------------
# Stress tests
# ---------------------------------------------------------------------------


class TestStress:
    def test_append_100k(self):
        d = Deque()
        start = time.perf_counter()
        for i in range(100_000):
            d.append(i)
        elapsed = time.perf_counter() - start
        assert len(d) == 100_000
        assert elapsed < 1.0, f"100k appends took {elapsed:.2f}s (expected < 1s)"

    def test_appendleft_100k(self):
        d = Deque()
        start = time.perf_counter()
        for i in range(100_000):
            d.appendleft(i)
        elapsed = time.perf_counter() - start
        assert len(d) == 100_000
        assert elapsed < 1.0, f"100k appendlefts took {elapsed:.2f}s (expected < 1s)"

    def test_popleft_100k(self):
        d = Deque(range(100_000))
        start = time.perf_counter()
        for _ in range(100_000):
            d.popleft()
        elapsed = time.perf_counter() - start
        assert len(d) == 0
        assert elapsed < 1.0, f"100k poplefts took {elapsed:.2f}s (expected < 1s)"

    def test_pop_100k(self):
        d = Deque(range(100_000))
        start = time.perf_counter()
        for _ in range(100_000):
            d.pop()
        elapsed = time.perf_counter() - start
        assert len(d) == 0
        assert elapsed < 1.0, f"100k pops took {elapsed:.2f}s (expected < 1s)"

    def test_iterate_100k(self):
        d = Deque(range(100_000))
        total = sum(d)
        assert total == sum(range(100_000))

    def test_rotate_large(self):
        d = Deque(range(10_000))
        d.rotate(3_333)
        assert len(d) == 10_000
        # rotating by the full length should restore
        d.rotate(10_000 - 3_333)
        assert d.to_list() == list(range(10_000))


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_sliding_window_maximum(self):
        """Classic sliding-window-maximum using a deque of indices."""
        nums = [1, 3, -1, -3, 5, 3, 6, 7]
        k = 3
        result = []
        dq = Deque()  # stores indices

        for i, val in enumerate(nums):
            # remove indices that are out of the window
            while not dq.is_empty() and dq.peek_front() < i - k + 1:
                dq.popleft()
            # remove indices whose corresponding values are less than current
            while not dq.is_empty() and nums[dq.peek_back()] <= val:
                dq.pop()
            dq.append(i)
            if i >= k - 1:
                result.append(nums[dq.peek_front()])

        assert result == [3, 3, 5, 5, 6, 7]

    def test_palindrome_checker(self):
        """Check if a string is a palindrome by comparing front and back."""

        def is_palindrome(s):
            d = Deque(s.lower())
            while len(d) > 1:
                if d.popleft() != d.pop():
                    return False
            return True

        assert is_palindrome("racecar")
        assert is_palindrome("madam")
        assert not is_palindrome("hello")
        assert is_palindrome("a")
        assert is_palindrome("")

    def test_undo_redo_system(self):
        """Undo/redo system: actions go on main deque, undo moves to redo."""
        actions = Deque()
        redo_stack = Deque()

        # perform actions
        actions.append("type 'H'")
        actions.append("type 'i'")
        actions.append("bold")

        # undo last action
        last = actions.pop()
        redo_stack.append(last)
        assert actions.to_list() == ["type 'H'", "type 'i'"]
        assert redo_stack.to_list() == ["bold"]

        # undo again
        last = actions.pop()
        redo_stack.append(last)
        assert actions.to_list() == ["type 'H'"]

        # redo
        redo_action = redo_stack.pop()
        actions.append(redo_action)
        assert actions.to_list() == ["type 'H'", "type 'i'"]

        # redo again
        redo_action = redo_stack.pop()
        actions.append(redo_action)
        assert actions.to_list() == ["type 'H'", "type 'i'", "bold"]
        assert redo_stack.is_empty()

    def test_work_stealing_scheduler(self):
        """Multiple deques: owner pops from back, thieves steal from front."""
        worker_a = Deque(["a1", "a2", "a3", "a4"])
        worker_b = Deque(["b1"])

        # Worker B finishes its work
        worker_b.popleft()
        assert worker_b.is_empty()

        # Worker B steals from front of Worker A's queue
        stolen = worker_a.popleft()
        worker_b.append(stolen)
        assert stolen == "a1"

        # Worker A continues from its own back
        own_task = worker_a.pop()
        assert own_task == "a4"

        # Final state
        assert worker_a.to_list() == ["a2", "a3"]
        assert worker_b.to_list() == ["a1"]

    def test_round_robin_with_rotate(self):
        """Use rotate to cycle through tasks in round-robin fashion."""
        tasks = Deque(["A", "B", "C", "D"])
        order = []

        for _ in range(8):
            current = tasks.peek_front()
            order.append(current)
            tasks.rotate(-1)

        assert order == ["A", "B", "C", "D", "A", "B", "C", "D"]

    def test_mixed_operations_sequence(self):
        """A long sequence of mixed operations to exercise many code paths."""
        d = Deque()
        d.append(1)
        d.append(2)
        d.appendleft(0)
        assert d.to_list() == [0, 1, 2]

        d.extend([3, 4])
        assert d.to_list() == [0, 1, 2, 3, 4]

        d.extendleft([-2, -1])
        assert d.to_list() == [-1, -2, 0, 1, 2, 3, 4]

        d.rotate(2)
        assert d.to_list() == [3, 4, -1, -2, 0, 1, 2]

        d.reverse()
        assert d.to_list() == [2, 1, 0, -2, -1, 4, 3]

        d.remove(-2)
        assert d.to_list() == [2, 1, 0, -1, 4, 3]

        assert d.count(1) == 1
        assert 4 in d
        assert d[2] == 0
        assert d[-1] == 3

        c = d.copy()
        d.clear()
        assert d.is_empty()
        assert c.to_list() == [2, 1, 0, -1, 4, 3]
