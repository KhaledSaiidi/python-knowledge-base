class Student:
    def check_pass_fail(self):
        if self.marks >= 40:
            return True
        else:
            return False
    def __init__(self, name,marks):
        self.name = name
        self.marks = marks
        

student1 = Student("Harry", 85)
did_pass = student1.check_pass_fail()
print(student1.name, student1.marks, did_pass)

class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
    def add(self, number):
        real = self.real + number.real
        imag = self.imag + number.imag
        result = Complex(real, imag)
        return result

n1 = Complex(5, 6j)
n2 = Complex(-4, 2j)
result = n1.add(n2)
print(result.real, result.imag)
