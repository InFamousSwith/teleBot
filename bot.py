import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def rules(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту следующим образом: \n<название валюты>  <в какую валюту перевести>  <количество переводимой валюты> \n Узнать доступные валюты:  /values'
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
      text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        quote, base, amount = values
        result = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(result, 2)}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
