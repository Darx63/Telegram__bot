import numpy as np
import telebot
from telebot import types # для указание типов
import config
import psycopg2

conn = psycopg2.connect(dbname = "db",
                                  user="admin",
                                  password="admin",
                                  host=os.environ.get("HOST"),
                                  port="5432")

cursor = conn.cursor()
cursor.execute('select * from coin_random cr')
records = cursor.fetchall()

eagle = records[0][0]
tails = records[0][1]

bot = telebot.TeleBot(os.environ.get("TOKEN"));

@bot.message_handler(commands=['help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🪙 Подкинь монету")
    btn2 = types.KeyboardButton("Результаты")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="""Привет, {0.first_name}! Выбери "Подкинь монету" для подбрасывания монеты.\nДля просмотра результатов, выбери "Результаты" """.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Подкинь монету" or message.text == "подкинь монету" or message.text == "🪙 Подкинь монету":
        coin = int(np.random.randint(2, size = 1))
        if coin == 1:
            global eagle
            eagle = eagle + 1
            cursor.execute("UPDATE coin_random SET eagle = %s", (eagle,))
            conn.commit()
            bot.send_message(message.from_user.id, "Орёл")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("🪙 Подкинь монету")
            btn2 = types.KeyboardButton("Результаты")
            markup.add(btn1, btn2)
        else:
            global tails
            tails = tails + 1
            cursor.execute("UPDATE coin_random SET tails = %s", (tails,))
            conn.commit()
            bot.send_message(message.from_user.id, "Решка")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("🪙 Подкинь монету")
            btn2 = types.KeyboardButton("Результаты")
            markup.add(btn1, btn2)
    elif message.text == "Результаты":
        bot.send_message(message.from_user.id, "За всё время выпал орёл "+ str(eagle) + " раз, решка "+ str(tails) + " раз. \nПроцент выпадения составляет: орёл - "
                        + str(eagle/(eagle+tails)*100)[:5] + "%, решка - " + str(tails/(eagle+tails)*100)[:5]+ "%")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🪙 Подкинь монету")
        btn2 = types.KeyboardButton("Результаты")
        markup.add(btn1, btn2)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)


