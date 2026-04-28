fruits = ['banana', 'orange', 'mango', 'lemon']

does_exist = 'banana' in fruits
print(does_exist)

fruits.append('lime')
fruits.insert(2, 'apple')
print(fruits)

fruits.remove('banana') # fruits.remove(0)
print(fruits)

del fruits[0]
print(fruits)


fruits = ['banana', 'orange', 'mango', 'lemon']
fruits_copy = fruits.copy()
print(fruits_copy)
fruits_copy.clear()
print(fruits_copy)

# join
positive_numbers = [1, 2, 3, 4, 5]
zero = [0]
negative_numbers = [-5, -4, -3, -2, -1]
integers = negative_numbers + zero + positive_numbers
print(integers)

# join with extend
num1 = [0, 1, 2, 3]
num2 = [4, 5, 6]
num1.extend(num2)
print('Numbers:', num1)

print(fruits.count('orange'))   # 1
ages = [22, 19, 24, 25, 26, 24, 25, 24]
print("Count: ", ages.count(24))
ages.reverse()
print("Reverse: ", ages)

# sort
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.sort()
print("Sorts: ", fruits)
fruits.sort(reverse=True)
print(fruits)
