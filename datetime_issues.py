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

user_date = input('Введите дату в формате "год-месяц-день": ').split('-')
user_date = [int(x) for x in user_date]
datetime_date = datetime.date(user_date[0], user_date[1], user_date[2])

print(now.date() - datetime_date)