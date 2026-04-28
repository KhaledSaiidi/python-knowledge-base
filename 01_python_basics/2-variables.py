first_name = 'khaled'
last_name = 'Saidi'
country = 'Finland'
city = 'Helsinki'
age = 250

is_married = True
skills = ['HTML', 'CSS', 'JS', 'Python']

person_info = {
    'fitst_name': 'khaled',
    'last_name': 'Saidi',
    'country': 'Finland',
    'city': 'Helsinki',
}


print('First name:', first_name)
print('Last Name:', last_name)
print('first name length is: ', len(first_name))
print('Personal informations:', person_info)

# Declaring multiple variables in one line
new_name, new_lastName, new_country, newAge = 'Khaled', 'Saidi', 'Doha', 27

print('True and True: ', True and True)
print('True or False:', True or False)

multi_line_string = '''This is a multi-line string.
It can span multiple lines.'''
print(multi_line_string)

language = 'Python'
print(language[0])  # Output: 'P'
a, b, c, d, e, f = language
print(a)
last_index = len(language) - 1
print(language[last_index])
first_three = language[:3]
print(first_three)
last_three = language[-3:]
print(last_three)
chars = language[1:4]
print(chars)
