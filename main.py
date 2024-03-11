import os
import shutil
import sys

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QTextEdit, \
    QVBoxLayout, QWidget, QHBoxLayout


class FileWidget(QWidget):
    def __init__(self, name, path, folder, parent=None):
        super(FileWidget, self).__init__(parent)
        self.path_field = None
        self.win = QWidget()
        self.edit_field = QTextEdit()
        self.name = name
        self.path = path
        self.folder = folder
        self.layout = QHBoxLayout()
        self.label = QTextEdit(self)
        self.setLayout(self.layout)
        self.set_attrs()

    def set_attrs(self):
        image = QImage("./img/file.png")
        img_label = QLabel()
        pixMap = QPixmap.fromImage(image)
        img_label.setPixmap(pixMap)
        self.label.setText(self.name)
        self.label.setMaximumHeight(26)
        btn_del = QPushButton("X")
        btn_del.clicked.connect(self.delete)
        btn_edit = QPushButton("edytuj tekst")
        btn_edit.clicked.connect(self.edit)
        btn_rename = QPushButton("zmien nazwe")
        btn_rename.clicked.connect(self.rename)
        btn_copy = QPushButton("kopiuj do..")
        btn_copy.clicked.connect(self.copy)
        self.layout.addWidget(img_label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(btn_rename)
        self.layout.addWidget(btn_copy)
        if self.name[-3:len(self.name)] == "txt":
            self.layout.addWidget(btn_edit)
        self.layout.addWidget(btn_del)

    def delete(self):
        os.remove(self.path)
        self.deleteLater()

    def edit(self):
        form = QVBoxLayout(self)
        with open(self.path, 'r') as file:
            data = file.read()
        self.edit_field.setText(data)
        self.edit_field.setMinimumWidth(200)
        self.edit_field.setMinimumHeight(100)
        confirm_btn = QPushButton("zapisz")
        confirm_btn.clicked.connect(self.confirm)
        form.addWidget(self.edit_field)
        form.addWidget(confirm_btn)
        self.win.setLayout(form)
        self.win.show()

    def confirm(self):
        f = open(self.path, "w")
        f.write(self.edit_field.toPlainText())
        f.close()
        self.win.close()

    def rename(self):
        os.rename(self.path, self.folder + "/" + self.label.toPlainText())

    def copy(self):
        def copy_to():
            shutil.copy2(self.path, self.path_field.toPlainText())
            new_win.hide()
        new_win = QWidget()
        form = QVBoxLayout(self)
        self.path_field = QTextEdit("wpisz sciezke")
        self.path_field.setMinimumWidth(200)
        self.path_field.setMinimumHeight(100)
        confirm_btn = QPushButton("kopiuj")
        confirm_btn.clicked.connect(copy_to)
        form.addWidget(self.path_field)
        form.addWidget(confirm_btn)
        new_win.setLayout(form)
        new_win.show()


class DirWidget(QWidget):
    def __init__(self, window, name, path, folder, parent=None):
        super(DirWidget, self).__init__(parent)
        self.window = window
        self.win = QWidget()
        self.edit_field = QTextEdit()
        self.name = name
        self.path = path
        self.folder = folder
        self.layout = QHBoxLayout()
        self.label = QTextEdit(self)
        self.setLayout(self.layout)
        self.set_attrs()

    def set_attrs(self):
        image = QImage("./img/directory.png")
        img_label = QLabel()
        pixMap = QPixmap.fromImage(image)
        img_label.setPixmap(pixMap)
        self.label.setText(self.name)
        self.label.setMaximumHeight(26)
        btn_del = QPushButton("X")
        btn_del.clicked.connect(self.delete)
        dir_btn = QPushButton("->")
        dir_btn.clicked.connect(lambda: self.window.load(self.path))
        btn_rename = QPushButton("zmien nazwe")
        btn_rename.clicked.connect(self.rename)
        self.layout.addWidget(img_label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(btn_rename)
        self.layout.addWidget(dir_btn)
        self.layout.addWidget(btn_del)

    def delete(self):
        os.remove(self.path)
        self.deleteLater()

    def confirm(self):
        f = open(self.path, "w")
        f.write(self.edit_field.toPlainText())
        f.close()
        self.win.close()

    def rename(self):
        os.rename(self.path, self.folder + "/" + self.label.toPlainText())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_field = None
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("File manager")
        self.setMinimumWidth(600)
        widget = QWidget(self)
        widget.setLayout(self.layout)

        self.file_layout = QVBoxLayout(self)
        file_widget = QWidget(self)
        file_widget.setLayout(self.file_layout)

        self.layout.addWidget(file_widget)
        self.setCentralWidget(widget)
        self.show()
        self.curr_dir = "./upload"
        self.load(self.curr_dir)

    def load(self, curr_dir):
        for i in reversed(range(self.file_layout.count())):
            self.file_layout.itemAt(i).widget().setParent(None)
        files = os.listdir(curr_dir)
        dir_label = QLabel()
        dir_label.setText(curr_dir)
        dir_label.setStyleSheet("""QLabel {background-color: silver}""")
        back_btn = QPushButton("wroc")
        back_btn.clicked.connect(lambda: self.load(curr_dir[0:curr_dir.rfind('/')]))
        new_btn = QPushButton("nowy plik")
        new_btn.clicked.connect(lambda: self.make_file(curr_dir))
        new_btn2 = QPushButton("nowy katalog")
        new_btn2.clicked.connect(lambda: self.make_dir(curr_dir))
        self.file_layout.addWidget(dir_label)
        self.file_layout.addWidget(new_btn)
        self.file_layout.addWidget(new_btn2)
        if curr_dir != "./upload":
            self.file_layout.addWidget(back_btn)
        for i in files:
            if os.path.isdir(curr_dir + "/" + i):
                dirr = curr_dir + "/" + i
                widget = DirWidget(self, name=i, path=dirr, folder=curr_dir)
                self.file_layout.addWidget(widget)
            else:
                dirr = curr_dir + "/" + i
                widget = FileWidget(name=i, path=dirr, folder=curr_dir)
                self.file_layout.addWidget(widget)

    def make_file(self, path):
        def create():
            open(path + "/" + self.name_field.toPlainText(), "x")
            win.hide()
            self.load(path)
        win = QWidget()
        form = QVBoxLayout(self)
        self.name_field = QTextEdit("podaj nazwe")
        confirm_btn = QPushButton("stworz")
        confirm_btn.clicked.connect(create)
        form.addWidget(self.name_field)
        form.addWidget(confirm_btn)
        win.setLayout(form)
        win.show()

    def make_dir(self, path):
        def create():
            os.mkdir(path + "/" + self.name_field.toPlainText())
            win.hide()
            self.load(path)
        win = QWidget()
        form = QVBoxLayout(self)
        self.name_field = QTextEdit("podaj nazwe")
        confirm_btn = QPushButton("stworz")
        confirm_btn.clicked.connect(create)
        form.addWidget(self.name_field)
        form.addWidget(confirm_btn)
        win.setLayout(form)
        win.show()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
