import telebot
from extensions import DataCheck, Converting, APIException
from constants import TOKEN, help_, currencies


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', ])
def start(message):
    bot.send_message(message.chat.id, text=f'Здравствуйте, {message.chat.first_name}! \n{help_}')

@bot.message_handler(commands=['help', ])
def help(message):
    bot.send_message(message.chat.id, text=help_)

@bot.message_handler(commands=['values', ])
def values(message):
    text = 'Доступные валюты:\n'
    for key in currencies.keys():
        text += key + '\n'
    bot.send_message(message.chat.id, text=text)

@bot.message_handler(content_types=['text', ])
def converting(message: telebot.types.Message):
    try:
        if DataCheck.datacheck(message):
            data = message.text.split(' ')
            base, quote, amount = data
            price = Converting.get_price(base, quote, amount) * eval(amount)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
        raise APIException
    else:
        bot.send_message(message.chat.id, f'Цена {amount} {currencies.get(base)} ({base}) \
равна {price} {currencies.get(quote)} ({quote})')

bot.infinity_polling()
