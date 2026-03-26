"""Comprehensive pytest suite for the HashMap class.

Run with:  pytest test_hash_map.py -v
"""

import time

import pytest

from hash_map import HashMap


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_default_capacity(self):
        hm = HashMap()
        assert hm.capacity() == 8

    def test_custom_capacity(self):
        hm = HashMap(capacity=16)
        assert hm.capacity() == 16

    def test_custom_load_factor(self):
        hm = HashMap(load_factor_threshold=0.5)
        # Just verify it was created; load factor behaviour tested elsewhere.
        assert hm.capacity() == 8

    def test_capacity_of_one(self):
        hm = HashMap(capacity=1)
        assert hm.capacity() == 1

    def test_large_capacity(self):
        hm = HashMap(capacity=1024)
        assert hm.capacity() == 1024

    def test_newly_created_is_empty(self):
        hm = HashMap()
        assert len(hm) == 0
        assert hm.is_empty()


# ---------------------------------------------------------------------------
# __len__
# ---------------------------------------------------------------------------

class TestLen:
    def test_empty(self):
        assert len(HashMap()) == 0

    def test_after_one_insert(self):
        hm = HashMap()
        hm["a"] = 1
        assert len(hm) == 1

    def test_after_multiple_inserts(self):
        hm = HashMap()
        for i in range(10):
            hm[i] = i
        assert len(hm) == 10

    def test_after_update_existing_key(self):
        hm = HashMap()
        hm["a"] = 1
        hm["a"] = 2
        assert len(hm) == 1

    def test_after_delete(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        del hm["a"]
        assert len(hm) == 1

    def test_after_delete_all(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        assert len(hm) == 0

    def test_after_clear(self):
        hm = HashMap()
        for i in range(5):
            hm[i] = i
        hm.clear()
        assert len(hm) == 0


# ---------------------------------------------------------------------------
# __bool__
# ---------------------------------------------------------------------------

class TestBool:
    def test_empty_is_falsy(self):
        assert not HashMap()

    def test_nonempty_is_truthy(self):
        hm = HashMap()
        hm["x"] = 1
        assert hm

    def test_after_clear_is_falsy(self):
        hm = HashMap()
        hm["x"] = 1
        hm.clear()
        assert not hm

    def test_after_delete_last_is_falsy(self):
        hm = HashMap()
        hm["x"] = 1
        del hm["x"]
        assert not hm


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------

class TestRepr:
    def test_empty(self):
        assert repr(HashMap()) == "HashMap({})"

    def test_single_pair(self):
        hm = HashMap()
        hm["a"] = 1
        assert repr(hm) == "HashMap({'a': 1})"

    def test_multiple_pairs_all_present(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        r = repr(hm)
        assert r.startswith("HashMap({")
        assert r.endswith("})")
        assert "'a': 1" in r
        assert "'b': 2" in r

    def test_repr_with_string_values(self):
        hm = HashMap()
        hm[1] = "hello"
        assert "1: 'hello'" in repr(hm)


# ---------------------------------------------------------------------------
# __contains__
# ---------------------------------------------------------------------------

class TestContains:
    def test_present(self):
        hm = HashMap()
        hm["a"] = 1
        assert "a" in hm

    def test_absent(self):
        hm = HashMap()
        assert "a" not in hm

    def test_empty_map(self):
        assert "anything" not in HashMap()

    def test_after_deletion(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        assert "a" not in hm

    def test_other_keys_unaffected(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        del hm["a"]
        assert "b" in hm

    def test_after_update(self):
        hm = HashMap()
        hm["a"] = 1
        hm["a"] = 2
        assert "a" in hm


# ---------------------------------------------------------------------------
# __getitem__
# ---------------------------------------------------------------------------

class TestGetItem:
    def test_present(self):
        hm = HashMap()
        hm["a"] = 42
        assert hm["a"] == 42

    def test_absent_raises(self):
        hm = HashMap()
        with pytest.raises(KeyError):
            _ = hm["missing"]

    def test_after_update(self):
        hm = HashMap()
        hm["a"] = 1
        hm["a"] = 2
        assert hm["a"] == 2

    def test_after_delete_raises(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        with pytest.raises(KeyError):
            _ = hm["a"]

    def test_multiple_keys(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        hm["c"] = 3
        assert hm["a"] == 1
        assert hm["b"] == 2
        assert hm["c"] == 3

    def test_int_key(self):
        hm = HashMap()
        hm[7] = "seven"
        assert hm[7] == "seven"


# ---------------------------------------------------------------------------
# __setitem__
# ---------------------------------------------------------------------------

class TestSetItem:
    def test_new_key(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm["a"] == 1

    def test_update_existing(self):
        hm = HashMap()
        hm["a"] = 1
        hm["a"] = 99
        assert hm["a"] == 99
        assert len(hm) == 1

    def test_many_keys(self):
        hm = HashMap()
        for i in range(100):
            hm[f"key{i}"] = i
        assert len(hm) == 100
        for i in range(100):
            assert hm[f"key{i}"] == i

    def test_none_as_value(self):
        hm = HashMap()
        hm["a"] = None
        assert hm["a"] is None
        assert "a" in hm

    def test_none_as_key(self):
        hm = HashMap()
        hm[None] = "none_value"
        assert hm[None] == "none_value"

    def test_zero_as_key(self):
        hm = HashMap()
        hm[0] = "zero"
        assert hm[0] == "zero"

    def test_empty_string_key(self):
        hm = HashMap()
        hm[""] = "empty"
        assert hm[""] == "empty"

    def test_int_keys(self):
        hm = HashMap()
        hm[1] = "one"
        hm[2] = "two"
        assert hm[1] == "one"
        assert hm[2] == "two"

    def test_str_keys(self):
        hm = HashMap()
        hm["hello"] = "world"
        assert hm["hello"] == "world"

    def test_tuple_key(self):
        hm = HashMap()
        hm[(1, 2)] = "tuple"
        assert hm[(1, 2)] == "tuple"

    def test_float_key(self):
        hm = HashMap()
        hm[3.14] = "pi"
        assert hm[3.14] == "pi"

    def test_bool_key(self):
        hm = HashMap()
        hm[True] = "true"
        assert hm[True] == "true"

    def test_frozenset_key(self):
        hm = HashMap()
        fs = frozenset([1, 2, 3])
        hm[fs] = "frozen"
        assert hm[fs] == "frozen"

    def test_negative_int_key(self):
        hm = HashMap()
        hm[-5] = "negative"
        assert hm[-5] == "negative"

    def test_large_int_key(self):
        hm = HashMap()
        hm[10**18] = "big"
        assert hm[10**18] == "big"

    def test_unhashable_key_raises_type_error(self):
        hm = HashMap()
        with pytest.raises(TypeError):
            hm[[1, 2]] = "list"


# ---------------------------------------------------------------------------
# Key equivalence (bool/int/float)
# ---------------------------------------------------------------------------

class TestKeyEquivalence:
    def test_bool_true_and_int_one_same_key(self):
        hm = HashMap()
        hm[1] = "one"
        hm[True] = "true"
        assert len(hm) == 1
        assert hm[1] == "true"

    def test_bool_false_and_int_zero_same_key(self):
        hm = HashMap()
        hm[0] = "zero"
        hm[False] = "false"
        assert len(hm) == 1
        assert hm[0] == "false"

    def test_int_and_float_same_key(self):
        hm = HashMap()
        hm[1] = "int"
        hm[1.0] = "float"
        assert len(hm) == 1
        assert hm[1] == "float"

    def test_distinct_keys_not_confused(self):
        hm = HashMap()
        hm[0] = "zero"
        hm[1] = "one"
        hm[2] = "two"
        assert len(hm) == 3
        assert hm[0] == "zero"
        assert hm[1] == "one"
        assert hm[2] == "two"


# ---------------------------------------------------------------------------
# __delitem__
# ---------------------------------------------------------------------------

class TestDelItem:
    def test_present(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        assert "a" not in hm

    def test_absent_raises(self):
        hm = HashMap()
        with pytest.raises(KeyError):
            del hm["missing"]

    def test_delete_then_readd(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        hm["a"] = 2
        assert hm["a"] == 2
        assert len(hm) == 1

    def test_delete_all(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        del hm["a"]
        del hm["b"]
        assert len(hm) == 0
        assert hm.is_empty()

    def test_delete_does_not_affect_others(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        hm["c"] = 3
        del hm["b"]
        assert hm["a"] == 1
        assert hm["c"] == 3

    def test_delete_from_empty_raises(self):
        with pytest.raises(KeyError):
            del HashMap()["x"]


# ---------------------------------------------------------------------------
# __eq__
# ---------------------------------------------------------------------------

class TestEquality:
    def test_same_pairs(self):
        a = HashMap()
        b = HashMap()
        a["x"] = 1
        b["x"] = 1
        assert a == b

    def test_different_values(self):
        a = HashMap()
        b = HashMap()
        a["x"] = 1
        b["x"] = 2
        assert a != b

    def test_different_keys(self):
        a = HashMap()
        b = HashMap()
        a["x"] = 1
        b["y"] = 1
        assert a != b

    def test_different_sizes(self):
        a = HashMap()
        b = HashMap()
        a["x"] = 1
        a["y"] = 2
        b["x"] = 1
        assert a != b

    def test_both_empty(self):
        assert HashMap() == HashMap()

    def test_different_capacities_same_data(self):
        a = HashMap(capacity=4)
        b = HashMap(capacity=32)
        for i in range(3):
            a[i] = i
            b[i] = i
        assert a == b

    def test_vs_non_hashmap(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm != {"a": 1}

    def test_vs_non_hashmap_returns_not_implemented(self):
        hm = HashMap()
        assert hm.__eq__(42) is NotImplemented

    def test_order_independent(self):
        a = HashMap()
        b = HashMap()
        a["x"] = 1
        a["y"] = 2
        b["y"] = 2
        b["x"] = 1
        assert a == b


# ---------------------------------------------------------------------------
# is_empty
# ---------------------------------------------------------------------------

class TestIsEmpty:
    def test_empty(self):
        assert HashMap().is_empty()

    def test_non_empty(self):
        hm = HashMap()
        hm["a"] = 1
        assert not hm.is_empty()

    def test_after_clear(self):
        hm = HashMap()
        hm["a"] = 1
        hm.clear()
        assert hm.is_empty()

    def test_after_delete_all(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        assert hm.is_empty()


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------

class TestGet:
    def test_present(self):
        hm = HashMap()
        hm["a"] = 42
        assert hm.get("a") == 42

    def test_absent_returns_none(self):
        assert HashMap().get("missing") is None

    def test_absent_returns_custom_default(self):
        assert HashMap().get("missing", 99) == 99

    def test_after_delete(self):
        hm = HashMap()
        hm["a"] = 1
        del hm["a"]
        assert hm.get("a") is None

    def test_default_not_used_when_present(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm.get("a", 999) == 1

    def test_none_value_distinguished_from_missing(self):
        hm = HashMap()
        hm["a"] = None
        # get returns None because it's the stored value, not because key is missing.
        assert hm.get("a", "SENTINEL") is None


# ---------------------------------------------------------------------------
# put
# ---------------------------------------------------------------------------

class TestPut:
    def test_new_key(self):
        hm = HashMap()
        hm.put("a", 1)
        assert hm["a"] == 1

    def test_update_key(self):
        hm = HashMap()
        hm.put("a", 1)
        hm.put("a", 2)
        assert hm["a"] == 2
        assert len(hm) == 1

    def test_put_matches_setitem(self):
        a = HashMap()
        b = HashMap()
        a["x"] = 10
        b.put("x", 10)
        assert a == b


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------

class TestRemove:
    def test_present_returns_value(self):
        hm = HashMap()
        hm["a"] = 42
        assert hm.remove("a") == 42
        assert "a" not in hm

    def test_absent_raises(self):
        with pytest.raises(KeyError):
            HashMap().remove("missing")

    def test_len_decreases(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        hm.remove("a")
        assert len(hm) == 1


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_non_empty(self):
        hm = HashMap()
        for i in range(10):
            hm[i] = i
        hm.clear()
        assert len(hm) == 0
        assert hm.is_empty()

    def test_already_empty(self):
        hm = HashMap()
        hm.clear()
        assert len(hm) == 0

    def test_usable_after_clear(self):
        hm = HashMap()
        hm["a"] = 1
        hm.clear()
        hm["b"] = 2
        assert hm["b"] == 2
        assert len(hm) == 1

    def test_capacity_unchanged(self):
        hm = HashMap(capacity=16)
        hm["a"] = 1
        hm.clear()
        assert hm.capacity() == 16


# ---------------------------------------------------------------------------
# keys
# ---------------------------------------------------------------------------

class TestKeys:
    def test_empty(self):
        assert HashMap().keys() == []

    def test_single(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm.keys() == ["a"]

    def test_multiple_order_independent(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        hm["c"] = 3
        assert set(hm.keys()) == {"a", "b", "c"}

    def test_after_delete(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        del hm["a"]
        assert set(hm.keys()) == {"b"}


# ---------------------------------------------------------------------------
# values
# ---------------------------------------------------------------------------

class TestValues:
    def test_empty(self):
        assert HashMap().values() == []

    def test_single(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm.values() == [1]

    def test_multiple(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        assert sorted(hm.values()) == [1, 2]

    def test_duplicates(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 1
        assert sorted(hm.values()) == [1, 1]


# ---------------------------------------------------------------------------
# items
# ---------------------------------------------------------------------------

class TestItems:
    def test_empty(self):
        assert HashMap().items() == []

    def test_single(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm.items() == [("a", 1)]

    def test_multiple_order_independent(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        assert set(hm.items()) == {("a", 1), ("b", 2)}

    def test_after_update(self):
        hm = HashMap()
        hm["a"] = 1
        hm["a"] = 2
        assert set(hm.items()) == {("a", 2)}


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------

class TestUpdate:
    def test_from_dict(self):
        hm = HashMap()
        hm.update({"a": 1, "b": 2})
        assert hm["a"] == 1
        assert hm["b"] == 2

    def test_from_hashmap(self):
        src = HashMap()
        src["x"] = 10
        dst = HashMap()
        dst.update(src)
        assert dst["x"] == 10

    def test_overlapping_keys(self):
        hm = HashMap()
        hm["a"] = 1
        hm.update({"a": 99, "b": 2})
        assert hm["a"] == 99
        assert hm["b"] == 2

    def test_empty_source(self):
        hm = HashMap()
        hm["a"] = 1
        hm.update({})
        assert hm["a"] == 1
        assert len(hm) == 1

    def test_update_empty_map(self):
        hm = HashMap()
        hm.update({"a": 1, "b": 2, "c": 3})
        assert len(hm) == 3


# ---------------------------------------------------------------------------
# setdefault
# ---------------------------------------------------------------------------

class TestSetDefault:
    def test_key_exists_returns_existing(self):
        hm = HashMap()
        hm["a"] = 1
        assert hm.setdefault("a", 999) == 1

    def test_key_exists_does_not_change(self):
        hm = HashMap()
        hm["a"] = 1
        hm.setdefault("a", 999)
        assert hm["a"] == 1

    def test_key_absent_sets_and_returns_default(self):
        hm = HashMap()
        result = hm.setdefault("a", 42)
        assert result == 42
        assert hm["a"] == 42

    def test_key_absent_no_default_sets_none(self):
        hm = HashMap()
        result = hm.setdefault("a")
        assert result is None
        assert hm["a"] is None

    def test_len_increases_when_absent(self):
        hm = HashMap()
        hm.setdefault("a", 1)
        assert len(hm) == 1

    def test_len_unchanged_when_present(self):
        hm = HashMap()
        hm["a"] = 1
        hm.setdefault("a", 2)
        assert len(hm) == 1


# ---------------------------------------------------------------------------
# pop
# ---------------------------------------------------------------------------

class TestPop:
    def test_present_returns_value_and_removes(self):
        hm = HashMap()
        hm["a"] = 42
        assert hm.pop("a") == 42
        assert "a" not in hm

    def test_absent_with_default(self):
        hm = HashMap()
        assert hm.pop("missing", 99) == 99

    def test_absent_without_default_raises(self):
        with pytest.raises(KeyError):
            HashMap().pop("missing")

    def test_len_decreases(self):
        hm = HashMap()
        hm["a"] = 1
        hm.pop("a")
        assert len(hm) == 0

    def test_absent_with_none_default(self):
        hm = HashMap()
        assert hm.pop("missing", None) is None

    def test_pop_does_not_affect_others(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        hm.pop("a")
        assert hm["b"] == 2

    def test_pop_too_many_args_raises_type_error(self):
        hm = HashMap()
        with pytest.raises(TypeError):
            hm.pop("key", "default", "extra")


# ---------------------------------------------------------------------------
# copy
# ---------------------------------------------------------------------------

class TestCopy:
    def test_same_data(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        cp = hm.copy()
        assert cp == hm

    def test_independence(self):
        hm = HashMap()
        hm["a"] = 1
        cp = hm.copy()
        cp["a"] = 999
        assert hm["a"] == 1

    def test_modification_independence(self):
        hm = HashMap()
        hm["a"] = 1
        cp = hm.copy()
        hm["b"] = 2
        assert "b" not in cp

    def test_copy_is_hashmap(self):
        hm = HashMap()
        hm["a"] = 1
        cp = hm.copy()
        assert isinstance(cp, HashMap)

    def test_copy_empty(self):
        hm = HashMap()
        cp = hm.copy()
        assert cp.is_empty()
        assert cp == hm


# ---------------------------------------------------------------------------
# load_factor
# ---------------------------------------------------------------------------

class TestLoadFactor:
    def test_empty(self):
        assert HashMap().load_factor() == 0.0

    def test_after_insertions(self):
        hm = HashMap(capacity=8)
        hm["a"] = 1
        hm["b"] = 2
        assert hm.load_factor() == 2 / 8

    def test_calculation(self):
        hm = HashMap(capacity=10)
        for i in range(5):
            hm[i] = i
        assert hm.load_factor() == pytest.approx(5 / 10)

    def test_after_delete(self):
        hm = HashMap(capacity=8)
        hm["a"] = 1
        hm["b"] = 2
        del hm["a"]
        assert hm.load_factor() == pytest.approx(1 / 8)


# ---------------------------------------------------------------------------
# capacity
# ---------------------------------------------------------------------------

class TestCapacity:
    def test_initial(self):
        assert HashMap(capacity=8).capacity() == 8

    def test_after_manual_resize(self):
        hm = HashMap(capacity=8)
        hm.resize(16)
        assert hm.capacity() == 16

    def test_after_auto_resize(self):
        hm = HashMap(capacity=4, load_factor_threshold=0.75)
        for i in range(4):  # load factor hits 1.0 > 0.75 at i=3
            hm[i] = i
        assert hm.capacity() > 4


# ---------------------------------------------------------------------------
# resize (manual)
# ---------------------------------------------------------------------------

class TestResize:
    def test_grow(self):
        hm = HashMap(capacity=4)
        hm["a"] = 1
        hm.resize(16)
        assert hm.capacity() == 16
        assert hm["a"] == 1

    def test_shrink(self):
        hm = HashMap(capacity=16)
        hm["a"] = 1
        hm.resize(4)
        assert hm.capacity() == 4
        assert hm["a"] == 1

    def test_all_keys_accessible(self):
        hm = HashMap(capacity=4)
        for i in range(10):
            hm[i] = i * 10
        hm.resize(32)
        for i in range(10):
            assert hm[i] == i * 10

    def test_len_unchanged(self):
        hm = HashMap(capacity=4)
        for i in range(5):
            hm[i] = i
        hm.resize(16)
        assert len(hm) == 5

    def test_resize_to_one(self):
        hm = HashMap(capacity=8)
        hm["a"] = 1
        hm["b"] = 2
        hm.resize(1)
        assert hm.capacity() == 1
        assert hm["a"] == 1
        assert hm["b"] == 2


# ---------------------------------------------------------------------------
# Auto-resize
# ---------------------------------------------------------------------------

class TestAutoResize:
    def test_triggers_on_load_factor_exceeded(self):
        hm = HashMap(capacity=4, load_factor_threshold=0.75)
        initial_cap = hm.capacity()
        # Insert enough to exceed 0.75 load factor (4 * 0.75 = 3, so 4th insert triggers)
        for i in range(4):
            hm[i] = i
        assert hm.capacity() > initial_cap

    def test_all_elements_accessible_after(self):
        hm = HashMap(capacity=4, load_factor_threshold=0.5)
        for i in range(20):
            hm[i] = i * 100
        for i in range(20):
            assert hm[i] == i * 100

    def test_load_factor_drops_after(self):
        hm = HashMap(capacity=4, load_factor_threshold=0.75)
        for i in range(10):
            hm[i] = i
        # After multiple resizes, load factor should be <= threshold
        assert hm.load_factor() <= 0.75

    def test_capacity_doubles(self):
        hm = HashMap(capacity=4, load_factor_threshold=0.75)
        # Insert 4 elements: after 4th, load_factor = 4/4 = 1.0 > 0.75 -> resize to 8
        for i in range(4):
            hm[i] = i
        assert hm.capacity() == 8

    def test_multiple_resizes(self):
        hm = HashMap(capacity=2, load_factor_threshold=0.75)
        for i in range(100):
            hm[i] = i
        # Started at 2, must have resized many times
        assert hm.capacity() >= 128
        assert len(hm) == 100


# ---------------------------------------------------------------------------
# Collisions
# ---------------------------------------------------------------------------

class TestCollisions:
    def _find_colliding_keys(self, capacity, count=3):
        """Find *count* distinct integer keys that hash to the same bucket."""
        buckets = {}
        key = 0
        while True:
            idx = hash(key) % capacity
            buckets.setdefault(idx, []).append(key)
            if any(len(v) >= count for v in buckets.values()):
                for v in buckets.values():
                    if len(v) >= count:
                        return v[:count]
            key += 1

    def test_insert_colliding_keys(self):
        cap = 4
        keys = self._find_colliding_keys(cap, 3)
        hm = HashMap(capacity=cap, load_factor_threshold=10.0)  # prevent auto-resize
        for i, k in enumerate(keys):
            hm[k] = i
        assert len(hm) == 3

    def test_retrieve_colliding_keys(self):
        cap = 4
        keys = self._find_colliding_keys(cap, 3)
        hm = HashMap(capacity=cap, load_factor_threshold=10.0)
        for i, k in enumerate(keys):
            hm[k] = i * 10
        for i, k in enumerate(keys):
            assert hm[k] == i * 10

    def test_delete_from_collision_chain(self):
        cap = 4
        keys = self._find_colliding_keys(cap, 3)
        hm = HashMap(capacity=cap, load_factor_threshold=10.0)
        for i, k in enumerate(keys):
            hm[k] = i
        del hm[keys[1]]  # delete middle of chain
        assert keys[1] not in hm
        assert hm[keys[0]] == 0
        assert hm[keys[2]] == 2

    def test_update_within_collision_chain(self):
        cap = 4
        keys = self._find_colliding_keys(cap, 3)
        hm = HashMap(capacity=cap, load_factor_threshold=10.0)
        for i, k in enumerate(keys):
            hm[k] = i
        hm[keys[1]] = 999
        assert hm[keys[1]] == 999
        assert len(hm) == 3

    def test_contains_in_collision_chain(self):
        cap = 4
        keys = self._find_colliding_keys(cap, 3)
        hm = HashMap(capacity=cap, load_factor_threshold=10.0)
        for i, k in enumerate(keys):
            hm[k] = i
        for k in keys:
            assert k in hm

    def test_delete_all_in_collision_chain(self):
        cap = 4
        keys = self._find_colliding_keys(cap, 3)
        hm = HashMap(capacity=cap, load_factor_threshold=10.0)
        for i, k in enumerate(keys):
            hm[k] = i
        for k in keys:
            del hm[k]
        assert len(hm) == 0
        for k in keys:
            assert k not in hm


# ---------------------------------------------------------------------------
# __iter__
# ---------------------------------------------------------------------------

class TestIter:
    def test_empty(self):
        assert list(HashMap()) == []

    def test_all_keys_yielded(self):
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        hm["c"] = 3
        assert set(hm) == {"a", "b", "c"}

    def test_len_matches(self):
        hm = HashMap()
        for i in range(20):
            hm[i] = i
        assert len(list(hm)) == 20

    def test_for_loop(self):
        hm = HashMap()
        hm["x"] = 10
        hm["y"] = 20
        collected = []
        for key in hm:
            collected.append(key)
        assert set(collected) == {"x", "y"}


# ---------------------------------------------------------------------------
# Stress tests
# ---------------------------------------------------------------------------

class TestStress:
    def test_insert_50000(self):
        hm = HashMap()
        n = 50_000
        for i in range(n):
            hm[i] = i * 2
        assert len(hm) == n
        for i in range(n):
            assert hm[i] == i * 2

    def test_delete_10000_from_50000(self):
        hm = HashMap()
        n = 50_000
        for i in range(n):
            hm[i] = i
        for i in range(10_000):
            del hm[i]
        assert len(hm) == 40_000
        for i in range(10_000, n):
            assert hm[i] == i
        for i in range(10_000):
            assert i not in hm

    def test_100000_under_3_seconds(self):
        hm = HashMap()
        n = 100_000
        start = time.time()
        for i in range(n):
            hm[i] = i
        for i in range(n):
            _ = hm[i]
        elapsed = time.time() - start
        assert elapsed < 3.0, f"Took {elapsed:.2f}s, expected < 3s"

    def test_auto_resize_multiple_times(self):
        hm = HashMap(capacity=2)
        n = 10_000
        for i in range(n):
            hm[i] = i
        assert len(hm) == n
        # capacity must have grown significantly from 2
        assert hm.capacity() >= n  # at least as many buckets as elements (due to load factor < 1)

    def test_mixed_operations(self):
        hm = HashMap()
        for i in range(1000):
            hm[i] = i
        for i in range(0, 1000, 2):
            del hm[i]
        assert len(hm) == 500
        for i in range(1, 1000, 2):
            assert hm[i] == i
        for i in range(0, 1000, 2):
            assert i not in hm


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_word_frequency_counter(self):
        text = "the cat sat on the mat the cat"
        hm = HashMap()
        for word in text.split():
            hm[word] = hm.get(word, 0) + 1
        assert hm["the"] == 3
        assert hm["cat"] == 2
        assert hm["sat"] == 1
        assert hm["on"] == 1
        assert hm["mat"] == 1
        assert len(hm) == 5

    def test_two_sum(self):
        """Use a HashMap to solve the classic two-sum problem."""
        nums = [2, 7, 11, 15]
        target = 9
        hm = HashMap()
        result = None
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hm:
                result = (hm[complement], i)
                break
            hm[num] = i
        assert result == (0, 1)

    def test_two_sum_no_solution(self):
        nums = [1, 2, 3]
        target = 100
        hm = HashMap()
        result = None
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hm:
                result = (hm[complement], i)
                break
            hm[num] = i
        assert result is None

    def test_group_anagrams(self):
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        hm = HashMap()
        for word in words:
            key = tuple(sorted(word))
            existing = hm.get(key, [])
            existing.append(word)
            hm[key] = existing
        groups = hm.values()
        # Convert to sets for order-independent comparison
        group_sets = [frozenset(g) for g in groups]
        assert frozenset({"eat", "tea", "ate"}) in group_sets
        assert frozenset({"tan", "nat"}) in group_sets
        assert frozenset({"bat"}) in group_sets
        assert len(groups) == 3

    def test_simple_cache(self):
        """Build a bounded cache: evict oldest entry when capacity exceeded."""
        cache = HashMap()
        insertion_order = []
        max_size = 5

        def cache_put(key, value):
            if key not in cache and len(cache) >= max_size:
                oldest = insertion_order.pop(0)
                del cache[oldest]
            if key in cache:
                insertion_order.remove(key)
            cache[key] = value
            insertion_order.append(key)

        for i in range(8):
            cache_put(f"key{i}", i)

        assert len(cache) == max_size
        # First 3 should have been evicted
        assert "key0" not in cache
        assert "key1" not in cache
        assert "key2" not in cache
        # Last 5 should be present
        for i in range(3, 8):
            assert cache[f"key{i}"] == i

    def test_character_counting(self):
        """Count character frequencies in a string."""
        s = "abracadabra"
        hm = HashMap()
        for ch in s:
            hm[ch] = hm.get(ch, 0) + 1
        assert hm["a"] == 5
        assert hm["b"] == 2
        assert hm["r"] == 2
        assert hm["c"] == 1
        assert hm["d"] == 1

    def test_invert_map(self):
        """Build an inverted index (value -> list of keys)."""
        hm = HashMap()
        hm["alice"] = "A"
        hm["bob"] = "B"
        hm["charlie"] = "A"
        hm["dave"] = "B"
        hm["eve"] = "C"

        inverted = HashMap()
        for k, v in hm.items():
            existing = inverted.get(v, [])
            existing.append(k)
            inverted[v] = existing

        assert set(inverted["A"]) == {"alice", "charlie"}
        assert set(inverted["B"]) == {"bob", "dave"}
        assert inverted["C"] == ["eve"]

    def test_nested_hashmaps(self):
        """HashMap values can be other HashMaps (though not keys)."""
        outer = HashMap()
        inner = HashMap()
        inner["x"] = 1
        outer["nested"] = inner
        assert outer["nested"]["x"] == 1

    def test_update_chain(self):
        """Multiple updates accumulate correctly."""
        hm = HashMap()
        hm.update({"a": 1, "b": 2})
        hm.update({"b": 3, "c": 4})
        hm.update({"d": 5})
        assert len(hm) == 4
        assert hm["a"] == 1
        assert hm["b"] == 3
        assert hm["c"] == 4
        assert hm["d"] == 5

    def test_copy_then_diverge(self):
        """Original and copy diverge after copy."""
        hm = HashMap()
        hm["a"] = 1
        hm["b"] = 2
        cp = hm.copy()
        hm["c"] = 3
        del cp["a"]
        assert len(hm) == 3
        assert len(cp) == 1
        assert "c" not in cp
        assert "a" in hm
