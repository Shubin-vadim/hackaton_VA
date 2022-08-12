# импорт необходимых модулей для запуска приложения
import sys
from PyQt5 import QtWidgets
from Destktop.app.Controllers.MainController import MainController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # получение пути к приложению
    main_class = MainController()
    main_class.show()  # показ начального экрана приложения
    sys.exit(app.exec_())  # завершение работы приложения
