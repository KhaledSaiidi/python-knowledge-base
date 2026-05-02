import logging

# 1 -- Pre Requisites: Functions, Scope, *args and **kwargs
print("----")
def inc(x) -> int:
    return x+1

# func as arg for another func:
def operate(func, x) -> int:
    result = func(x)
    return result
print(operate(inc,3))

print("\n----")
# func inside of another func: closure 
def print_msg(message):
    greeting = "Hello"
    def printer():
        print(greeting, message)
    return printer
func = print_msg("Man")
func()

print("\n----")

# 2 -- Decorators:
def display_info(func):
    def inner():
        print("Executing", func.__name__, "function")
        func()
        print("Finished execution")
    return inner

@display_info
def printer():
    print("Hello World")
\
printer()
print("\n----")

# 3 -- Decorators with params:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def smart_divide(func):
    def inner(a, b):
        print("Dividing", a,"by", b)
        if b == 0:
            logging.error("cannot divide by o")
            return
        return func(a,b)
    return inner

@smart_divide # -> its like smart_divide(divide(a, b))
def divide(a, b):
    return a / b

value1 = divide(15, 3)
print(value1)

value2 = divide(5, 0)
print(value2)