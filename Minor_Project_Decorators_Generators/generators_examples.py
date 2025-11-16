"""
generators_examples.py
Comprehensive generator examples from beginner to advanced.
Includes basic generators, generator expressions, pipelines,
infinite generators, real-world use cases, and memory efficiency demos.
"""


# -------------------------------------------------------
# 1. BASIC GENERATOR
# -------------------------------------------------------
def simple_generator():
    """Yields numbers 1, 2, 3"""
    yield 1
    yield 2
    yield 3


for value in simple_generator():
    print(value)


# -------------------------------------------------------
# 2. GENERATOR USING LOOP (MORE PRACTICAL)
# -------------------------------------------------------
def count_upto(n):
    """Yield numbers from 1 to n."""
    for i in range(1, n + 1):
        yield i


print(list(count_upto(5)))


# -------------------------------------------------------
# 3. MEMORY-EFFICIENT LARGE RANGE
# -------------------------------------------------------
def large_range(n):
    """Yield values up to n without storing all in memory."""
    for i in range(n):
        yield i


# demonstrate memory efficiency
import sys
list_memory = sys.getsizeof(list(range(1_000_000)))
gen_memory = sys.getsizeof(large_range(1_000_000))

print(f"List memory: {list_memory} bytes")
print(f"Generator memory: {gen_memory} bytes")


# -------------------------------------------------------
# 4. GENERATOR EXPRESSIONS
# -------------------------------------------------------
squares = (x * x for x in range(10))
print("Squares:", list(squares))


# -------------------------------------------------------
# 5. INFINITE GENERATOR (CAUTION)
# -------------------------------------------------------
def infinite_counter():
    """Infinite counter generator."""
    n = 1
    while True:
        yield n
        n += 1


# Only take first 5 values
counter = infinite_counter()
for _ in range(5):
    print(next(counter))


# -------------------------------------------------------
# 6. PIPELINE GENERATORS (DATA STREAMING)
# -------------------------------------------------------
def read_lines(lines):
    """Simulate line streaming from a file."""
    for line in lines:
        yield line


def filter_errors(lines):
    """Filter lines containing the word ERROR."""
    for line in lines:
        if "ERROR" in line:
            yield line


logs = [
    "INFO: System started",
    "ERROR: Disk failure",
    "WARNING: Low battery",
    "ERROR: Connection lost"
]

pipeline = filter_errors(read_lines(logs))
print(list(pipeline))


# -------------------------------------------------------
# 7. SENDING VALUES INTO GENERATORS
# -------------------------------------------------------
def bidirectional():
    """Receive and yield values using send()."""
    value = yield "Ready"
    while True:
        value = yield f"Received: {value}"


gen = bidirectional()
print(next(gen))          
print(gen.send("Hello"))  
print(gen.send("Data"))   


# -------------------------------------------------------
# 8. REAL-WORLD USE CASE: LAZY FILE READER
# -------------------------------------------------------
def lazy_file_reader(file_path):
    """Read a large file line-by-line."""
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()


# Example (commented for safety):
# for line in lazy_file_reader("large_data.txt"):
#     print(line)


# -------------------------------------------------------
# 9. CHAINING GENERATORS FOR TRANSFORMATIONS
# -------------------------------------------------------
def tokenize(lines):
    for line in lines:
        for word in line.split():
            yield word


text = ["Python generators are powerful", "They save memory"]

words = tokenize(read_lines(text))
print(list(words))

