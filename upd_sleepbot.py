import telebot
from telebot import types
import os
import random
import time, datetime
import json

MY_TOKEN = os.getenv('token')
bot = telebot.TeleBot(MY_TOKEN)

info = {}
TEXT_ERROR = 'Произошла ошибка. Попробуй использовать другую команду или перезапустить бот.'
button_stat_press = False


def get_date():
    return datetime.datetime.now().strftime('%d.%m.%Y')


def get_time():
    return datetime.datetime.now().strftime('%X')



@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    "Запуск бота"

    global info

    if not os.path.exists(f'{message.chat.id}.json'):
        info[message.chat.id] = {'name': message.chat.first_name}
        current_user = info.get(message.chat.id)
        current_user['sleeps_counter'] = 0
        current_user['wakes_counter'] = 0
        current_user['dates'] = []
        current_user['cycles'] = {}
        print('not exist')
        with open(f'{message.chat.id}.json', 'w+') as f:
            json.dump(info[message.chat.id], f)
    else:
        print('exist')
        with open(f'{message.chat.id}.json', 'r') as f:
            info[message.chat.id] = json.load(f)

    current_user = info.get(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('О командах')
    markup.add(button)

    bot.send_message(message.chat.id,'Привет, ' + current_user.get('name') + '! Я буду помогать тебе отслеживать параметры сна. '
                                      'Используй команды /sleep, /wake, /quality, /notes '
                                      'и кнопки ниже, чтобы управлять ботом.', reply_markup=markup)



## блок начала сна

@bot.message_handler(commands=['sleep'])
def sleep(message: telebot.types.Message):

    current_date = get_date()
    current_user = info.get(message.chat.id)
    if current_date not in current_user.get('dates'):
        current_user['dates'].append(current_date)

    with open(f'{message.chat.id}.json', 'w+') as f:
        json.dump(info[message.chat.id], f)

    delta = int(current_user.get('sleeps_counter')) - int(current_user.get('wakes_counter'))

    if delta == 1:
            bot.send_message(message.chat.id, 'Похоже, ты пытаешься начать новый цикл сна, не закончив предыдущий. '
                                              'Воспользуйся командой /wake, чтобы завершить текущий цикл.')
    elif delta == 0:
            ask_about_new_cycle(current_user, current_date, message)
    else:
            bot.send_message(message.chat.id, TEXT_ERROR)


def ask_about_new_cycle(user, date, m: telebot.types.Message):
    if user.get(date):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Да, начать новый цикл')
        button2 = types.KeyboardButton('Оставить предыдущую запись')
        markup.add(button1, button2)
        bot.send_message(m.chat.id, 'Сегодня ты уже пользовался командой /sleep. '
                                          'Если ты начнешь новый цикл сна, то предыдущий цикл за текущий день перезапишется. '
                                    'Ты хочешь продолжить?', reply_markup=markup)
    elif not user.get(date):
        create_new_cycle(user, date, m)


def create_new_cycle(user, date, m: telebot.types.Message):
    absolute_time = time.time()
    relative_time = get_time()
    cycle = user.get('cycles')
    cycle[date] = {'quality': 0, 'notes': None,
                  'sleep_relative_time': relative_time, 'sleep_absolute_time': absolute_time,
                  'wake_relative_time': None, 'wake_absolute_time': None, 'duration': None}

    user['sleeps_counter'] += 1

    bot.send_message(m.chat.id, 'Отмечено время отхода ко сну: ' + relative_time)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('О командах')
    markup.add(button)

    options = ['Доброй ночи!', 'Уютных снов!', 'Мягких подушек!', 'Спокойной ночи!', 'Комфортного сна!']
    bot.send_message(m.chat.id, random.choice(options) + ' Не забудь сообщить о пробуждении командой /wake',
                     reply_markup=markup)

    with open(f'{m.chat.id}.json', 'w+') as f:
        json.dump(info[m.chat.id], f)



## блок пробуждения

@bot.message_handler(commands=['wake'])
def wake(message: telebot.types.Message):
    current_user = info.get(message.chat.id)
    current_date = current_user.get('dates')[-1]

    delta = int(current_user.get('sleeps_counter')) - int(current_user.get('wakes_counter'))

    if delta == 0:
        bot.send_message(message.chat.id, 'Я не вижу, чтобы ты сообщил о начале сна. '
                                          'Используй команду /sleep.')
    elif delta == 1:
        finish_cycle(current_user, current_date, message)
    else:
        bot.send_message(message.chat.id, TEXT_ERROR)

    with open(f'{message.chat.id}.json', 'w+') as f:
        json.dump(info[message.chat.id], f)


def finish_cycle(user, date, m: telebot.types.Message):
    absolute_time = time.time()
    relative_time = get_time()

    cycle = user.get('cycles')
    cycle.get(date)['wake_relative_time'] = relative_time
    cycle.get(date)['wake_absolute_time'] = absolute_time

    user['wakes_counter'] += 1

    bot.send_message(m.chat.id, 'Отмечено время пробуждения: ' + relative_time)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('О командах')
    markup.add(button)

    options = ['Доброе утро!', 'Надеюсь, ты хорошо поспал!', 'Вперед, в новый день!']
    bot.send_message(m.chat.id, random.choice(options) +
                     ' Продолжительность твоего сна составила примерно ' + check_duration(user, date) +
                     ' Не забудь оценить качество сна командой /quality и оставить заметки командой /notes',
                     reply_markup=markup)

    with open(f'{m.chat.id}.json', 'w+') as f:
        json.dump(info[m.chat.id], f)


def check_duration(user, date):
    cycle = user.get('cycles')
    time_delta_sec = cycle.get(date)['wake_absolute_time'] - cycle.get(date)['sleep_absolute_time']
    time_delta_hour = round(time_delta_sec / 3600, 2)
    cycle.get(date)['duration'] = time_delta_hour

    if time_delta_hour != 0.0:
        notification = (str(time_delta_hour) + ' часов!')
    else:
        notification = (str(round(time_delta_sec, 2)) + ' секунд!')
    return notification



## блок качества сна

@bot.message_handler(commands=['quality'])
def quality(message: telebot.types.Message):
    if check_possibility_quality(message):
        add_quality(message)
    else:
        bot.send_message(message.chat.id, 'Ты еще не внес цикл сна, качество которого можно было бы оценить. '
                                          'Используй команды /sleep и /wake, чтобы начать.')

    with open(f'{message.chat.id}.json', 'w+') as f:
        json.dump(info[message.chat.id], f)


def check_possibility_quality(m: telebot.types.Message):
    current_user = info.get(m.chat.id)
    if current_user.get('sleeps_counter') != 0 and current_user.get('sleeps_counter') == current_user.get(
            'wakes_counter'):
        return True


def add_quality(m: telebot.types.Message):
    quality_list = m.text.split(' ')
    try:
        quality_list[1]
    except IndexError:
        bot.send_message(m.chat.id, 'Ты не ввёл оценку. '
                                    'Пожалуйста, введи число от 1 до 10 после команды (пример: /quality 8)')
    else:
        react_on_quality(quality_list, m)

    with open(f'{m.chat.id}.json', 'w+') as f:
        json.dump(info[m.chat.id], f)


def react_on_quality(quality_list, m: telebot.types.Message):
    try:
        quality_list[1] = int(quality_list[1])
    except ValueError:
        bot.send_message(m.chat.id, info.get(m.chat.id).get('name') + ', дорогуша, не ломай мою программу :('
                                    '\nВведи число от 1 до 10! (пример /quality 6)')
    else:
        if quality_list[1] not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            bot.send_message(m.chat.id, 'Оценка должна быть числом от 1 до 10. Попробуй еще раз.')
        else:
            if quality_list[1] <= 5:
                bot.reply_to(m, 'Что-то беспокоило? Ты можешь написать об этом в заметках.')
            elif quality_list[1] == 10:
                bot.reply_to(m, 'Супер! Надеюсь, таких ночей будет только больше!')
            else:
                bot.reply_to(m, 'Здорово, что тебе удалось хорошо отдохнуть сегодня!')
            bot.send_message(m.chat.id, 'Воспользуйся командой /notes, чтобы внести заметки '
                                        '(пример: /notes спалось хорошо, снился странный сон про кабачки)')

            current_user = info.get(m.chat.id)
            current_date = current_user.get('dates')[-1]
            cycle = current_user.get('cycles')
            cycle.get(current_date)['quality'] = quality_list[1]

        with open(f'{m.chat.id}.json', 'w+') as f:
            json.dump(info[m.chat.id], f)



## блок заметок о сне

@bot.message_handler(commands=['notes'])
def notes(message: telebot.types.Message):
    if check_possibility_notes(message):
        add_notes(message)
    else:
        bot.send_message(message.chat.id, 'Вводить заметки можно только после оценки качества сна. Используй команду /quality.')

    with open(f'{message.chat.id}.json', 'w+') as f:
        json.dump(info[message.chat.id], f)


def check_possibility_notes(m: telebot.types.Message):
    current_user = info.get(m.chat.id)
    try:
        current_date = current_user.get('dates')[-1]
    except Exception as e:
        bot.send_message(m.chat.id, 'Произошла ошибка: ' + str(e) + '. Напиши моему разработчику, он знает, что это значит. '
                                                                    'И прекрати ломать меня!! Не вызывай заметки, когда тебе этого захочется!')
    else:
        cycle = current_user.get('cycles')
        if cycle.get(current_date).get('quality') != 0:
            return True


def add_notes(m: telebot.types.Message):
    notes_list = m.text.split(' ')
    try:
        notes_list[1]
    except IndexError:
        bot.send_message(m.chat.id, 'Ты не написал заметку. '
                                    'Пожалуйста, напиши любой текст после команды '
                                    '(пример: /notes спала нормально, снился странный сон про яблоки)')
    else:
        note_processing(notes_list, m)

    with open(f'{m.chat.id}.json', 'w+') as f:
        json.dump(info[m.chat.id], f)


def note_processing(notes_list, m: telebot.types.Message):
    notes_list.remove('/notes')
    notes_str = ' '.join(notes_list)

    current_user = info.get(m.chat.id)
    current_date = current_user.get('dates')[-1]
    cycle = current_user.get('cycles')
    cycle.get(current_date)['notes'] = notes_str

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Моя статистика')
    markup.add(button)

    bot.send_message(m.chat.id,'Тебе доступна статистика текущего и других циклов!', reply_markup=markup)

    with open(f'{m.chat.id}.json', 'w+') as f:
        json.dump(info[m.chat.id], f)



## прочие функции обработки сообщений

@bot.message_handler(func=lambda message: message.text == 'О командах')
def about_commands(message: telebot.types.Message):
    bot.send_message(message.chat.id,'Сообщи об отходе ко сну командой /sleep, о пробуждении — командой /wake'
                     '\nОцени качество сна по 10-балльной шкале с помощью /quality (пример: /quality 8)'
                     '\nДобавь заметки по желанию, используя /notes (пример: /notes спала отлично, снился странный сон про арбузы)')


@bot.message_handler(func=lambda message: message.text == 'Да, начать новый цикл')
def new_cycle(message: telebot.types.Message):
    current_date = get_date()
    current_user = info.get(message.chat.id)
    create_new_cycle(current_user, current_date, message)


@bot.message_handler(func=lambda message: message.text == 'Оставить предыдущую запись')
def cycle_cancellation(message: telebot.types.Message):
    current_date = get_date()
    bot.send_message(message.chat.id, 'Хорошо. Статистика для ' + current_date + ' не изменена.')



## вывод статистики

@bot.message_handler(func=lambda message: message.text == 'Моя статистика')
def print_stat(message: telebot.types.Message):
    global button_stat_press
    if check_possibility_stat(message):
        button_stat_press = True
        select_date(message)
    else:
        bot.send_message(message.chat.id, 'Внеси запись о цикле сна, чтобы получить доступ к статистике.')
    return button_stat_press


def check_possibility_stat(m: telebot.types.Message):
    current_user = info.get(m.chat.id)
    current_date = current_user.get('dates')[-1]
    cycle = current_user.get('cycles')
    if cycle.get(current_date).get('notes'):
        return True


def select_date(message: telebot.types.Message):
    current_user = info.get(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for date in current_user.get('dates'):
        button = types.KeyboardButton(date)
        markup.add(button)

    bot.send_message(message.chat.id, 'Выбери дату начала сна, чтобы посмотреть его статистику.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def other_text(message: telebot.types.Message):
    current_user = info.get(message.chat.id)
    if not message.text in current_user.get('dates'):
        bot.reply_to(message, 'Я не смог распознать команду. Попробуй еще раз.')
        return
    if not print_stat(message):
        bot.send_message(message.chat.id, TEXT_ERROR)
        return
    bot.send_message(message.chat.id, 'Твоя статистика за ' + message.text)
    current_date = info.get(message.chat.id).get('cycles').get(message.text)
    bot.send_message(message.chat.id, 'Время отхода ко сну: ' + current_date.get('sleep_relative_time') +
                             '\nВремя пробуждения: ' + current_date.get('wake_relative_time') +
                             '\nПродолжительность сна в часах: ' + str(current_date.get('duration')) +
                             '\nКачество сна: ' + str(current_date.get('quality')) +
                             '\nЗаметки: ' + current_date.get('notes'))
    bot.send_message(message.chat.id, 'Не забудь вызвать меня командой /sleep, когда соберешься спать!')





bot.polling(none_stop=True)

print(info)