# return → ends the function completely
# yield → pause → send value → keep state → resume later

def generate_fibonaci():
    n1 = 0
    n2 = 1
    while True:
        yield n1
        n1, n2 = n2, n1 + n2
seq = generate_fibonaci()
print("--- generate_fibonaci ---")
print(next(seq))
print(next(seq))
print(next(seq))

def generate_fibonacci_limited(limit):
    n1 = 0
    n2 = 1
    for _ in range(limit):
        yield n1
        n1, n2 = n2, n1 + n2 

seq_limited = generate_fibonacci_limited(10)
print("--- generate_fibonaci limited ---")
print(next(seq_limited))
print(next(seq_limited))
print(next(seq_limited))