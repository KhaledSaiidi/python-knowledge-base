print('To escepe line. \nDo.')
print('Day 1\t3\t5\t6')
print('This is a back slash \\')

challenge = 'thirty days of Python'
print(challenge.capitalize())
print(challenge.upper())
print(challenge.lower())

print(challenge.count('y'))
print(challenge.count('y', 7, 16)) # start 7 stops before 16

print(challenge.endswith('on')) 
challenge = 'thirty\tdays\tof\tpython'
print(challenge)
print(challenge.expandtabs())
print(challenge.expandtabs(10))


first_name = 'Khaled'
last_name = 'Saidi'
print(last_name.find('id'))
job = 'PE'
country = 'Finland'

sentence = 'I am {} {}. I am a {}. I live in {}'.format(
    first_name, last_name,job, country,
)
print(sentence)
radius = 10
pi = 3.14
area = pi
result = 'The area of circle with {} is {}'.format(
    str(radius), str(area)
)
print(result)

challenge = "thirty"
print(challenge.isdecimal())
challenge = '30'
print(challenge.isdecimal())

web_tech = ['html', 'python', 'go']
result = '#, '.join(web_tech)
print(result)

challenge = 'thirty days of python'
print(challenge.split())  # ['thirty', 'days', 'of', 'python']

name = input("Enter name: ")
number = int(input("Enter number: "))
print(name)
print(number)

name = "khaled"
print(dir(name))