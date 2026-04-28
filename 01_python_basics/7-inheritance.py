class Polygon:
    def __init__(self, sides):
        self.sides = sides
    
    def display_info(self):
        print('''A Polygon is two D.
Shaped with straigth lines.''')
    
    def get_perimiter(self):
        perimeter = sum(self.sides)
        return perimeter
    
class Triangle(Polygon):
    def display_info(self):
        print("A triangles with {} sides".format(str(len(self.sides))))
        super().display_info()
t1 = Triangle([5, 6, 7])
perimiter = t1.get_perimiter()
print(perimiter)
t1.display_info()
