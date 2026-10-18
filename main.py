import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class Logging(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Вход')
        self.resize(600, 600)
        self.button_go_to_registration = QPushButton('Регистрация', self)
        self.button_go_to_registration.move(50, 50)
        self.button_go_to_registration.clicked.connect(self.on_button_go_to_reg_click)

    def on_button_go_to_reg_click(self):
        log.hide()
        global reg
        reg = Registration()
        reg.show()


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 1. Настройка главного окна
        self.setWindowTitle('Регистрация')
        self.resize(600, 600)

        self.label_registration = QLabel('Регистрация', self)
        self.label_registration.setAlignment(Qt.AlignCenter)
        self.label_registration.setStyleSheet('font-size: 14px;font-weight: bold;')

        self.label_name = QLabel('Введите ваше имя:', self)
        self.label_name.setAlignment(Qt.AlignCenter)

        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText('Например, Александр')
        self.input_name.setStyleSheet('padding: 5px; font-size: 14px;')

        self.label_password = QLabel('Введите ваш пароль:', self)
        self.label_password.setAlignment(Qt.AlignCenter)

        self.input_password = QLineEdit(self)
        self.input_password.setPlaceholderText('Например, Qwert123')
        self.input_password.setStyleSheet('padding: 5px; font-size: 14px;')

        self.button_registration = QPushButton('Подтвердить!', self)
        self.button_registration.setStyleSheet(
            'background-color: #4CAF50; color: white; font-weight: bold;')

        self.button_go_to_logging = QPushButton('Войти', self)
        self.button_registration.setStyleSheet(
            'background-color: #4CAF50; color: white; font-weight: bold;')

        self.label_result = QLabel('', self)
        self.label_result.setAlignment(Qt.AlignCenter)
        self.label_result.setStyleSheet('font-size: 16px; color: blue;')

        self.button_registration.clicked.connect(self.on_button_registration_click)
        self.button_go_to_logging.clicked.connect(self.on_button_logging_click)

        self.input_name.returnPressed.connect(self.on_button_registration_click)
        self.input_password.returnPressed.connect(self.on_button_registration_click)

        self.label_registration.move(50, 50)
        self.label_name.move(50, 100)
        self.input_name.move(50, 150)
        self.label_password.move(50, 250)
        self.input_password.move(50, 300)
        self.button_registration.move(50, 400)
        self.label_result.move(50, 250)
        self.button_go_to_logging.move(50, 450)

    def on_button_registration_click(self):
        user_name = self.input_name.text()
        user_password = self.input_password.text()

        if user_name.strip() and user_password.strip():
            self.label_result.setText(f'Привет, {user_name}! 👋')
            self.input_name.clear()
            self.input_password.clear()
            self.label_result.resize(300, 50)
            self.input_name.setFocus()
        elif not user_name.strip() and not user_password.strip():
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите имя и пароль!')
            self.input_name.setFocus()
        elif not user_name.strip():
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите имя!')
            self.input_name.setFocus()
        elif not user_password.strip():
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите пароль!')
            self.input_password.setFocus()

    def on_button_logging_click(self):
        reg.hide()
        global log
        log = Logging()
        log.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    reg = Registration()
    reg.show()
    sys.exit(app.exec_())
