import psycopg2
from psycopg2 import sql

def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            database="EHP_Project"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к базе данных:", error)
        return None


def insert_data(connection, mail_id, date_time, data):
    cursor = connection.cursor()

    if "keylog" in data.lower():
        table_name = "table_for_keylogs"
        data = data.split(" ")[1] if len(data.split(" ")) > 1 else ""
        data_type = "keylog_hash"
    elif "password" in data.lower():
        table_name = "table_for_passwords"
        data = data.split(" ")[1] if len(data.split(" ")) > 1 else ""
        data_type = "password_hash"
    else:
        return False

    try:
        # Подготовка запроса на вставку данных в таблицу
        query = sql.SQL("INSERT INTO {} (mail_id, date_time, {}) VALUES (%s, %s, %s)").format(
            sql.Identifier(table_name), sql.Identifier(data_type))

        cursor.execute(query, (mail_id, date_time, data))

        connection.commit()
        print("Данные успешно добавлены в базу данных.")
        return True
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при вставке данных:", error)
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()


connection = connect_to_database()
if connection:
    file_path = "filtered_data.txt"
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(") (")
            mail_id = data[0].strip("()")
            date_time = data[1].strip("()")
            hash_data = data[2].strip("()\n")
            what_done = "Insertion"

            insert_data(connection, mail_id, date_time, hash_data)

    connection.close()