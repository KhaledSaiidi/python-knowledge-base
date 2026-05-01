import os
with open("01_python_basics/message.txt", "r") as f: # r, w or a (append)

    content = f.read(6)
    print(content)
    more_content = f.read(12)
    print(more_content)
    
    f.seek(0)
    lines = f.readlines()
    print(lines) # To a list
    # f.close() <- Not needed as with relies on Python’s context management protocol (__enter__ / __exit__), 
    # File is automatically closed

with open("01_python_basics/python.txt", "w") as f:
    f.write('''Python is awesome
I love Python''')
    
with open("01_python_basics/python.txt", "a") as f:
    f.write('\nBut Go is better')
    lines = ["\nGo is way better", "\nGo is more robust"]
    f.writelines(lines)


current_dir = os.getcwd()
print(current_dir)
# os.chdir("00_setup")
# print(os.getcwd())

print(os.listdir("01_python_basics"))

# os.mkdir("test")
# os.rename("test", "test_new")
os.remove("file/path/to/remove")