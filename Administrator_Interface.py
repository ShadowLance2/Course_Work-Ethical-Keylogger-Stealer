from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
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
    except psycopg2.Error as e:
        show_error_popup(f"Ошибка при подключении к базе данных: {e}")
        return None


def show_all_tables():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            connection.close()
            return tables
    except psycopg2.Error as e:
        show_error_popup(f"Ошибка при получении списка таблиц: {e}")
    return []


def show_table(table_name):
    try:
        connection = connect_to_database()
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
        show_error_popup(f"Ошибка при отображении таблицы: {e}")


def show_error_popup(message):
    popup = Popup(title="Ошибка", content=Label(text=message), size_hint=(0.4, 0.4))
    popup.open()


class MainApp(App):
    def build(self):
        tables = show_all_tables()
        layout = BoxLayout(orientation='vertical')

        if tables:
            for table in tables:
                table_name = table[0]
                button = Button(text=f"Показать {table_name}")
                button.bind(on_release=lambda btn, t=table_name: show_table(t))
                layout.add_widget(button)
        else:
            label = Label(text="Нет доступных таблиц")
            layout.add_widget(label)

        return layout


if __name__ == "__main__":
    MainApp().run()