from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
                             QLineEdit, QListWidget)
import mysql.connector as connector

def get_connection():
    try:
        connection = connector.connect(
            host='127.0.0.1',
            user='root',
            password='Zevsasdf05',
            database='contacts_db'
        )
    except connector.Error as s:
        print("Error")
        print(s)

def add_contact(name, phone_number, email):
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        query = "INSERT INTO contacts (name, phone_number, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, phone_number, email))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        print("Ulanish amalga oshmadi")


def get_contacts():
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacts")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    return []

def delete_contact(contact_id):
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        query = "DELETE FROM contacts WHERE id = %s"
        cursor.execute(query, (contact_id,))
        connection.commit()
        cursor.close()
        connection.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kontaktlar Ro'yxati")

        self.name_label = QLabel("Ism")
        self.name_input = QLineEdit()
        self.phone_label = QLabel("Telefon raqami")
        self.phone_input = QLineEdit()
        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()

        self.name_input.setObjectName("nameInput")
        self.phone_input.setObjectName("phoneInput")
        self.email_input.setObjectName("emailInput")
        self.add_button = QPushButton("Kontakt qo'shish")
        self.add_button.setObjectName("addButton")

        self.contact_list = QListWidget()
        self.contact_list.setObjectName("contactList")

        self.delete_button = QPushButton("Kontaktni o'chirish")
        self.delete_button.setObjectName("deleteButton")

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.contact_list)
        layout.addWidget(self.delete_button)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton#addButton {
                background-color: #2196F3;
            }
            QPushButton#deleteButton {
                background-color: #f44336;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.setLayout(layout)

    def add_contact_to_db(self):
        name = self.name_input.text()
        phone_number = self.phone_input.text()
        email = self.email_input.text()

        add_contact(name, phone_number, email)

        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

        self.update_contact_list()

    def update_contact_list(self):
        self.contact_list.clear()
        contacts = get_contacts()
        for contact in contacts:
            self.contact_list.addItem(f"{contact[0]}: {contact[1]} - {contact[2]} - {contact[3]}")

    def delete_selected_contact(self):
        selected_item = self.contact_list.currentItem()
        if selected_item:
            contact_id = int(selected_item.text().split(":")[0])
            delete_contact(contact_id)
            self.update_contact_list()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
