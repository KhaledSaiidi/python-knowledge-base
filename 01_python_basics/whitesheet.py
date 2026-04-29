from dataclasses import dataclass
# class Triangle:
#     def __init__(self, a: float, b: float, c: float) -> None:
#         self.a = a
#         self.b = b
#         self.c = c
#     def calculate_perimeter(self) -> float:
#         result = self.a + self.b + self.c
#         return result

# t1 = Triangle(3.1,4.2,5.3)
# print(f"The perimeter of the t1 is {t1.calculate_perimeter():.2f}")

@dataclass
class Triangle:
    a: float
    b: float
    c: float
    def __post_init__(self) -> None:
        if self.a <= 0 or self.b <= 0 or self.c <= 0:
            raise ValueError("All sides must be positive numbers")
        if (self.a + self.b <= self.c or 
            self.c + self.b <= self.a or
            self.a + self.c <= self.b):
            raise ValueError("Invalid triangle dimensions")
        
    def calculate_perimeter(self) -> float:
        result = self.a + self.b + self.c
        return result
    def __repr__(self) -> str:
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"