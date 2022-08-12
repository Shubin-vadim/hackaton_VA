# импорт необходимых модулей
import json
import random
import Destktop.app.Models.BrowserModel
import Destktop.app.Models.RecognationObjectsModel


class DataModel:
    # инициализация объектов других классов
    def __init__(self):
        self.browser = Destktop.app.Models.BrowserModel.BrowserModel()
        self.recogn = Destktop.app.Models.RecognationObjectsModel.RecognationObjectsModel()

    # основная функция получения ответа и действия пользователя
    def get_answer(self, text):
        filname = r"app/Controllers/data/commands.json"
        with open(filname, "r", encoding="utf-8") as f:  # открытие файла с командами
            data = json.load(f)
        key_text = self.get_key_request(text, data)  # получение ключа от текста
        # ключевые слова, запаисанные в commands2.json
        if key_text is not None:
            value_text = self.get_request(text, data)  # получение значения от пользователя
            class_command = self.classify_text(self.clear_phrase(key_text), data)  # класс ключевого слова
            if class_command:
                answer = self.get_answer_by_intent(class_command, data)  # получение ответа
                action = self.performing_action(
                    class_command, key_text, value_text
                )  # выполнение действия и получение ответа на него
                return answer, action

        stub = self.get_failure_phrase(data)
        return stub, False

    # получение ключевого слова от пользователя
    def get_key_request(self, text, data):
        text = text.split()
        for key, value in data["intents"].items():
            for example in value["examples"]:
                if text[0] == example:
                    return text[0]

        # получение вторичного значения из фразы пользователя

    def get_request(self, text, data):
        arr_text = text.split(maxsplit=1)
        if len(arr_text) == 1:
            val = str(arr_text[0])
        else:
            val = str(arr_text[1])
        for key, value in data["intents"].items():
            for example in value["examples"]:
                val = val.replace(example, "")
        val = val.strip()
        return val

    # классификация текста и получения от него ключа
    def classify_text(self, text, data):
        for key, value in data["intents"].items():
            for example in value["examples"]:
                example = self.clear_phrase(example)
                example = self.clear_phrase(example)
                if example == text:
                    return key

    # очистка фразы от ненужных символов
    def clear_phrase(self, phrase):
        phrase = phrase.lower()
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
        result = "".join(symbol for symbol in phrase if symbol in alphabet)
        return result

    # выбор рандомного значения, зависящее от ключа пользователя
    def get_answer_by_intent(self, intent, data):
        if intent in data["intents"]:
            responses = data["intents"][intent]["responses"]
            return random.choice(responses)

    # получение фразы-заглушки, если команды не существует
    def get_failure_phrase(self, data):
        failure_phrases = data["failure_phrases"]
        return random.choice(failure_phrases)

    # запись отзыва пользователя в текстовый файл
    def write_review(self, text):
        path = r"app/Controllers/data/Reviews.txt"
        f = open(path, "a")
        f.write(text + "  " + "\n")
        f.close()

    # Основная функция для выполнения определенных команд
    def performing_action(self, key_action="", key_text="", value_text=""):
        main_text = value_text.replace(" ", "")
        if key_action == "bye":
            return True
        if key_action == "action_browser":
            if ("открой" in key_text) or ("поиск" in key_text) or ("найти" in key_text) or ("найди" in key_text):
                rezult = self.browser.filter_internet(self.browser.search_in_google(main_text))
                if not self.browser.definition_of_plural(value_text):
                    self.browser.openUrl(rezult[0])
                else:
                    self.browser.openUrl(random.choice(rezult))
        elif key_action == "humor":
            return self.browser.tell_anecdote()
        elif key_action == "weather":
            return self.browser.weather()
        elif key_action == "music":
            url = "https://my.mail.ru/music/search/" + str(value_text)
            self.browser.openUrl(url)
        elif key_action == "support":
            self.write_review(value_text)
        elif key_action == "recognation_objects":
            self.recogn.recogn_objects()
