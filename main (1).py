import threading
import time

from LSTMmodel import Model
from tgbot import TelegramBot
from tinkoff import ConvertFromExcel, TinkoffClient

TICKET = 'BBG004730N88'
MONTH = 30 * 24 * 3600
DAY = 24 * 3600


def read_candles(file_path, window):
    client = TinkoffClient(window, TICKET)
    serializer = ConvertFromExcel(file_path)
    client.serialize_candles(serializer)
    serializer.save()


def window(file_path='window.xlsx', window=145):
    while True:
        read_candles(file_path, window)
        time.sleep(DAY)


def model_learn(model, file_path='data.xlsx', window=6000):
    while True:
        time.sleep(MONTH)
        read_candles(file_path, window)
        model.create_model()
        model.save_model('keras_model.keras')


def main():
    model = Model('data.xlsx')
    threading.Thread(target=window).start()
    threading.Thread(target=model_learn, args=(model,)).start()

    tg_bot = TelegramBot(model, 'window.xlsx')
    tg_bot.start()

    return 0


if __name__ == '__main__':
    main()
