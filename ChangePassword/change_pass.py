from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QStatusBar, QMenuBar, QAction
import sys, sqlite3, re
########################################################################################################################
class EncodeAndDecode():
    def __init__(self):
        self.DIC = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,
               'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
               'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17,
               's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
               'y': 24, 'z': 25, '0': 26, '1': 27, '2': 28, '3': 29,
               '4': 30, '5': 31, '6': 32, '7': 33, '8': 34, '9': 35}

    def Encode(self, msg, key=3):
        encode_string = ''
        for i in msg:
            if i not in self.DIC:
                encode_string += i
                continue
            ch = self.DIC[i] + key
            if ch > 34:  # букв в алфавите 26 (у нас счет с нуля)
                ch = ch - 36
            encode_string += self.get_key(self.DIC, ch)
        return encode_string

    def Decode(self, msg, key=3):
        decodec_string = ''
        for i in msg:
            if i not in self.DIC:
                decodec_string += i
                continue
            ch = self.DIC[i] - key
            if ch < 0:
                ch = 36 + ch
            decodec_string += self.get_key(self.DIC, ch)
        return decodec_string

    def get_key(self, dic, val):
        for i in dic.items():
            if val in i:
                return i[0]
########################################################################################################################
class AboutProgramm(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "О программе"
        self.top = 200
        self.left = 500
        self.width = 480
        self.height = 100

        self.InitUi()

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        lable = QLabel('Программу написал Тарбаев Владимир!')

        vbox = QVBoxLayout()
        vbox.addWidget(lable)
        self.setLayout(vbox)

        self.setLayout(vbox)
########################################################################################################################
class CreateUser(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Создание нового пользователя"
        self.top = 200
        self.left = 500
        self.width = 480
        self.height = 100

        self.InitUi()

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.btn_add_user = QPushButton('Добавить пользователя в БД')
        self.btn_add_user.setFont(QtGui.QFont("Sanserif", 15))

        self.btn_hide = QPushButton('Закрыть форму')
        self.btn_hide.setFont(QtGui.QFont("Sanserif", 15))

        self.statusBar = QStatusBar()

        self.login_box = QHBoxLayout()
        self.login_lable = QLabel('Логин пользователя: ')
        self.login_line = QLineEdit()
        self.login_box.addWidget(self.login_lable)
        self.login_box.addWidget(self.login_line)

        self.pass_box = QHBoxLayout()
        self.pass_lable = QLabel('Пароль пользователя: ')
        self.pass_line = QLineEdit()
        self.pass_box.addWidget(self.pass_lable)
        self.pass_box.addWidget(self.pass_line)

        self.confirm_pass_box = QHBoxLayout()
        self.confirm_pass_lable = QLabel('Повторите\nпароль пользователя: ')
        self.confirm_pass_line = QLineEdit()
        self.confirm_pass_box.addWidget(self.confirm_pass_lable)
        self.confirm_pass_box.addWidget(self.confirm_pass_line)

        vbox = QVBoxLayout()
        vbox.addLayout(self.login_box)
        vbox.addLayout(self.pass_box)
        vbox.addLayout(self.confirm_pass_box)
        vbox.addWidget(self.btn_add_user)
        vbox.addWidget(self.btn_hide)
        vbox.addWidget(self.statusBar)
        self.setLayout(vbox)

        self.btn_hide.clicked.connect(self.hide)
        self.btn_add_user.clicked.connect(self.add_new_user)

        self.show()

    def get_max_id(self):
        with sqlite3.connect('lab_1.db') as conn:
            max_id = 0
            curr = conn.cursor()
            curr.execute("SELECT MAX(id) FROM main.users ")
            for i in curr.fetchone():
                max_id = i
            curr.close()
            return max_id + 1

    def add_new_user(self):
        en_dec = EncodeAndDecode()
        login = self.login_line.text()
        password = self.pass_line.text()
        rep_password = self.confirm_pass_line.text()
        id = self.get_max_id()
        is_valid_pass = re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$', password)
        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            if login and password and rep_password:
                if password == rep_password:
                    if is_valid_pass:
                        curr.execute("INSERT INTO main.users (id, name, password, is_block) VALUES ({} ,'{}', '{}',0)".format(id ,login, en_dec.Encode(password)))
                        self.statusBar.showMessage('Пользователь был создан!', 3000)
                        conn.commit()
                        curr.close()
                    else:
                        self.statusBar.showMessage('Пароль не подходит по маске!', 3000)
                else:
                    self.statusBar.showMessage('Не совпадают пароли!', 3000)
            else:
                self.statusBar.showMessage('Сначала заполните все поля!', 3000)
########################################################################################################################
class AdminArea(QDialog):
    def __init__(self, user_login, user_pass):
        super().__init__()

        self.title = "Личный кабинет пользователя - {}".format(user_login)
        self.top = 200
        self.left = 500
        self.width = 480
        self.height = 100

        self.data_from_db = []
        self.position = -1

        self.login = user_login
        self.user_password = user_pass

        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            curr.execute("SELECT id FROM main.users WHERE name='{}'".format(self.login))
            data = curr.fetchone()
            id = data[0]

        self.login_box_admin = QHBoxLayout()
        lable1 = QLabel('Логин: ')
        lable2 = QLabel(user_login)
        self.login_box_admin.addWidget(lable1)
        self.login_box_admin.addWidget(lable2)

        self.id_box_admin = QHBoxLayout()
        lable3 = QLabel('ID: ')
        lable4 = QLabel(str(id))
        self.id_box_admin.addWidget(lable3)
        self.id_box_admin.addWidget(lable4)

        self.InitUi()

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.save_user_data = QPushButton('Сохранить изменения в базе')
        self.save_user_data.setFont(QtGui.QFont("Sanserif", 15))

        self.next_user_data = QPushButton('Следущая записть')
        self.next_user_data.setFont(QtGui.QFont("Sanserif", 15))

        self.prev_user_data = QPushButton('Предидущая запись')
        self.prev_user_data.setFont(QtGui.QFont("Sanserif", 15))

        self.btn_exit = QPushButton('Завершить работу')
        self.btn_exit.setFont(QtGui.QFont("Sanserif", 15))

        self.btn_enter_to_main_window = QPushButton('Вернуться в главное меню')
        self.btn_enter_to_main_window.setFont(QtGui.QFont("Sanserif", 15))

        self.btn_open_form_add_user = QPushButton("Создать нового пользователя")
        self.btn_open_form_add_user.setFont(QtGui.QFont("Sanserif", 15))

        main_menu = QMenuBar()
        file_menu = main_menu.addMenu('File')
        help_menu = main_menu.addMenu('Help')

        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(sys.exit)
        file_menu.addAction(exit_button)

        about_btn = QAction('About', self)
        about_btn.setStatusTip('About programm')
        about_btn.triggered.connect(self.open_from_about_programm)
        help_menu.addAction(about_btn)

        self.login_box = QHBoxLayout()
        self.login_lable = QLabel('Логин пользователя: ')
        self.login_line = QLineEdit()
        self.login_box.addWidget(self.login_lable)
        self.login_box.addWidget(self.login_line)

        self.pass_box = QHBoxLayout()
        self.pass_lable = QLabel('Пароль пользователя: ')
        self.pass_line = QLineEdit()
        self.pass_box.addWidget(self.pass_lable)
        self.pass_box.addWidget(self.pass_line)

        self.is_block_user_box = QHBoxLayout()
        self.is_block_user_lable = QLabel('Заблокирован пользователь: ')
        self.is_block_user_line = QLineEdit()
        self.is_block_user_box.addWidget(self.is_block_user_lable)
        self.is_block_user_box.addWidget(self.is_block_user_line)

        self.btn_prev_next_box = QHBoxLayout()
        self.btn_prev_next_box.addWidget(self.prev_user_data)
        self.btn_prev_next_box.addWidget(self.next_user_data)

        self.statusBar = QStatusBar()

        vbox = QVBoxLayout()
        vbox.addWidget(main_menu)
        vbox.addLayout(self.login_box_admin)
        vbox.addLayout(self.id_box_admin)
        vbox.addLayout(self.login_box)
        vbox.addLayout(self.pass_box)
        vbox.addLayout(self.is_block_user_box)
        vbox.addLayout(self.btn_prev_next_box)
        vbox.addWidget(self.save_user_data)
        vbox.addWidget(self.btn_open_form_add_user)
        vbox.addWidget(self.btn_enter_to_main_window)
        vbox.addWidget(self.btn_exit)
        vbox.addWidget(self.statusBar)
        self.setLayout(vbox)

        self.btn_enter_to_main_window.clicked.connect(self.enter_ro_main_window)
        self.save_user_data.clicked.connect(self.change_user_data)
        self.next_user_data.clicked.connect(self.get_next_user_data)
        self.prev_user_data.clicked.connect(self.get_privius_user_data)
        self.btn_exit.clicked.connect(sys.exit)
        self.btn_open_form_add_user.clicked.connect(self.open_from_add_user)

        self.get_next_user_data()
        self.show()

    def open_from_about_programm(self):
        dialog = AboutProgramm()
        dialog.exec()

    def open_from_add_user(self):
        dialog = CreateUser()
        dialog.setModal(False)
        dialog.exec()

    def get_privius_user_data(self):
        en_dec = EncodeAndDecode()
        if self.position == 0:
            self.position = len(self.data_from_db)
        self.position = self.position - 1
        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            curr.execute("SELECT id, name, password, is_block FROM main.users")
            self.data_from_db = curr.fetchall()
            self.login_line.setText(self.data_from_db[self.position][1])
            self.pass_line.setText(en_dec.Decode(self.data_from_db[self.position][2]))
            self.is_block_user_line.setText(str(self.data_from_db[self.position][3]))
        print(self.position)

    def get_next_user_data(self):
        en_dec = EncodeAndDecode()
        self.position = self.position + 1
        if self.position == len(self.data_from_db):
            self.position = 0
        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            curr.execute("SELECT id, name, password, is_block FROM main.users")
            self.data_from_db = curr.fetchall()
            self.login_line.setText(self.data_from_db[self.position][1])
            self.pass_line.setText(en_dec.Decode(self.data_from_db[self.position][2]))
            self.is_block_user_line.setText(str(self.data_from_db[self.position][3]))
        print(self.position)

    def change_user_data(self):
        en_dec = EncodeAndDecode()
        login = self.login_line.text()
        password = self.pass_line.text()
        is_block = self.is_block_user_line.text()
        id = self.get_id(login)
        print(id, login, password, is_block)
        is_valid_pass = re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$', password)
        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            if login and password and is_block:
                if is_valid_pass:
                    curr.execute("UPDATE main.users SET name='{}', password='{}', is_block={} WHERE id={}".format(login, en_dec.Encode(password), is_block, id))
                    self.statusBar.showMessage('Данные пользователя были успешно изменены!', 3000)
                    conn.commit()
                    curr.close()
                else:
                    self.statusBar.showMessage('Пароль не подходит по маске!', 3000)
            else:
                self.statusBar.showMessage('Сначала заполните все поля!', 3000)

    def get_id(self, login):
        with sqlite3.connect('lab_1.db') as conn:
            id = 0
            curr = conn.cursor()
            curr.execute("SELECT id FROM main.users WHERE name='{}'".format(login))
            for i in curr.fetchone():
                id = i
            curr.close()
            return id

    def enter_ro_main_window(self):
        mydialog = MainWindow()
        self.hide()
        mydialog.exec()
########################################################################################################################
class UserWindow(QDialog):
    def __init__(self, user_login, user_pass):
        super().__init__()

        self.title = "Личный кабинет пользователя - {}".format(user_login)
        self.top = 200
        self.left = 500
        self.width = 480
        self.height = 100

        self.login = user_login
        self.user_password = user_pass

        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            curr.execute("SELECT id FROM main.users WHERE name='{}'".format(self.login))
            data = curr.fetchone()
            id = data[0]

        self.login_box = QHBoxLayout()
        lable1 = QLabel('Логин: ')
        lable2 = QLabel(user_login)
        self.login_box.addWidget(lable1)
        self.login_box.addWidget(lable2)

        self.id_box = QHBoxLayout()
        lable3 = QLabel('ID: ')
        lable4 = QLabel(str(id))
        self.id_box.addWidget(lable3)
        self.id_box.addWidget(lable4)

        self.InitUI()

    def InitUI(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        enter_to_main_window = QPushButton('Выйти в главное меню')
        enter_to_main_window.setFont(QtGui.QFont("Sanserif", 15))

        change_pass_btn = QPushButton('Сменить пароль')
        change_pass_btn.setFont(QtGui.QFont("Sanserif", 15))

        self.exit_btn = QPushButton('Завершить работу')
        self.exit_btn.setFont(QtGui.QFont("Sanserif", 15))

        main_menu = QMenuBar()
        file_menu = main_menu.addMenu('File')
        help_menu = main_menu.addMenu('Help')

        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(sys.exit)
        file_menu.addAction(exit_button)

        about_btn = QAction('About', self)
        about_btn.setStatusTip('About programm')
        about_btn.triggered.connect(self.open_from_about_programm)
        help_menu.addAction(about_btn)

        old_pass_box = QHBoxLayout()
        old_pass_lable = QLabel('Старый пароль: ')
        self.old_pass_line = QLineEdit()
        old_pass_box.addWidget(old_pass_lable)
        old_pass_box.addWidget(self.old_pass_line)

        new_pass_box = QHBoxLayout()
        new_pass_lable = QLabel('Новый пароль: ')
        self.new_pass_line = QLineEdit()
        new_pass_box.addWidget(new_pass_lable)
        new_pass_box.addWidget(self.new_pass_line)

        repete_new_pass_box = QHBoxLayout()
        repete_new_pass_lable = QLabel('Повторите новый пароль: ')
        self.repete_new_pass_line = QLineEdit()
        repete_new_pass_box.addWidget(repete_new_pass_lable)
        repete_new_pass_box.addWidget(self.repete_new_pass_line)

        self.statusBar = QStatusBar()
        self.statusBar.showMessage('Вы вошли в личный кабинет, тут вы можете сменить пароль')

        vbox = QVBoxLayout()
        vbox.addWidget(main_menu)
        vbox.addLayout(self.login_box)
        vbox.addLayout(self.id_box)
        vbox.addLayout(old_pass_box)
        vbox.addLayout(new_pass_box)
        vbox.addLayout(repete_new_pass_box)
        vbox.addWidget(change_pass_btn)
        vbox.addWidget(enter_to_main_window)
        vbox.addWidget(self.exit_btn)
        vbox.addWidget(self.statusBar)
        self.setLayout(vbox)

        self.exit_btn.clicked.connect(sys.exit)
        change_pass_btn.clicked.connect(self.change_user_pass)
        enter_to_main_window.clicked.connect(self.enter_ro_main_window)
        self.show()

    def open_from_about_programm(self):
        dialog = AboutProgramm()
        dialog.exec()

    def enter_ro_main_window(self):
        mydialog = MainWindow()
        self.hide()
        mydialog.exec()

    def change_user_pass(self):
        en_dec = EncodeAndDecode()
        old_password_from_line = self.old_pass_line.text()
        new_password_from_line = self.new_pass_line.text()
        repete_new_password_from_line = self.repete_new_pass_line.text()
        is_valid_pass = re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$', new_password_from_line)
        with sqlite3.connect('lab_1.db') as conn:
            curr = conn.cursor()
            curr.execute("SELECT password FROM main.users WHERE name='{}'".format(self.login))
            data = curr.fetchone()
            password_from_db = en_dec.Decode(data[0])
            if old_password_from_line == password_from_db:
                if new_password_from_line == repete_new_password_from_line:
                    if is_valid_pass:
                        curr.execute("UPDATE main.users SET password='{}' WHERE name='{}'".format(en_dec.Encode(new_password_from_line), self.login))
                        self.statusBar.showMessage('Пароль успешно сменен!', 2000)
                    else:
                        self.statusBar.showMessage('Пароль не подходит по маске!', 2000)
                else:
                    self.statusBar.showMessage('Новые пароли не совпадают!', 2000)
            else:
                self.statusBar.showMessage('Старый пароль введен не верно!', 2000)
########################################################################################################################
class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "Главное меню"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 100

        self.attempt = 0

        self.InitUI()

    def InitUI(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Line edit (Login)
        login_box = QHBoxLayout()
        self.login_label = QLabel("Логин : ")
        self.line_login = QLineEdit()
        login_box.addWidget(self.login_label)
        login_box.addWidget(self.line_login)

        # Line edit (Password)
        pass_box = QHBoxLayout()
        self.pass_lable = QLabel("Пароль : ")
        self.line_pass = QLineEdit()
        self.line_pass.setEchoMode(QLineEdit.Password)
        pass_box.addWidget(self.pass_lable)
        pass_box.addWidget(self.line_pass)

        # Button (Sing in)
        self.btn_connect = QPushButton("Войти")
        self.btn_connect.setFont(QtGui.QFont("Sanserif", 13))

        # Button (exit)
        self.btn_exit = QPushButton("Заверщшить работу программы")
        self.btn_exit.setFont(QtGui.QFont("Sanserif", 13))

        # Status bar
        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Добро пожаловать!", 5000)

        # Slots - Signals
        self.btn_exit.clicked.connect(sys.exit)
        self.btn_connect.clicked.connect(self.getUserData)

        # Layout
        vbox = QVBoxLayout()
        vbox.addLayout(login_box)
        vbox.addLayout(pass_box)
        vbox.addWidget(self.btn_connect)
        vbox.addWidget(self.btn_exit)
        vbox.addWidget(self.statusBar)

        self.setLayout(vbox)

        self.show()

    def getUserData(self):
        en_dec = EncodeAndDecode()
        if self.attempt == 3:
            sys.exit()
        login = self.line_login.text()
        password = self.line_pass.text()
        with sqlite3.connect("lab_1.db") as conn:
            curr = conn.cursor()
            curr.execute("SELECT name, password, is_block FROM main.USERS WHERE name='{}' and password='{}'".format(login, en_dec.Encode(password)))
            data = curr.fetchone()
            print(data)
            if data:
                if login == data[0]:
                    if data[0] == 'admin':
                        self.open_admin_area(login, password)
                    elif True == data[2]:
                        self.statusBar.showMessage("Ваш пользователь заблокирован!", 3000)
                    else:
                        self.openSecondWindow(login, password)
                        self.attempt = 0
            else:
                self.statusBar.showMessage('Вы ввели неправельный логин или пароль!', 3000)
                self.attempt = self.attempt + 1

    def open_admin_area(self, login, password):
        mydialog = AdminArea(login, password)
        self.hide()
        mydialog.exec()

    def openSecondWindow(self, login, password):
        mydialog = UserWindow(login, password)
        self.hide()
        mydialog.exec()
########################################################################################################################
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec())