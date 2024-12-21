import sys
import os
import json
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QStackedWidget, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Participant Management App")
        self.resize(400, 400)

        # Apply stylesheet
        self.setStyleSheet(self.get_stylesheet())

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Stacked widget to switch between frames
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Initialize frames
        self.init_sign_in_frame()
        self.init_sign_up_frame()

        # Set initial frame
        self.stack.setCurrentWidget(self.sign_in_frame)

    def init_sign_in_frame(self):
        """Design the Sign-In Frame"""
        self.sign_in_frame = QWidget()
        layout = QFormLayout()

        # Username and password fields
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.username_input.setPlaceholderText("Enter your username")
        self.password_input.setPlaceholderText("Enter your password")

        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)

        # Sign-In button
        sign_in_button = QPushButton("Sign In")
        layout.addWidget(sign_in_button)

        # Signal to connect to your validation logic
        # TODO: Add implementation to verify login details
        sign_in_button.clicked.connect(self.handle_sign_in)

        self.sign_in_frame.setLayout(layout)
        self.stack.addWidget(self.sign_in_frame)

    def init_sign_up_frame(self):
        """Design the Sign-Up Frame"""
        self.sign_up_frame = QWidget()
        layout = QFormLayout()

        # Input fields for participant details
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.id_input = QLineEdit()
        self.cellphone_input = QLineEdit()
        self.tel_input = QLineEdit()
        self.address_input = QTextEdit()
        self.skills_input = QTextEdit()

        self.name_input.setPlaceholderText("Enter name")
        self.surname_input.setPlaceholderText("Enter surname")
        self.id_input.setPlaceholderText("Enter ID number")
        self.cellphone_input.setPlaceholderText("Enter cellphone number")
        self.tel_input.setPlaceholderText("Enter telephone number")
        self.address_input.setPlaceholderText("Enter address")
        self.skills_input.setPlaceholderText("Enter skills")

        layout.addRow("Name:", self.name_input)
        layout.addRow("Surname:", self.surname_input)
        layout.addRow("ID Number:", self.id_input)
        layout.addRow("Cellphone Number:", self.cellphone_input)
        layout.addRow("Telephone Number:", self.tel_input)
        layout.addRow("Address:", self.address_input)
        layout.addRow("Skills:", self.skills_input)

        # Submit button to save participant details
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)

        # Signal to connect to the save logic
        # TODO: Add implementation to store data in secondary storage
        submit_button.clicked.connect(self.save_participant_data)

        self.sign_up_frame.setLayout(layout)
        self.stack.addWidget(self.sign_up_frame)

    def handle_sign_in(self):
        """Handle Sign-In Logic"""
        # TODO: Validate username and password
        # If valid, switch to the Sign-Up frame

        try:
            username = self.username_input.text()
            password = self.password_input.text()
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, 'login.json')

            with open(file_path, 'r') as file:
                data = json.load(file)
                users = data.get('users', [])

                if not username or not password:
                    self.show_message('Login error', 'Missing details.')
                else:
                    for user in users:
                        if user['username'] == username and user['password'] == password:
                            self.stack.setCurrentWidget(self.sign_up_frame)
                            return    
                    self.show_message('Login error', 'Invalid Login details.')

        except Exception as error:
          print(error)
          self.show_message('Login error', 'Unable to connect to secondary storage.')

    def save_participant_data(self):
        """Save Participant Data"""
        # TODO: Collect data from inputs and store it in a file or database
        try:
            name = self.name_input.text()
            surname = self.surname_input.text()
            id_number = self.id_input.text()
            cell_phone = self.cellphone_input.text()
            telephone = self.tel_input.text()
            address = self.address_input.toPlainText()
            skills = self.skills_input.toPlainText()

            if not name or not surname or not id_number or not cell_phone or not telephone or not address or not skills:
                self.show_message('Unable to proceed', 'Missing details.')
            else:
                if len(id_number) != 13:
                    self.show_message('Unable to proceed', 'Invalid SA ID Number.\nMust be 13 digits.')
                else:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_dir, 'participant.json')

                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        users = data.get('participants', [])

                        new_user = {
                            "name": name,
                            "surname": surname,
                            "id number": id_number,
                            "cellphone number": cell_phone,
                            "telephone number": telephone,
                            "address": address,
                            "skills": skills,
                            "username": self.generate_username()
                        }
                        data['participants'].append(new_user)
                        
                        with open(file_path, 'w') as file:
                            json.dump(data, file, indent=4)

                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_dir, 'login.json')

                    with open(file_path, 'r') as lfile:
                        data = json.load(lfile)
                        users = data.get('users', [])

                        new_user = {
                            "username": self.generate_username(),
                            "password": self.generate_password()
                        }
                        data['users'].append(new_user)
                        
                        with open(file_path, 'w') as file:
                            json.dump(data, file, indent=4)

                        self.show_message('Success', 'Participant data saved successfully.')

        except Exception as error:
            print(error)
            self.show_message('Unable to proceed', 'Unable to connect to secondary storage.')

    def generate_username(self):
        surname = self.surname_input.text()
        surname = surname.upper()

        id_number = self.id_input.text()

        code = 0
        special = id_number[:3]
        random_number = random.randint(100, 999)

        special = int(special)  # Convert to integer
        special = (special * random_number) % 1000000

        if id_number[0] == '0':
            code = 0
        else:
            code = 1

        username = surname[0:3] + str(special) + '-SKYE' + str(code)
        return str(username)

    def generate_password(self):
        surname = self.surname_input.text()
        id_number = self.id_input.text()

        random_number = random.randint(1, 50)
        special = id_number[:3]  # Extract first 3 digits
        special = int(special)
        special = (special * random_number) % 1000000
        
        password = surname[0:3].lower() + str(special) + id_number[6:8]
        return str(password)

    def show_message(self, title, message):
        """Display a message dialog"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information if title == "Success" else QMessageBox.Critical)
        msg.exec_()

    def get_stylesheet(self):
        """Returns a stylesheet for styling the application.""" 
        return """
        QWidget {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }

        QLineEdit, QTextEdit {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 8px;
        }

        QPushButton {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
        }

        QPushButton:hover {
            background-color: #0056b3;
        }

        QFormLayout QLabel {
            font-weight: bold;
        }

        QTextEdit {
            min-height: 60px;
        }

        QStackedWidget {
            margin: 10px;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())
