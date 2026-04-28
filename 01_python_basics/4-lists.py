# -------------------------------- List
# Use when you need an ordered, mutable collection that allows duplicates
# Common ops: append(), extend(), insert(), remove(), pop(), sort(), reverse(), copy(), indexing []

fruits = ['banana', 'orange', 'mango']

fruits_copy = fruits.copy()
# creates a shallow copy → new list with same values (modifying copy won't affect original)

fruits.append('apple')
# adds 'apple' to the end → ['banana', 'orange', 'mango', 'apple']

fruits.extend(['kiwi', 'grape'])
# adds multiple items → ['banana', 'orange', 'mango', 'apple', 'kiwi', 'grape']

fruits.insert(1, 'pear')
# inserts at index 1 → ['banana', 'pear', 'orange', 'mango', 'apple', 'kiwi', 'grape']

fruits.remove('orange')
del fruits[0]
# removes first occurrence → ['banana', 'pear', 'mango', 'apple', 'kiwi', 'grape']

last = fruits.pop()
# removes and returns last item → last='grape', list updated

fruits.sort()
fruits.sort(reverse=True)
# sorts alphabetically → ['apple', 'banana', 'kiwi', 'mango', 'pear']

fruits.reverse()
# reverses order → ['pear', 'mango', 'kiwi', 'banana', 'apple']

first = fruits[0]
# access by index → first='pear'



# -------------------------------- Tuple
# Use when you need an ordered, immutable collection (fixed data, safer for constants)
# Common ops: indexing [], count(), index(), unpacking (x, y = coordinates)

coordinates = (10, 20)

x = coordinates[0]
# access element → x=10

count_10 = coordinates.count(10)
# counts occurrences → count_10=1

index_20 = coordinates.index(20)
# finds index → index_20=1

x, y = coordinates
# unpack tuple → x=10, y=20

coordinates_copy = tuple(coordinates)
# creates a copy (same values, new tuple object)



# -------------------------------- Set
# Use when you need unique elements and fast membership checks (no duplicates, unordered)
# Common ops: add(), remove(), discard(), union(|), intersection(&), difference(-), copy(), in

unique_numbers = {1, 2, 3, 4}

set_copy = unique_numbers.copy()
# creates a shallow copy → new set with same values

unique_numbers.add(5)
# adds element → {1,2,3,4,5}

unique_numbers.remove(2)
# removes element, error if not found → {1,3,4,5}

unique_numbers.discard(10)
# removes if exists, no error if not → unchanged

other_set = {3, 4, 6}

union_set = unique_numbers | other_set
# combines all unique → {1,3,4,5,6}

intersection_set = unique_numbers & other_set
# common elements → {3,4}

difference_set = unique_numbers - other_set
# elements only in first → {1,5}

exists = 3 in unique_numbers
# membership check → True



# -------------------------------- Dictionary (dict)
# Use when you need key-value mapping for structured data and fast lookups by key
# Common ops: get(), keys(), values(), items(), update(), pop(), copy(), access via user["key"]

user = {
    "name": "Khaled",
    "age": 25
}

user_copy = user.copy()
# creates a shallow copy → new dict with same key-value pairs

name = user["name"]
# direct access → "Khaled" (error if key missing)

age = user.get("age")
# safe access → 25 (returns None if missing)

keys = user.keys()
# returns all keys → dict_keys(['name','age'])

values = user.values()
# returns all values → dict_values(['Khaled',25])

items = user.items()
# returns key-value pairs → dict_items([('name','Khaled'),('age',25)])

user.update({"age": 26, "city": "Tunis"})
# updates/adds keys → {'name':'Khaled','age':26,'city':'Tunis'}

removed = user.pop("city")
# removes and returns value → removed='Tunis'