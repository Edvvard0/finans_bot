# import sqlite3

from telebot import types, TeleBot


# Инициализация телеграм бота
TOKEN = '7382523397:AAE9bCchn84A4ndqpUEME-A6YkmDAR4_V38'
bot = TeleBot(TOKEN)

expenses = []
finans = []

#категории
food = []
hobby = []
sport = []
other = []


def func_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/spend")
    item2 = types.KeyboardButton("/cash")
    markup.row(item1, item2)
    item3 = types.KeyboardButton("/balance")
    markup.add(item3)
    return markup


def verify_many(message, x):
    if not x.isdigit() or x[0]==0:
          bot.send_message(message.chat.id, 'некоректный ввод данных')
          return False
    return True


@bot.message_handler(commands=['start'])
def spend(message):
    markup = func_markup()
    bot.send_message(message.chat.id,'привет я бот для ведения учета твойх финансов',reply_markup=markup)

@bot.message_handler(commands=['balance'])
def balance(message):
    bot.reply_to(message, f"Ваш баланс: {sum(finans)-sum(expenses)},\n"
                          f"вы потратили {sum(expenses)} \n"
                          f"вы заработали {sum(finans)}")

# Обработчик команды для расходов
@bot.message_handler(commands=['spend'])
def spend(message):
    bot.send_message(message.chat.id, 'сколько вы потратили')
    bot.register_next_step_handler(message, get_spend)


def get_spend(message):
        amount = message.text
        if verify_many(message, amount):
            expenses.append(int(amount))

            markup = func_markup()
            bot.reply_to(message, f"расход на сумму {amount} добавлен",reply_markup=markup)


@bot.message_handler(commands=['cash'])
def finanses(message):
    bot.send_message(message.chat.id, 'сколько ты заработал')
    bot.register_next_step_handler(message, get_finans)

def get_finans(message):
        amount = message.text
        if verify_many(message, amount):
            finans.append(int(amount))

            markup = func_markup()
            bot.reply_to(message, f"Доход на сумму {amount} добавлен",reply_markup=markup)


# Запуск телеграм бота
bot.polling()

