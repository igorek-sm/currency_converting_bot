import requests
import json
import telebot
from constants import API_KEY, currencies


class APIException(Exception):
    pass


class DataCheck:
    @staticmethod
    def datacheck(message: telebot.types.Message):
        data = message.text.split(' ')

        if len(data) != 3:
            raise APIException('Вы должны ввести три параметра!')

        base, quote, amount = data

        if base == quote:
            raise APIException('Вы должны ввести разные валюты!')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        if amount <= 0:
            raise APIException('Количество валюты должно быть больше нуля!')

        return True


class Converting:
    @staticmethod
    def get_price(base, quote, amount):
        req = requests.get(f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}\
&base_currency={currencies.get(base)}&currencies={currencies.get(quote)}').content
        value = json.loads(req)['data'][currencies.get(quote)]['value']
        return value
