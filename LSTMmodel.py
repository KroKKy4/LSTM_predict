import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential


class Model:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__sc = 0.00267773
        self.__min = -0.03788995
        self.__scaler = MinMaxScaler(feature_range=(0, 1))
        self.__model = Sequential()

    def __read_and_normalize_data_for_tr(self):
        data = pd.read_excel(self.__file_path)

        train = pd.DataFrame(data[0: len(data)])
        train_close = train.iloc[:, 4:5].values

        data_training_array = self.__scaler.fit_transform(train_close)
        self.__min = self.__scaler.min_
        self.__sc = self.__scaler.scale_
        return data_training_array

    def read_and_normalize_data_for_tests(self, file_path):
        data = pd.read_excel(file_path)
        test = pd.DataFrame(data[0: len(data)])

        test_close = test.iloc[:, 4:5].values
        test_df = pd.DataFrame(test_close)

        x_test = []
        x_test.append(test_df * self.__sc + self.__min)
        x_test = np.array(x_test)

        return x_test

    def get_scaler_params(self):
        return (self.__min, self.__sc)

    def save_model(self,
                   file_path: str) -> None:
        self.__model.save(file_path)

    def __construct_model(self,
                          x_train: np.array,
                          y_train: np.array) -> None:
        self.__model.add(LSTM(units=100, activation='tanh',
                              return_sequences=True,
                              input_shape=(x_train.shape[1], 1)))

        self.__model.add(Dropout(0.1))

        self.__model.add(LSTM(units=200, activation='tanh'))

        self.__model.add(Dense(units=1))

        self.__model.compile(optimizer='adam', loss='mean_absolute_error',
                             metrics=[tf.keras.metrics.MeanAbsoluteError()])
        self.__model.fit(x_train, y_train, epochs=100)

    def create_model(self) -> None:
        data_training_array = self.__read_and_normalize_data_for_tr()

        x_train = []
        y_train = []

        for i in range(100, data_training_array.shape[0]):
            x_train.append(data_training_array[i-100: i])
            y_train.append(data_training_array[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        self.__construct_model(x_train, y_train)
