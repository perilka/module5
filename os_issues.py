import os, shutil

# Создание директории
if not os.path.exists('Управление_файлами'):
    os.mkdir('Управление_файлами')

# Создание файлов
with open('Управление_файлами/file1.txt', 'w', encoding='utf8') as f:
    f.write('бла бла бла')

with open('Управление_файлами/file2.txt', 'w', encoding='utf8') as f:
    f.write('ля ля ля')

# Вывод содержимого
files_and_dirs = os.listdir('Управление_файлами')
print('Файлы и директории:', files_and_dirs)

# Удаление файла
os.remove('Управление_файлами/file1.txt')

# Создание поддиректории
if not os.path.exists('Управление_файлами/Поддиректория'):
    os.mkdir('Управление_файлами/Поддиректория')

# Перемещение файла
os.rename('Управление_файлами/file2.txt', 'Управление_файлами/Поддиректория/file2.txt')

# Удаление исходной директории
shutil.rmtree('Управление_файлами')