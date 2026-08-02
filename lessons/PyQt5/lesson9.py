from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QCheckBox, QInputDialog, QListWidgetItem, QMessageBox
import json
import os
class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()          
        self.notes = []
        self.filename = 'notes.json'
        self.load_notes()
        self.connect_buttons()

    def initUI(self):
        self.setWindowTitle('To-Do app')
        self.resize(450, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: Comic Sans MS;
            }
            QPushButton {
                background-color: beige;
                color: black;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: orange;
            }
            QListWidget {
                background-color: beige;
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #ddd;
            }
            QCheckBox {
                color: #333;
                font-size: 11px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 10px;
                height: 10px;
            }
        """)
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.button_layout_note = QHBoxLayout()
        self.notes_list_widget = QListWidget()
        self.btn_save_note = QPushButton("Сохранить")
        self.btn_create_note = QPushButton("Создать")
        self.btn_delete_note = QPushButton("Удалить")
        self.button_layout_note.addWidget(self.btn_create_note)
        self.button_layout_note.addWidget(self.btn_delete_note)
        self.right_layout.addWidget(self.notes_list_widget)
        self.right_layout.addLayout(self.button_layout_note)
        self.right_layout.addWidget(self.btn_save_note)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)
    def create_note(self):
        inputdialog, ok = QInputDialog.getText(self, 'Добавить заметку', 'Введите заметку:')
        if ok and inputdialog.strip():
            if not any(note['text'] == inputdialog for note in self.notes):
                new_note = {
                    'text': inputdialog,
                    'checked': False
                }
                self.notes.append(new_note)
                self.fill_notes_list(new_note)
                self.save()
            else:
                QMessageBox.warning(self, "Предупреждение", "Такая заметка уже существует!")
    def delete_note(self):
        selected_items = self.notes_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Информация", "Выберите заметку для удаления")
            return
        selected_item = selected_items[0]
        checkbox = self.notes_list_widget.itemWidget(selected_item)
        if checkbox:
            note_text = checkbox.text()
            reply = QMessageBox.question(self, 'Подтверждение', 
                                        f'Удалить заметку "{note_text}"?',
                                        QMessageBox.Yes | QMessageBox.No, 
                                        QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.notes = [note for note in self.notes if note['text'] != note_text]
                row = self.notes_list_widget.row(selected_item)
                self.notes_list_widget.takeItem(row)
                self.save()
    def save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.notes, file, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {e}")
    def load_notes(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.notes = json.load(file)
                    for note in self.notes:
                        self.fill_notes_list(note)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {e}")
    def connect_buttons(self):       
        self.btn_save_note.clicked.connect(self.save)
        self.btn_create_note.clicked.connect(self.create_note)
        self.btn_delete_note.clicked.connect(self.delete_note)
    def update_checkbox_state(self, state, item):
        checkbox = self.notes_list_widget.itemWidget(item)
        if checkbox:
            note_text = checkbox.text()
            for note in self.notes:
                if note['text'] == note_text:
                    note['checked'] = (state == Qt.Checked)
                    break
            self.save()
    def fill_notes_list(self, note):
        self.notes_list_widget.clear()
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        checkbox = QCheckBox(note['text'])
        checkbox.setCheckState(Qt.Checked if note['checked'] else Qt.Unchecked)
        checkbox.stateChanged.connect(lambda state, item=item: self.update_checkbox_state(state, item))
        self.notes_list_widget.addItem(item)
        self.notes_list_widget.setItemWidget(item, checkbox)
if __name__ == '__main__':
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec()