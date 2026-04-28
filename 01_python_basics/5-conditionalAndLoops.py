score = int(input("Enter your sccore: "))

if score >= 50:
    print("You have passed the exam with {}".format(str(score)))
    print("Congrats")
elif score >= 20 and score < 50:
    print("You have a second try")
else:
    print("Sorry You have failed the exam with {}".format(str(score)))


count = 0
while count <= score:
    print("Count is still {} less then 5".format(str(count)))
    count+=1

text = "Python"

for character in text:
    print(character)

text = "Python is a great language"
for word in text.split():
    print(word)

# range 1, 6 gives from 1 -> 5 
for i in range(1, 6):
    print(i)
    if i == 3:
        break
i = 0
marks = list()
while i < 5:
    mark = int(input("Enter your mark: "))
    if mark == 0:
        continue
    marks.append(mark)
    i += 1

def get_grade(marks):
    for mark in marks:
        if mark >= 80:
            print("Grade A as your score is {}".format(str(mark)))
        elif mark < 80 and mark >= 60:
            print("Grade B as your score is {}".format(str(mark)))
        elif mark < 60 and mark >= 50:
            print("Grade C as your score is {}".format(str(mark)))
        else:
            print("Grade F as your score is {}".format(str(mark)))

def find_average_marks(marks):
    sum_of_marks = sum(marks)
    total_markes = len(marks)
    average_marks = sum_of_marks//total_markes
    return average_marks

get_grade(marks)
average_marks = find_average_marks(marks)
print("The average marks in this class is {}".format(average_marks))

