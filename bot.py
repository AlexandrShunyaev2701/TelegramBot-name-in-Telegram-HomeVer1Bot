#HomeVer1Bot - это имя бот для поиска его в телеграм
import telebot
import requests
import json
from bs4 import BeautifulSoup

class BotException(Exception):
    pass


TOKEN = '5856144285:AAGkM8tSdruQVOyB421xDEAVMgEjWrb3_oM'
bot = telebot.TeleBot(TOKEN)

url = "https://api.open-meteo.com/v1/forecast?latitude=47.52&longitude=42.20&daily=temperature_2m_max," \
      "temperature_2m_min,precipitation_sum,precipitation_hours," \
      "windspeed_10m_max&windspeed_unit=ms&timezone=Europe%2FMoscow"


@bot.message_handler(commands=['start'])
def hello(message: telebot.types.Message):
    bot.reply_to(message, 'Привет, я Бот! Пока я умею совсем немного, но все таки уже могу что - то тебе рассказать.'
                          'Для начала работы введи /summary')

@bot.message_handler(commands=['summary'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Я могу рассказать тебе про погоду. \n для этого введи команду /weather.'
                                      'Если тебе интересны последние новости, введи: /news')



@bot.message_handler(commands=['weather'])
def weather(message: telebot.types.Message):
    try:
        r = requests.get(url=url)
        data = json.loads(r.content)
        dayli = data["daily"]
        temp_max = dayli["temperature_2m_max"]
        temp_min = dayli["temperature_2m_min"]
        wind = dayli["windspeed_10m_max"]
        precipitation = dayli["precipitation_sum"]
        bot.send_message(message.chat.id, text=f'Сегодня в Волгодонске: \n'
                                           f'Температура воздуха: от {temp_min[0]}°С до {temp_max[0]}°С\n'
                                           f'Порывы ветра до {wind[0]} м/с\n'
                                           f'Колличество осадков: {precipitation[0]}мм')
    except BotException as e:
        bot.send_message(message.chat.id, f"Ой, кажется возникла ошибка при запросе к серверу: {e}")

@bot.message_handler(commands=["news"])
def news(message: telebot.types.Message):
    try:
        base = 'https://www.rbc.ru'
        html = requests.get(base).content
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', class_='js-news-feed-list')
        span = div.find_all('span', class_="news-feed__item__title")
        a = div.find_all('a', class_="news-feed__item js-visited js-news-feed-item js-yandex-counter")

        for _, hyp in zip(span, a):
            title = _.getText().replace('\n', '') + hyp.get('href')
            bot.send_message(message.chat.id, text=f'{title}')
    except BotException as e:
        bot.send_message(message.chat.id, f"Ой, кажется возникла ошибка при запросе к серверу: {e}")


bot.polling(none_stop=True)

