# warm-up Drill

from turtle import st

from numpy import true_divide


def max_value(numbers: list[int]) -> int:
    if len(numbers) == 0:
        raise ValueError("Numbers cannot be empty")
    largest_number:int = numbers[0]
    for number in numbers:
        if number > largest_number:
            largest_number = number
    return largest_number

    
    # ["aws", "k8s", "aws"]
    # -> {"aws": 2, "k8s": 1}
def count_words(words: list[str]) -> dict[str, int]:
    counted_words: dict[str, int] = {}
    for word in words:
        if word in counted_words:
            counted_words[word] += 1
        else:
            counted_words[word] = 1
    return counted_words

def unique_items(items: list[str]) -> set[str]:
    if len(items) == 0:
        raise ValueError("Items cannot be empty")
    finale_items: set[str] = set()
    for item in items: 
        finale_items.add(item)
    return finale_items



def reverse_string(value: str) -> str:
    value_list: list[str] = list(value)
    value_list.reverse()
    reversed_string: str = "".join(value_list)
    return reversed_string



# Drill 1 — Lists
# Given:
# numbers = [4, 7, 2, 7, 9, 2, 1]
# Return only numbers greater than 4.
# Expected:
# [7, 7, 9]

def drill_1(numbers: list[int]) -> list[int]:
    num_gt_4 = []
    for number in numbers:
        if number > 4:
            num_gt_4.append(number)
    return num_gt_4

# Drill 2 — Dict
# Given:
# services = ["api", "worker", "api", "db", "worker", "api"]
# Produce:
# {
#     "api": 3,
#     "worker": 2,
#     "db": 1
# }

def drill_2(services: list[str]) -> dict[str, int]:
    result = {}
    for service in services:
        if service in result:
            result[service] += 1
        else:
            result[service] = 1
    return result

# Drill 3 — Set
# Given:
# cluster_a = ["api", "worker", "redis"]
# cluster_b = ["api", "worker", "postgres"]
# Find services existing in both clusters.
# Expected:
# {"api", "worker"}

def drill_3(cluster_a: list[str], cluster_b: list[str]) -> set[str]:
    cluster_a_set: set[str] = set(cluster_a)
    result = set()
    for service in cluster_b:
        if service in cluster_a_set:
            result.add(service)
    return result

# Drill 4 — Strings
# Given:
# log = "ERROR database connection failed"
# Write a function:
# def is_error(log):
#     ...
# returning True if the line starts with "ERROR".
# These are intentionally simple. The purpose is fluency.
def is_error(log: str) -> bool:
    log = log.lower()
    return log.startswith("error")