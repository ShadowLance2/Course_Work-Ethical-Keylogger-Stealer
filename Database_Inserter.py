import psycopg2

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