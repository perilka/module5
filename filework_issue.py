def get_words(file) -> list[str]:
    words_list = []
    for line in file:
        words = line.strip().split()
        for word in words:
            words_list.append(word.lower())
    return words_list

def get_words_dict(words_list: list[str]) -> dict[str:int]:
    words_dict = {}
    for word in words_list:
        words_dict[word] = words_list.count(word)
    return words_dict


# name = input('Введите название файла: ') можно оптимизировать под любой файл, не только для датч_сонг

f = open('dutch_song.txt', 'r')
words_lst = get_words(f)
words_dct = get_words_dict(words_lst)
print(f'Кол-во слов: {len(words_lst)}')
print(f'Кол-во уникальных слов: {len(words_dct.keys())}')
print(f'Все использованные слова:')
for key, value in words_dct.items():
    print(f'{key} {value}')
f.close()