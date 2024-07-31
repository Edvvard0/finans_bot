# import sqlite3

from telebot import types, TeleBot
import psycopg2
from config import host, user, password, db_name

# Инициализация телеграм бота
TOKEN = '7382523397:AAE9bCchn84A4ndqpUEME-A6YkmDAR4_V38'
bot = TeleBot(TOKEN)


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

#DATA_BASE

def conn():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    return connection


def select_db(user_tg_name, columns):
    connection = conn()
    with connection.cursor() as cursor:
        cursor.execute(
            """select %s from users_finance_bot where user_tg_id = %s;""", (columns, user_tg_name)
        )
        many = cursor.fetchone()
        print(f'{many} select_db')
    return many


def add_user_db(user_tg_name):
    # при команде старт будет создаваться новая запись в бд
    connection = conn()
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO users_finance_bot (user_tg_id, cash, spend)
            VALUES (%s, %s, %s);""", (user_tg_name, 0, 0)
        )

def update(user_tg_id, amount, flag = True):
    x = amount
    connection = conn()
    if flag:
        with connection.cursor() as cursor:
            sql_update_query = """Update users_finance_bot set cash = cash + %s where user_tg_id = %s"""
            cursor.execute(sql_update_query, (x, user_tg_id))
    else:
        with connection.cursor() as cursor:
            sql_update_query = """Update users_finance_bot set spend = spend + %s where user_tg_id = %s"""
            cursor.execute(sql_update_query, (x, user_tg_id))

@bot.message_handler(commands=['start'])
def spend(message):
    markup = func_markup()
    bot.send_message(message.chat.id,'привет я бот для ведения учета твойх финансов',reply_markup=markup)
    # bot.send_message(message.chat.id, message.from_user.username)
    add_user_db(message.from_user.username)


@bot.message_handler(commands=['balance'])
def balance(message):

    many_spend = select_db(message.from_user.username, 'spend')
    many_cash = select_db(message.from_user.username, 'cash')
    print(f'{many_cash} balance')

    # bot.reply_to(message, f"Ваш баланс: {many_cash - many_spend},\n"
    #                       f"вы потратили {many_spend} \n"
    #                       f"вы заработали {many_cash}")

# Обработчик команды для расходов
@bot.message_handler(commands=['spend'])
def spend(message):
    bot.send_message(message.chat.id, 'сколько вы потратили')
    bot.register_next_step_handler(message, get_spend)



def get_spend(message):
        amount = message.text
        if verify_many(message, amount):
            amount = int(amount)

            markup = func_markup()
            bot.reply_to(message, f"расход на сумму {amount} добавлен",reply_markup=markup)
            update(message.from_user.username, amount, flag=False)

@bot.message_handler(commands=['cash'])
def finanses(message):
    bot.send_message(message.chat.id, 'сколько ты заработал')
    bot.register_next_step_handler(message, get_finans)

def get_finans(message):
        amount = message.text
        if verify_many(message, amount):
            amount = int(amount)

            markup = func_markup()
            bot.reply_to(message, f"Доход на сумму {amount} добавлен",reply_markup=markup)
            update(message.from_user.username, amount)


# Запуск телеграм бота
bot.polling()

