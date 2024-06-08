import os
from datetime import timedelta
from decimal import Decimal

from dotenv import load_dotenv
from openpyxl import Workbook

from tinkoff.invest import CandleInterval, Client, Quotation
from tinkoff.invest.schemas import CandleSource
from tinkoff.invest.utils import now

load_dotenv()


def convert_quotation(quotation: Quotation):
    if quotation.units == 0 and quotation.nano == 0:
        big_decimal = Decimal('0')
    else:
        big_decimal = (Decimal(quotation.units) + Decimal(quotation.nano)
                       / Decimal(10 ** 9))
    return big_decimal


class ConvertFromExcel:
    def __init__(self, file_path):
        self.__workbook = Workbook()
        self.__sheet = self.__workbook.active
        self.__sheet.append(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        self.__file_path = file_path

    def serialize_candle(self, candle):
        self.__sheet.append([candle.time.strftime('%Y-%m-%d'),
                             convert_quotation(candle.open),
                             convert_quotation(candle.high),
                             convert_quotation(candle.low),
                             convert_quotation(candle.close),
                             candle.volume])

    def save(self):
        self.__workbook.save(self.__file_path)

    def __del__(self):
        self.__workbook.save(self.__file_path)
        self.__workbook.close()


class TinkoffClient:
    def __init__(self,
                 count_days: int,
                 instrument_id: str):
        self.__TOKEN = os.getenv('TINKOFF_TOKEN')
        self.__count_days = count_days
        self.__instrument_id = instrument_id

    def serialize_candles(self,
                          serializer: ConvertFromExcel) -> None:
        with Client(self.__TOKEN) as client:
            for candle in client.get_all_candles(
                instrument_id=self.__instrument_id,
                from_=now() - timedelta(days=self.__count_days),
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
                candle_source_type=CandleSource.CANDLE_SOURCE_UNSPECIFIED,
            ):
                serializer.serialize_candle(candle)
