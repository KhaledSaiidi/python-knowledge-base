
from dataclasses import dataclass, field

numbers = [1, 2 , 9]
value = numbers.__iter__()

item1 = value.__next__()
item2 = next(value)

print(item1, item2)

# Iterators let you produce values lazily (one at a time) instead of loading everything in memory.
# They maintain internal state, enabling efficient traversal of large or infinite sequences.

@dataclass
class Even:
    max: int
    n: int = field(init=False, default=2)
    def __iter__(self): 
        return self
    def __next__(self):
        if self.n <= self.max:
            result = self.n
            self.n += 2
            return result
        else:
            raise StopIteration

numbers = Even(10)
print(next(numbers), next(numbers), next(numbers))


def even_generator(max: int):
    n = 2

    while n <= max:
        yield n
        n += 2


numbers = even_generator(4)
print(next(numbers), next(numbers))