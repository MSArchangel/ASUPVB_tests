import sys, sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox,
                             QMainWindow, QStackedWidget, QSpacerItem, QSizePolicy, QFrame,
                             QGraphicsDropShadowEffect, QScrollArea, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor
from graph_test import get_results
from CHS_for_theory import EMERGENCY_DATA
from test_question import build_questions

user_id, results, IMAGES, SCHETCHIK_FOR_IMAGES = [None], [None], EMERGENCY_DATA, [0]
GLOBAL_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #F4F7F6;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    color: #2D3436;
}

QFrame#card {
    background-color: #FFFFFF;
    border: 1px solid #E3EAEF;
    border-radius: 20px;
}

QLabel#title {
    font-size: 28px;
    font-weight: 700;
    color: #1E2A38;
    margin-bottom: 5px;
    background-color: #FFFFFF;
}

QLabel#logo {
    font-size: 64px;
    background: transparent;
    margin-bottom: 6px;
}
QLabel#subtitle {
    font-size: 16px;
    color: #7B8A97;
    font-style: italic;
    margin-bottom: 22px;
    background-color: #FFFFFF
}
QLineEdit::placeholder {
    color: #B2BEC3;
    font-style: italic;
}
QLabel#hint_text {
    font-size: 12px;
    color: #90A4AE;
    margin-top: -8px;
}
QLabel#error_text {
    font-size: 13px;
    color: #D63031;
    font-weight: 600;
    background-color: #FDECEA;
    border: 1px solid #F5C6C0;
    border-radius: 8px;
    padding: 8px 12px;
}
QLabel#footer_text {
    font-size: 12px;
    color: #B2BEC3;
    margin-top: 10px;
}

QLabel#theory_text {
    font-size: 15px;
    color: #3D4C59;
    background-color: #F8FAFB;
    border: 1px solid #E3EAEF;
    border-left: 4px solid #FF8A3D;
    border-radius: 10px;
    padding: 18px 22px;
}

QLabel#info_text {
    font-size: 16px;
    color: #636E72;
    background: transparent;
}

QLabel#image_label{
    background-color: #FFFFFF;
}

QMessageBox {
    background-color: #FFFFFF;
}
QMessageBox QLabel {
    font-size: 15px;
    color: #2D3436;
}
QMessageBox QPushButton {
    background-color: #F1F5F8;
    color: #2D3436;
    border: 1px solid #DFE6E9;
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 14px;
    font-weight: 600;
    min-width: 90px;
}
QMessageBox QPushButton:hover {
    background-color: #EAF4FD;
    border-color: #0984E3;
    color: #0984E3;
}

QLabel#result_text {
    font-size: 15px;
    color: #00B894;
    font-weight: 500;
    margin-top: 10px;
}

QLineEdit {
    background-color: #F8FAFB;
    border: 1.5px solid #DFE6E9;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 18px;
    color: #2D3436;
    selection-background-color: #74B9FF;
}
QLineEdit:focus {
    border: 1.5px solid #0984E3;
    background-color: #FFFFFF;
}
QLineEdit::placeholder { color: #B2BEC3; }

QPushButton#primary_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FF8A3D, stop:1 #E06000);
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 13px;
    font-size: 19px;
    font-weight: 600;
}
QPushButton#primary_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FF9C55, stop:1 #F06E00);
}
QPushButton#primary_btn:pressed {
    background: #C25400;
    padding-top: 14px;
    padding-bottom: 12px;
}
QPushButton#primary_btn:disabled {
    background: #CFD8DC;
    color: #90A4AE;
}

QPushButton#nav_btn {
    background-color: #FFFFFF;
    border: 2px solid #DFE6E9;
    border-radius: 15px;
    font-size: 16px;
    font-weight: 700;
    color: #0984E3;
}
QPushButton#nav_btn:hover {
    border-color: #0984E3;
    background-color: #EAF4FD;
}
QPushButton#nav_btn:pressed { background-color: #D4E9FB; }

QPushButton#back_btn {
    background: transparent;
    border: none;
    color: #636E72;
    font-size: 14px;
    font-weight: 500;
    padding: 6px 10px;
}
QPushButton#back_btn:hover { color: #0984E3; }

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

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px 2px 4px 0;
}
QScrollBar::handle:vertical {
    background: #C4D0DA;
    border-radius: 5px;
    min-height: 40px;
}
QScrollBar::handle:vertical:hover { background: #9FB0BE; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QRadioButton {
    spacing: 12px;
    font-size: 16px;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1.5px solid transparent;
    background-color: #F8FAFB;
}
QRadioButton:hover { border-color: #B9D7F2; background-color: #F0F7FD; }
QRadioButton:checked { border-color: #0984E3; background-color: #EAF4FD; }
QRadioButton::indicator {
    width: 18px; height: 18px;
    border-radius: 9px;
    border: 2px solid #B9C6D2;
    background: #FFFFFF;
}
QRadioButton::indicator:checked {
    border-color: #0984E3;
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                stop:0 #0984E3, stop:0.5 #0984E3, stop:0.51 #FFFFFF);
}
QProgressBar {
    background: #E4EBEF;
    border: none;
    border-radius: 7px;
    height: 14px;
    text-align: center;
    font-size: 11px;
    color: #2D3436;
}

QProgressBar::chunk {
    border-radius: 7px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00B894, stop:1 #55EFC4);}

QRadioButton[answerState="correct"] {
    background-color: #E8F8EE;
    border: 1.5px solid #27AE60;
    color: #1E7E34;
    font-weight: 600;
}

QRadioButton[answerState="wrong"] {
    background-color: #FDECEA;
    border: 1.5px solid #D63031;
    color: #B02A1F;
    font-weight: 600;
}

QRadioButton[answerState="correct"]::indicator { border-color: #27AE60; }
QRadioButton[answerState="wrong"]::indicator  { border-color: #D63031; }
QRadioButton:disabled { color: #90A4AE; }
QRadioButton[answerState="correct"]:disabled { color: #1E7E34; }
QRadioButton[answerState="wrong"]:disabled  { color: #B02A1F; }

QLabel#feedback { font-size: 22px; font-weight: 800; background: transparent; }
QLabel#feedback[state="ok"]  { color: #27AE60; }
QLabel#feedback[state="bad"] { color: #D63031; }
"""


class ScaledImageLabel(QLabel):
    def __init__(self, pixmap=None, parent=None):
        super().__init__(parent)
        self._pixmap = pixmap or QPixmap()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(240, 180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._rescale()

    def set_image(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self._rescale()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._rescale()

    def _rescale(self):
        if not self._pixmap.isNull():
            self.setPixmap(self._pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


def build_card(parent: QWidget) -> QVBoxLayout:
    outer = QVBoxLayout(parent)
    outer.setContentsMargins(35, 35, 35, 35)

    card = QFrame(parent)
    card.setObjectName("card")

    shadow = QGraphicsDropShadowEffect(parent)
    shadow.setBlurRadius(35)
    shadow.setColor(QColor(31, 45, 61, 45))
    shadow.setOffset(0, 8)
    card.setGraphicsEffect(shadow)

    inner = QVBoxLayout(card)
    inner.setContentsMargins(60, 60, 60, 60)
    inner.setSpacing(15)

    outer.addWidget(card)
    return inner


def fit_window_to_screen(window, width_ratio=0.55, height_ratio=0.88,
                         min_size=(760, 640), max_size=(1200, 1080)):
    screen = QApplication.primaryScreen().availableGeometry()
    w = max(min_size[0], min(int(screen.width() * width_ratio), max_size[0]))
    h = max(min_size[1], min(int(screen.height() * height_ratio), max_size[1]))
    window.resize(w, h)
    window.move(screen.center() - window.rect().center())


SECTION_COLORS = {
    "⚠": "#E67E22",  # ОПАСНОСТЬ — оранжевый
    "🔎": "#0984E3",  # ПРЕДВЕСТНИКИ — синий
    "🚨": "#D63031",  # ПОРЯДОК ДЕЙСТВИЙ — красный
}


def pretty_theory_html(raw: str) -> str:
    """Превращает сырой текст из EMERGENCY_DATA в аккуратный rich-text."""
    html = ""
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        for emoji, color in SECTION_COLORS.items():
            if s.startswith(emoji):
                html += (f"<p style='font-size:16px; font-weight:700; color:{color}; "
                         f"margin-top:12px; margin-bottom:2px;'>{s}</p>")
                break
        else:
            indent = "margin-left:22px;" if line.startswith(" ") else ""
            html += f"<p style='{indent} margin-top:1px; margin-bottom:1px;'>{s}</p>"
    return html


class LoginWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    def init_ui(self):
        layout = build_card(self)

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
        layout = build_card(self)

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
        layout = build_card(self)

        title = QLabel("Главное меню")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.btn_theory = QPushButton("Теория")
        self.btn_theory.setObjectName("primary_btn")
        self.btn_theory.setCursor(Qt.PointingHandCursor)
        self.btn_theory.clicked.connect(self.on_btn_theory_click)

        self.btn_tests = QPushButton("Тесты")
        self.btn_tests.setObjectName("primary_btn")
        self.btn_tests.setCursor(Qt.PointingHandCursor)
        self.btn_tests.clicked.connect(self.on_btn_tests_click)

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

    def on_btn_theory_click(self):
        self.switch_callback(4)

    def on_btn_tests_click(self):
        self.switch_callback(5)


class TheoryWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()

    @staticmethod
    def current_index() -> int:
        return SCHETCHIK_FOR_IMAGES[0] % len(IMAGES)

    def init_ui(self):
        self.setWindowTitle('Теория')
        layout = build_card(self)

        index = self.current_index()

        self.chs_title = QLabel(IMAGES[index][2])
        self.chs_title.setObjectName("title")
        self.chs_title.setAlignment(Qt.AlignCenter)

        self.label_image = ScaledImageLabel()
        self.label_image.set_image(QPixmap(f"IMAGES/{IMAGES[index][0]}"))
        self.label_image.setObjectName('image_label')

        self.text_label = QLabel(pretty_theory_html(IMAGES[index][1]))
        self.text_label.setObjectName("theory_text")
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignJustify)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.text_label)
        self.scroll.setMinimumHeight(200)

        self.btn_next = QPushButton("->")
        self.btn_next.setObjectName("nav_btn")
        self.btn_next.setCursor(Qt.PointingHandCursor)
        self.btn_next.setFixedSize(60, 30)
        self.btn_next.clicked.connect(self.on_btn_next_click)

        self.btn_back = QPushButton("<-")
        self.btn_back.setObjectName("nav_btn")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setFixedSize(60, 30)
        self.btn_back.clicked.connect(self.on_btn_back_click)

        self.btn_back_to_main_menu = QPushButton("Вернуться назад <-")
        self.btn_back_to_main_menu.setObjectName("back_btn")
        self.btn_back_to_main_menu.setCursor(Qt.PointingHandCursor)
        self.btn_back_to_main_menu.clicked.connect(self.on_btn_back_to_main_menu_click)
        self.btn_back_to_main_menu.setFixedSize(250, 40)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.btn_back)
        h_layout.addWidget(self.btn_next)
        h_layout.addStretch()

        layout.addWidget(self.btn_back_to_main_menu, alignment=Qt.AlignLeft)
        layout.addWidget(self.chs_title)
        layout.addWidget(self.label_image, stretch=4)
        layout.addWidget(self.scroll, stretch=2)
        layout.addLayout(h_layout)

    def on_btn_next_click(self):
        SCHETCHIK_FOR_IMAGES[0] += 1
        self.show_slide()

    def on_btn_back_click(self):
        SCHETCHIK_FOR_IMAGES[0] -= 1
        self.show_slide()

    def show_slide(self):
        index = self.current_index()
        self.chs_title.setText(IMAGES[index][2])
        self.label_image.set_image(QPixmap(f"IMAGES/{IMAGES[index][0]}"))
        self.text_label.setText(pretty_theory_html(IMAGES[index][1]))
        self.scroll.verticalScrollBar().setValue(0)

    def on_btn_back_to_main_menu_click(self):
        self.switch_callback(2)


class TestWidget(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.questions, self.current, self.correct_count = [], 0, 0
        self.answered = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Тестирование')
        layout = build_card(self)

        self.btn_back = QPushButton("Выйти и завершить тест <-")
        self.btn_back.setObjectName("back_btn")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setFixedSize(250, 40)
        self.btn_back.clicked.connect(self.on_btn_back_click)

        self.progress_label = QLabel("")
        self.progress_label.setObjectName("subtitle")
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.question_label = QLabel("")
        self.question_label.setObjectName("title")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)

        self.radio_buttons = []
        self.radio_btn_group = QButtonGroup(self)
        for i in range(1, 5):
            btn = QRadioButton("")
            btn.setCursor(Qt.PointingHandCursor)
            self.radio_btn_group.addButton(btn, i)
            self.radio_buttons.append(btn)
        self.radio_btn_group.idClicked.connect(self.on_radio_selected)

        self.feedback = QLabel("")
        self.feedback.setObjectName("feedback")
        self.feedback.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.btn_back, alignment=Qt.AlignLeft)
        layout.addStretch()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.question_label)
        for btn in self.radio_buttons:
            layout.addWidget(btn)
        layout.addWidget(self.feedback)
        layout.addStretch()

    @staticmethod
    def _refresh_style(widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _set_state(self, widget, state):
        widget.setProperty("answerState", state)
        self._refresh_style(widget)

    def clear_selection(self):
        self.radio_btn_group.setExclusive(False)
        for btn in self.radio_buttons:
            btn.setChecked(False)
            btn.setAutoExclusive(False)
        self.radio_btn_group.setExclusive(True)

    def start_test(self):
        self.questions = build_questions()
        self.current, self.correct_count = 0, 0
        self.show_question()

    def show_question(self):
        self.answered = False
        q = self.questions[self.current]
        self.progress_label.setText(f"Вопрос {self.current + 1} из {len(self.questions)}")
        self.question_label.setText(q["question"])
        self.feedback.setText("")
        self.feedback.setProperty("state", "")
        self._refresh_style(self.feedback)
        self.clear_selection()
        for i, btn in enumerate(self.radio_buttons):
            btn.setText(q["options"][i])
            btn.setChecked(False)
            btn.setEnabled(True)
            self._set_state(btn, "")

    def on_radio_selected(self, button_id):
        if self.answered:
            return
        self.answered = True
        q = self.questions[self.current]
        chosen = self.radio_btn_group.button(button_id)

        for btn in self.radio_buttons:
            btn.setEnabled(False)  # блокируем до следующего вопроса

        if button_id - 1 == q["correct"]:
            self.correct_count += 1
            self._set_state(chosen, "correct")
            self.feedback.setText("ПРАВИЛЬНО!")
            self.feedback.setProperty("state", "ok")
        else:
            self._set_state(chosen, "wrong")
            self._set_state(self.radio_btn_group.button(q["correct"] + 1), "correct")
            self.feedback.setText("НЕПРАВИЛЬНО!")
            self.feedback.setProperty("state", "bad")
        self._refresh_style(self.feedback)

        QTimer.singleShot(3000, self.next_question)

    def next_question(self):
        self.current += 1
        if self.current < len(self.questions):
            self.show_question()
        else:
            self.finish_test()

    def finish_test(self):
        total = len(self.questions)
        self.progress_label.setText("Тест завершён!")
        self.question_label.setText(f"Результат: {self.correct_count} из {total}")
        for btn in self.radio_buttons:
            btn.setText("")
            btn.setEnabled(False)
            btn.hide()
        self.feedback.setText("")
        self.save_result(total)

    def save_result(self, total):
        import datetime
        connection = sqlite3.connect('database_logins.db')
        cursor = connection.cursor()
        row = cursor.execute(
            "SELECT results, dates FROM loggins WHERE id = ?", (user_id[0],)).fetchone()
        results_str = ((row[0] or "").strip() + f" {self.correct_count}").strip()
        dates_str = ((row[1] or "").strip() +
                     f" {datetime.datetime.now():%d.%m}").strip()
        cursor.execute("UPDATE loggins SET results = ?, dates = ? WHERE id = ?",
                       (results_str, dates_str, user_id[0]))
        connection.commit()
        connection.close()

    def on_btn_back_click(self):
        self.switch_callback(2)


class GraphikWidget(QWidget):
    PLACEHOLDER = "Нажмите на кнопку ниже, чтобы построить график:"
    NO_DATA = ("Пройдите хотя бы два теста, чтобы увидеть график "
               "Ваших результатов.\nЖелаем успехов!")

    def __init__(self, switch_callback):
        super().__init__()
        self.db_path = 'database_logins.db'
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.switch_callback = switch_callback
        self._graph_pixmap = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Графики о прохождении тестов')
        layout = build_card(self)

        self.btn_back = QPushButton("Вернуться назад <-")
        self.btn_back.setObjectName("back_btn")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.on_btn_back_click)
        self.btn_back.setFixedSize(250, 40)

        self.label = QLabel(self.PLACEHOLDER)
        self.label.setObjectName("info_text")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMinimumSize(400, 350)
        self.label.setSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)

        self.btn_to_create = QPushButton("Построить график!")
        self.btn_to_create.setObjectName("primary_btn")
        self.btn_to_create.setCursor(Qt.PointingHandCursor)
        self.btn_to_create.clicked.connect(self.on_btn_to_create_click)

        layout.addWidget(self.btn_back, alignment=Qt.AlignLeft)
        layout.addWidget(self.label, stretch=1)
        layout.addWidget(self.btn_to_create)

    def _apply_graph(self):
        if self._graph_pixmap is None or self._graph_pixmap.isNull():
            return
        if self.label.width() <= 0 or self.label.height() <= 0:
            return
        self.label.setPixmap(self._graph_pixmap.scaled(
            self.label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_graph()

    def on_btn_back_click(self):
        self._graph_pixmap = None
        self.label.setText(self.PLACEHOLDER)
        self.switch_callback(2)

    def on_btn_to_create_click(self):
        if len(results) >= 2:
            get_results(user_id[0])
            pixmap = QPixmap("test_results_light.png")
            if pixmap.isNull():
                self.label.setText("Не удалось загрузить изображение графика.")
                return
            self._graph_pixmap = pixmap
            self._apply_graph()
        else:
            self._graph_pixmap = None
            self.label.setText(self.NO_DATA)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        fit_window_to_screen(self)
        self.setMinimumSize(720, 620)

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
        self.theory_page = TheoryWidget(self.switch_page)
        self.test_page = TestWidget(self.switch_page)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.reg_page)
        self.stack.addWidget(self.spisok_page)
        self.stack.addWidget(self.graphik_page)
        self.stack.addWidget(self.theory_page)
        self.stack.addWidget(self.test_page)

    def switch_page(self, index):
        if index == 0 or index == 1:
            self.setWindowTitle("Авторизация")
        elif index == 2:
            self.setWindowTitle('Основное окно')
        elif index == 3:
            self.setWindowTitle('Аналитика прохождения')
        elif index == 4:
            self.setWindowTitle('Теория')
        elif index == 5:
            self.setWindowTitle('Тест')
            self.test_page.start_test()
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(GLOBAL_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

