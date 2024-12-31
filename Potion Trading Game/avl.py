""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.
            complexity: O(logn) where n is the number of nodes in the tree
        """
        #If root node is empty, set the root node with the input key and item
        if current is None:
            current = AVLTreeNode(key,item)
            self.length += 1
        #If the key is less than the key of the current, it will go the left of the current and use recursion for insertion
        elif key < current.key:
            #Set the current node to be the left of the previous, use recursion to repeat the process
            current.left=self.insert_aux(current.left,key,item)
            #Recalculate the height of the avl after insertion
            current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        #If the key is larger than what is in the current node, then it will go to the right of the avl tree
        elif key > current.key:
            #Set the current node to be the right of the previous, use recursion to repeat the process
            current.right=self.insert_aux(current.right,key,item)
            #Recalculate the height of the avl, after insertion
            current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        else:
            raise ValueError("Duplicate keys")
        return self.rebalance(current)

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
            returns the new root of the subtree.
            complexity: O(logn) where n is the number of nodes
        """
        # If the current node doesn't exits raise an error
        if current is None:
           raise ValueError("Item is not in tree")
        # If the key provided is less than the current key, traverse down the left side, then recalculate the height.
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
            current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        # If the key provided is greater than the current key, traverse down the right side, then recalculate the height.
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
            current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        else:
            # If it is a leaf node, reduce the length of the tree
            if self.is_leaf(current):
                self.length -= 1
                return None
            # If there is no left child, reduce the length of the tree and the height of the current node
            elif current.left is None:
                self.length -= 1
                current.height -= 1
                return current.right
            # If there is no right child, reduce the length of the tree and the height of the current node
            elif current.right is None:
                self.length -= 1
                current.height -= 1
                return current.left

            # Get the successor of the node and replace it with the current node then delete
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        # Rebalance the tree and return the current value
        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        #set temporary value holders
        child = current.right
        center = child.left
        #swap values
        child.left = current
        current.right = center
        #recalculate heights
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        child.height = max(self.get_height(child.left), self.get_height(child.right)) + 1

        #return child which is the new root
        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """
        #set temporary value holders
        child = current.left
        center = child.right
        #swap values
        child.right = current
        current.left = center
        #recalculate heights
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        child.height = max(self.get_height(child.left), self.get_height(child.right)) + 1

        #return child which is the new root
        return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current


    def kth_largest(self, k: int) -> AVLTreeNode:
        """
        Returns the kth largest element in the tree.
        k=1 would return the largest.

        complexity: O(log(N)) as this is the complexity of the auxiliary method
        """
        # When root is not existent return placeholder value
        if self.root is None:
            return -1

        count = [0]
        self.kth_largest_aux(self.root, k, count)
        return self.result


    def kth_largest_aux(self, root: AVLTreeNode, k: int, count: int):
        """
        Finds the kth largest element in the AVL tree

        complexity: O(log(N)) where N is the number of nodes in the tree

        This fits the complexity as it traverses the tree using inorder meaning the worst case is traversing all the way down
        the right side of the tree which is O(depth) where depth is the log of the number of nodes in tree meaning the complexity is O(log(n))
        """
        # When the next value is none or the count is larger than k, return nothing
        if root is None or count[0] >= k:
            return

        self.kth_largest_aux(root.right, k, count) # Traverse down the right side first (keys to the right are larger)
        count[0] += 1 # Increment the count

        # If the count is equal to k, this is the kth largest node
        if count[0] == k:
            self.result = root # Store it for return in the caller method
            return root # Return this value
        self.kth_largest_aux(root.left, k, count) # Traverse down the left to find the next largest node

