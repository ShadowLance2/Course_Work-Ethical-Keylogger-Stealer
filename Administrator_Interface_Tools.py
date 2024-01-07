from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from bs4 import BeautifulSoup
import imaplib
import email
import psycopg2
from psycopg2 import sql
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class EmailExtractor(App):

    def build(self):
        self.username_input = TextInput(hint_text='Адрес электронной почты', size_hint=(1, 0.2))
        self.password_input = TextInput(hint_text='Пароль', password=True, size_hint=(1, 0.2))
        self.submit_button = Button(text='Извлечь данные', size_hint=(1, 0.2))
        self.submit_button.bind(on_press=self.on_submit)
        self.insert_button = Button(text='Вставить данные', size_hint=(1, 0.2))
        self.insert_button.bind(on_press=self.on_insert)
        self.output_label = Label(text='', size_hint=(1, 0.3))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.submit_button)
        layout.add_widget(self.insert_button)
        layout.add_widget(self.output_label)

        tables = self.show_all_tables()
        if tables:
            for table in tables:
                table_name = table[0]
                button = Button(text=f"Показать {table_name}")
                button.size_hint = (0.4, 0.3)
                button.bind(on_release=lambda btn, t=table_name: self.show_table(t))
                layout.add_widget(button)
        else:
            label = Label(text="Нет доступных таблиц")
            layout.add_widget(label)

        return layout

    # Извлечение данных из контента писем
    def extract_data(self, content):
        blocks = content.split("=" * 50 + "\n")
        filtered_data = []

        for block in blocks:
            lines = block.strip().split("\n")
            data = {}

            for line in lines:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key, value = parts[0].strip(), parts[1].strip()
                    data[key] = value

            if "Message-ID" in data and "Content" in data and "Body" in data:
                message_id = data["Message-ID"]
                content_info = data["Content"]

                body_index = -1
                for i, line in enumerate(lines):
                    if line.startswith("Body: EHP"):
                        body_index = i
                        break

                body = (
                    lines[body_index].split("Body: EHP", 1)[-1].strip()
                    if body_index != -1
                    else ""
                )
                filtered_data.append(
                    f"({message_id}) ({content_info}) ({body})"
                )

        with open("filtered_data.txt", "w") as filtered_file:
            for data in filtered_data:
                filtered_file.write(data + "\n")

    # Получение всех электронных писем
    def get_all_emails(self, username, password, identifier):
        try:
            mail = imaplib.IMAP4_SSL('imap.mail.ru', 993)
            mail.login(username, password)
            mail.select("inbox")

            result, data = mail.search(None, "ALL")
            emails = []

            for num in data[0].split():
                result, data = mail.fetch(num, "(RFC822)")
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                message_id = msg.get("Message-ID")
                if not message_id:
                    message_id = msg.get("Message-Id")
                if not message_id:
                    message_id = msg.get("MessageId")

                body = self.extract_text_from_email(msg)
                if identifier in body:
                    emails.append({"Message-ID": message_id, "Subject": str(msg["Subject"]), "Date": msg["Date"], "Body": body})

            mail.close()
            mail.logout()
            return emails
        except Exception as e:
            return None

    # Извлечение текста из электронного письма
    def extract_text_from_email(self, msg):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                try:
                    payload = part.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        body += payload
                    elif content_type == "text/html":
                        soup = BeautifulSoup(payload, "html.parser")
                        body += soup.get_text()
                except Exception as e:
                    print(e)
        else:
            payload = msg.get_payload(decode=True).decode()
            body += payload

        return body

    # Сохранение электронных писем
    def save_emails(self, emails):
        with open("all_emails_mail_ru.txt", "w") as file:
            for email in emails:
                file.write(f"Message-ID: {email['Message-ID']}\n")
                file.write(f"Content: {email['Date']}\n")
                file.write(f"Body: {email['Body']}\n")
                file.write("=" * 50 + "\n")

    def on_submit(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        identifier = "EHP"

        if not username or not password:
            self.output_label.text = "Ошибка: Пожалуйста, заполните все поля данных."
            return

        emails = self.get_all_emails(username, password, identifier)
        if emails is None:
            self.output_label.text = "Ошибка при входе в почтовый ящик. Проверьте правильность логина и пароля."
            return

        self.save_emails(emails)

        with open("all_emails_mail_ru.txt", "r") as file:
            content = file.read()
            self.extract_data(content)

        with open("filtered_data.txt", "r") as file:
            content = file.read()
            self.output_label.text = content

    def on_insert(self, instance):
        connection = self.connect_to_database()
        if connection:
            file_path = "filtered_data.txt"
            with open(file_path, "r") as file:
                lines = file.readlines()
                successful_insertions = 0

                for line in lines:
                    data = line.split(") (")
                    mail_id = data[0].strip("()")
                    date_time = data[1].strip("()")
                    hash_data = data[2].strip("()\n")

                    if not self.insert_data(connection, mail_id, date_time, hash_data):
                        what_done = "Error"
                    else:
                        successful_insertions += 1

                if successful_insertions > 0:
                    self.output_label.text = f"Уникальные данные были вставлены в базу данных. Количество успешных вставок: {successful_insertions}"
                else:
                    self.output_label.text = "Ошибка при вставке данных в базу данных. Все данные уже представлены в БД и не могут быть вставлены повторно."

            connection.close()

    def connect_to_database(self):
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

    def insert_data(self, connection, mail_id, date_time, data):
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

    def show_all_tables(self):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                tables = cursor.fetchall()
                connection.close()
                return tables
        except psycopg2.Error as e:
            self.show_error_popup(f"Ошибка при получении списка таблиц: {e}")
        return []

    def show_table(self, table_name):
        try:
            connection = self.connect_to_database()
            if connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]  # Получим имена столбцов

                connection.close()

                content = BoxLayout(orientation='vertical')

                scroll_view = ScrollView()

                table_layout = GridLayout(cols=len(column_names), size_hint_y=None)
                table_layout.bind(minimum_height=table_layout.setter('height'))
                content.add_widget(scroll_view)
                scroll_view.add_widget(table_layout)

                # Добавляем названия столбцов
                for name in column_names:
                    label = Label(text=name, size_hint=(1, None), height=30, bold=True)
                    table_layout.add_widget(label)

                # Добавляем данные из таблицы
                for row in rows:
                    for value in row:
                        label = Label(text=str(value), size_hint=(1, None), height=30)
                        table_layout.add_widget(label)

                popup = Popup(title=f"Таблица {table_name}", content=content, size_hint=(0.8, 0.8))
                popup.open()
        except psycopg2.Error as e:
            self.show_error_popup(f"Ошибка при отображении таблицы: {e}")

    def show_error_popup(self, message):
        popup = Popup(title="Ошибка", content=Label(text=message), size_hint=(0.4, 0.4))
        popup.open()

if __name__ == "__main__":
    EmailExtractor().run()