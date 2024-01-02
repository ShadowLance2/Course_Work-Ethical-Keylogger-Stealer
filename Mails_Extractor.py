from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from bs4 import BeautifulSoup
import imaplib
import email


class Email_Extractor(App):

    # Метод создания интерфейса приложения
    def build(self):
        self.username_input = TextInput(hint_text='Адрес электронной почты')
        self.password_input = TextInput(hint_text='Пароль', password=True)
        self.submit_button = Button(text='Ввод')
        self.submit_button.bind(on_press=self.on_submit)
        self.output_label = Label(text='')

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.submit_button)
        layout.add_widget(self.output_label)

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

    # Извлечение текста из электронного письма
    def extract_text_from_email(self, msg):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
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

    # Обработка нажатия кнопки ввода
    def on_submit(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        identifier = "EHP"

        emails = self.get_all_emails(username, password, identifier)
        self.save_emails(emails)

        with open("all_emails_mail_ru.txt", "r") as file:
            content = file.read()
            self.extract_data(content)

        with open("filtered_data.txt", "r") as file:
            content = file.read()
            self.output_label.text = content


if __name__ == "__main__":
    Email_Extractor().run()
