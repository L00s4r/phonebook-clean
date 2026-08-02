from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
 QVBoxLayout, QPushButton, QListWidget, QTextEdit, QLineEdit, QInputDialog)
import json
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.notes = self.get_json()
        self.fill_notes_list()
        self.connect_buttons()
    def initUI(self):
        self.setWindowTitle('Smart notes')
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.button_layout_note = QHBoxLayout()
        self.button_layout_tag = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.notes_list_widget = QListWidget()
        self.tags_list_widget = QListWidget()
        self.btn_save_note = QPushButton("Сохранить")
        self.btn_create_note = QPushButton("Создать")
        self.btn_delete_note = QPushButton("Удалить")
        self.btn_search_tag = QPushButton("Искать по тегу")
        self.btn_create_tag = QPushButton("Добавить")
        self.btn_delete_tag = QPushButton("Удалить")
        self.button_layout_note.addWidget(self.btn_create_note)
        self.button_layout_note.addWidget(self.btn_delete_note)
        self.button_layout_tag.addWidget(self.btn_create_tag)
        self.button_layout_tag.addWidget(self.btn_delete_tag)
        self.right_layout.addWidget(self.notes_list_widget)
        self.right_layout.addLayout(self.button_layout_note)
        self.right_layout.addWidget(self.btn_save_note)
        self.right_layout.addWidget(self.tags_list_widget)
        self.right_layout.addLayout(self.button_layout_tag)
        self.right_layout.addWidget(self.btn_search_tag)
        self.main_layout.addWidget(self.text_edit)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)
    def get_json(self):
        notes = read_json()
        return notes
    def fill_notes_list(self):
        names = list(self.notes.keys())
        self.notes_list_widget.clear()
        self.notes_list_widget.addItems(names)
    def connect_buttons(self):
       self.notes_list_widget.itemClicked.connect(self.show_note)        
       self.btn_save_note.clicked.connect(self.save_note)
       self.btn_create_note.clicked.connect(self.add_note)
       self.btn_delete_note.clicked.connect(self.del_note)
       self.btn_search_tag.clicked.connect(self.search_tag)
       self.btn_create_tag.clicked.connect(self.add_tag)
       self.btn_delete_tag.clicked.connect(self.del_tag)
    def show_note(self):
        note_head = self.notes_list_widget.selectedItems()[0].text()
        note = self.notes[note_head]
        self.text_edit.setText(note["text"])
        self.fill_tags_list(note["tags"])
    def fill_tags_list(self, tags):
        self.tags_list_widget.clear()
        self.tags_list_widget.addItems(tags)
    def save_note(self):
        note_text = self.text_edit.toPlainText()
        select_note = self.notes_list_widget.selectedItems()
        current_note = select_note[0].text()
        self.notes[current_note]["text"] = note_text
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(self.notes, file, ensure_ascii=False)
    def add_note(self):
        inputdialog, ok = QInputDialog.getText(self, 'add_note', 'Введите заметку')
        if ok:
            if not inputdialog in self.notes:
                self.notes[inputdialog] = {"text": "", "tags": []}
            else:
                return
        self.notes_list_widget.addItem(inputdialog)
    def del_note(self):
        selected_items = self.notes_list_widget.selectedItems()
        if not selected_items:
            return
        note_name = selected_items[0].text()
        if note_name in self.notes:
            del self.notes[note_name]
        self.text_edit.clear()
        self.tags_list_widget.clear()
        self.notes_list_widget.takeItem(self.notes_list_widget.row(selected_items[0]))
    def search_tag(self):
        searching, ok = QInputDialog.getText(self, 'search...', 'Введите тэг')
        accept = []
        if ok and searching:
            for note, item in self.notes.items():
                if searching in item["tags"]:
                    accept.append(note)
            self.fill_filtered_notes(accept)
        else:
            self.fill_notes_list()
    def fill_filtered_notes(self, notes):
        self.notes_list_widget.clear()
        self.notes_list_widget.addItems(notes)
    def add_tag(self):
        select_note = self.notes_list_widget.selectedItems()
        if select_note:
            tag, ok = QInputDialog.getText(self, "add_tag", "Введите тэг")
            if ok and tag:
                current_note = select_note[0].text()
                self.notes[current_note]["tags"].append(tag)
                self.fill_tags_list(self.notes[current_note]["tags"])
        else:
            pass
    def del_tag(self):
        select_note = self.notes_list_widget.selectedItems()
        if select_note:        
            select_tag = self.tags_list_widget.selectedItems()
            if select_tag:
                current_tag = select_tag[0].text()
                current_note = select_note[0].text()
                ss = self.notes[current_note]["tags"].index(current_tag)
                if current_note in self.notes:
                    del self.notes[current_note]["tags"][ss]
                self.fill_tags_list(self.notes[current_note]["tags"])
def read_json():
    with open('notes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
def create_json():
    notes = {
        'Добро пожаловать!':{
            "text": 'Добро пожаловать в приложение умные заметки',
            "tag": ['Добро пожаловать', 'умные заметки']
        }
    }
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False)
#create_json()
app = QApplication([])
main_win = MainWindow()
main_win.show()
app.exec_()