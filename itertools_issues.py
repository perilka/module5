import itertools



# Задача 1
items = [1, 2, 3, 4]
for i in itertools.combinations(items, 2):
    print(i)


# Задача 2
word = 'python'
for i in itertools.permutations(word):
    print(i)


# Задача 3
l1 = ['a', 'b']
l2 = [1, 2, 3]
l3 = ['x', 'y']

## 1 способ
count = 0
for item in itertools.cycle(l1 + l2 + l3):
    if count > 5: # это и подразумевается под "повторяя этот цикл 5 раз"? или нужна 4 тут?
        break
    print(item)
    count += 1

## 2 способ
count = 0
for item in itertools.cycle(itertools.chain(l1, l2, l3)):
    if count > 5: # это и подразумевается под "повторяя этот цикл 5 раз"? или нужна 4 тут?
        break
    print(item)
    count += 1


# Задача 4
def fibonacci(n):
    a = 0
    b = 1
    yield a
    yield b
    count = 0
    while count != n:
        c = a + b
        a = b
        b = c
        yield b
        count += 1

for number in fibonacci(10):
    print(number)


# Задача 5
colors = ['red', 'blue']
clothes = ['shirt', 'shoes']

for item in itertools.product(colors, clothes):
    print(item)