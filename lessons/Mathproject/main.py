from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QRect, QEasingCurve
from PyQt5.QtGui import QPainter, QPainterPath, QLinearGradient, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, QHBoxLayout, QComboBox, QSplashScreen
from GlowButton import GlowButton
from random import randint, choice
import pygame 
import os
import shutil
import json
import hashlib
from window_for_messages import message_window
from gtts import gTTS

def resource_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def read_max_flame():
    json_path = resource_path('cfg.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("max_flame", 0)
        except:
            return 0
    return 0

def save_max_flame(flame):
    json_path = resource_path('cfg.json')
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump({"max_flame": flame}, file, ensure_ascii=False, indent=4)

class main_win(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drag_position = None
        self.flame_json = 0
        
        self.initUI()
        
        self.max_flame_record = read_max_flame()
        self.question_combo_record.setText(f'🏆 Рекорд: {self.max_flame_record}🔥')
        
        self.rights = 0
        self.new_flame = 0
        self.counter_flame = 0
        self.total_questions = 0
        self.speech_cache = {}
        self.command_list = ['Хочу сложнее', 'Хочу проще', 'Давай начнем', 'Теория по сложению', 'Теория по умножению', 'Теория по вычитанию', 'Теория по делению']
        self.topics = ['сложение',  'вычитание', 'умножение', 'деление']
        self.winner = ["Правильно! Молодец!", "Молодец! Классно!", "Умница! Здорово!", "Так держать!", "Ты гений!"]
        self.looser = ["Все получится! Будь внимательнее!", "Не сдавайся! Попробуй ещё!", "Ты справишься! Удачи!", "В следующий раз повезёт!", "Бывает! Старайся дальше!"]

        pygame.mixer.init()        

        sounds_dir = resource_path("Sounds")

        self.lose_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "lose.mp3"))
        self.right_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "right.mp3"))
        self.voice_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "voice.mp3"))

        self.voice_multi_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "voice_multiplication.mp3"))
        self.voice_addition_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "voice_addition.mp3"))
        self.voice_minus_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "voice_minus.mp3"))
        self.voice_division_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "voice_division.mp3"))
        pygame.mixer.music.load(os.path.join(sounds_dir, "back_mus.mp3"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        self.voice_sound.play()

        self.current_topic_index = 0  
        self.multiplication_levels = [
            {'name': 'Легкий', 'min': 1, 'max': 10},
            {'name': 'Средний', 'min': 10, 'max': 20},
            {'name': 'Сложный', 'min': 20, 'max': 100}
        ]
        self.divison_levels = [
            {'name': 'Легкий', 'min': 1, 'max': 20},
            {'name': 'Средний', 'min': 1, 'max': 50},
            {'name': 'Сложный', 'min': 1, 'max': 150}
        ]
        self.addition_levels = [
            {'name': 'Легкий', 'min': 1, 'max': 50},
            {'name': 'Средний', 'min': 51, 'max': 500},
            {'name': 'Сложный', 'min': 501, 'max': 1000}
        ]
        self.subtraction_levels = [
            {'name': 'Легкий', 'min': 1, 'max': 50},
            {'name': 'Средний', 'min': 50, 'max': 500},
            {'name': 'Сложный', 'min': 500, 'max': 1000}
        ]
        self.current_difficulty = 0
        self.current_question_index = 0
        self.current_question_text = ""
        self.current_right_answer = None
        self.quiz_active = False
        self.correct_counts = {
            'умножение': [0, 0, 0],
            'деление': [0, 0, 0],
            'сложение': [0, 0, 0],
            'вычитание': [0, 0, 0]
        }
        self.required_correct = 3

        self.connect_buttons()

        QTimer.singleShot(100, self.show_animation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        radius = 20 
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(135, 192, 245))  
        gradient.setColorAt(1.0, QColor(26, 95, 180))   
        painter.fillPath(path, gradient)
        pen = QPen(QColor(0,0,0,100))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, radius, radius)

    def speak(self, text: str, lang='ru'):
        try:
            cache_dir = resource_path("Cache")
            os.makedirs(cache_dir, exist_ok=True)
            
            cache_key = hashlib.md5(f"{text}_{lang}".encode()).hexdigest()
            cached_file = os.path.join(cache_dir, f"{cache_key}.mp3")
            
            if not os.path.exists(cached_file):
                tts = gTTS(text=text, lang=lang, slow=False)
                tts.save(cached_file)
            
            sound = pygame.mixer.Sound(cached_file)
            self.current_channel = sound.play()
            pygame.mixer.music.set_volume(0.1)
            self.check_sound_finished()
        except Exception as e:
            print(f"Ошибка озвучки: {e}")

    def check_sound_finished(self):
        if self.current_channel and self.current_channel.get_busy():
            QTimer.singleShot(100, self.check_sound_finished)
        else:
            pygame.mixer.music.set_volume(0.4)

    def show_animation(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        end_rect = self.geometry()
        start_rect = QRect(
            end_rect.x() + end_rect.width() // 4,
            end_rect.y() - 50,
            end_rect.width() // 2,
            end_rect.height() // 2
        )
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()

    def initUI(self):
        self.setWindowTitle('Personal Assistant')

        pygame.display.init()
        info = pygame.display.Info()

        self.setGeometry(info.current_w//4, info.current_h // 4, 500, 580)
        
        self.flame = 0
        title_layout = QHBoxLayout()
        title_layout.addStretch()
        self.minimize_btn = QPushButton("─")
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)
        title_layout.addWidget(self.minimize_btn)
        title_layout.addWidget(self.close_btn)
        question_lay = QHBoxLayout()
        combo_line_lay = QHBoxLayout()
        self.question_text = QLabel('За правильные ответы, я буду тебя хвалить, \nа пока напиши: "Давай начнем"')
        self.question_combo = QLabel(f'{self.flame}🔥 (комбо-очки)')
        self.question_combo_record = QLabel(f'🏆 Рекорд: 0🔥')
        self.question_combo_record.setStyleSheet("color: gold; font-size: 30px; background-color: transparent;")  # ← стиль
        question_lay.addWidget(self.question_text, 4)
        question_lay.addWidget(self.question_combo, 1)
        self.assistant_text = QLabel('Привет, я научу тебя простейшим математическим вычислениям!')
        self.progress_label = QLabel('Прогресс: 0/3 в легком уровне')
        self.progress_label.hide()
        self.by = QLabel("By: Zemtsov Yaroslav")
        self.by.setFixedHeight(15)
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText('Команды и ответы')        
        self.combo_box = QComboBox()
        self.combo_list = ["Выбор команд",
                        "Хочу сложнее",
                        "Давай начнем",
                        "Хочу проще", 
                        "Теория по умножению", 
                        "Теория по сложению", 
                        "Теория по вычитанию", 
                        "Теория по делению"
                        ]
        self.combo_box.addItems(self.combo_list)
        combo_line_lay.addWidget(self.line_edit, 2)        
        combo_line_lay.addStretch()
        combo_line_lay.addWidget(self.combo_box)
        self.button = GlowButton("Ответить/Отправить")
        self.button1 = GlowButton("Остановить музыку")
        self.setStyleSheet('''
            QWidget {
                font-family: Comic Sans MS;
            }
            QLabel {
                color: black;
                font-size: 30px;
                background-color: transparent;
            }
            QLabel#by_label {
                font-size: 12px;
                color: rgba(255, 255, 255, 100);
                background-color: transparent;
            }
            GlowButton {
                background-color: rgba(0, 255, 255, 200);
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: black;
                border: 1px solid rgba(0, 128, 128, 100);
            }
            QLineEdit {
                color: black;
                selection-background-color: cyan;
                font-size: 16px;
                background-color: #06bbc4;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #999;
            }
            QPushButton#close_btn, QPushButton#minimize_btn {
                background-color: rgba(255, 255, 255, 100);
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton#close_btn:hover {
                background-color: rgba(255, 0, 0, 200);
            }
            QPushButton#minimize_btn:hover {
                background-color: rgba(255, 255, 255, 200);
                color: black;
            }
            QMessageBox {
                background-color: rgb(6, 131, 214);
                color: black;
                border: none;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #00e6ff, stop:1 #00aaff);
                color: black;
                border: none;
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                border: none;
                border-radius: 0px 10px 10px 0px;
                background-color: rgba(0,0,0,0);
            }
            
            QComboBox QAbstractItemView {
                background-color: rgba(0, 200, 255, 0.3);
                color: black;
                selection-background-color: #6599c9;
            }
        ''')     
        self.minimize_btn.setObjectName("close_btn")
        self.close_btn.setObjectName("close_btn")
        self.by.setObjectName("by_label")
        self.question_text.setStyleSheet("color: blue; font-size: 30px; background-color: transparent;")
        self.assistant_text.setStyleSheet("color: blue; font-size: 30px; background-color: transparent;")
        self.question_combo.setStyleSheet("color: #8a2301; font-size: 30px; background-color: transparent;")
        self.by.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 180); background-color: transparent;")
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 10, 20, 20)
        self.main_layout.addLayout(title_layout)
        self.main_layout.addWidget(self.assistant_text)
        self.main_layout.addWidget(self.progress_label)    
        self.main_layout.addWidget(self.question_combo_record, alignment=Qt.AlignRight)  # ← добавляем сюда
        self.main_layout.addLayout(question_lay)      
        self.main_layout.addLayout(combo_line_lay)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.button1)   
        self.qh_lay = QHBoxLayout()
        self.qh_lay.addStretch()
        self.by.setFixedHeight(15)
        self.by.setFixedWidth(130)
        self.qh_lay.addWidget(self.by)
        self.qh_lay.addStretch()
        
        self.main_layout.addLayout(self.qh_lay)
        self.setLayout(self.main_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.pos().y() < 100:
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
                
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.pos().y() < 100:
                self.move(event.globalPos() - self.drag_position)
                event.accept()

    def connect_buttons(self):
        self.combo_box.currentTextChanged.connect(self.paste_commands)
        self.button.clicked.connect(self.btn_click)  
        self.button1.clicked.connect(self.pause_music)
        self.line_edit.returnPressed.connect(self.button.click)

    def paste_commands(self, com):
        self.line_edit.setText(com)
        self.combo_box.blockSignals(True)
        self.combo_box.setCurrentIndex(0)
        self.combo_box.blockSignals(False)

    def btn_click(self):
        user_input = self.line_edit.text().strip()
        if not user_input:
            return
        if user_input in self.command_list:
            self.use_command(user_input)
        else:
            self.check_answer(user_input)
        self.line_edit.clear()

    def pause_music(self):
        if self.button1.text() == "Остановить музыку":
            pygame.mixer.music.stop()
            self.button1.setText("Включить музыку")
        elif self.button1.text() == "Включить музыку":
            pygame.mixer.music.play(-1)
            self.button1.setText("Остановить музыку")

    def use_command(self, command):
        if command == 'Давай начнем':
            self.start_quiz()
            self.assistant_text.setText('Больше команда "Давай начнем" не доступна!')
            self.command_list.remove('Давай начнем')
            self.combo_box.removeItem(2)
        elif command == 'Хочу сложнее':
            self.increase_difficulty()
        elif command == 'Хочу проще':
            self.decrease_difficulty()
        elif command == 'Теория по умножению':
            self.voice_multi_sound.play()
            self.Multiplication_theory()        
        elif command == 'Теория по сложению':
            self.voice_addition_sound.play()
            self.Addition_theory()
        elif command == 'Теория по вычитанию':
            self.voice_minus_sound.play()
            self.Minus_theory()
        elif command == 'Теория по делению':
            self.voice_division_sound.play()
            self.Division_theory()

    def start_quiz(self):
        self.quiz_active = True
        self.progress_label.show()
        self.current_topic_index = 0 
        self.current_difficulty = 0   
        self.rights = 0
        self.total_questions = 0
        self.flame = 0
        self.question_combo.setText(f'{self.flame}🔥 (комбо-очки)')
        for topic in self.correct_counts:
            self.correct_counts[topic] = [0, 0, 0]
        self.generate_new_question()

    def get_current_levels(self):
        if self.topics[self.current_topic_index] == 'умножение':
            return self.multiplication_levels
        elif self.topics[self.current_topic_index] == 'деление':
            return self.divison_levels
        elif self.topics[self.current_topic_index] == 'сложение':
            return self.addition_levels
        else:
            return self.subtraction_levels
        
    def update_progress_display(self):
        topic = self.topics[self.current_topic_index]
        current_count = self.correct_counts[topic][self.current_difficulty]
        levels = self.get_current_levels()
        level_name = levels[self.current_difficulty]['name']
        self.progress_label.setText(
            f'Прогресс: {current_count}/{self.required_correct} в {level_name}'
        )
        if current_count >= self.required_correct:
            self.progress_label.setStyleSheet('font-size: 29px; color: #67f72b; background-color: transparent;')
        else:
            self.progress_label.setStyleSheet('font-size: 29px; color: #e32727; background-color: transparent;') 
            
    def generate_new_question(self):
        topic = self.topics[self.current_topic_index]
        levels = self.get_current_levels()
        difficulty = levels[self.current_difficulty]
        if topic == 'умножение':
            num1 = randint(difficulty['min'], difficulty['max'])
            num2 = randint(difficulty['min'], difficulty['max'])
            self.current_question_text = f"{num1} × {num2} = ?"
            self.current_right_answer = str(num1 * num2)
        elif topic == 'деление':
            num1 = randint(difficulty['min'], difficulty['max'])
            num2 = randint(difficulty['min'], difficulty['max'])
            self.current_question_text = f"{num1} / {num2} = ?"
            if num1 % num2 == 0:
                self.current_right_answer = str(num1 // num2)
            elif num1 % num2 > 0 :
                self.generate_new_question()
            if num1 == num2:
                self.generate_new_question()
        elif topic == 'сложение':
            num1 = randint(difficulty['min'], difficulty['max'])
            num2 = randint(difficulty['min'], difficulty['max'])
            self.current_question_text = f"{num1} + {num2} = ?"
            self.current_right_answer = str(num1 + num2)
        elif topic == 'вычитание':
            num1 = randint(difficulty['min'], difficulty['max'])
            num2 = randint(difficulty['min'], num1)
            self.current_question_text = f"{num1} - {num2} = ?"
            self.current_right_answer = str(num1 - num2)
        self.show_current_question()
        self.update_progress_display()
        
    def show_current_question(self):
        topic_icons = {'умножение': 'x', 'деление': '/', 'сложение': '+', 'вычитание': '-'}
        topic_names = {'умножение': 'Умножение', 'деление': 'Деление','сложение': 'Сложение', 'вычитание': 'Вычитание'}
        levels = self.get_current_levels()
        difficulty_names = ['Лёгкий', 'Средний', 'Сложный']
        current_level = levels[self.current_difficulty]
        range_text = f"(от {current_level['min']} до {current_level['max']})"
        self.question_text.setText(
            f"{topic_icons[self.topics[self.current_topic_index]]} "
            f"{topic_names[self.topics[self.current_topic_index]]} | "
            f"{difficulty_names[self.current_difficulty]} {range_text}\n\n"
            f"{self.current_question_text}"
        )
        self.line_edit.setPlaceholderText("Введите ответ...")  

    def finish_quiz(self):
        self.quiz_active = False
        addition_score = self.correct_counts['сложение'][0] + self.correct_counts['сложение'][1] + self.correct_counts['сложение'][2]
        subtraction_score = self.correct_counts['вычитание'][0] + self.correct_counts['вычитание'][1] + self.correct_counts['вычитание'][2]
        multiplication_score = self.correct_counts['умножение'][0] + self.correct_counts['умножение'][1] + self.correct_counts['умножение'][2]
        division_score = self.correct_counts['деление'][0] + self.correct_counts['деление'][1] + self.correct_counts['деление'][2]
        recommendations = []
        
        if addition_score < 9:
            recommendations.append("🔸 **Сложение**: стоит потренироваться складывать числа в столбик")
        elif addition_score < 15:
            recommendations.append("🔸 **Сложение**: уже неплохо, но можно еще подтянуть сложение больших чисел")
        else:
            recommendations.append("✅ **Сложение**: отличный результат!")
        
        if subtraction_score < 9:
            recommendations.append("🔸 **Вычитание**: обрати внимание на вычитание с переходом через разряд")
        elif subtraction_score < 15:
            recommendations.append("🔸 **Вычитание**: хороший результат, но стоит закрепить")
        else:
            recommendations.append("✅ **Вычитание**: ты отлично справляешься с вычитанием!")
        
        if multiplication_score < 9:
            recommendations.append("🔸 **Умножение**: советую повторить таблицу умножения")
        elif multiplication_score < 15:
            recommendations.append("🔸 **Умножение**: неплохо, но можно выучить таблицу умножения до автоматизма")
        else:
            recommendations.append("✅ **Умножение**: таблица умножения у тебя в кармане!")
        
        if division_score < 9:
            recommendations.append("🔸 **Деление**: советую повторить теорию по делению")
        elif division_score < 15:
            recommendations.append("🔸 **Деление**: неплохо, но можно выучить более сложные примеры по делению")
        else:
            recommendations.append("✅ **Деление**: ты - мастер деления!")
        if self.flame > self.new_flame:
            self.new_flame = self.flame
        if self.new_flame > self.max_flame_record:
            self.max_flame_record = self.new_flame
            save_max_flame(self.max_flame_record)
            self.question_combo_record.setText(f'🏆 Рекорд: {self.max_flame_record}🔥')
        
        result_message = (
            f"🎉 Ты прошел всю викторину! 🎉\n\n"
            f"📊 Твоя статистика:\n"
            f"Всего правильных ответов: {self.rights}\n"
            f"Правильных по темам:\n"
            f"   + Сложение: {addition_score}\n"
            f"   - Вычитание: {subtraction_score}\n"
            f"   x Умножение: {multiplication_score}\n"
            f"   / Деление: {division_score}\n\n"
            f"🔥 Твое максимальное комбо сегодня: {self.new_flame}\n\n"
            f"📚 Рекомендации:\n" + "\n".join(recommendations)
        )
        
        self.question_text.setText("🎉 Обучение завершено!")
        self.question_combo.setText("🏆")
        self.button.setEnabled(False)
        self.button1.setEnabled(False)
        cache_dir = resource_path("Cache")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        self.result_message1 = message_window("Итоги викторины", result_message)
        self.result_message1.show()

    def check_answer(self, user_answer):
        if not self.quiz_active:
            self.question_text.setText("Сначала введите 'Давай начнем'")
            return
        try:
            self.total_questions += 1
            if user_answer == self.current_right_answer:
                self.right_sound.play()
                self.rights += 1
                self.flame += 1
                self.question_combo.setText(f'{self.flame}🔥 (комбо-очки)')
                if self.flame == 5:
                    splash_pixmap = QPixmap(resource_path("images/5.png"))
                    self.splash = QSplashScreen(splash_pixmap)
                    self.splash.show()
                    QTimer.singleShot(2000, self.splash.close)
                elif self.flame == 10:
                    splash_pixmap = QPixmap(resource_path("images/10.png"))
                    self.splash = QSplashScreen(splash_pixmap)
                    self.splash.show()
                    QTimer.singleShot(2000, self.splash.close)
                elif self.flame == 20:
                    splash_pixmap = QPixmap(resource_path("images/20.png"))
                    self.splash = QSplashScreen(splash_pixmap)
                    self.splash.show()
                    QTimer.singleShot(2000, self.splash.close)      
                elif self.flame == 30:
                    splash_pixmap = QPixmap(resource_path("images/30.png"))
                    self.splash = QSplashScreen(splash_pixmap)
                    self.splash.show()
                    QTimer.singleShot(2000, self.splash.close)      
                self.speak(choice(self.winner)) 
                
                self.question_combo.setStyleSheet("font-size: 30px; color: gold; background-color: transparent;")
                QTimer.singleShot(350, lambda: self.question_combo.setStyleSheet("font-size: 30px; color: red; background-color: transparent;"))

                topic = self.topics[self.current_topic_index]
                self.correct_counts[topic][self.current_difficulty] += 1
                self.generate_new_question()
            else:
                self.counter_flame += 1
                self.a = choice(self.looser)
                self.lose_sound.play()
                pygame.time.wait(int(self.lose_sound.get_length() * 1000))
                self.speak(f"{self.a}... правильный ответ: {self.current_right_answer}")
                if self.counter_flame == 1:
                    self.new_flame == self.flame
                    self.flame = 0
                else:
                    if self.flame > self.new_flame:
                        self.new_flame = self.flame
                        self.flame = 0
                    else:
                        self.flame = 0
                self.question_combo.setText(f'{self.flame}🔥 (комбо-очки)')
                self.question_combo.setStyleSheet("color: #8a2301; font-size: 30px; background-color: transparent;")
                self.generate_new_question()    
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите число!")
            
    def can_increase_difficulty(self):
        topic = self.topics[self.current_topic_index]
        return self.correct_counts[topic][self.current_difficulty] >= self.required_correct
        
    def increase_difficulty(self):
        if not self.quiz_active:
            QMessageBox.warning(self, "Предупреждение", "Сначала начните викторину командой 'Давай начнем'")
            return
        levels = self.get_current_levels()
        topic = self.topics[self.current_topic_index]
        if not self.can_increase_difficulty():
            needed = self.required_correct - self.correct_counts[topic][self.current_difficulty]
            QMessageBox.warning(
                self, 
                "Ошибка", 
                f"❌ Нужно еще {needed} правильных ответа в этом уровне!\n"
                f"Сейчас: {self.correct_counts[topic][self.current_difficulty]}/{self.required_correct}"
            )
            return
        if self.current_difficulty < len(levels) - 1:
            self.current_difficulty += 1
            self.assistant_text.setText(f"Переходим на уровень: {levels[self.current_difficulty]['name']}!")
            self.generate_new_question()
        else:
            if self.current_topic_index < len(self.topics) - 1:
                self.current_topic_index += 1
                self.current_difficulty = 0 
                new_topic = self.topics[self.current_topic_index]
                self.assistant_text.setText(f"Переходим к теме: {new_topic}!")
                self.generate_new_question()
            else:
                self.finish_quiz()       
                
    def decrease_difficulty(self):
        if not self.quiz_active:
            QMessageBox.warning(self, "Ошибка", "Сначала начните викторину командой 'Давай начнем'")
            return
        levels = self.get_current_levels()
        if self.current_difficulty > 0:
            self.current_difficulty -= 1
            self.assistant_text.setText(f"Возвращаемся на уровень: {levels[self.current_difficulty]['name']}!")
            self.generate_new_question()
        else:
            QMessageBox.warning(self, "Ошибка", "❌ Это минимальный уровень сложности!")       
            
    def Multiplication_theory(self):
        self.window_multi = message_window("Умножение", 
                        "Когда ты умножаешь одно число на другое (эти числа называются множители) \n"
                        "Ты увеличиваешь первое число само на себя, столько раз, сколько было указано  во втором числе. \n"
                        "Например: 2x2 - то есть 2+2 = 4, 2x3 = 2+2+2 = 6, 5x5 = 5+5+5+5+5 = 25. Но чтобы умножать их быстрее, \n"
                        "советую выучить таблицу умножения. \n"
                        "Также, чтобы умножить к примеру:  12 x 13 тебе нужно разложить второе число 13 по разрядам, то есть 13 это 10 + 3, и перемножение мы можем сделать следующим образом: 12 x 10 + 12 x 3 = 120 + 36 = 156.\n")   
        self.window_multi.show()

    def Division_theory(self):
        self.window_division = message_window("Деление", 
                        "Для упрощения деления простых чисел, желательно выучить таблицу умножения. \n"
                        "Когда ты делишь одно число(делимое) на другое число(делитель),\n"
                        "ты разбиваешь его на столько частей, сколько написано во втором числе.\n"
                        "Например: 10 разделить на 2. 10 состоит из двух пятерок, значит ответ будет 5. \n"
                        "18 разделить на 3. 18 состоит из трех шестерок значит ответ - 6.\n"
                        "Чтобы разделить 145 на 5 нужно сделать следующие шаги: \n"
                        "делим на пять каждый разряд числа 145, 1 на 5 не делится, \n" 
                        "значит берем следующее число - 14, 14 на 5 делится, но с остатком 4, то есть число  14 состоит из двух пятерок и еще остается 4, \n" 
                        "при делении 14 на 5, в результат деления записываем 2, а вместо 14 осталось 4, продолжаем делить число 145, которое стало числом 45, \n" 
                        "это число состоит из девяти пятерок, смотри таблицу умножения, соответственно вписываем в результат деления цифру 9, итоговый ответ - 29")        
        self.window_division.show()

    def Addition_theory(self):
        self.window_addtion = message_window("Сложение", 
                        "Когда ты складываешь одно число с другим(они называются слагаемые)\n"
                        "Ты увеличиваешь первое число на другое. \n"
                        "Например: 3+2 -  это три единицы плюс две единицы, всего пять единиц. \n"  
                        "Следующий пример: 55+55 - для упрощения сложения, мы можем посчитать отдельно десятки,\n "
                        "отдельно единицы, то есть - 50+50 = 100, а 5+5 = 10 итого будет 100 + 10 = 110\n"
                        "3444+5460 = советую делать столбиком, пример в текстовой части:\n"
                        "  3444\n"
                        "+\n"
                        "  5460\n"
                        "------\n"
                        "  8904 \nКогда мы сложили 4 и 6, получилось 10, вниз мы записываем 0, а к следующему шагу(4+4) добавляем 1, получается 9")                      
        self.window_addtion.show()

    def Minus_theory(self):
        self.window_minus = message_window("Вычитание", 
                        "Ты вычитаешь из первого числа(уменьшаемое), второе число(вычитаемое)\n"
                        "Например: 7 - 5 разница между этими числами две еденицы, это и есть ответ. \n"
                        "Следующий пример:  65 - 35 - для упрощения вычитания, вычитаемое делим на \n"
                        "разряды, то есть 35 это 30 и 5, сначала вычитаем из шестидесяти пяти 30, получаем 35, \n"
                        "а затем из 35 вычитаем 5, получаем итоговый ответ - 30. Более сложный пример: \n"
                        "5460-3444 = советую делать столбиком, пример в текстовой части: \n"
                        "5460\n"
                        "-\n"
                        "3444\n"
                        "------\n"
                        "2016 Когда мы вычли 4 из 0, нам пришлось занять 1 цифру из 6, и мы получаем 6-1 = 5, а к предыдущему шагу(0-4) к 0 добавляем 10, получается 10 - 4 = 6.")
        self.window_minus.show()

if __name__ == '__main__':
    app = QApplication([])
    image_dir = resource_path("images")
    splash_pixmap = QPixmap(os.path.join(image_dir, "asdasdads.png"))
    splash = QSplashScreen(splash_pixmap)
    splash.show()

    QTimer.singleShot(3000, splash.close) 

    window = main_win()
    QTimer.singleShot(3000, window.show)
    app.exec_()