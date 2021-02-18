import telebot
import requests
from bs4 import BeautifulSoup as BS
import config

bot = telebot.TeleBot(config.token)

def parse(html):
    for i in html.select('#content'):
        t0_min = i.select('.temperature .min')[0].text
        t0_max = i.select('.temperature .max')[0].text
        t1_min = i.select('.temperature .min')[1].text
        t1_max = i.select('.temperature .max')[1].text
        text = i.select('.wDescription .description')[0].text
    return [text, t0_min, t0_max, t1_min, t1_max]   

@bot.message_handler(commands=['kiev','bobr','nizh'])
def weather(message):
    region = ''
    if message.text == '/kiev':
        region = 'киев'
    elif message.text == '/bobr':
        region = 'бобровица'
    elif message.text == '/nizh':
        region = 'нежин'
    else: print('else')               
    req = requests.get('https://sinoptik.ua/погода-'+region)
    html = BS(req.content, 'html.parser')
    temp = []
    temp = parse(html)
    bot.send_message(message.chat.id, temp[0] + '\n' + temp[1] + '  ' + temp[2] + '\nЗавтра: ' + temp[3] + '  ' + temp[4])

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Тут тебе не помогут')


if __name__ == '__main__':
    bot.polling(True)

     