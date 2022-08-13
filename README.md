# Голосовой помощник для инвалидов по зрению

1. [Клонирование репозитория](#clone)
2. [Установка зависимостей](#set_req)
3. [Запуск программы](#run)
4. [Возможности голосового ассистента](#opportunity)

# <a name="clone">Клонирование репозитория</a>
```
git clone https://github.com/Shubin-vadim/hackaton_VA.git
```
# <a name="set_req">Установка зависимостей</a>

1. Версия для компьютера
```
cd Destkop
pip3 install -r requirements_Destkop.txt
```
2. Мобильная версия
```
cd mobile
pip3 install -r requirements_mobile.txt
```
# <a name="run">Запуск программы для любой из версий</a>
```
python main.py
```
# <a name="opportunity">Возможности голосового ассистента</a>
1. Поиск информация в интернете. Ключевые слова: "найди", "найти" + информация для поиска.
2. Рассказ анектода. Ключевые слова: "пошути", "анедот".
3. Узнать погоду на данный момент. Ключевые слова: "погода", "пагода" + город.
4. Прослушивание музыки. Ключевые слова: "песни", "песня", "музыка", "музыки" + исполнитель.
5. Запуск базовых програм. Ключевые слова: "открой", "запусти" + название программы.
6. Просмотр фильма/сериала. Ключевые слова: "посмотреть", "пасматреть", "смотреть", "сматреть" + название фильма/сериала.