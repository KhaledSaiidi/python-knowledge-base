# warm-up Drill

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

    