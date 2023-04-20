import telebot
from telebot import types
from config import convert
from config import actual
from exception import ConvertionException
from config import check_func

bot = telebot.TeleBot('5929517159:AAHEP_2ygmnCAzk0msJU8WHEmsQycFu2HzU')


@bot.message_handler(commands=["start"])
def start(message):
    keys = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Перезапустить бот.')
    button2 = types.KeyboardButton('Актуальный курс и справочник валют.')
    keys.add(button1, button2)
    bot.send_message(message.chat.id, f'Для проверки актуального курса и получения справки '
                                      f'воспользуйтесь клавиатурой.')
    bot.send_message(message.chat.id, f'Введите конвертируемые валюты и их количество.'
                                      f'формат ввода rub usd 100'.format(message.from_user), reply_markup=keys)
    bot.register_next_step_handler(message, menu)



@bot.message_handler(content_types=['text'])
def menu(message):
    mess = message.text.strip()
    if mess == 'Перезапустить бот.':
        start(message)
    elif mess == 'Актуальный курс и справочник валют.':
        bot.send_message(message.chat.id, actual())
        bot.send_message(message.chat.id, f'Введите конвертируемые валюты и их количество формат ввода rub usd 100')
    else:
        quantity(message)

def quantity(message):
    user_input = message.text.split(' ')
    qua = user_input[2]
    try:
        if len(user_input) != 3:
            raise ConvertionException(f'Слишком много переменных!.')
        if len(check_func(user_input[0], user_input[1])) != 2:
            raise ConvertionException(f'Валюта не доступна для конвертации!.')
        float(qua)
    except ValueError:
        bot.reply_to(message, f'Ошибка.\n{qua} Не является числом!')
    except ConvertionException as a:
        bot.reply_to(message, f'Ошибка.\n{a}')
    except Exception as a:
        bot.reply_to(message, f'Ошибка.\n{a}')
    else:
        res = convert(user_input[0], user_input[1])
        bot.send_message(message.chat.id, f' {round(res * float(qua), 2)}  {user_input[1]}')
        keys_up = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('🇺🇸USD/RUB🇷🇺', callback_data=f'USD RUB {qua}')
        button2 = types.InlineKeyboardButton('🇺🇸USD/EUR🇪🇺', callback_data=f'USD EUR {qua}')
        button3 = types.InlineKeyboardButton('🇷🇺RUB/EUR🇪🇺', callback_data=f'RUB EUR {qua}')
        button4 = types.InlineKeyboardButton('🇷🇺RUB/USD🇺🇸', callback_data=f'RUB USD {qua}')
        button5 = types.InlineKeyboardButton('🇷🇺RUB/THB🇹🇭', callback_data=f'RUB THB {qua}')
        button6 = types.InlineKeyboardButton('🇹🇭THB/RUB🇷🇺', callback_data=f'THB RUB {qua}')
        keys_up.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, f'💵Популярные пары для конвертации.\n для изменения количества валюты'
                                          f'повторите ввод.💵', reply_markup=keys_up)
        bot.register_next_step_handler(message, menu)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    value = call.data.split(' ')
    summ, res = convert(value[0], value[1]), float(value[2])
    bot.send_message(call.message.chat.id, f' {round(res * summ, 2)}  {value[1]}')


bot.polling(none_stop=True, interval=0)