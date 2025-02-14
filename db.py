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


    #create a new table До использования бота создайте таблицу
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users_finance_bot(
                id serial PRIMARY KEY,
                user_tg_id varchar(20) NOT NULL,
                cash int NOT NULL,
                spend int NOT NULL);"""
        )

        # connection.commit()
        print("[INFO] Table created successfully")



except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")
