import numpy as np
from tensorflow.keras.models import load_model


class Predict:
    def __init__(self):
        # сделать обновление модели
        self.__model = load_model('keras_model.keras')

    def one_day(self, data: np.array) -> int:
        return self.__model.predict(data)

    def two_days(self, data: np.array) -> int:
        new_element = np.array([self.__model.predict(data)])
        data = np.delete(data, 0, 1)
        data = np.concatenate((data, new_element), axis=1)

        return self.__model.predict(data)

    def three_days(self, data: np.array) -> int:
        new_first_element = np.array([self.one_day(data)])
        new_second_element = np.array([self.two_days(data)])

        for i in range(2):
            data = np.delete(data, 0, 1)

        data = np.concatenate((data, new_first_element, new_second_element),
                              axis=1)

        return self.__model.predict(data)

    def four_days(self, data: np.array) -> int:
        new_first_element = np.array([self.one_day(data)])
        new_second_element = np.array([self.two_days(data)])
        new_third_element = np.array([self.three_days(data)])

        for i in range(3):
            data = np.delete(data, 0, 1)
        data = np.concatenate((data, new_first_element, new_second_element,
                               new_third_element), axis=1)

        return self.__model.predict(data)

    def five_days(self, data: np.array) -> int:
        new_first_element = np.array([self.one_day(data)])
        new_second_element = np.array([self.two_days(data)])
        new_third_element = np.array([self.three_days(data)])
        new_four_element = np.array([self.four_days(data)])

        for i in range(4):
            data = np.delete(data, 0, 1)

        data = np.concatenate((data, new_first_element, new_second_element,
                               new_third_element, new_four_element), axis=1)

        return self.__model.predict(data)
