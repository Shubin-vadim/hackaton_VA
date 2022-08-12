import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()


class VoiceRecognationModel:
    def recordAudio(self):  # распознавание речи пользователя и предварительная обработка данных
        recognize = sr.Recognizer()
        with sr.Microphone() as source:
            recognize.adjust_for_ambient_noise(source)
            audio = recognize.listen(source)
        try:
            data = recognize.recognize_google(audio, language="ru-RU").lower()
        except sr.UnknownValueError:  # исключение в случае невозможности распознавания речи
            data = "Извините,но я вас не понимаю"
            return data, None
        except sr.RequestError:  # исключение в случае не подключению к системе распознавания речи Google
            data = "Не удалось запросить результаты у службы распознавания речи Google"
            return data, None
        return data, True

    def speak(self, text):  # воспроизведение текста
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    def stop_loop(self):
        if engine._inLoop:  # остановка цикла движка воспроизведения речи
            engine.endLoop()
