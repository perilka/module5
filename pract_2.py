import random
from collections import Counter
from collections import namedtuple
from collections import defaultdict
from collections import deque

# Задание 1
random_numbers = []
i = 0
while i != 10:
    num = random.randint(0,10)
    random_numbers.append(num)
    i += 1
print(random_numbers)

print(Counter(random_numbers))
print(Counter(random_numbers).most_common(3))


# Задание 2
Book = namedtuple('Book', ['title', 'author', 'genre'])

book1 = Book('title1', 'author1', 'genre1')
book2 = Book('title2', 'author2', 'genre2')
book3 = Book('title3', 'author3', 'genre3')

books = [book1, book2, book3]

for book in books:
    print(f'title: {book.title}, author: {book.author}, genre: {book.genre}')


# Задание 3
d = defaultdict(list)
d['a'] = ['aardappel']
d['b'] = ['banaan']
d['c'] = ['citroen']
for key in d.keys():
    print(d[key])


# Задание 4
my_deque = deque([1, 2, 3])
print(my_deque)
my_deque.append(4)
print(my_deque)
my_deque.appendleft(0)
print(my_deque)
my_deque.pop()
print(my_deque)
my_deque.popleft()
print(my_deque)


# Задание 5
def append(dq: deque, obj):
    return dq.append(obj)

def appendleft(dq: deque, obj):
    return dq.appendleft(obj)

def pop(dq: deque):
    return dq.pop()

def popleft(dq: deque):
    return dq.popleft()

new_deque = deque([1, 2, 3])

append(new_deque, 4)
print(new_deque)
appendleft(new_deque, 0)
print(new_deque)
pop(new_deque)
print(new_deque)
popleft(new_deque)
print(new_deque)