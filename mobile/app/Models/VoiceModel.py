import speech_recognition as sr
from pyttsx3.drivers import sapi5
import pyttsx3

# инициализация движка воспроизведения речи
engine = pyttsx3.init()


class VoiceModel:

    def recordAudio(self, phrase='Говорите: '):  # распознавание речи пользователя и предварительная обработка данных
        recognize = sr.Recognizer()
        with sr.Microphone() as source:
            recognize.adjust_for_ambient_noise(source)
            audio = recognize.listen(source)
        try:
            data = recognize.recognize_google(audio, language='ru-RU').lower() # получение фразы и перевод в нижний регистр
        except sr.UnknownValueError:  # исключение в случае невозможности распознавания речи
            data = "Извините,но я вас не понимаю"
            return (data, None)
        except sr.RequestError as e:  # исключение в случае не подключению к системе распознавания речи Google
            data = "Не удалось запросить результаты у службы распознавания речи Google"
            return (data, None)
        return (data, True)

    def speak(self, text):  # воспроизведение текста
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    def stop_loop(self):  # # остановка цикла движка воспроизведения речи
        if engine._inLoop:
            engine.endLoop()