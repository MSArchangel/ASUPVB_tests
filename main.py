import sys, sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox,
                             QMainWindow, QStackedWidget, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

user_id, results = [None], [None]
GLOBAL_STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #F4F7F6;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        color: #2D3436;
    }

    QLabel#title {
        font-size: 26px;
        font-weight: 600;
        color: #2D3436;
        margin-bottom: 10px;
    }

    QLabel#subtitle {
        font-size: 14px;
        color: #636E72;
        margin-bottom: 20px;
    }

    QLineEdit {
        background-color: #FFFFFF;
        border: 1px solid #DFE6E9;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        color: #2D3436;
        selection-background-color: #74B9FF;
    }
    QLineEdit:focus {
        border: 1px solid #0984E3;
    }
    QLineEdit::placeholder {
        color: #B2BEC3;
    }

    QPushButton#primary_btn {
        background-color: #CC5500;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#primary_btn:hover {
        background-color: green;
    }
    QPushButton#primary_btn:pressed {
        background-color: #0662A6;
    }
    
    QPushButton#secondary_btn {
        background-color: transparent;
        color: #0984E3;
        border: none;
        font-size: 13px;
        font-weight: 500;
    }
    QPushButton#secondary_btn:hover {
        color: #0874C3;
        text-decoration: underline;
    }

    QLabel#result_text {
        font-size: 15px;
        color: #00B894;
        font-weight: 500;
        margin-top: 10px;
    }
"""


class LoginWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(15)

        title = QLabel("С возвращением!")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Войдите в свой аккаунт")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("Введите имя пользователя")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.setObjectName("primary_btn")
        self.btn_login.setCursor(Qt.PointingHandCursor)

        self.btn_to_reg = QPushButton("Нет аккаунта? Зарегистрироваться")
        self.btn_to_reg.setObjectName("secondary_btn")
        self.btn_to_reg.setCursor(Qt.PointingHandCursor)

        self.label_result = QLabel("")
        self.label_result.setObjectName("result_text")
        self.label_result.setAlignment(Qt.AlignCenter)
        self.label_result.hide()

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.input_login)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.label_result)
        layout.addStretch()
        layout.addWidget(self.btn_to_reg, alignment=Qt.AlignCenter)

        self.btn_login.clicked.connect(self.check_login)
        self.btn_to_reg.clicked.connect(lambda: self.switch_callback(1))
        self.input_login.returnPressed.connect(self.check_login)
        self.input_password.returnPressed.connect(self.check_login)

    def check_login(self):
        login_from_edit = self.input_login.text().strip()
        password_from_edit = self.input_password.text().strip()
        fl = 0

        db_path = 'database_logins.db'
        connection = sqlite3.connect(db_path)

        cursor = connection.cursor()
        arr = cursor.execute("SELECT id, login, password FROM loggins").fetchall()
        if login_from_edit and password_from_edit:
            for id, login, password in arr:
                if login == login_from_edit and password == password_from_edit:
                    user_id[0] = id
                    QMessageBox.information(self, "Подтверждение успешного входа",
                                            "Вы успешно вошли в свою учётную запись!\nС возвращением!")
                    self.switch_callback(2)
                    fl = 1
            else:
                if fl == 0:
                    QMessageBox.warning(self, 'Ошибка входа',
                                        'Пожалуйста, проверьте правильность ввода данных, данные в БД отсутствуют!')
        else:
            QMessageBox.warning(self, 'Ошибка входа', 'Пожалуйста, заполните все поля!')
            if not login_from_edit:
                self.input_login.setFocus()
            elif not password_from_edit:
                self.input_password.setFocus()


class RegistrationWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(15)

        title = QLabel("Создать аккаунт")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Пожалуйста, заполните данные для регистрации:")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Введите ваше имя")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Придумайте надежный пароль")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_register.setObjectName("primary_btn")
        self.btn_register.setCursor(Qt.PointingHandCursor)

        self.btn_to_login = QPushButton("Уже есть аккаунт? Войти")
        self.btn_to_login.setObjectName("secondary_btn")
        self.btn_to_login.setCursor(Qt.PointingHandCursor)

        self.label_result = QLabel("")
        self.label_result.setObjectName("result_text")
        self.label_result.setAlignment(Qt.AlignCenter)
        self.label_result.hide()

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.input_name)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.label_result)
        layout.addStretch()
        layout.addWidget(self.btn_to_login, alignment=Qt.AlignCenter)

        self.btn_register.clicked.connect(self.check_registration)
        self.btn_to_login.clicked.connect(lambda: self.switch_callback(0))
        self.input_name.returnPressed.connect(self.check_registration)
        self.input_password.returnPressed.connect(self.check_registration)

    def check_registration(self):
        name_from_edit = self.input_name.text().strip()
        password_from_edit = self.input_password.text().strip()

        db_path = 'database_logins.db'
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if (name_from_edit and password_from_edit) and len(password_from_edit) >= 6:
            result = QMessageBox.warning(self, "Предупреждение",
                                         "Вы уверены, что хотите создать учётную запись с введенными данными?",
                                         QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                QMessageBox.information(self, "Подтверждение успешной регистрации",
                                        "Ваша учётная запись успешно создана!\nДобро пожаловать!")
                cursor.execute("INSERT INTO loggins (login, password, results) VALUES (?, ?, ?)",
                               (name_from_edit, password_from_edit, ""))
                connection.commit()
                user_id[0] = [x for x in cursor.execute(
                    f'SELECT id FROM loggins WHERE login = "{name_from_edit}" AND password = "{password_from_edit}"').fetchall()][
                    0][0]
                self.switch_callback(2)
            else:
                pass
        else:
            QMessageBox.warning(self, 'Ошибка входа', 'Пожалуйста, заполните все поля!')
            if not name_from_edit:
                self.input_name.setFocus()
            elif not password_from_edit:
                self.input_password.setFocus()


class SpisokWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        self.db_path = 'database_logins.db'
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.setWindowTitle('Основное окно')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(15)

        title = QLabel("Главное меню")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.btn_theory = QPushButton("Теория")
        self.btn_theory.setObjectName("primary_btn")
        self.btn_theory.setCursor(Qt.PointingHandCursor)

        self.btn_tests = QPushButton("Тесты")
        self.btn_tests.setObjectName("primary_btn")
        self.btn_tests.setCursor(Qt.PointingHandCursor)

        self.btn_graphik = QPushButton("Графики")
        self.btn_graphik.setObjectName("primary_btn")
        self.btn_graphik.setCursor(Qt.PointingHandCursor)
        self.btn_graphik.clicked.connect(self.on_btn_graphic_click)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.btn_theory)
        layout.addWidget(self.btn_tests)
        layout.addWidget(self.btn_graphik)
        layout.addStretch()

    def on_btn_graphic_click(self):
        global results
        results = [int(a) for a in [x[0] for x in self.cursor.execute(
            f'SELECT results FROM loggins WHERE id = "{user_id[0]}"').fetchall()][0].split()]

        self.switch_callback(3)


class GraphikWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.db_path = 'database_logins.db'
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Графики о прохождении тестов')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(15)
        layout.addStretch()

        self.label = QLabel("Нажмите на кнопку ниже, чтобы посторить график:")

        self.btn_back = QPushButton("Вернуться назад <-")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.on_btn_back_click)

        self.btn_to_create = QPushButton("Построить график!")
        self.btn_to_create.setCursor(Qt.PointingHandCursor)
        self.btn_to_create.clicked.connect(self.on_btn_to_create_click)

        layout.addWidget(self.btn_back)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_to_create)

        layout.addStretch()

    def on_btn_back_click(self):
        self.label.setText("Нажмите на кнопку ниже, чтобы посторить график:")
        self.switch_callback(2)

    def on_btn_to_create_click(self):
        if len(results) >= 2:
            self.label.setText("График ваших результатов")
        else:
            self.label.setText(
                "Пройдите хотя бы два теста, чтобы увидеть график Ваших результатов.\nЖелаем успехов!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(650, 800)
        self.setWindowTitle("Авторизация")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.login_page = LoginWidget(self.switch_page)
        self.reg_page = RegistrationWidget(self.switch_page)
        self.spisok_page = SpisokWidget(self.switch_page)
        self.graphik_page = GraphikWidget(self.switch_page)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.reg_page)
        self.stack.addWidget(self.spisok_page)
        self.stack.addWidget(self.graphik_page)

    def switch_page(self, index):
        if index == 0 or index == 1:
            self.setWindowTitle("Авторизация")
        elif index == 2:
            self.setWindowTitle('Основное окно')
        elif index == 3:
            self.setWindowTitle('Аналитика прохождения')
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(GLOBAL_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
