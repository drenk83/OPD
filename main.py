import telebot
import difflib

import random
from telebot import types

import sqlite3
way = 'C:\Dev\db.sqlite' # путь до бд
data_table = sqlite3.connect(way)
cursor = data_table.cursor()

data = cursor.execute('SELECT * FROM data_Table').fetchall()
print(data)

voprosi = []
otveti = []

global c
c = 0

for index in data:
    voprosi.append(index[1])

for index in data:
    otveti.append(index[2])

bot = telebot.TeleBot('6235533628:AAFh0CL3s52ToNoSQdrMMj2T68vjjfW4HYY') #Сюда надо вставить короч хуйню (токен)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    helper = difflib.get_close_matches(message.text.lower(), voprosi, n=3, cutoff=0.4)
    msg = 'Меня нет'
    global c

    if helper != []:
        if len(helper) == 1:
            stroka1 = str(helper[0])
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            ans1 = types.KeyboardButton(f'{stroka1}')
            keyboard.add(ans1)
            if c == 0:
                bot.send_message(message.chat.id, 'Возможно вы имели ввиду:', reply_markup=keyboard)
                c = 1

        elif len(helper) == 2:
            stroka1 = str(helper[0])
            stroka2 = str(helper[1])
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            ans1 = types.KeyboardButton(f'{stroka1}')
            ans2 = types.KeyboardButton(f'{stroka2}')
            keyboard.add(ans1, ans2)
            if c == 0:
                bot.send_message(message.chat.id, 'Варианты:', reply_markup=keyboard)
                c = 1
        else:
            stroka1 = str(helper[0])
            stroka2 = str(helper[1])
            stroka3 = str(helper[2])

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            ans1 = types.KeyboardButton(f'{stroka1}')
            ans2 = types.KeyboardButton(f'{stroka2}')
            ans3 = types.KeyboardButton(f'{stroka3}')


            keyboard.add(ans1, ans2, ans3)
            if c == 0:
                bot.send_message(message.chat.id, 'Варианты:', reply_markup=keyboard)
                c = 1

        if helper != []:
            msg = str(helper[0])
            print(msg, 'if1')
            indx = voprosi.index(msg)
            #print(indx)

        otv = message.text

        if otv in voprosi:
            print(message.text, '----------if2--')
            bot.send_message(message.chat.id, str(otveti[indx]), reply_markup=types.ReplyKeyboardRemove())
            c = 0
    else:
        print(message.text, '-else1 прекол не понят')
        bot.send_message(message.chat.id, 'прекол не понят')
        c = 0


if __name__ == "main":
    bot.infinity_polling()

bot.polling(none_stop=True, interval=0)
