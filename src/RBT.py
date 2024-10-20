import sys
from datetime import datetime
from file_utils import read_data_files, write_to_file, compute_avg, get_lines_to_write

sys.setrecursionlimit(30000)


# Data structure that represents a node in the tree
class Node:
    def __init__(self, data):
        self.data = data  # holds the key
        self.parent = None  # pointer to the parent
        self.left = None  # pointer to left child
        self.right = None  # pointer to right child
        self.color = 1  # 1 -> Red, 0 -> Black


# class RedBlackTree implements the operations in Red Black Tree
class RedBlackTree:
    def __init__(self):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    # find the node with the minimum key
    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right != self.NULL:
            node = node.right
        return node

    # rotate left at node x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # fix the rb tree modified by the delete operation
    def fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        # case 3.3
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        # case 3.3
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                        # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def delete_node_helper(self, node, key):
        # find the node containing key
        z = self.NULL
        while node != self.NULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.NULL:
            return False

        y = z
        y_original_color = y.color
        if z.left == self.NULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.NULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.fix_delete(x)

        return True

    # fix the red-black tree
    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == 1:
                    # case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # case 3.2.2
                        k = k.parent
                        self.right_rotate(k)
                    # case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color == 1:
                    # mirror case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # mirror case 3.2.2
                        k = k.parent
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def pre_order_helper(self, node):
        if node != self.NULL:
            print(node.data + " ", end='')
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    def in_order_helper(self, node):
        if node != self.NULL:
            self.in_order_helper(node.left)
            print(node.data + " ", end='')
            self.in_order_helper(node.right)

    def post_order_helper(self, node):
        if node != self.NULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            print(node.data + " ", end='')

    def search_tree_helper(self, node, key):
        if node == self.NULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # insert the key to the tree in its appropriate position
    # and fix the tree
    def insert(self, key):
        # Ordinary Binary Search Insertion
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1  # new node must be red

        y = None
        x = self.root

        while x != self.NULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        # if new node is a root node, simply return
        if node.parent is None:
            node.color = 0
            return

        # if the grandparent is None, simply return
        if node.parent.parent is None:
            return

        # Fix the tree
        self.fix_insert(node)

    # search the tree for the key k
    # and return the corresponding node
    def search(self, k):
        return self.search_tree_helper(self.root, k)

    # delete the node from the tree
    def delete(self, data):
        return self.delete_node_helper(self.root, data)

    def tree_height(self):
        return self._height_helper(self.root)

    def _height_helper(self, node):
        start = datetime.now()
        if node == self.NULL:
            end = datetime.now()
            return (0, end - start)
        
        left_height = self._height_helper(node.left)[0]
        right_height = self._height_helper(node.right)[0]
        
        height = max(left_height, right_height) + 1
        end = datetime.now()
        return (height, end - start)


def rbt_insert(rbt: RedBlackTree):
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
            rbt.insert(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(rbt.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)
        
def rbt_search(rbt: RedBlackTree):
    # initialize the empty tree first
    rbt_insert(rbt)
    
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
            rbt.search(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(rbt.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)

def rbt_delete(rbt: RedBlackTree):
    # initialize the empty tree first
    rbt_insert(rbt)
    
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
            rbt.delete(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(rbt.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)
    
def avg_exec_time_insert(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging RBT insert..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        rbt = RedBlackTree()
        exec_times = rbt_insert(rbt)
        
        # write each execution time one by one
        lines_to_write = get_lines_to_write(i, exec_times, 'rbt')
        
    for line in lines_to_write:
        write_to_file(line, 'rbt', 'insert')
    
    compute_avg('rbt', 'insert')
    
def avg_exec_time_search(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging RBT search..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        rbt = RedBlackTree()
        # ignore insertion for this
        rbt_insert(rbt)
        exec_times = rbt_search(rbt)
        
        # write each execution time one by one
        lines_to_write = get_lines_to_write(i, exec_times, 'rbt')
        
    for line in lines_to_write:
        write_to_file(line, 'rbt', 'search')
    
    compute_avg('rbt', 'search')
    
def avg_exec_time_delete(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging RBT delete..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        rbt = RedBlackTree()
        # ignore insertion for this
        rbt_insert(rbt)
        exec_times = rbt_delete(rbt)
        
        # write each execution time one by one
        lines_to_write = get_lines_to_write(i, exec_times, 'rbt')
        
    for line in lines_to_write:
        write_to_file(line, 'rbt', 'delete')
    
    compute_avg('rbt', 'delete')
    
if __name__ == '__main__':
    # initialize the tree
    # rbt = RedBlackTree()
    
    # print(rbt_insert(rbt))
    # print(rbt.tree_height())
    # print(rbt_search(rbt))
    # print(rbt_delete(rbt))
    
    avg_exec_time_insert()
    avg_exec_time_search()
    avg_exec_time_delete()
    # print('Uncomment above as necessary')