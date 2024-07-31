import psycopg2
from config import host, user, password, db_name

# подключение к бд
try:
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True


    # create a new table До использования бота создайте таблицу
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users_finance_bot(
    #             id serial PRIMARY KEY,
    #             user_tg_id varchar(20) NOT NULL,
    #             cash int NOT NULL,
    #             spend int NOT NULL);"""
    #     )
    #
    #     # connection.commit()
    #     print("[INFO] Table created successfully")

    #при команде старт будет сщздаваться новая запись в бд
    # user_id = 'Edward'
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO users_finance_bot (user_tg_id, cash, spend)
    #         VALUES (%s, %s, %s);""", (user_id, 0, 0)
    #     )

    # обновление spend cash
    # user_tg_id = 'Edward'
    # x = 100
    # with connection.cursor() as cursor:
    #     sql_update_query = """Update users_finance_bot set cash = cash + %s where user_tg_id = %s"""
    #     cursor.execute(sql_update_query, (x, user_tg_id))

    user_tg_id = 'Edward'
    x = 100
    with connection.cursor() as cursor:
        sql_update_query = """SELECT cash FROM users_finance_bot WHERE user_tg_id = Edward"""
        cursor.execute(sql_update_query)
    print(cursor.fetchone())

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")