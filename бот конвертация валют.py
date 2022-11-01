import telebot
import requests
import json
import traceback
TOKEN = '5555832495:AAELdDcSPIHrfEsgZBR0zHiiRCcUaqciZhI'


keys = {
    'евро': 'EUR',
    'рубль': 'RUB',
    'доллар': 'USD',
}

bot = telebot.TeleBot(TOKEN)

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}')
        resp = json.loads(r.content)
        new_price = resp[qoute_key] * float(amount)
        new_price = round(new_price, 3)
        message =f"Цена {amount} {base} в {quote} : {new_price}"
        return message


@bot.message_handler(commands = ['values'])
def available_currencies(message: telebot.types.Message):
    text = 'Доступные валюты'
    for k in keys.keys():
        text = '\n'.join(text, k)
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)



bot.polling()