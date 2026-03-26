"""
Comprehensive pytest test suite for the LinkedList implementation.

Run with:  uv run pytest test_linked_list.py -v
"""

import pytest
from linked_list import LinkedList, Node


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty(self):
        ll = LinkedList()
        assert len(ll) == 0

    def test_from_list(self):
        ll = LinkedList([1, 2, 3])
        assert list(ll) == [1, 2, 3]

    def test_from_tuple(self):
        ll = LinkedList((10, 20, 30))
        assert list(ll) == [10, 20, 30]

    def test_from_generator(self):
        ll = LinkedList(x * x for x in range(5))
        assert list(ll) == [0, 1, 4, 9, 16]

    def test_from_string(self):
        ll = LinkedList("abc")
        assert list(ll) == ["a", "b", "c"]

    def test_single_element(self):
        ll = LinkedList([42])
        assert list(ll) == [42]
        assert len(ll) == 1

    def test_from_range(self):
        ll = LinkedList(range(5))
        assert list(ll) == [0, 1, 2, 3, 4]

    def test_from_set_has_correct_length(self):
        s = {1, 2, 3}
        ll = LinkedList(s)
        assert len(ll) == 3

    def test_none_iterable_gives_empty(self):
        ll = LinkedList(None)
        assert len(ll) == 0

    def test_head_attribute_exists(self):
        ll = LinkedList()
        assert ll.head is None

    def test_head_is_node_when_nonempty(self):
        ll = LinkedList([5])
        assert isinstance(ll.head, Node)
        assert ll.head.value == 5


# ---------------------------------------------------------------------------
# __len__
# ---------------------------------------------------------------------------

class TestLen:
    def test_empty(self):
        assert len(LinkedList()) == 0

    def test_one(self):
        assert len(LinkedList([1])) == 1

    def test_many(self):
        assert len(LinkedList(range(100))) == 100

    def test_after_push(self):
        ll = LinkedList()
        ll.push_front(1)
        assert len(ll) == 1
        ll.push_back(2)
        assert len(ll) == 2

    def test_after_pop(self):
        ll = LinkedList([1, 2, 3])
        ll.pop_front()
        assert len(ll) == 2
        ll.pop_back()
        assert len(ll) == 1

    def test_after_clear(self):
        ll = LinkedList([1, 2, 3])
        ll.clear()
        assert len(ll) == 0

    def test_after_remove(self):
        ll = LinkedList([1, 2, 3])
        ll.remove(2)
        assert len(ll) == 2


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------

class TestRepr:
    def test_empty(self):
        assert repr(LinkedList()) == "LinkedList([])"

    def test_single(self):
        assert repr(LinkedList([1])) == "LinkedList([1])"

    def test_multiple(self):
        assert repr(LinkedList([1, 2, 3])) == "LinkedList([1, 2, 3])"

    def test_strings(self):
        assert repr(LinkedList(["a", "b"])) == "LinkedList(['a', 'b'])"

    def test_after_modification(self):
        ll = LinkedList([1, 2, 3])
        ll.pop_front()
        assert repr(ll) == "LinkedList([2, 3])"

    def test_after_push(self):
        ll = LinkedList()
        ll.push_back(10)
        assert repr(ll) == "LinkedList([10])"


# ---------------------------------------------------------------------------
# __contains__
# ---------------------------------------------------------------------------

class TestContains:
    def test_present(self):
        ll = LinkedList([1, 2, 3])
        assert 2 in ll

    def test_absent(self):
        ll = LinkedList([1, 2, 3])
        assert 4 not in ll

    def test_empty_list(self):
        ll = LinkedList()
        assert 1 not in ll

    def test_after_removal(self):
        ll = LinkedList([1, 2, 3])
        ll.remove(2)
        assert 2 not in ll

    def test_head_value(self):
        ll = LinkedList([10, 20, 30])
        assert 10 in ll

    def test_tail_value(self):
        ll = LinkedList([10, 20, 30])
        assert 30 in ll

    def test_string_values(self):
        ll = LinkedList(["hello", "world"])
        assert "hello" in ll
        assert "foo" not in ll

    def test_none_value(self):
        ll = LinkedList([1, None, 3])
        assert None in ll


# ---------------------------------------------------------------------------
# __eq__
# ---------------------------------------------------------------------------

class TestEquality:
    def test_equal_lists(self):
        assert LinkedList([1, 2, 3]) == LinkedList([1, 2, 3])

    def test_different_lengths(self):
        assert LinkedList([1, 2]) != LinkedList([1, 2, 3])

    def test_different_values(self):
        assert LinkedList([1, 2, 3]) != LinkedList([1, 2, 4])

    def test_empty_lists(self):
        assert LinkedList() == LinkedList()

    def test_not_a_linked_list(self):
        assert LinkedList([1, 2, 3]) != [1, 2, 3]

    def test_not_a_linked_list_returns_not_equal(self):
        assert not (LinkedList([1, 2, 3]) == [1, 2, 3])

    def test_single_element_equal(self):
        assert LinkedList([42]) == LinkedList([42])

    def test_single_element_not_equal(self):
        assert LinkedList([42]) != LinkedList([43])

    def test_order_matters(self):
        assert LinkedList([1, 2]) != LinkedList([2, 1])

    def test_none_comparison(self):
        assert LinkedList() != None  # noqa: E711


# ---------------------------------------------------------------------------
# __getitem__ and __setitem__
# ---------------------------------------------------------------------------

class TestIndexing:
    def test_positive_index(self):
        ll = LinkedList([10, 20, 30])
        assert ll[0] == 10
        assert ll[1] == 20
        assert ll[2] == 30

    def test_negative_index(self):
        ll = LinkedList([10, 20, 30])
        assert ll[-1] == 30
        assert ll[-2] == 20
        assert ll[-3] == 10

    def test_out_of_range_positive(self):
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll[2]

    def test_out_of_range_negative(self):
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll[-3]

    def test_single_element(self):
        ll = LinkedList([99])
        assert ll[0] == 99
        assert ll[-1] == 99

    def test_empty_raises(self):
        ll = LinkedList()
        with pytest.raises(IndexError):
            ll[0]

    def test_setitem_positive(self):
        ll = LinkedList([1, 2, 3])
        ll[1] = 99
        assert list(ll) == [1, 99, 3]

    def test_setitem_negative(self):
        ll = LinkedList([1, 2, 3])
        ll[-1] = 99
        assert list(ll) == [1, 2, 99]

    def test_setitem_head(self):
        ll = LinkedList([1, 2, 3])
        ll[0] = 99
        assert ll[0] == 99

    def test_setitem_out_of_range(self):
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll[5] = 99

    def test_setitem_negative_out_of_range(self):
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll[-3] = 99

    def test_setitem_empty(self):
        ll = LinkedList()
        with pytest.raises(IndexError):
            ll[0] = 1


# ---------------------------------------------------------------------------
# is_empty
# ---------------------------------------------------------------------------

class TestIsEmpty:
    def test_empty(self):
        assert LinkedList().is_empty() is True

    def test_non_empty(self):
        assert LinkedList([1]).is_empty() is False

    def test_after_clear(self):
        ll = LinkedList([1, 2, 3])
        ll.clear()
        assert ll.is_empty() is True

    def test_after_removing_all(self):
        ll = LinkedList([1])
        ll.pop_front()
        assert ll.is_empty() is True

    def test_after_push_to_empty(self):
        ll = LinkedList()
        ll.push_front(1)
        assert ll.is_empty() is False


# ---------------------------------------------------------------------------
# push_front
# ---------------------------------------------------------------------------

class TestPushFront:
    def test_single(self):
        ll = LinkedList()
        ll.push_front(1)
        assert list(ll) == [1]

    def test_multiple_maintains_order(self):
        ll = LinkedList()
        ll.push_front(3)
        ll.push_front(2)
        ll.push_front(1)
        assert list(ll) == [1, 2, 3]

    def test_return_value_is_none(self):
        ll = LinkedList()
        result = ll.push_front(1)
        assert result is None

    def test_updates_length(self):
        ll = LinkedList()
        for i in range(10):
            ll.push_front(i)
        assert len(ll) == 10

    def test_push_front_to_existing(self):
        ll = LinkedList([2, 3])
        ll.push_front(1)
        assert list(ll) == [1, 2, 3]

    def test_push_front_none_value(self):
        ll = LinkedList()
        ll.push_front(None)
        assert list(ll) == [None]
        assert len(ll) == 1


# ---------------------------------------------------------------------------
# push_back
# ---------------------------------------------------------------------------

class TestPushBack:
    def test_single(self):
        ll = LinkedList()
        ll.push_back(1)
        assert list(ll) == [1]

    def test_multiple_maintains_order(self):
        ll = LinkedList()
        ll.push_back(1)
        ll.push_back(2)
        ll.push_back(3)
        assert list(ll) == [1, 2, 3]

    def test_return_value_is_none(self):
        ll = LinkedList()
        result = ll.push_back(1)
        assert result is None

    def test_updates_length(self):
        ll = LinkedList()
        for i in range(10):
            ll.push_back(i)
        assert len(ll) == 10

    def test_push_back_to_existing(self):
        ll = LinkedList([1, 2])
        ll.push_back(3)
        assert list(ll) == [1, 2, 3]

    def test_push_back_none_value(self):
        ll = LinkedList()
        ll.push_back(None)
        assert list(ll) == [None]


# ---------------------------------------------------------------------------
# pop_front
# ---------------------------------------------------------------------------

class TestPopFront:
    def test_single_element(self):
        ll = LinkedList([42])
        val = ll.pop_front()
        assert val == 42
        assert len(ll) == 0

    def test_multiple(self):
        ll = LinkedList([1, 2, 3])
        assert ll.pop_front() == 1
        assert ll.pop_front() == 2
        assert ll.pop_front() == 3

    def test_empty_raises(self):
        ll = LinkedList()
        with pytest.raises(IndexError):
            ll.pop_front()

    def test_pop_all_then_push(self):
        ll = LinkedList([1])
        ll.pop_front()
        ll.push_front(99)
        assert list(ll) == [99]

    def test_pop_updates_length(self):
        ll = LinkedList([1, 2, 3])
        ll.pop_front()
        assert len(ll) == 2

    def test_remaining_order(self):
        ll = LinkedList([1, 2, 3, 4])
        ll.pop_front()
        assert list(ll) == [2, 3, 4]


# ---------------------------------------------------------------------------
# pop_back
# ---------------------------------------------------------------------------

class TestPopBack:
    def test_single_element(self):
        ll = LinkedList([42])
        val = ll.pop_back()
        assert val == 42
        assert len(ll) == 0

    def test_multiple(self):
        ll = LinkedList([1, 2, 3])
        assert ll.pop_back() == 3
        assert ll.pop_back() == 2
        assert ll.pop_back() == 1

    def test_empty_raises(self):
        ll = LinkedList()
        with pytest.raises(IndexError):
            ll.pop_back()

    def test_pop_updates_length(self):
        ll = LinkedList([1, 2, 3])
        ll.pop_back()
        assert len(ll) == 2

    def test_remaining_order(self):
        ll = LinkedList([1, 2, 3, 4])
        ll.pop_back()
        assert list(ll) == [1, 2, 3]

    def test_pop_back_then_push_back(self):
        ll = LinkedList([1, 2])
        ll.pop_back()
        ll.push_back(99)
        assert list(ll) == [1, 99]


# ---------------------------------------------------------------------------
# insert
# ---------------------------------------------------------------------------

class TestInsert:
    def test_at_beginning(self):
        ll = LinkedList([2, 3])
        ll.insert(0, 1)
        assert list(ll) == [1, 2, 3]

    def test_at_middle(self):
        ll = LinkedList([1, 3])
        ll.insert(1, 2)
        assert list(ll) == [1, 2, 3]

    def test_at_end(self):
        ll = LinkedList([1, 2])
        ll.insert(2, 3)
        assert list(ll) == [1, 2, 3]

    def test_into_empty_at_zero(self):
        ll = LinkedList()
        ll.insert(0, 1)
        assert list(ll) == [1]

    def test_out_of_range_raises(self):
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll.insert(5, 99)

    def test_negative_out_of_range_raises(self):
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll.insert(-5, 99)

    def test_insert_at_len_appends(self):
        ll = LinkedList([1, 2, 3])
        ll.insert(3, 4)
        assert list(ll) == [1, 2, 3, 4]

    def test_updates_length(self):
        ll = LinkedList([1, 2])
        ll.insert(1, 99)
        assert len(ll) == 3

    def test_insert_into_empty_at_nonzero_raises(self):
        ll = LinkedList()
        with pytest.raises(IndexError):
            ll.insert(1, 99)

    def test_insert_multiple_at_beginning(self):
        ll = LinkedList([3])
        ll.insert(0, 2)
        ll.insert(0, 1)
        assert list(ll) == [1, 2, 3]

    def test_negative_index(self):
        ll = LinkedList([10, 20, 30])
        ll.insert(-1, 99)
        assert list(ll) == [10, 20, 99, 30]


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------

class TestRemove:
    def test_present(self):
        ll = LinkedList([1, 2, 3])
        ll.remove(2)
        assert list(ll) == [1, 3]

    def test_absent_raises(self):
        ll = LinkedList([1, 2, 3])
        with pytest.raises(ValueError):
            ll.remove(99)

    def test_first_occurrence_only(self):
        ll = LinkedList([1, 2, 2, 3])
        ll.remove(2)
        assert list(ll) == [1, 2, 3]

    def test_remove_head(self):
        ll = LinkedList([1, 2, 3])
        ll.remove(1)
        assert list(ll) == [2, 3]

    def test_remove_tail(self):
        ll = LinkedList([1, 2, 3])
        ll.remove(3)
        assert list(ll) == [1, 2]

    def test_remove_only_element(self):
        ll = LinkedList([1])
        ll.remove(1)
        assert list(ll) == []
        assert len(ll) == 0

    def test_remove_from_empty_raises(self):
        ll = LinkedList()
        with pytest.raises(ValueError):
            ll.remove(1)

    def test_remove_updates_length(self):
        ll = LinkedList([1, 2, 3])
        ll.remove(2)
        assert len(ll) == 2

    def test_remove_duplicates_keeps_rest(self):
        ll = LinkedList([1, 2, 2, 2, 3])
        ll.remove(2)
        assert ll.count(2) == 2


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_non_empty(self):
        ll = LinkedList([1, 2, 3])
        ll.clear()
        assert len(ll) == 0
        assert list(ll) == []

    def test_already_empty(self):
        ll = LinkedList()
        ll.clear()
        assert len(ll) == 0

    def test_then_add_elements(self):
        ll = LinkedList([1, 2, 3])
        ll.clear()
        ll.push_back(99)
        assert list(ll) == [99]
        assert len(ll) == 1

    def test_clear_sets_head_none(self):
        ll = LinkedList([1, 2])
        ll.clear()
        assert ll.head is None


# ---------------------------------------------------------------------------
# copy
# ---------------------------------------------------------------------------

class TestCopy:
    def test_values_equal(self):
        ll = LinkedList([1, 2, 3])
        cp = ll.copy()
        assert list(cp) == [1, 2, 3]

    def test_is_different_object(self):
        ll = LinkedList([1, 2, 3])
        cp = ll.copy()
        assert cp is not ll

    def test_modification_independence(self):
        ll = LinkedList([1, 2, 3])
        cp = ll.copy()
        cp.push_back(4)
        assert list(ll) == [1, 2, 3], "Modifying copy should not affect original"
        assert list(cp) == [1, 2, 3, 4]

    def test_original_modification_independence(self):
        ll = LinkedList([1, 2, 3])
        cp = ll.copy()
        ll.push_front(0)
        assert list(cp) == [1, 2, 3], "Modifying original should not affect copy"

    def test_copy_empty(self):
        ll = LinkedList()
        cp = ll.copy()
        assert list(cp) == []
        assert len(cp) == 0

    def test_copy_single(self):
        ll = LinkedList([42])
        cp = ll.copy()
        assert list(cp) == [42]


# ---------------------------------------------------------------------------
# count
# ---------------------------------------------------------------------------

class TestCount:
    def test_zero_occurrences(self):
        ll = LinkedList([1, 2, 3])
        assert ll.count(99) == 0

    def test_one_occurrence(self):
        ll = LinkedList([1, 2, 3])
        assert ll.count(2) == 1

    def test_many_occurrences(self):
        ll = LinkedList([1, 2, 2, 3, 2])
        assert ll.count(2) == 3

    def test_empty_list(self):
        assert LinkedList().count(1) == 0

    def test_after_push(self):
        ll = LinkedList([1, 2])
        ll.push_back(2)
        assert ll.count(2) == 2

    def test_after_remove(self):
        ll = LinkedList([1, 2, 2, 3])
        ll.remove(2)
        assert ll.count(2) == 1

    def test_count_none(self):
        ll = LinkedList([None, 1, None])
        assert ll.count(None) == 2


# ---------------------------------------------------------------------------
# index
# ---------------------------------------------------------------------------

class TestIndex:
    def test_found(self):
        ll = LinkedList([10, 20, 30])
        assert ll.index(20) == 1

    def test_not_found_raises(self):
        ll = LinkedList([1, 2, 3])
        with pytest.raises(ValueError):
            ll.index(99)

    def test_first_occurrence(self):
        ll = LinkedList([1, 2, 2, 3])
        assert ll.index(2) == 1

    def test_head(self):
        ll = LinkedList([10, 20, 30])
        assert ll.index(10) == 0

    def test_tail(self):
        ll = LinkedList([10, 20, 30])
        assert ll.index(30) == 2

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            LinkedList().index(1)

    def test_single_element_found(self):
        assert LinkedList([42]).index(42) == 0


# ---------------------------------------------------------------------------
# reverse
# ---------------------------------------------------------------------------

class TestReverse:
    def test_empty(self):
        ll = LinkedList()
        ll.reverse()
        assert list(ll) == []

    def test_single(self):
        ll = LinkedList([1])
        ll.reverse()
        assert list(ll) == [1]

    def test_multiple(self):
        ll = LinkedList([1, 2, 3, 4])
        ll.reverse()
        assert list(ll) == [4, 3, 2, 1]

    def test_preserves_elements(self):
        ll = LinkedList([3, 1, 4, 1, 5])
        ll.reverse()
        assert sorted(list(ll)) == [1, 1, 3, 4, 5]

    def test_is_in_place(self):
        ll = LinkedList([1, 2, 3])
        original_id = id(ll)
        ll.reverse()
        assert id(ll) == original_id

    def test_reverse_returns_none(self):
        ll = LinkedList([1, 2])
        result = ll.reverse()
        assert result is None

    def test_double_reverse(self):
        ll = LinkedList([1, 2, 3, 4, 5])
        ll.reverse()
        ll.reverse()
        assert list(ll) == [1, 2, 3, 4, 5]

    def test_two_elements(self):
        ll = LinkedList([1, 2])
        ll.reverse()
        assert list(ll) == [2, 1]


# ---------------------------------------------------------------------------
# to_list
# ---------------------------------------------------------------------------

class TestToList:
    def test_empty(self):
        assert LinkedList().to_list() == []

    def test_single(self):
        assert LinkedList([42]).to_list() == [42]

    def test_multiple(self):
        assert LinkedList([1, 2, 3]).to_list() == [1, 2, 3]

    def test_returns_python_list(self):
        result = LinkedList([1, 2]).to_list()
        assert type(result) is list

    def test_independent_of_linked_list(self):
        ll = LinkedList([1, 2, 3])
        py_list = ll.to_list()
        ll.push_back(4)
        assert py_list == [1, 2, 3], "Modifying LinkedList should not affect returned list"


# ---------------------------------------------------------------------------
# sorted
# ---------------------------------------------------------------------------

class TestSorted:
    def test_empty(self):
        ll = LinkedList()
        result = ll.sorted()
        assert list(result) == []

    def test_single(self):
        ll = LinkedList([1])
        result = ll.sorted()
        assert list(result) == [1]

    def test_already_sorted(self):
        ll = LinkedList([1, 2, 3])
        result = ll.sorted()
        assert list(result) == [1, 2, 3]

    def test_reverse_sorted(self):
        ll = LinkedList([3, 2, 1])
        result = ll.sorted()
        assert list(result) == [1, 2, 3]

    def test_with_duplicates(self):
        ll = LinkedList([3, 1, 2, 1])
        result = ll.sorted()
        assert list(result) == [1, 1, 2, 3]

    def test_does_not_mutate_original(self):
        ll = LinkedList([3, 1, 2])
        _ = ll.sorted()
        assert list(ll) == [3, 1, 2], "sorted() must not mutate the original list"

    def test_returns_new_linked_list(self):
        ll = LinkedList([3, 1, 2])
        result = ll.sorted()
        assert isinstance(result, LinkedList)
        assert result is not ll

    def test_large_random(self):
        import random
        data = [random.randint(0, 1000) for _ in range(500)]
        ll = LinkedList(data)
        result = ll.sorted()
        assert list(result) == sorted(data)

    def test_negative_numbers(self):
        ll = LinkedList([3, -1, 0, -5, 2])
        assert list(ll.sorted()) == [-5, -1, 0, 2, 3]

    def test_all_same(self):
        ll = LinkedList([7, 7, 7, 7])
        assert list(ll.sorted()) == [7, 7, 7, 7]


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------

class TestMerge:
    def test_both_empty(self):
        a = LinkedList()
        b = LinkedList()
        result = a.merge(b)
        assert list(result) == []

    def test_first_empty(self):
        a = LinkedList()
        b = LinkedList([1, 2, 3])
        result = a.merge(b)
        assert list(result) == [1, 2, 3]

    def test_second_empty(self):
        a = LinkedList([1, 2, 3])
        b = LinkedList()
        result = a.merge(b)
        assert list(result) == [1, 2, 3]

    def test_equal_length(self):
        a = LinkedList([1, 3, 5])
        b = LinkedList([2, 4, 6])
        result = a.merge(b)
        assert list(result) == [1, 2, 3, 4, 5, 6]

    def test_unequal_length(self):
        a = LinkedList([1, 5])
        b = LinkedList([2, 3, 4, 6])
        result = a.merge(b)
        assert list(result) == [1, 2, 3, 4, 5, 6]

    def test_with_duplicates(self):
        a = LinkedList([1, 2, 4])
        b = LinkedList([1, 3, 4])
        result = a.merge(b)
        assert list(result) == [1, 1, 2, 3, 4, 4]

    def test_does_not_mutate_originals(self):
        a = LinkedList([1, 3, 5])
        b = LinkedList([2, 4, 6])
        _ = a.merge(b)
        assert list(a) == [1, 3, 5], "merge() must not mutate self"
        assert list(b) == [2, 4, 6], "merge() must not mutate other"

    def test_result_is_new_linked_list(self):
        a = LinkedList([1])
        b = LinkedList([2])
        result = a.merge(b)
        assert isinstance(result, LinkedList)
        assert result is not a
        assert result is not b

    def test_interleaved(self):
        a = LinkedList([1, 4, 7, 10])
        b = LinkedList([2, 5, 8, 11])
        result = a.merge(b)
        assert list(result) == [1, 2, 4, 5, 7, 8, 10, 11]

    def test_all_from_first(self):
        a = LinkedList([1, 2, 3])
        b = LinkedList([4, 5, 6])
        result = a.merge(b)
        assert list(result) == [1, 2, 3, 4, 5, 6]


# ---------------------------------------------------------------------------
# has_cycle
# ---------------------------------------------------------------------------

class TestHasCycle:
    """
    To test cycle detection, we manually manipulate the internal .head and
    .next pointers to create cycles. This is the one place where tests
    reach into internal structure, because there is no public API to create
    a cycle (nor should there be).
    """

    def test_no_cycle(self):
        ll = LinkedList([1, 2, 3, 4, 5])
        assert ll.has_cycle() is False

    def test_empty_no_cycle(self):
        ll = LinkedList()
        assert ll.has_cycle() is False

    def test_single_node_no_cycle(self):
        ll = LinkedList([1])
        assert ll.has_cycle() is False

    def test_single_node_cycle(self):
        ll = LinkedList([1])
        # Point the single node back to itself
        ll.head.next = ll.head
        assert ll.has_cycle() is True

    def test_cycle_at_head(self):
        ll = LinkedList([1, 2, 3])
        # Make the tail point back to the head
        node = ll.head
        while node.next:
            node = node.next
        node.next = ll.head
        assert ll.has_cycle() is True

    def test_cycle_at_middle(self):
        ll = LinkedList([1, 2, 3, 4, 5])
        # Make the tail point back to node 3 (index 2)
        middle = ll.head.next.next  # node with value 3
        node = middle
        while node.next:
            node = node.next
        node.next = middle
        assert ll.has_cycle() is True

    def test_cycle_between_last_two(self):
        ll = LinkedList([1, 2, 3])
        # Make node 3 point back to node 2
        second = ll.head.next  # value 2
        third = second.next     # value 3
        third.next = second
        assert ll.has_cycle() is True

    def test_two_nodes_cycle(self):
        ll = LinkedList([1, 2])
        ll.head.next.next = ll.head
        assert ll.has_cycle() is True

    def test_two_nodes_no_cycle(self):
        ll = LinkedList([1, 2])
        assert ll.has_cycle() is False


# ---------------------------------------------------------------------------
# midpoint
# ---------------------------------------------------------------------------

class TestMidpoint:
    def test_odd_length(self):
        ll = LinkedList([1, 2, 3, 4, 5])
        assert ll.midpoint() == 3

    def test_even_length(self):
        # For even length, return the earlier middle
        ll = LinkedList([1, 2, 3, 4])
        assert ll.midpoint() == 2

    def test_single_element(self):
        ll = LinkedList([42])
        assert ll.midpoint() == 42

    def test_empty_raises(self):
        ll = LinkedList()
        with pytest.raises(IndexError):
            ll.midpoint()

    def test_two_elements(self):
        ll = LinkedList([10, 20])
        assert ll.midpoint() == 10

    def test_three_elements(self):
        ll = LinkedList([10, 20, 30])
        assert ll.midpoint() == 20

    def test_six_elements(self):
        ll = LinkedList([1, 2, 3, 4, 5, 6])
        assert ll.midpoint() == 3

    def test_seven_elements(self):
        ll = LinkedList([1, 2, 3, 4, 5, 6, 7])
        assert ll.midpoint() == 4


# ---------------------------------------------------------------------------
# remove_duplicates
# ---------------------------------------------------------------------------

class TestRemoveDuplicates:
    def test_no_duplicates(self):
        ll = LinkedList([1, 2, 3])
        ll.remove_duplicates()
        assert list(ll) == [1, 2, 3]

    def test_all_duplicates(self):
        ll = LinkedList([5, 5, 5, 5])
        ll.remove_duplicates()
        assert list(ll) == [5]

    def test_mixed(self):
        ll = LinkedList([1, 2, 3, 2, 1, 4])
        ll.remove_duplicates()
        assert list(ll) == [1, 2, 3, 4]

    def test_empty(self):
        ll = LinkedList()
        ll.remove_duplicates()
        assert list(ll) == []

    def test_single(self):
        ll = LinkedList([1])
        ll.remove_duplicates()
        assert list(ll) == [1]

    def test_preserves_first_occurrence_order(self):
        ll = LinkedList([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
        ll.remove_duplicates()
        assert list(ll) == [3, 1, 4, 5, 9, 2, 6]

    def test_updates_length(self):
        ll = LinkedList([1, 1, 2, 2, 3, 3])
        ll.remove_duplicates()
        assert len(ll) == 3

    def test_adjacent_duplicates(self):
        ll = LinkedList([1, 1, 2, 2, 3, 3])
        ll.remove_duplicates()
        assert list(ll) == [1, 2, 3]

    def test_returns_none(self):
        ll = LinkedList([1, 2, 2])
        result = ll.remove_duplicates()
        assert result is None


# ---------------------------------------------------------------------------
# Iteration
# ---------------------------------------------------------------------------

class TestIteration:
    def test_for_loop(self):
        ll = LinkedList([10, 20, 30])
        values = []
        for v in ll:
            values.append(v)
        assert values == [10, 20, 30]

    def test_list_conversion(self):
        ll = LinkedList([1, 2, 3])
        assert list(ll) == [1, 2, 3]

    def test_multiple_iterations(self):
        ll = LinkedList([1, 2, 3])
        first = list(ll)
        second = list(ll)
        assert first == second == [1, 2, 3]

    def test_sum(self):
        ll = LinkedList([1, 2, 3, 4, 5])
        assert sum(ll) == 15

    def test_unpacking(self):
        ll = LinkedList([1, 2, 3])
        a, b, c = ll
        assert (a, b, c) == (1, 2, 3)

    def test_enumerate(self):
        ll = LinkedList(["a", "b", "c"])
        pairs = list(enumerate(ll))
        assert pairs == [(0, "a"), (1, "b"), (2, "c")]

    def test_empty_iteration(self):
        ll = LinkedList()
        values = list(ll)
        assert values == []

    def test_iteration_preserves_list(self):
        ll = LinkedList([1, 2, 3])
        _ = list(ll)
        assert len(ll) == 3
        assert list(ll) == [1, 2, 3]


# ---------------------------------------------------------------------------
# Stress tests
# ---------------------------------------------------------------------------

class TestStress:
    def test_build_large_list(self):
        ll = LinkedList(range(100_000))
        assert len(ll) == 100_000

    def test_push_front_10k(self):
        ll = LinkedList()
        for i in range(10_000):
            ll.push_front(i)
        assert len(ll) == 10_000
        assert ll[0] == 9999

    def test_push_back_10k(self):
        ll = LinkedList()
        for i in range(10_000):
            ll.push_back(i)
        assert len(ll) == 10_000
        assert ll[-1] == 9999

    def test_iteration_large(self):
        ll = LinkedList(range(50_000))
        total = sum(ll)
        assert total == sum(range(50_000))

    def test_reverse_large(self):
        ll = LinkedList(range(10_000))
        ll.reverse()
        assert ll[0] == 9999
        assert ll[-1] == 0

    def test_sorted_10k(self):
        import random
        data = list(range(10_000))
        random.shuffle(data)
        ll = LinkedList(data)
        result = ll.sorted()
        assert list(result) == list(range(10_000))

    def test_pop_front_until_empty(self):
        ll = LinkedList(range(5_000))
        for _ in range(5_000):
            ll.pop_front()
        assert len(ll) == 0

    def test_count_large(self):
        ll = LinkedList([1, 2, 3] * 10_000)
        assert ll.count(2) == 10_000

    def test_remove_duplicates_large(self):
        ll = LinkedList(list(range(100)) * 100)
        assert len(ll) == 10_000
        ll.remove_duplicates()
        assert len(ll) == 100
        assert list(ll) == list(range(100))


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_browser_history(self):
        """Simulate browser history: push URLs, pop to go back."""
        history = LinkedList()
        history.push_back("google.com")
        history.push_back("github.com")
        history.push_back("python.org")
        history.push_back("docs.python.org")

        # Go back twice
        assert history.pop_back() == "docs.python.org"
        assert history.pop_back() == "python.org"

        # Navigate somewhere new
        history.push_back("stackoverflow.com")
        assert list(history) == ["google.com", "github.com", "stackoverflow.com"]

    def test_polynomial_addition(self):
        """
        Represent polynomials as linked lists of (coefficient, exponent) tuples,
        sorted by exponent. Add two polynomials by merging.

        p1 = 3x^2 + 2x + 1  ->  [(1,0), (2,1), (3,2)]
        p2 = 5x^3 + 4x      ->  [(4,1), (5,3)]
        sum = 5x^3 + 3x^2 + 6x + 1
        """
        p1 = LinkedList([(1, 0), (2, 1), (3, 2)])
        p2 = LinkedList([(4, 1), (5, 3)])

        # Collect all terms
        all_terms = {}
        for coeff, exp in p1:
            all_terms[exp] = all_terms.get(exp, 0) + coeff
        for coeff, exp in p2:
            all_terms[exp] = all_terms.get(exp, 0) + coeff

        # all_terms maps exponent -> coefficient; rebuild as (coeff, exp) sorted by exp
        result = LinkedList(
            (coeff, exp) for exp, coeff in sorted(all_terms.items())
        )
        expected = LinkedList([(1, 0), (6, 1), (3, 2), (5, 3)])
        assert result == expected

    def test_reverse_sentence(self):
        """Reverse a sentence word by word using a linked list."""
        sentence = "the quick brown fox"
        words = LinkedList(sentence.split())
        words.reverse()
        reversed_sentence = " ".join(words)
        assert reversed_sentence == "fox brown quick the"

    def test_round_trip_operations(self):
        """Build a list, sort it, reverse it, convert to Python list, rebuild."""
        ll = LinkedList([5, 3, 8, 1, 9, 2])
        sorted_ll = ll.sorted()
        sorted_ll.reverse()
        py_list = sorted_ll.to_list()
        assert py_list == [9, 8, 5, 3, 2, 1]
        rebuilt = LinkedList(py_list)
        assert rebuilt == sorted_ll

    def test_copy_and_mutate(self):
        """Copy a list, mutate both independently, verify separation."""
        original = LinkedList([1, 2, 3, 4, 5])
        backup = original.copy()

        original.reverse()
        original.push_front(0)
        backup.push_back(6)
        backup.remove(1)

        assert list(original) == [0, 5, 4, 3, 2, 1]
        assert list(backup) == [2, 3, 4, 5, 6]

    def test_merge_and_deduplicate(self):
        """Merge two sorted lists, then remove duplicates."""
        a = LinkedList([1, 2, 3, 5])
        b = LinkedList([2, 3, 4, 6])
        merged = a.merge(b)
        assert list(merged) == [1, 2, 2, 3, 3, 4, 5, 6]
        merged.remove_duplicates()
        assert list(merged) == [1, 2, 3, 4, 5, 6]

    def test_midpoint_after_operations(self):
        """Build list dynamically, check midpoint at various stages."""
        ll = LinkedList()
        ll.push_back(10)
        assert ll.midpoint() == 10

        ll.push_back(20)
        assert ll.midpoint() == 10  # earlier middle for even

        ll.push_back(30)
        assert ll.midpoint() == 20  # middle of 3

        ll.push_front(5)
        # [5, 10, 20, 30] -> earlier middle is index 1 = 10
        assert ll.midpoint() == 10

    def test_index_and_setitem(self):
        """Use index() to find a value, then update it with __setitem__."""
        ll = LinkedList(["apple", "banana", "cherry"])
        idx = ll.index("banana")
        ll[idx] = "blueberry"
        assert list(ll) == ["apple", "blueberry", "cherry"]
        assert "banana" not in ll
        assert "blueberry" in ll

    def test_stack_behavior(self):
        """Use push_front/pop_front as a stack (LIFO)."""
        stack = LinkedList()
        for item in [1, 2, 3, 4, 5]:
            stack.push_front(item)
        popped = []
        while not stack.is_empty():
            popped.append(stack.pop_front())
        assert popped == [5, 4, 3, 2, 1]

    def test_queue_behavior(self):
        """Use push_back/pop_front as a queue (FIFO)."""
        queue = LinkedList()
        for item in [1, 2, 3, 4, 5]:
            queue.push_back(item)
        dequeued = []
        while not queue.is_empty():
            dequeued.append(queue.pop_front())
        assert dequeued == [1, 2, 3, 4, 5]
