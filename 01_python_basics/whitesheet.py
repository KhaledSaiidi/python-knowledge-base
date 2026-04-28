class Triangle:
    def __init__(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c
    def calculate_perimeter(self):
        result = self.a + self.b + self.c
        return result

t1 = Triangle(3,4,5)
print(t1.calculate_perimeter())
