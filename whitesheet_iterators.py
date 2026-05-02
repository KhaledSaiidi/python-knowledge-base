from dataclasses import dataclass

@dataclass
class MyRange:
    value: int
    end: int

    def __iter__(self):
        return self
    def __next__(self):
        if self.value >= self.end:
            raise StopIteration
        current = self.value
        self.value += 1
        return current

nums = MyRange(1, 10)
print("------ Using the Class MyRange ------")
for _ in range(4):
    print(next(nums))

def my_range(start, end): 
    current = start
    while current < end:
        yield current
        current += 1

nums2 = my_range(1, 10)
print("------ Using the Func my_range ------")
for _ in range(4):
    print(next(nums2))