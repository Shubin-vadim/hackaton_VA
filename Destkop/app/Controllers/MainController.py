# импорт необходимых модулей
import datetime
from pyttsx3.drivers import sapi5
import Destktop.app.Models.DataModel
from PyQt5 import QtCore, QtWidgets
from Destktop.app.Views.MainView import MainView
from Destktop.app.Models.VoiceRecognationModel import VoiceRecognationModel

# контройлер для главного экрана приложения


class MainController(QtWidgets.QMainWindow):
    # установка настроек и значений по умолчанию для всех элементов
    def __init__(self, parent=None):
        super().__init__(parent)
        self.oldPos = None
        self.phrase = None
        self.ui = MainView()  # класс разметки дизайна приложения
        self.voice_recogn = VoiceRecognationModel()  # класс для воспроизведения и распознавания речи
        self.answer = Destktop.app.Models.DataModel.DataModel()  # класс для работы с данными от пользователя
        self.ui.setupUi(self)  # установка разметки дизайна
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # установка флагов для приложения, чтобы не переопределять настройки на платформах
        self.center()  # центрирование приложения
        self.ui.send_btn.clicked.connect(
            self.start_conversation
        )  # установка собития на кнопку
        self.stop = False  # флаг на паузу диалога
        self.repeat_start = False  # флаг на повторное общение с ассистентом

    # метод для разметки приложения по центру
    def center(self):
        frame_geometry = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

    # метод для нажатия кнопки мыши
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    # метод  для перемещения окна приложения, т.к. стандартные элементы убраны
    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # метод для отправки сообщений в чат
    def send_message(self, text, user=True):
        item = QtWidgets.QListWidgetItem()
        if user:
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            item.setText("Вы" + ": " + text)
        else:
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            item.setText("Алена" + ": " + text)
        self.ui.chat_list.addItem(item)

    # метод для выявления времени суток пользователя
    def getTimeOfDay(self):
        getTime = int(datetime.datetime.now().hour)
        if 0 <= getTime < 6:
            text = "Доброе ночи"
        elif 6 <= getTime < 12:
            text = "Доброе утро"
        elif 12 <= getTime < 18:
            text = "Добрый день"
        else:
            text = "Добрый вечер!"
        self.send_message(text, user=False)
        self.voice_recogn.speak(text)

    # метод для начала диалога
    def start_conversation(self):
        self.ui.send_btn.hide()
        self.ui.chat_list.show()
        if not self.repeat_start:
            start_text = " Могу ли я вам чем-нибудь помочь?"
            self.getTimeOfDay()
            self.ui.chat_list.clear()  # очистка поля от текста
            self.send_message(start_text, user=False)  # отправка сообщения в чат
            self.voice_recogn.speak(start_text)  # приветствие пользователя

        self.repeat_start = True
        self.stop = False
        self.phrase = "Говорите"
        while not self.stop:  # запуск бесконечного цикла работы
            self.ui.chat_list.clear()
            self.send_message(self.phrase, user=False)
            self.voice_recogn.speak(self.phrase)
            data, statement = self.voice_recogn.recordAudio()  #
            if statement is None:  # пропуск действий при сбоях
                self.send_message(data, user=False)
                self.voice_recogn.speak(data)
                continue
            answer, action = self.answer.get_answer(data)  # получение ответа и действия пользователю
            self.ui.chat_list.clear()
            if type(action) is str:
                self.send_message(action, user=False)
                self.voice_recogn.speak(action)
            self.send_message(answer, user=False)
            self.voice_recogn.speak(answer)
            if action:
                self.stop = True
                self.ui.chat_list.hide()
                self.ui.send_btn.show()
                break

            self.voice_recogn.stop_loop()  # остановка цикла движка воспроизведения речи
