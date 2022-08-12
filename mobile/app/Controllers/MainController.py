from kivy.lang import Builder
from kivy.uix.widget import Widget
import datetime

from app.Models.DataModel import DataModel
from app.Models.VoiceModel import VoiceModel


Builder.load_file(r'app/Views/mainview.kv')


class MainController(Widget):
    def __init__(self):
        super().__init__()
        self.voice_recogn = VoiceModel()  # класс для воспроизведения и распознавания речи
        self.answer = DataModel() # класс для работы с данными от пользователя
        self.stop = False  # флаг на паузу диалога
        self.repeat_start = False  # флаг на повторное

    # метод для выявления времени суток пользователя
    def getTimeOfDay(self):
        getTime = int(datetime.datetime.now().hour)
        if getTime >= 0 and getTime < 6:
            text = 'Доброе ночи'
        elif getTime >= 6 and getTime < 12:
            text = 'Доброе утро'
        elif getTime >= 12 and getTime < 18:
            text = 'Добрый день'
        elif getTime >= 18 and getTime != 0:
            text = 'Добрый вечер!'
        self.voice_recogn.speak(text)


        # метод для начала диалога
    def start_convertion(self):
        if self.repeat_start == False:
            start_text = ' Могу ли я вам чем-нибудь помочь?'
            self.getTimeOfDay()
            self.voice_recogn.speak(start_text)  # приветствие пользователя

        self.repeat_start = True
        self.stop = False
        self.phrase = 'Говорите'
        while self.stop == False:  # запуск бесконечного цикла до тех пор, пока пользователь не завершит разговор с ботом
            self.voice_recogn.speak(self.phrase)
            data, statement = self.voice_recogn.recordAudio()  # получение сообщения от пользователя
            if statement == None:  # пропуск действий в случае ошибки или не возможности распознать речь пользователя
                self.voice_recogn.speak(data)
                continue
            answer, action = self.answer.get_answer(data)  # получение ответа и действия пользователю
            if type(action) is str:  # озвучка и отправка сообщения, если действие является строкой
                self.voice_recogn.speak(action)
            self.voice_recogn.speak(answer)
            if action == True:
                self.stop = True
                break
            self.voice_recogn.stop_loop()  # остановка цикла движка воспроизведения речи