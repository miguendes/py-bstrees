py-bstrees - Pythonic Binary Search Trees for Aliens™
==========================

[![Build Status](https://travis-ci.org/mendesmiguel/py-bstrees.svg?branch=master)](https://travis-ci.org/mendesmiguel/py-bstrees) [![codecov](https://codecov.io/gh/mendesmiguel/py-bstrees/branch/master/graph/badge.svg)](https://codecov.io/gh/mendesmiguel/py-bstrees)
 [![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/download/releases/3.6.0/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)



`py-bstrees` implements different types of binary search trees.

Reference: https://en.wikipedia.org/wiki/Binary_search_tree

In computer science, binary search trees (BST), sometimes called ordered or sorted binary trees, are a particular 
type of container: data structures that store "items" (such as numbers, names etc.) in memory. They allow fast lookup, 
addition and removal of items, and can be used to implement either dynamic sets of items, or lookup tables that allow 
finding an item by its key (e.g., finding the phone number of a person by name)."

Dependencies
------------
To run this project you need the following dependencies:

- Python 3.6+
- Pipenv 2018+

Installation
------------

#### 1. Clone the repo

``` {.sourceCode .bash}
$ git clone git@github.com:mendesmiguel/py-bstrees.git
```

#### 2. Install Dependencies

To install all dependencies, you can use [pipenv](http://pipenv.org/).

Pipenv will spin up a virtualenv and install the dependencies based on a `Pipenv.lock` file inside the root of
the project.

``` {.sourceCode .bash}
$ cd py-bstrees/
$ pipenv install 
```

#### 3. (Optional) Run the tests

``` {.sourceCode .bash}
$ python3 -m unittest
```


How to Contribute
-----------------

1.  Check for open issues or open a fresh issue to start a discussion
    around a feature idea or a bug. 
2.  Fork [the repository](https://github.com/mendesmiguel/py-bstrees) on
    GitHub to start making your changes to the **master** branch (or
    branch off of it).
3.  Write a test which shows that the bug was fixed or that the feature
    works as expected.
4.  Send a pull request and bug the maintainer until it gets merged and
    published. :)
