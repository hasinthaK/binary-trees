# Advanced Algorithms - Tree Data Structures Implementation

This repository contains the implementation of three different tree data structures as part of the Advanced Algorithms module for MSc. The implemented trees are:

1. Binary Search Tree (BST)
2. Red-Black Tree (RBT)
3. Splay Tree (ST)

## Project Structure

The project is organized as follows:

- `src/`: Contains the source code for all implementations
  - `BST.py`: Binary Search Tree implementation
  - `RBT.py`: Red-Black Tree implementation
  - `ST.py`: Splay Tree implementation
  - `file_utils.py`: Utility functions for file operations

## Implementations

### Binary Search Tree (BST)

The BST implementation can be found in:

```15:149:src/BST.py```

This implementation includes methods for insertion, deletion, and searching.

### Red-Black Tree (RBT)

The RBT implementation can be found in:

```18:301:src/RBT.py```

This implementation includes methods for insertion, deletion, searching, and the necessary rotations and fixups to maintain the Red-Black Tree properties.

### Splay Tree (ST)

The Splay Tree implementation can be found in:

```16:185:src/ST.py```

This implementation includes methods for insertion, deletion, searching, and the splaying operation.

## Performance Testing

Each tree implementation includes methods to test the performance of insertion, searching, and deletion operations:

Similar methods exist for RBT and ST in their respective files.

## File Utilities

The `file_utils.py` contains helper functions to read data from files:

## Usage

To run the performance tests for each tree, uncomment the relevant print statements in the `__main__` section of each file:

```216:222:src/BST.py
if __name__ == '__main__':
    # initialize the tree
    bst = BinarySearchTree()
    
    print(bst_insert(bst))
    # print(bst_search(bst))
    # print(bst_delete(bst))
```

Similar sections exist for RBT and ST.

## Note

This project is set up with a `.gitignore` file to exclude common Python-related files and directories from version control.

## Submission

This repository is submitted as part of the coursework for the Advanced Algorithms module in the MSc program.
