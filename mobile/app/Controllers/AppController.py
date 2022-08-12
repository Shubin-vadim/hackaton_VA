from kivy.app import App
from app.Controllers.MainController import MainController


class AppController(App):
    def build(self):
        return MainController()
