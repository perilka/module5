from functools import reduce

# Задание 1
def cubing(x: int|float) -> int|float:
    return x ** 3

numbers = [1, 2, 3, 4]
cubed_numbers = list(map(cubing, numbers))


# Задание 2
def is_divisible_by_five(x: int) -> bool:
    return x % 5 == 0

numbers = [2, 5, 34, 10]
filtered_numbers = list(filter(is_divisible_by_five, numbers))


# Задание 3
def is_uneven(x: int|float) -> bool:
    return x % 2 != 0

def multiply(x: int|float, y: int|float) -> int|float:
    return x * y

numbers = [1, 2, 3, 4, 5]

result = reduce(multiply, list(filter(is_uneven, numbers)))