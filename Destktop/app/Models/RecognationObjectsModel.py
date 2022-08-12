# импорт необходимых модулей
import numpy as np
import cv2
from Destktop.app.Models.VoiceRecognationModel import VoiceRecognationModel
import Destktop.app.Models.BrowserModel


class RecognationObjectsModel:  # класс для распознавания объектов
    def __init__(self, obj=None):
        self.object = obj
        self.message = VoiceRecognationModel()
        self.browser = Destktop.app.Models.BrowserModel.BrowserModel()

    def findObjects(self, outputs, img):  # метод для нахождения объекто
        hT, wT, cT = img.shape
        bbox = []
        classIds = []
        confs = []
        confThreshold = 0.5
        nmsThreshold = 0.2
        classNames = []
        classFile = r"app\Models\config\coco.names"  # файл с именами объектов распознавания

        with open(classFile, "r") as f:
            classNames = f.read().rstrip("\n").split("\n")

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)  # берём индекс объекта с максимальным значением
                confidence = scores[classId]
                if confidence > confThreshold:
                    w, h = int(det[2] * wT), int(det[3] * hT)  # вычисление ширины и высоты объекта
                    x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)  # вычисление координат объекта
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))  # получение значения вероятности принадлежности объекта к классу

        # Работа с рамкой объекта изображения
        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(
                img, (x, y), (x + w, y + h), (255, 0, 255), 2, cv2.LINE_AA
            )  # рисуем ограничивающий прямоугольник
            cv2.putText(img, f"{classNames[classIds[i]].upper()}{int(confs[i] * 100)}%",
                        (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)  # вставляем наименование объекта и его вероятность принадлежности
            self.object = classNames[classIds[i]].upper()
            self.message.speak(
                "Впереди " + self.browser.translate_phrase(self.object)
            )  # воспроизведение наименования объекта

    def recogn_objects(self):
        whT = 320
        modelConfiguration = r"app\Models\config\yolov3-tiny.cfg"  # наименование конфигурационного файла
        modelWeights = r"app\Models\config\yolov3-tiny.weights"  # наименование файла весов

        net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)  # чтение нейронной сети с помощью её конфига и весов
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)  # установка серверной части нейронной сети
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # установка сети на CPU

        cap = cv2.VideoCapture(0)  # настройка веб-камеры
        wCap, hCap = 640, 480
        cap.set(3, wCap)
        cap.set(4, hCap)
        webcam = True

        while True:  # покадровое чтение с веб камеры
            if webcam:
                success, frame = cap.read()
            else:
                frame = cv2.imread(
                    r"https://bugaga.ru/uploads/posts/2017-01/1483531805_dvulikaya-koshka-yana-8.jpg"
                )
            blob = cv2.dnn.blobFromImage(
                frame, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False
            )  # конвертирование изображения в формат данных NN
            net.setInput(blob)  # установка формата данных сети
            layersNames = net.getLayerNames()  # получение имен слоёв сети

            outputNames = [
                (layersNames[i - 1]) for i in net.getUnconnectedOutLayers()
            ]  # получение имен сети только выходных слоёв

            outputs = net.forward(outputNames)  # получение результатов от 3-х выходных слоёв сети
            self.findObjects(outputs, frame)  # нахождение объекта изобраэения и получение его вероятности
            cv2.imshow("Cap", frame)
            k = cv2.waitKey(1)
            if k == 27 or cv2.getWindowProperty("Cap", cv2.WND_PROP_VISIBLE) < 1:  # завершение цикла
                break
        cap.release()  # освобождение веб камеры
        cv2.destroyAllWindows()  # закрытие окон, кроме главного
