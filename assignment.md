# ABC File Parser and Analysis

This assignment is Category 3 for use of AI:

![](images/Screenshot%20from%202025-11-03%2017-46-03.png)
  
**Weight:** 30%
**Submission:** GitHub repository URL + In-class demo

---

You will build an application in Python that:

1. Reads ABC files from multiple folders (representing different books)
2. Parses and stores tunes into a list of dictionaries
3. Stores the data in an sql database
3. Loads data into pandas for analysis
4. Create a simple user interface so that a user can query the data
5. Maintains proper version control with Git/GitHub

---

## Dataset Structure
```
abc_books/
├── 0/
│   ├── tune001.abc
│   ├── tune002.abc
│   └── tune003.abc
├── 1/
│   ├── tune100.abc
│   ├── tune101.abc
│   └── tune102.abc
├── 2/
│   ├── tune200.abc
│   └── tune201.abc
└── 3/
    └── tune300.abc
```

- Each numbered folder represents a "book" (collection)
- Each folder contains one or more ABC files
- Each ABC file may contain one or more tunes
- Folder numbers start at 0

---

## Part 1: File Loading & Parsing (30%)

- Recursively traverse the `abc_books/` directory
- Identify all `.abc` files
- Determine the book number from the parent folder name

### Parse and Insert Tunes

For each ABC file:
1. Parse and load all tunes in the file (using logic from previous lab) into a list of dictionaries
2. Insert each tune into a database table in SQLITE or MYSQL with the correct book number

---

## Part 2: Data Loading with Pandas (20%)

<<<<<<< HEAD
### Load Data from SQLITE
=======
### Load Data from SQLITE or MYSQL
>>>>>>> 28a6a772cfe54b4dedd22bda42db4392f3b410f1

Create a function that loads the entire tunes table into a pandas DataFrame.

```python

    df = pd.read_sql(query, conn)
```    

### Create Analysis Functions

Write functions to analyze the data. Some ideas to get you started, but include any others you think might be useful. Use your imagination to consider how a user might want to query and analyse this data:

```python
def get_tunes_by_book(df, book_number):
    """Get all tunes from a specific book"""
    pass

def get_tunes_by_type(df, tune_type):
    """Get all tunes of a specific type"""
    pass

def search_tunes(df, search_term):
    """Search tunes by title (case insensitive)"""
    pass

```

---

## Part 3: Interactive Elements (30%)

Create a way for a user to interact with the data and run queries. This can be purely menu based like this:

- https://www.youtube.com/watch?v=p3Vui6q_wPw

Or you can use py5, tkinter or django

## Part 4: Documentation & Github (20%)

Fork [this repo]()

Your README must be in [this format](README.MD):

- Use docstrings for all functions and classes
- Include type hints where appropriate
- Add comments for complex logic
- Make regular commits!!

## Grading Rubric

| Component | Points |
|-----------|--------|
| Loading & parsing | 30% |
| Data Analysys | 20% |
| Interactive Elements | 30% |
| Github, documentation & presentation | 20% |

Overall Grade Descriptors

- 1 Exceeds requirements with exceptional implementation, self-directed learning evident, polished and professional
- 2.1 Meets all requirements with high quality implementation and good attention to detail
- 2.2 Meets all core requirements with competent implementation
- Pass - Meets some of the requirements
- Fail - Fails to meet minimum requirements or non-functional

## Submission Requirements

1. **GitHub Repository URL** via Brightspace
2. In class demo

Optional elements:

- [Parse the tunes and generate search keys](https://arrow.tudublin.ie/sciendoc/71/)
- Add plot visualizations (matplotlib)
- Implement edit/delete tune functionality
- Create playlist/favorites feature
- Export to PDF/MIDI