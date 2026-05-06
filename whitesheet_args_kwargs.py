def print_section(title):
    print(f"\n--- {title} ---")


# *args collects extra positional arguments into a tuple.
def add_numbers(*args):
    print("args:", args)
    print("type(args):", type(args).__name__)
    print("sum:", sum(args))


# **kwargs collects extra keyword arguments into a dict.
def show_profile(**kwargs):
    print("kwargs:", kwargs)
    print("type(kwargs):", type(kwargs).__name__)
    for key, value in kwargs.items():
        print(f"{key} = {value}")


# You can use both in one function.
def describe_order(product, *extras, **details):
    print("product:", product)
    print("extras (*args):", extras)
    print("details (**kwargs):", details)


print_section("*args Example")
add_numbers(10, 20, 30, 40)

print_section("**kwargs Example")
show_profile(name="Khaled", language="Python", level="good")

print_section("Difference")
print("*args collects positional arguments into a tuple.")
print("**kwargs collects keyword arguments into a dict.")

print_section("Using Both Together")
describe_order(
    "Laptop",
    "mouse",
    "keyboard",
    color="silver",
    storage="1TB",
    warranty=True,
)

print_section("Argument Unpacking")
numbers = [1, 2, 3]
profile = {"name": "Sara", "city": "Tunis"}

add_numbers(*numbers)
show_profile(**profile)
