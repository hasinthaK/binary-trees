import sys
from datetime import datetime
from file_utils import read_data_files, construct_line_to_write, write_to_file, compute_avg

sys.setrecursionlimit(30000)


class Node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None


# Binary Search Tree
class BinarySearchTree:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

    def traverse_in_order(self, lst):
        if self.left:
            self.left.traverse_in_order(lst)
        lst.append(self.val)
        if self.right:
            self.right.traverse_in_order(lst)
        return lst

    def traverse_pre_order(self, lst):
        lst.append(self.val)
        if self.left:
            self.left.traverse_pre_order(lst)
        if self.right:
            self.right.traverse_pre_order(lst)
        return lst

    def traverse_post_order(self, lst):
        if self.left:
            self.left.traverse_post_order(lst)
        if self.right:
            self.right.traverse_post_order(lst)
        lst.append(self.val)
        return lst

    def find_node_and_parent(self, val, parent=None):
        # returning the node and its parent so we can delete the node and reconstruct the tree from its parent
        if val == self.val:
            return self, parent
        if val < self.val:
            if self.left:
                return self.left.find_node_and_parent(val, self)
            else:
                return False
        else:
            if self.right:
                return self.right.find_node_and_parent(val, self)
            else:
                return False

    def insert(self, val):
        # check if there is no root
        if self.val is None:
            self.val = val
        # check where to insert
        else:
            # check for duplicate then stop and return
            if val == self.val:
                return 'No duplicates allowed in BST'
            # check if value to be inserted < currentNode's value
            if val < self.val:
                # check if there is a left node to currentNode if true then recurse
                if self.left:
                    self.left.insert(val)
                # insert where left of currentNode when currentNode.left=None
                else:
                    self.left = BinarySearchTree(val)

            # same steps as above here the condition we check is value to be inserted > currentNode's value
            else:
                if self.right:
                    self.right.insert(val)
                else:
                    self.right = BinarySearchTree(val)

    def search(self, val):
        if val == self.val:
            return True

        if val < self.val:
            if self.left is None:
                return False
            return self.left.search(val)

        if self.right is None:
            return False
        return self.right.search(val)

    # deleting a node means we have to rearrange some part of the tree
    def delete(self, val):
        # check if the value we want to delete is in the tree
        if not self.find_node_and_parent(val):
            return False
        # we get the node we want to delete and its parent-node from find_node_and_parent method
        deleting_node, parent_node = self.find_node_and_parent(val)
        # check how many children nodes does the node we are going to delete have by traverse_pre_order from the deleting_node
        nodes_effected = deleting_node.traverse_pre_order([])
        # if len(nodes_effected)==1 means, the node to be deleted doesn't have any children
        # so we can just check from its parent node the position(left or right) of node we want to delete
        # and point the position to 'None' i.e node is deleted
        if len(nodes_effected) == 1:
            if parent_node.left is not None and parent_node.left.val == deleting_node.val:
                parent_node.left = None
            else:
                parent_node.right = None
            return True
        # if len(nodes_effected) > 1 which means the node we are going to delete has 'children',
        # so the tree must be rearranged from the deleting_node
        else:
            # if the node we want to delete doesn't have any parent means the node to be deleted is 'root' node
            if parent_node is None:
                nodes_effected.remove(deleting_node.val)
                # make the 'root' node i.e self value,left,right to None,
                # this means we need to implement a new tree again without the delted node
                self.left = None
                self.right = None
                self.val = None
                # construction of new tree
                for node in nodes_effected:
                    self.insert(node)
                return True

            # if the node we want to delete has a parent
            # traverse from parent_node
            nodes_effected = parent_node.traverse_pre_order([])
            # deleting the node
            if parent_node.left == deleting_node:
                parent_node.left = None
            else:
                parent_node.right = None
            # removing the parent_node, deleting_node and inserting the nodes_effected in the tree
            nodes_effected.remove(deleting_node.val)
            nodes_effected.remove(parent_node.val)
            for node in nodes_effected:
                self.insert(node)

        return True
    
    def tree_height(self):
        start = datetime.now()
        if self.val is None:
            end = datetime.now()
            return (0, end - start)
        
        left_height = self.left.tree_height()[0] if self.left else 0
        right_height = self.right.tree_height()[0] if self.right else 0
        
        height = max(left_height, right_height) + 1
        end = datetime.now()
        return (height, end - start)


def bst_insert(bst: BinarySearchTree):
    insert_values = read_data_files('insert')
    
    # execution times for insertion of each file
    exec_times = []
    
    # execution times for tree_height
    # this should not be returned for coder runner activity
    tree_height_exec_times = []
    
    # insert values from each file into the tree
    for values in insert_values.values():
        start = datetime.now()
        
        # insert each value from file to the tree
        for value in values:
            bst.insert(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(bst.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)
        
def bst_search(bst: BinarySearchTree):
    # initialize the empty tree first
    bst_insert(bst)
    
    search_values = read_data_files('search')
    
    # execution times for search of each file
    exec_times = []
    
    # execution times for tree_height
    # this should not be returned for coder runner activity
    tree_height_exec_times = []
    
    # search values of each file from the tree
    for values in search_values.values():
        start = datetime.now()
        
        # search each value of file from the tree
        for value in values:
            bst.search(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(bst.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)

def bst_delete(bst: BinarySearchTree):
    # initialize the empty tree first
    bst_insert(bst)
    
    delete_values = read_data_files('delete')
    
    # execution times for deletion of each file
    exec_times = []
    
    # execution times for tree_height
    # this should not be returned for coder runner activity
    tree_height_exec_times = []
    
    # delete values of each file from the tree
    for values in delete_values.values():
        start = datetime.now()
        
        # delete each value of file from the tree
        for value in values:
            bst.delete(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(bst.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)
    
def avg_exec_time_insert(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging BST insert..')
    lines_to_write = []
    
    for i in range(iterations):
        # re-initialize tree each time
        bst = BinarySearchTree()
        ([one_1, one_2, one_3, two_1, two_2, two_3], [h_one_1, h_one_2, h_one_3, h_two_1, h_two_2, h_two_3]) = bst_insert(bst)
        
        # write each execution time one by one
        lines_to_write.append(construct_line_to_write(i, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 2, one_2.total_seconds(), h_one_2.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 3, one_3.total_seconds(), h_one_3.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 1, two_1.total_seconds(), h_two_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 2, two_2.total_seconds(), h_two_2.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 1, two_3.total_seconds(), h_two_3.total_seconds(), 'bst'))
        
    for line in lines_to_write:
        write_to_file(line, 'bst', 'insert')
    
    compute_avg('bst', 'insert')
    
def avg_exec_time_search(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging BST search..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        bst = BinarySearchTree()
        # ignore insertion for this
        bst_insert(bst)
        ([one_1, one_2, one_3, two_1, two_2, two_3], [h_one_1, h_one_2, h_one_3, h_two_1, h_two_2, h_two_3]) = bst_search(bst)
        
        # write each execution time one by one
        lines_to_write.append(construct_line_to_write(i, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 2, one_2.total_seconds(), h_one_2.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 3, one_3.total_seconds(), h_one_3.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 1, two_1.total_seconds(), h_two_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 2, two_2.total_seconds(), h_two_2.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 1, two_3.total_seconds(), h_two_3.total_seconds(), 'bst'))
        
    for line in lines_to_write:
        write_to_file(line, 'bst', 'search')
    
    compute_avg('bst', 'search')
    
def avg_exec_time_delete(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging BST delete..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        bst = BinarySearchTree()
        # ignore insertion for this
        bst_insert(bst)
        ([one_1, one_2, one_3, two_1, two_2, two_3], [h_one_1, h_one_2, h_one_3, h_two_1, h_two_2, h_two_3]) = bst_delete(bst)
        
        # write each execution time one by one
        lines_to_write.append(construct_line_to_write(i, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 2, one_2.total_seconds(), h_one_2.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 1, 3, one_3.total_seconds(), h_one_3.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 1, two_1.total_seconds(), h_two_1.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 2, two_2.total_seconds(), h_two_2.total_seconds(), 'bst'))
        lines_to_write.append(construct_line_to_write(i, 2, 1, two_3.total_seconds(), h_two_3.total_seconds(), 'bst'))
        
    for line in lines_to_write:
        write_to_file(line, 'bst', 'delete')
    
    compute_avg('bst', 'delete')
    
if __name__ == '__main__':
    # initialize the tree
    # bst = BinarySearchTree()
    
    # print(bst_insert(bst))
    # print(bst.tree_height())
    # print(bst_search(bst))
    # print(bst_delete(bst))
    
    # avg_exec_time_insert()
    # avg_exec_time_search()
    # avg_exec_time_delete()
    print('Uncomment above as necessary')