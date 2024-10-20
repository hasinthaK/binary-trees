import sys
from datetime import datetime
from file_utils import read_data_files, write_to_file, compute_avg, get_lines_to_write

sys.setrecursionlimit(30000)


class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    # rotate left at node x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
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
        if y.right is not None:
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

    # Splaying operation. It moves x to the root of the tree
    def splay(self, x):
        while x.parent is not None:
            if x.parent.parent is None:
                if x == x.parent.left:
                    # zig rotation
                    self.right_rotate(x.parent)
                else:
                    # zag rotation
                    self.left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # zig-zig rotation
                self.right_rotate(x.parent.parent)
                self.right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # zag-zag rotation
                self.left_rotate(x.parent.parent)
                self.left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # zig-zag rotation
                self.left_rotate(x.parent)
                self.right_rotate(x.parent)
            else:
                # zag-zig rotation
                self.right_rotate(x.parent)
                self.left_rotate(x.parent)

    # joins two trees s and t
    def join(self, s, t):
        if s is None:
            return t

        if t is None:
            return s

        x = self.maximum(s)
        self.splay(x)
        x.right = t
        t.parent = x
        return x

    def search_tree_helper(self, node, key):
        if node is None or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def delete_node_helper(self, node, key):
        x = None
        t = None
        s = None
        while node is not None:
            if node.data == key:
                x = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if x is None:
            return False

        # split operation
        self.splay(x)
        if x.right is not None:
            t = x.right
            t.parent = None
        else:
            t = None

        s = x
        s.right = None
        x = None

        # join operation
        if s.left is not None:
            s.left.parent = None

        self.root = self.join(s.left, t)
        s = None
        return True

    # find the node with the minimum key
    def minimum(self, node):
        while node.left is not None:
            node = node.left
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right is not None:
            node = node.right
        return node

    # insert the key to the tree in its appropriate position
    def insert(self, key):
        node = Node(key)
        y = None
        x = self.root

        while x is not None:
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
        # splay the node
        self.splay(node)

    # search the tree for the key k
    # and return the corresponding node
    def search(self, k):
        x = self.search_tree_helper(self.root, k)
        if x is not None:
            self.splay(x)

    # delete the node from the tree
    def delete(self, data):
        self.delete_node_helper(self.root, data)
        
    def tree_height(self):
        return self._height_helper(self.root)

    def _height_helper(self, node):
        start = datetime.now()
        if node is None:
            end = datetime.now()
            return (0, end - start)
        
        left_height = self._height_helper(node.left)[0]
        right_height = self._height_helper(node.right)[0]
        
        height = max(left_height, right_height) + 1
        end = datetime.now()
        return (height, end - start)

def st_insert(st: SplayTree):
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
            st.insert(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(st.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)
        
def st_search(st: SplayTree):
    # initialize the empty tree first
    st_insert(st)
    
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
            st.search(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(st.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)

def st_delete(st: SplayTree):
    # initialize the empty tree first
    st_insert(st)
    
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
            st.delete(value)
            
        end = datetime.now()
        # add execution time for each file
        exec_times.append(end - start)
        
        # add tree_height exec time for each file
        tree_height_exec_times.append(st.tree_height()[1])
        
    # return only exec_times for code runner
    # return exec_times
    return (exec_times, tree_height_exec_times)
    
def avg_exec_time_insert(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging ST insert..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        st = SplayTree()
        exec_times = st_insert(st)
        
        # write each execution time one by one
        lines_to_write = get_lines_to_write(i, exec_times, 'st')
        
    for line in lines_to_write:
        write_to_file(line, 'st', 'insert')
    
    compute_avg('st', 'insert')
    
def avg_exec_time_search(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging ST search..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        st = SplayTree()
        # ignore insertion for this
        st_insert(st)
        exec_times = st_search(st)
        
        # write each execution time one by one
        lines_to_write = get_lines_to_write(i, exec_times, 'st')
        
    for line in lines_to_write:
        write_to_file(line, 'st', 'search')
    
    compute_avg('st', 'search')
    
def avg_exec_time_delete(iterations: int = 3):
    '''
    Execute the tree operation for the specified no of iterations
    & write the execution times in csv. Finally calculate average
    execution time & write back.
    '''
    print('Averaging ST delete..')
    lines_to_write = []
    for i in range(iterations):
        # re-initialize tree each time
        st = SplayTree()
        # ignore insertion for this
        st_insert(st)
        exec_times = st_delete(st)
        
        # write each execution time one by one
        lines_to_write = get_lines_to_write(i, exec_times, 'st')
        
    for line in lines_to_write:
        write_to_file(line, 'st', 'delete')
    
    compute_avg('st', 'delete')

if __name__ == '__main__':
    # initialize the tree
    # st = SplayTree()
    
    # print(st_insert(st))
    # print(st.tree_height())
    # print(st_search(st))
    # print(st_delete(st))
    
    avg_exec_time_insert()
    avg_exec_time_search()
    avg_exec_time_delete()
    # print('Uncomment above as necessary')