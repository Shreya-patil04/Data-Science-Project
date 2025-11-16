"""
decorators_examples.py
Comprehensive decorator examples from beginner to advanced.
Covers function decorators, argument-based decorators, class decorators,
nested decorators, real-world use cases, and performance benchmarking.
"""


# -------------------------------------------------------
# 1. BASIC DECORATOR
# -------------------------------------------------------
def simple_decorator(func):
    """Basic decorator that prints before and after function execution."""
    def wrapper():
        print("[simple_decorator] Before function execution")
        result = func()
        print("[simple_decorator] After function execution")
        return result
    return wrapper


@simple_decorator
def greet():
    return "Hello World"


print(greet())


# -------------------------------------------------------
# 2. DECORATOR WITH FUNCTION ARGUMENTS
# -------------------------------------------------------
def log_arguments(func):
    """Decorator to log passed arguments."""
    def wrapper(*args, **kwargs):
        print(f"[log_arguments] Arguments: {args}, Kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper


@log_arguments
def add(x, y):
    return x + y


print(add(5, 10))


# -------------------------------------------------------
# 3. DECORATOR THAT RETURNS MODIFIED OUTPUT
# -------------------------------------------------------
def uppercase_output(func):
    """Converts returned string to uppercase."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper


@uppercase_output
def get_message():
    return "hello from python decorators"


print(get_message())


# -------------------------------------------------------
# 4. DECORATOR WITH PARAMETERS (NESTED DECORATORS)
# -------------------------------------------------------
def repeat(times):
    """Decorator that repeats a function multiple times."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(3)
def welcome(name):
    print(f"Welcome, {name}!")


welcome("Shreya")


# -------------------------------------------------------
# 5. REAL-WORLD USE CASE: PERFORMANCE MEASUREMENT
# -------------------------------------------------------
import time


def measure_time(func):
    """Decorator to measure execution time of functions."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[measure_time] Execution Time: {round(end - start, 5)} seconds")
        return result
    return wrapper


@measure_time
def heavy_task():
    for _ in range(5_000_000):
        pass
    return "Done"


print(heavy_task())


# -------------------------------------------------------
# 6. REAL-WORLD USE CASE: AUTHENTICATION CHECK
# -------------------------------------------------------
USER_ROLE = "admin"


def require_admin(func):
    """Only allow access if user is admin."""
    def wrapper(*args, **kwargs):
        if USER_ROLE != "admin":
            return "Access Denied. Admins only."
        return func(*args, **kwargs)
    return wrapper


@require_admin
def delete_user():
    return "User deleted successfully."


print(delete_user())


# -------------------------------------------------------
# 7. CLASS-BASED DECORATOR
# -------------------------------------------------------
class CounterDecorator:
    """Counts how many times a function is called."""
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[CounterDecorator] Call #{self.count}")
        return self.func(*args, **kwargs)


@CounterDecorator
def say_hi():
    return "Hi!"


print(say_hi())
print(say_hi())
print(say_hi())


# -------------------------------------------------------
# 8. CHAINED DECORATORS
# -------------------------------------------------------
@uppercase_output
@log_arguments
def full_name(first, last):
    return f"{first} {last}"


print(full_name("Shreya", "Patil"))

