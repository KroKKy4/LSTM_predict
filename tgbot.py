import os

import telebot
from dotenv import load_dotenv
from telebot import types

from predict import Predict

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))


def create_markup():
    markup = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('1 день')
    itembtn2 = types.KeyboardButton('2 дня')
    itembtn3 = types.KeyboardButton('3 дня')
    itembtn4 = types.KeyboardButton('4 дня')
    itembtn5 = types.KeyboardButton('5 дней')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    return markup
# def create_markup():
    # markup = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)

    # days = ['Первый', 'Второй', 'Третий', 'Четвертый', 'Пятый']

    # for day_label in days:
    #     itembtn = types.KeyboardButton(f'{day_label} день')
    #     markup.add(itembtn)

    # return markup


class TelegramBot:
    def __init__(self, model, file_path):
        self.__bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
        self.__predict = Predict()
        self.__model = model
        self.__file_path = file_path

        self.greetings()
        self.answer_bot()

        self.__markup = create_markup()

    def start(self):
        self.__bot.polling(none_stop=True)

    def greetings(self):
        @self.__bot.message_handler(commands=['start'])
        def start_bot(message):
            bot.send_message(message.chat.id, 'Прогнозируем цену'
                             'акции SBERBANK',
                             reply_markup=self.__markup)

    def answer_bot(self):
        @self.__bot.message_handler(func=lambda message: True)
        def echo_all(message):

            min_, scaler_ = self.__model.get_scaler_params()
            x_test = (self.__model.read_and_normalize_data_for_tests
                      ('window.xlsx'))
            if message.text == '1 день':
                bot.reply_to(message, (self.__predict.one_day(x_test)
                                       - min_)/scaler_)
            elif message.text == '2 дня':
                bot.reply_to(message, (self.__predict.two_days(x_test)
                                       - min_)/scaler_)
            elif message.text == '3 дня':
                bot.reply_to(message, (self.__predict.three_days(x_test)
                                       - min_)/scaler_)
            elif message.text == '4 дня':
                bot.reply_to(message, (self.__predict.four_days(x_test)
                                       - min_)/scaler_)
            elif message.text == '5 дней':
                bot.reply_to(message, (self.__predict.five_days(x_test)
                                       - min_)/scaler_)
            else:
                bot.reply_to(message, "Некорректная комманда")
