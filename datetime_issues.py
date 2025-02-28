import datetime, calendar

# Часть 1

now = datetime.datetime.now()

weekdays = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}
print(weekdays[now.weekday()])

if calendar.isleap(now.year):
    print('Год високосный')
else:
    print('Год не високосный')


# Часть 2

parsed_date = datetime.datetime.strptime(input('Введите дату в формате "год-месяц-день": '), "%Y-%m-%d")
print(now - parsed_date)