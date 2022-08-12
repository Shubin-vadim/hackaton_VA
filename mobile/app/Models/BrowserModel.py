import webbrowser
import requests
import re
import bs4
import inflect
from googletrans import Translator
from googlesearch import search
from app.Models.VoiceModel import VoiceModel

# инициализация движка для перевода и работы речью
inflect = inflect.engine()
translator = Translator()


class BrowserModel:
    def __init__(self):
        self.recogn_voice = VoiceModel()

    # фильтрация данных из интернета
    def filter_internet(self, sites):
        result = []
        for i in sites:
            if 'http' in i and i.find('.jpg') == -1 and i.find('.png') == -1 and i.find('.gif') == -1:
                result.append(i)
            else:
                continue
        return result

    # открытие веб-страницы браузера
    def openUrl(self, url):
        webbrowser.open(url)

    # поиск данных в гугле
    def search_in_google(self, query):
        sities = []
        for i in search(query, num_results=25, lang="ru"):
            sities.append(i)
        return sities

        # перевод фразы
    def translate_phrase(self, text, lang_src='en', lang_dest='ru'):
            translation = translator.translate(str(text), src=lang_src, dest=lang_dest)
            return translation.text

    # рассказ анекдота
    def tell_anecdote(self):
        get_site = requests.get('https://nekdo.ru/random/')
        pars = bs4.BeautifulSoup(get_site.text, "html.parser")
        select_anecdote = pars.select('.text')
        anectode_text = (select_anecdote[0].getText().strip())
        reg = re.compile('[^0-9a-zA-Zа-яА-я .,!?-]')
        rezult = reg.sub('', anectode_text)
        return rezult

    # получение погоды в реальном времени
    def weather(self, city='Ярославль'):
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        api_key = 'bd37d72510fa04c2fa2237b9a0f31805'
        question = 'Погоду какого города вы бы хотели знать?'
        self.recogn_voice.speak(question)
        weather_city, flag = self.recogn_voice.recordAudio(question)
        if flag is None:
            complete_url = base_url + 'appid=' + api_key + '&q=' + city
        else: complete_url = base_url + 'appid=' + api_key + '&q=' + weather_city
        response = requests.get(complete_url)
        data = response.json()
        if data['cod'] == 404:
            text = 'Извините, но погода города не определена'
            return text
        else:
            temperature = int(data['main']['temp'] - 273.15)
            humidity = int(data['main']['humidity'])
            weather_description = data['weather'][0]['description']
            answer_text = 'В городе' + ' ' + city + ' ' + 'температура составляет' + ' ' + str(temperature)\
                          + ',\n влажность ' + str(humidity) + '.\nОписание: ' + self.translate_phrase(
                weather_description)
            return answer_text


    # перевод русской речи в английскую для выявления многозначности или однозначности слов пользователя
    def definition_of_plural(self, text):
        translation = translator.translate(str(text), src='ru', dest='en')
        text_translate = translation.text
        if inflect.singular_noun(str(text_translate)) == False:
            return False
        else:
            return True