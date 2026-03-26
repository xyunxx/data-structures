"""
Test suite for BinarySearchTree.

Run with:  pytest test_binary_search_tree.py -v
"""

import random

import pytest

from binary_search_tree import BinarySearchTree


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_balanced_7():
    r"""Build a balanced BST with 7 nodes.

            4
           / \
          2   6
         / \ / \
        1  3 5  7
    """
    bst = BinarySearchTree()
    for v in [4, 2, 6, 1, 3, 5, 7]:
        bst.insert(v)
    return bst


def _build_left_skewed(n=5):
    """Build a left-skewed BST by inserting values in descending order."""
    return BinarySearchTree(range(n, 0, -1))


def _build_right_skewed(n=5):
    """Build a right-skewed BST by inserting values in ascending order."""
    return BinarySearchTree(range(1, n + 1))


# ===========================================================================
# TestConstruction
# ===========================================================================

class TestConstruction:
    def test_empty(self):
        bst = BinarySearchTree()
        assert len(bst) == 0

    def test_from_list(self):
        bst = BinarySearchTree([5, 3, 7, 1, 4])
        assert len(bst) == 5
        assert bst.inorder() == [1, 3, 4, 5, 7]

    def test_from_sorted_list_degenerate(self):
        bst = BinarySearchTree([1, 2, 3, 4, 5])
        assert len(bst) == 5
        assert bst.inorder() == [1, 2, 3, 4, 5]
        # Should be a right-skewed tree: height == n - 1
        assert bst.height() == 4

    def test_from_single_element(self):
        bst = BinarySearchTree([42])
        assert len(bst) == 1
        assert bst.inorder() == [42]

    def test_from_iterable_with_duplicates(self):
        bst = BinarySearchTree([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        assert bst.inorder() == [1, 2, 3, 4, 5, 6, 9]
        assert len(bst) == 7

    def test_from_generator(self):
        bst = BinarySearchTree(x * x for x in range(1, 6))
        assert bst.inorder() == [1, 4, 9, 16, 25]

    def test_from_tuple(self):
        bst = BinarySearchTree((10, 20, 30))
        assert len(bst) == 3

    def test_from_set(self):
        bst = BinarySearchTree({5, 3, 8})
        assert len(bst) == 3

    def test_from_empty_iterable(self):
        bst = BinarySearchTree([])
        assert len(bst) == 0
        assert bst.is_empty()


# ===========================================================================
# TestLen
# ===========================================================================

class TestLen:
    def test_empty(self):
        assert len(BinarySearchTree()) == 0

    def test_one(self):
        assert len(BinarySearchTree([10])) == 1

    def test_many(self):
        assert len(BinarySearchTree([5, 3, 7, 1, 4, 6, 8])) == 7

    def test_after_inserts(self):
        bst = BinarySearchTree()
        for i in range(1, 11):
            bst.insert(i)
            assert len(bst) == i

    def test_after_removes(self):
        bst = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        bst.remove(3)
        assert len(bst) == 6
        bst.remove(7)
        assert len(bst) == 5

    def test_duplicate_insert_no_change(self):
        bst = BinarySearchTree([5, 3, 7])
        assert len(bst) == 3
        bst.insert(5)
        assert len(bst) == 3

    def test_size_matches_len(self):
        bst = _build_balanced_7()
        assert bst.size() == len(bst) == 7


# ===========================================================================
# TestBool
# ===========================================================================

class TestBool:
    def test_empty_is_falsy(self):
        assert not BinarySearchTree()

    def test_nonempty_is_truthy(self):
        assert BinarySearchTree([1])

    def test_after_clear(self):
        bst = _build_balanced_7()
        bst.clear()
        assert not bst

    def test_after_removing_all(self):
        bst = BinarySearchTree([1])
        bst.remove(1)
        assert not bst


# ===========================================================================
# TestRepr
# ===========================================================================

class TestRepr:
    def test_empty(self):
        assert repr(BinarySearchTree()) == "BinarySearchTree([])"

    def test_single(self):
        assert repr(BinarySearchTree([5])) == "BinarySearchTree([5])"

    def test_multiple_shows_sorted(self):
        bst = BinarySearchTree([5, 3, 7, 1])
        assert repr(bst) == "BinarySearchTree([1, 3, 5, 7])"

    def test_strings(self):
        bst = BinarySearchTree(["c", "a", "b"])
        assert repr(bst) == "BinarySearchTree(['a', 'b', 'c'])"


# ===========================================================================
# TestContains
# ===========================================================================

class TestContains:
    def test_root(self):
        bst = _build_balanced_7()
        assert 4 in bst

    def test_leaf(self):
        bst = _build_balanced_7()
        assert 1 in bst
        assert 7 in bst

    def test_internal(self):
        bst = _build_balanced_7()
        assert 2 in bst
        assert 6 in bst

    def test_absent(self):
        bst = _build_balanced_7()
        assert 0 not in bst
        assert 8 not in bst
        assert 100 not in bst

    def test_empty_tree(self):
        assert 1 not in BinarySearchTree()

    def test_after_removal(self):
        bst = _build_balanced_7()
        bst.remove(3)
        assert 3 not in bst


# ===========================================================================
# TestEquality
# ===========================================================================

class TestEquality:
    def test_same_structure(self):
        a = BinarySearchTree([4, 2, 6, 1, 3, 5, 7])
        b = BinarySearchTree([4, 2, 6, 1, 3, 5, 7])
        assert a == b

    def test_same_values_different_structure(self):
        a = BinarySearchTree([4, 2, 6, 1, 3, 5, 7])
        b = BinarySearchTree([1, 2, 3, 4, 5, 6, 7])
        assert a != b

    def test_empty_trees(self):
        assert BinarySearchTree() == BinarySearchTree()

    def test_different_sizes(self):
        a = BinarySearchTree([1, 2, 3])
        b = BinarySearchTree([1, 2])
        assert a != b

    def test_not_equal_to_non_bst(self):
        bst = BinarySearchTree([1, 2, 3])
        assert bst != [1, 2, 3]
        assert bst != "hello"

    def test_single_node(self):
        assert BinarySearchTree([5]) == BinarySearchTree([5])

    def test_single_different(self):
        assert BinarySearchTree([5]) != BinarySearchTree([6])

    def test_equal_after_same_removal(self):
        a = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        b = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        a.remove(3)
        b.remove(3)
        assert a == b

    def test_not_equal_after_different_removal(self):
        a = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        b = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        a.remove(3)
        b.remove(7)
        assert a != b


# ===========================================================================
# TestIsEmpty
# ===========================================================================

class TestIsEmpty:
    def test_empty(self):
        assert BinarySearchTree().is_empty()

    def test_non_empty(self):
        assert not BinarySearchTree([1]).is_empty()

    def test_after_clear(self):
        bst = _build_balanced_7()
        bst.clear()
        assert bst.is_empty()

    def test_after_remove_all(self):
        bst = BinarySearchTree([10])
        bst.remove(10)
        assert bst.is_empty()


# ===========================================================================
# TestInsert
# ===========================================================================

class TestInsert:
    def test_root(self):
        bst = BinarySearchTree()
        bst.insert(10)
        assert len(bst) == 1
        assert 10 in bst

    def test_left_child(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        assert bst.inorder() == [5, 10]

    def test_right_child(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(15)
        assert bst.inorder() == [10, 15]

    def test_deep_insert(self):
        bst = BinarySearchTree([10, 5, 15, 3, 7])
        bst.insert(1)
        assert bst.inorder() == [1, 3, 5, 7, 10, 15]

    def test_duplicate_ignored(self):
        bst = BinarySearchTree([10, 5, 15])
        bst.insert(10)
        assert len(bst) == 3
        assert bst.inorder() == [5, 10, 15]

    def test_duplicate_size_unchanged(self):
        bst = _build_balanced_7()
        original_size = len(bst)
        for v in [4, 2, 6, 1, 3, 5, 7]:
            bst.insert(v)
        assert len(bst) == original_size

    def test_many_inserts_verify_traversals(self):
        values = [50, 25, 75, 12, 37, 62, 87, 6, 18, 31]
        bst = BinarySearchTree(values)
        assert bst.inorder() == sorted(values)
        assert bst.preorder()[0] == 50  # root
        assert len(bst) == len(values)

    def test_insert_negative_values(self):
        bst = BinarySearchTree([-5, -10, -1, 0, 3])
        assert bst.inorder() == [-10, -5, -1, 0, 3]

    def test_insert_preserves_structure(self):
        bst = BinarySearchTree([10, 5, 15])
        bst.insert(3)
        # preorder should show: 10, 5, 3, 15
        assert bst.preorder() == [10, 5, 3, 15]


# ===========================================================================
# TestRemove
# ===========================================================================

class TestRemove:
    def test_leaf(self):
        bst = _build_balanced_7()
        bst.remove(1)
        assert 1 not in bst
        assert len(bst) == 6
        assert bst.inorder() == [2, 3, 4, 5, 6, 7]

    def test_one_child_left(self):
        # Build tree where node 2 has only a left child (1), no right child.
        bst = BinarySearchTree([10, 5, 15, 2, 1])
        bst.remove(2)
        assert 2 not in bst
        assert 1 in bst
        assert bst.is_valid_bst()

    def test_one_child_right(self):
        bst = BinarySearchTree([10, 5, 15, 12, 20, 25])
        bst.remove(20)
        assert 20 not in bst
        assert 25 in bst
        assert bst.is_valid_bst()

    def test_two_children(self):
        bst = _build_balanced_7()
        # Remove 2, which has children 1 and 3.
        # In-order successor of 2 is 3.
        bst.remove(2)
        assert 2 not in bst
        assert bst.inorder() == [1, 3, 4, 5, 6, 7]
        assert bst.is_valid_bst()

    def test_two_children_verify_successor_replacement(self):
        bst = _build_balanced_7()
        # Remove 6, which has children 5 and 7. Successor is 7.
        bst.remove(6)
        assert bst.inorder() == [1, 2, 3, 4, 5, 7]
        assert bst.is_valid_bst()

    def test_remove_root(self):
        bst = _build_balanced_7()
        bst.remove(4)
        assert 4 not in bst
        assert len(bst) == 6
        assert bst.is_valid_bst()
        assert bst.inorder() == [1, 2, 3, 5, 6, 7]

    def test_remove_root_two_children_successor(self):
        # Root 4 has two children. In-order successor is 5.
        bst = _build_balanced_7()
        bst.remove(4)
        # 5 should now be in the root's position.
        assert bst.preorder()[0] == 5

    def test_remove_from_empty_raises(self):
        with pytest.raises(ValueError):
            BinarySearchTree().remove(1)

    def test_remove_nonexistent_raises(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.remove(100)

    def test_remove_all_one_by_one(self):
        bst = _build_balanced_7()
        values = [4, 2, 6, 1, 3, 5, 7]
        for i, v in enumerate(values):
            bst.remove(v)
            assert len(bst) == 7 - i - 1
            assert bst.is_valid_bst()
        assert bst.is_empty()

    def test_bst_property_maintained_after_removals(self):
        bst = BinarySearchTree([50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43])
        for v in [25, 75, 50]:
            bst.remove(v)
            assert bst.is_valid_bst()

    def test_remove_leaf_from_two_node_tree(self):
        bst = BinarySearchTree([10, 5])
        bst.remove(5)
        assert len(bst) == 1
        assert bst.inorder() == [10]

    def test_remove_root_single_node(self):
        bst = BinarySearchTree([10])
        bst.remove(10)
        assert bst.is_empty()

    def test_remove_then_reinsert(self):
        bst = _build_balanced_7()
        bst.remove(3)
        assert 3 not in bst
        bst.insert(3)
        assert 3 in bst
        assert bst.is_valid_bst()


# ===========================================================================
# TestSearch
# ===========================================================================

class TestSearch:
    def test_found_at_root(self):
        bst = _build_balanced_7()
        assert bst.search(4) is True

    def test_found_deep(self):
        bst = BinarySearchTree([50, 25, 75, 12, 37, 6])
        assert bst.search(6) is True

    def test_not_found(self):
        bst = _build_balanced_7()
        assert bst.search(99) is False

    def test_empty_tree(self):
        assert BinarySearchTree().search(1) is False

    def test_search_matches_contains(self):
        bst = _build_balanced_7()
        for v in range(0, 10):
            assert bst.search(v) == (v in bst)


# ===========================================================================
# TestMin
# ===========================================================================

class TestMin:
    def test_single_node(self):
        assert BinarySearchTree([42]).min() == 42

    def test_left_skewed(self):
        bst = _build_left_skewed(5)
        assert bst.min() == 1

    def test_balanced(self):
        assert _build_balanced_7().min() == 1

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            BinarySearchTree().min()

    def test_after_removing_min(self):
        bst = _build_balanced_7()
        bst.remove(1)
        assert bst.min() == 2

    def test_right_skewed(self):
        bst = _build_right_skewed(5)
        assert bst.min() == 1

    def test_negative_values(self):
        bst = BinarySearchTree([5, -3, 10, -7, 0])
        assert bst.min() == -7


# ===========================================================================
# TestMax
# ===========================================================================

class TestMax:
    def test_single_node(self):
        assert BinarySearchTree([42]).max() == 42

    def test_right_skewed(self):
        bst = _build_right_skewed(5)
        assert bst.max() == 5

    def test_balanced(self):
        assert _build_balanced_7().max() == 7

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            BinarySearchTree().max()

    def test_after_removing_max(self):
        bst = _build_balanced_7()
        bst.remove(7)
        assert bst.max() == 6

    def test_left_skewed(self):
        bst = _build_left_skewed(5)
        assert bst.max() == 5

    def test_negative_values(self):
        bst = BinarySearchTree([-10, -20, -5, -1])
        assert bst.max() == -1


# ===========================================================================
# TestHeight
# ===========================================================================

class TestHeight:
    def test_empty(self):
        assert BinarySearchTree().height() == -1

    def test_single_node(self):
        assert BinarySearchTree([10]).height() == 0

    def test_balanced(self):
        assert _build_balanced_7().height() == 2

    def test_degenerate_right(self):
        bst = _build_right_skewed(5)
        assert bst.height() == 4

    def test_degenerate_left(self):
        bst = _build_left_skewed(5)
        assert bst.height() == 4

    def test_after_removal(self):
        bst = _build_balanced_7()
        bst.remove(1)
        bst.remove(3)
        # Tree is now: 4(2, 6(5, 7)) -- 2 has no children
        assert bst.height() == 2

    def test_two_nodes(self):
        bst = BinarySearchTree([10, 5])
        assert bst.height() == 1

    def test_three_nodes_balanced(self):
        bst = BinarySearchTree([10, 5, 15])
        assert bst.height() == 1


# ===========================================================================
# TestInorder
# ===========================================================================

class TestInorder:
    def test_empty(self):
        assert BinarySearchTree().inorder() == []

    def test_single(self):
        assert BinarySearchTree([10]).inorder() == [10]

    def test_balanced(self):
        assert _build_balanced_7().inorder() == [1, 2, 3, 4, 5, 6, 7]

    def test_degenerate(self):
        bst = _build_right_skewed(5)
        assert bst.inorder() == [1, 2, 3, 4, 5]

    def test_sorted_output(self):
        vals = [38, 12, 77, 4, 25, 60, 90]
        bst = BinarySearchTree(vals)
        assert bst.inorder() == sorted(vals)

    def test_negative_values(self):
        bst = BinarySearchTree([0, -5, 5, -10, -1])
        assert bst.inorder() == [-10, -5, -1, 0, 5]


# ===========================================================================
# TestPreorder
# ===========================================================================

class TestPreorder:
    def test_empty(self):
        assert BinarySearchTree().preorder() == []

    def test_single(self):
        assert BinarySearchTree([10]).preorder() == [10]

    def test_known_tree(self):
        bst = _build_balanced_7()
        # Insert order: 4, 2, 6, 1, 3, 5, 7
        # Preorder: root, left subtree, right subtree
        assert bst.preorder() == [4, 2, 1, 3, 6, 5, 7]

    def test_captures_structure(self):
        # Two trees with same values but different insertion order.
        a = BinarySearchTree([4, 2, 6, 1, 3, 5, 7])
        b = BinarySearchTree([1, 2, 3, 4, 5, 6, 7])
        assert a.preorder() != b.preorder()

    def test_right_skewed(self):
        bst = _build_right_skewed(4)
        assert bst.preorder() == [1, 2, 3, 4]

    def test_left_skewed(self):
        bst = _build_left_skewed(4)
        assert bst.preorder() == [4, 3, 2, 1]


# ===========================================================================
# TestPostorder
# ===========================================================================

class TestPostorder:
    def test_empty(self):
        assert BinarySearchTree().postorder() == []

    def test_single(self):
        assert BinarySearchTree([10]).postorder() == [10]

    def test_known_tree(self):
        bst = _build_balanced_7()
        assert bst.postorder() == [1, 3, 2, 5, 7, 6, 4]

    def test_right_skewed(self):
        bst = _build_right_skewed(4)
        assert bst.postorder() == [4, 3, 2, 1]

    def test_left_skewed(self):
        bst = _build_left_skewed(4)
        assert bst.postorder() == [1, 2, 3, 4]


# ===========================================================================
# TestLevelorder
# ===========================================================================

class TestLevelorder:
    def test_empty(self):
        assert BinarySearchTree().levelorder() == []

    def test_single(self):
        assert BinarySearchTree([10]).levelorder() == [10]

    def test_balanced(self):
        bst = _build_balanced_7()
        assert bst.levelorder() == [4, 2, 6, 1, 3, 5, 7]

    def test_degenerate_right(self):
        bst = _build_right_skewed(4)
        assert bst.levelorder() == [1, 2, 3, 4]

    def test_degenerate_left(self):
        bst = _build_left_skewed(4)
        assert bst.levelorder() == [4, 3, 2, 1]

    def test_partial_tree(self):
        bst = BinarySearchTree([10, 5, 15, 3])
        assert bst.levelorder() == [10, 5, 15, 3]


# ===========================================================================
# TestIter
# ===========================================================================

class TestIter:
    def test_empty(self):
        assert list(BinarySearchTree()) == []

    def test_single(self):
        assert list(BinarySearchTree([10])) == [10]

    def test_sorted_order(self):
        bst = _build_balanced_7()
        assert list(bst) == [1, 2, 3, 4, 5, 6, 7]

    def test_for_loop(self):
        bst = BinarySearchTree([5, 3, 7])
        collected = []
        for v in bst:
            collected.append(v)
        assert collected == [3, 5, 7]

    def test_multiple_iterations(self):
        bst = _build_balanced_7()
        assert list(bst) == list(bst)


# ===========================================================================
# TestIsValidBST
# ===========================================================================

class TestIsValidBST:
    def test_valid_balanced(self):
        assert _build_balanced_7().is_valid_bst()

    def test_empty(self):
        assert BinarySearchTree().is_valid_bst()

    def test_single_node(self):
        assert BinarySearchTree([10]).is_valid_bst()

    def test_valid_after_insertions(self):
        bst = BinarySearchTree()
        for v in [50, 25, 75, 12, 37, 62, 87]:
            bst.insert(v)
            assert bst.is_valid_bst()

    def test_valid_after_removals(self):
        bst = _build_balanced_7()
        for v in [2, 6, 4]:
            bst.remove(v)
            assert bst.is_valid_bst()

    def test_valid_degenerate(self):
        assert _build_right_skewed(10).is_valid_bst()
        assert _build_left_skewed(10).is_valid_bst()

    def test_detects_invalid_left_child(self):
        bst = BinarySearchTree([5, 3, 7, 1, 4])
        # Corrupt: make left child bigger than root
        bst._root.left.value = 10
        assert not bst.is_valid_bst()

    def test_detects_invalid_deep_violation(self):
        bst = BinarySearchTree([10, 5, 15, 3, 7])
        # Corrupt: node in left subtree that is < its parent but > root
        bst._root.left.right.value = 12
        assert not bst.is_valid_bst()


# ===========================================================================
# TestSuccessor
# ===========================================================================

class TestSuccessor:
    def test_has_right_subtree(self):
        bst = _build_balanced_7()
        # Successor of 4 is 5 (leftmost of right subtree 6->5)
        assert bst.successor(4) == 5

    def test_no_right_subtree_ancestor(self):
        bst = _build_balanced_7()
        # Successor of 3 is 4 (parent of subtree)
        assert bst.successor(3) == 4

    def test_successor_of_1(self):
        bst = _build_balanced_7()
        assert bst.successor(1) == 2

    def test_successor_of_5(self):
        bst = _build_balanced_7()
        assert bst.successor(5) == 6

    def test_max_has_no_successor(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.successor(7)

    def test_not_found(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.successor(100)

    def test_empty_tree(self):
        with pytest.raises(ValueError):
            BinarySearchTree().successor(1)

    def test_single_node_no_successor(self):
        with pytest.raises(ValueError):
            BinarySearchTree([10]).successor(10)

    def test_all_successors_in_sequence(self):
        bst = _build_balanced_7()
        assert bst.successor(1) == 2
        assert bst.successor(2) == 3
        assert bst.successor(3) == 4
        assert bst.successor(4) == 5
        assert bst.successor(5) == 6
        assert bst.successor(6) == 7


# ===========================================================================
# TestPredecessor
# ===========================================================================

class TestPredecessor:
    def test_has_left_subtree(self):
        bst = _build_balanced_7()
        # Predecessor of 4 is 3 (rightmost of left subtree)
        assert bst.predecessor(4) == 3

    def test_no_left_subtree_ancestor(self):
        bst = _build_balanced_7()
        # Predecessor of 5 is 4 (ancestor)
        assert bst.predecessor(5) == 4

    def test_predecessor_of_7(self):
        bst = _build_balanced_7()
        assert bst.predecessor(7) == 6

    def test_predecessor_of_3(self):
        bst = _build_balanced_7()
        assert bst.predecessor(3) == 2

    def test_min_has_no_predecessor(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.predecessor(1)

    def test_not_found(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.predecessor(100)

    def test_empty_tree(self):
        with pytest.raises(ValueError):
            BinarySearchTree().predecessor(1)

    def test_single_node_no_predecessor(self):
        with pytest.raises(ValueError):
            BinarySearchTree([10]).predecessor(10)

    def test_all_predecessors_in_sequence(self):
        bst = _build_balanced_7()
        assert bst.predecessor(7) == 6
        assert bst.predecessor(6) == 5
        assert bst.predecessor(5) == 4
        assert bst.predecessor(4) == 3
        assert bst.predecessor(3) == 2
        assert bst.predecessor(2) == 1


# ===========================================================================
# TestFloor
# ===========================================================================

class TestFloor:
    def test_exact_match(self):
        bst = BinarySearchTree([10, 20, 30, 40, 50])
        assert bst.floor(30) == 30

    def test_between_values(self):
        bst = BinarySearchTree([10, 20, 30, 40, 50])
        assert bst.floor(25) == 20

    def test_less_than_min_raises(self):
        bst = BinarySearchTree([10, 20, 30])
        with pytest.raises(ValueError):
            bst.floor(5)

    def test_at_min(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.floor(10) == 10

    def test_larger_than_max(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.floor(100) == 30

    def test_empty_tree_raises(self):
        with pytest.raises(ValueError):
            BinarySearchTree().floor(5)

    def test_just_below_value(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.floor(19) == 10

    def test_just_above_value(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.floor(21) == 20

    def test_floor_with_balanced_tree(self):
        bst = _build_balanced_7()
        assert bst.floor(4) == 4
        with pytest.raises(ValueError):
            bst.floor(0)


# ===========================================================================
# TestCeiling
# ===========================================================================

class TestCeiling:
    def test_exact_match(self):
        bst = BinarySearchTree([10, 20, 30, 40, 50])
        assert bst.ceiling(30) == 30

    def test_between_values(self):
        bst = BinarySearchTree([10, 20, 30, 40, 50])
        assert bst.ceiling(25) == 30

    def test_greater_than_max_raises(self):
        bst = BinarySearchTree([10, 20, 30])
        with pytest.raises(ValueError):
            bst.ceiling(35)

    def test_at_max(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.ceiling(30) == 30

    def test_smaller_than_min(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.ceiling(1) == 10

    def test_empty_tree_raises(self):
        with pytest.raises(ValueError):
            BinarySearchTree().ceiling(5)

    def test_just_above_value(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.ceiling(21) == 30

    def test_just_below_value(self):
        bst = BinarySearchTree([10, 20, 30])
        assert bst.ceiling(19) == 20

    def test_ceiling_with_balanced_tree(self):
        bst = _build_balanced_7()
        assert bst.ceiling(4) == 4
        with pytest.raises(ValueError):
            bst.ceiling(8)


# ===========================================================================
# TestRangeQuery
# ===========================================================================

class TestRangeQuery:
    def test_full_range(self):
        bst = _build_balanced_7()
        assert bst.range_query(1, 7) == [1, 2, 3, 4, 5, 6, 7]

    def test_partial_range(self):
        bst = _build_balanced_7()
        assert bst.range_query(3, 5) == [3, 4, 5]

    def test_empty_range(self):
        bst = _build_balanced_7()
        assert bst.range_query(10, 20) == []

    def test_range_below_all(self):
        bst = _build_balanced_7()
        assert bst.range_query(-10, 0) == []

    def test_single_match(self):
        bst = _build_balanced_7()
        assert bst.range_query(4, 4) == [4]

    def test_all_matches(self):
        bst = _build_balanced_7()
        assert bst.range_query(0, 100) == [1, 2, 3, 4, 5, 6, 7]

    def test_empty_tree(self):
        assert BinarySearchTree().range_query(1, 10) == []

    def test_boundaries_inclusive(self):
        bst = BinarySearchTree([10, 20, 30, 40, 50])
        assert bst.range_query(20, 40) == [20, 30, 40]

    def test_no_match_between_values(self):
        bst = BinarySearchTree([10, 30, 50])
        assert bst.range_query(11, 29) == []

    def test_sorted_output(self):
        bst = BinarySearchTree([50, 20, 80, 10, 30, 60, 90])
        result = bst.range_query(15, 65)
        assert result == sorted(result)


# ===========================================================================
# TestKthSmallest
# ===========================================================================

class TestKthSmallest:
    def test_k_equals_1_is_min(self):
        bst = _build_balanced_7()
        assert bst.kth_smallest(1) == 1

    def test_k_equals_size_is_max(self):
        bst = _build_balanced_7()
        assert bst.kth_smallest(7) == 7

    def test_middle(self):
        bst = _build_balanced_7()
        assert bst.kth_smallest(4) == 4

    def test_k_zero_raises(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.kth_smallest(0)

    def test_k_too_large_raises(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.kth_smallest(8)

    def test_empty_tree_raises(self):
        with pytest.raises(ValueError):
            BinarySearchTree().kth_smallest(1)

    def test_single_node(self):
        assert BinarySearchTree([42]).kth_smallest(1) == 42

    def test_all_positions(self):
        bst = _build_balanced_7()
        for k in range(1, 8):
            assert bst.kth_smallest(k) == k

    def test_negative_k_raises(self):
        bst = _build_balanced_7()
        with pytest.raises(ValueError):
            bst.kth_smallest(-1)


# ===========================================================================
# TestToSortedList
# ===========================================================================

class TestToSortedList:
    def test_empty(self):
        assert BinarySearchTree().to_sorted_list() == []

    def test_single(self):
        assert BinarySearchTree([10]).to_sorted_list() == [10]

    def test_multiple(self):
        bst = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        result = bst.to_sorted_list()
        assert result == [1, 3, 4, 5, 6, 7, 8]
        assert result == sorted(result)

    def test_degenerate(self):
        bst = _build_right_skewed(5)
        assert bst.to_sorted_list() == [1, 2, 3, 4, 5]

    def test_matches_inorder(self):
        bst = _build_balanced_7()
        assert bst.to_sorted_list() == bst.inorder()


# ===========================================================================
# TestClear
# ===========================================================================

class TestClear:
    def test_non_empty(self):
        bst = _build_balanced_7()
        bst.clear()
        assert bst.is_empty()
        assert len(bst) == 0
        assert bst.inorder() == []

    def test_already_empty(self):
        bst = BinarySearchTree()
        bst.clear()
        assert bst.is_empty()

    def test_usable_after_clear(self):
        bst = _build_balanced_7()
        bst.clear()
        bst.insert(100)
        bst.insert(50)
        bst.insert(150)
        assert len(bst) == 3
        assert bst.inorder() == [50, 100, 150]
        assert bst.is_valid_bst()

    def test_height_after_clear(self):
        bst = _build_balanced_7()
        bst.clear()
        assert bst.height() == -1


# ===========================================================================
# TestStress
# ===========================================================================

class TestStress:
    def test_large_random_insert_inorder_sorted(self):
        random.seed(42)
        values = random.sample(range(100_000), 10_000)
        bst = BinarySearchTree(values)
        result = bst.inorder()
        assert result == sorted(values)

    def test_large_random_contains(self):
        random.seed(43)
        values = random.sample(range(100_000), 10_000)
        bst = BinarySearchTree(values)
        value_set = set(values)
        # Check 500 that are in the tree.
        for v in values[:500]:
            assert v in bst
        # Check 500 that are NOT in the tree.
        for v in range(100_000, 100_500):
            assert v not in bst

    def test_sequential_insert_degenerate(self):
        bst = BinarySearchTree(range(10_000))
        assert len(bst) == 10_000
        assert bst.min() == 0
        assert bst.max() == 9999
        assert bst.inorder() == list(range(10_000))

    def test_large_remove_maintains_bst(self):
        random.seed(44)
        values = random.sample(range(100_000), 10_000)
        bst = BinarySearchTree(values)
        to_remove = random.sample(values, 1_000)
        for v in to_remove:
            bst.remove(v)
        assert len(bst) == 9_000
        assert bst.is_valid_bst()
        result = bst.inorder()
        assert result == sorted(result)

    def test_large_kth_smallest(self):
        random.seed(45)
        values = random.sample(range(100_000), 5_000)
        bst = BinarySearchTree(values)
        sorted_vals = sorted(values)
        assert bst.kth_smallest(1) == sorted_vals[0]
        assert bst.kth_smallest(5000) == sorted_vals[-1]
        assert bst.kth_smallest(2500) == sorted_vals[2499]

    def test_large_range_query(self):
        random.seed(46)
        values = random.sample(range(100_000), 10_000)
        bst = BinarySearchTree(values)
        result = bst.range_query(25_000, 75_000)
        expected = sorted(v for v in values if 25_000 <= v <= 75_000)
        assert result == expected


# ===========================================================================
# TestIntegration
# ===========================================================================

class TestIntegration:
    def test_exam_scores(self):
        """Use a BST to analyze exam scores."""
        scores = [72, 85, 91, 60, 78, 95, 88, 67, 73, 82, 55, 99, 64, 76, 89]
        bst = BinarySearchTree(scores)

        # Find all scores in the B range (80-89).
        b_range = bst.range_query(80, 89)
        assert b_range == [82, 85, 88, 89]

        # Find the median score (8th out of 15).
        median = bst.kth_smallest(8)
        assert median == 78

        # Find min and max.
        assert bst.min() == 55
        assert bst.max() == 99

    def test_alphabetical_ordering(self):
        """Use a BST for dictionary-style ordering of words."""
        words = ["mango", "apple", "cherry", "banana", "date", "elderberry"]
        bst = BinarySearchTree(words)

        # Iteration should give alphabetical order.
        assert list(bst) == sorted(words)

        # Floor and ceiling for nearest words.
        assert bst.floor("coconut") == "cherry"
        assert bst.ceiling("coconut") == "date"

        # Search.
        assert bst.search("cherry")
        assert not bst.search("fig")

    def test_schedule_slots(self):
        """Use a BST to manage time slots (as integers representing minutes)."""
        # Meetings at these minute marks.
        slots = [540, 600, 660, 720, 810, 900, 960]
        bst = BinarySearchTree(slots)

        # Find the next available slot after 650.
        next_slot = bst.ceiling(650)
        assert next_slot == 660

        # Find predecessor: the meeting just before 810.
        prev_slot = bst.predecessor(810)
        assert prev_slot == 720

        # Find successor: the meeting just after 600.
        next_after_600 = bst.successor(600)
        assert next_after_600 == 660

        # All meetings between 600 and 900 inclusive.
        window = bst.range_query(600, 900)
        assert window == [600, 660, 720, 810, 900]

    def test_build_remove_rebuild(self):
        """Full lifecycle: build, query, remove, rebuild."""
        bst = BinarySearchTree([50, 30, 70, 20, 40, 60, 80])
        assert len(bst) == 7
        assert bst.height() == 2

        # Remove some nodes.
        bst.remove(30)
        bst.remove(70)
        assert len(bst) == 5
        assert bst.is_valid_bst()

        # Insert replacements.
        bst.insert(35)
        bst.insert(65)
        assert len(bst) == 7
        assert bst.is_valid_bst()
        assert 35 in bst
        assert 65 in bst
        assert 30 not in bst

    def test_floor_ceiling_comprehensive(self):
        """Floor and ceiling with various boundary conditions."""
        bst = BinarySearchTree([10, 20, 30, 40, 50])

        # Exact matches.
        for v in [10, 20, 30, 40, 50]:
            assert bst.floor(v) == v
            assert bst.ceiling(v) == v

        # Between values.
        assert bst.floor(15) == 10
        assert bst.ceiling(15) == 20
        assert bst.floor(25) == 20
        assert bst.ceiling(25) == 30
        assert bst.floor(45) == 40
        assert bst.ceiling(45) == 50

        # Edges.
        assert bst.floor(100) == 50
        assert bst.ceiling(1) == 10

        with pytest.raises(ValueError):
            bst.floor(5)
        with pytest.raises(ValueError):
            bst.ceiling(55)

    def test_traversal_consistency(self):
        """All traversals return the same set of values."""
        bst = BinarySearchTree([50, 25, 75, 12, 37, 62, 87])
        vals = sorted([50, 25, 75, 12, 37, 62, 87])
        assert sorted(bst.inorder()) == vals
        assert sorted(bst.preorder()) == vals
        assert sorted(bst.postorder()) == vals
        assert sorted(bst.levelorder()) == vals
        assert sorted(bst) == vals

    def test_successor_predecessor_inverse(self):
        """Successor and predecessor are inverses for interior nodes."""
        bst = _build_balanced_7()
        for v in [2, 3, 4, 5, 6]:
            s = bst.successor(v)
            assert bst.predecessor(s) == v

    def test_string_bst(self):
        """BST works with strings, not just integers."""
        bst = BinarySearchTree(["delta", "alpha", "charlie", "bravo"])
        assert bst.inorder() == ["alpha", "bravo", "charlie", "delta"]
        assert bst.min() == "alpha"
        assert bst.max() == "delta"
        assert bst.search("charlie")
        assert not bst.search("echo")
        assert bst.successor("bravo") == "charlie"
        assert bst.predecessor("charlie") == "bravo"
        assert bst.floor("cat") == "bravo"
        assert bst.ceiling("cat") == "charlie"

    def test_float_bst(self):
        """BST works with floats."""
        bst = BinarySearchTree([3.14, 2.72, 1.41, 1.73, 2.24])
        assert bst.inorder() == [1.41, 1.73, 2.24, 2.72, 3.14]
        assert bst.floor(2.5) == 2.24
        assert bst.ceiling(2.5) == 2.72
