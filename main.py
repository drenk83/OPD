import telebot
import difflib

import random
from telebot import types

import sqlite3
way = 'C:\Dev\gr\db.sqlite' # путь до бд
data_table = sqlite3.connect(way)
cursor = data_table.cursor()

data = cursor.execute('SELECT * FROM data_Table').fetchall()
print(data)

voprosi = []
otveti = []
flags = []

global c
c = 0

for index in data:
    voprosi.append(index[1])

for index in data:
    otveti.append(index[2])

for index in data:
    flags.append(index[3])

bot = telebot.TeleBot('') #Сюда надо вставить короч хуйню (токен)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    veroiatnie_voprosi = difflib.get_close_matches(message.text.lower(), voprosi, n=30, cutoff=0.4)

    flag = []
    helper = []
    count = 0

    # Сдесь происходит отделение вопросов с одинаковым флагом
    for voprosik in veroiatnie_voprosi:
        if count < 3:
            number = voprosi.index(voprosik)

            if int(flags[number]) == 0:
                helper.append(voprosik)
            elif int(flags[number]) in flag:
                continue
            else:
                helper.append(voprosik)
            count = count + 1
            flag.append(int(flags[number]))

    msg = 'Меня нет'
    global c
    hlp = str(message.text)

    if helper != []:
        if len(helper) == 1:
            stroka1 = str(helper[0])
            if hlp not in voprosi:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                ans1 = types.KeyboardButton(f'{stroka1}')
                keyboard.add(ans1)
                if c == 0:
                    bot.send_message(message.chat.id, 'Возможно вы имели ввиду:', reply_markup=keyboard)
                    c = 1

        elif len(helper) == 2:
            stroka1 = str(helper[0])
            stroka2 = str(helper[1])
            if hlp not in voprosi:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                ans1 = types.KeyboardButton(f'{stroka1}')
                ans2 = types.KeyboardButton(f'{stroka2}')
                keyboard.add(ans1, ans2)
                if c == 0:
                    bot.send_message(message.chat.id, 'Возможно вы имели ввиду:', reply_markup=keyboard)
                    c = 1
        else:
            stroka1 = str(helper[0])
            stroka2 = str(helper[1])
            stroka3 = str(helper[2])
            if hlp not in voprosi:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                ans1 = types.KeyboardButton(f'{stroka1}')
                ans2 = types.KeyboardButton(f'{stroka2}')
                ans3 = types.KeyboardButton(f'{stroka3}')


                keyboard.add(ans1, ans2, ans3)
                if c == 0:
                    bot.send_message(message.chat.id, 'Возможно вы имели ввиду:', reply_markup=keyboard)
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
        print(message.text, '- нет в базе')
        bot.send_message(message.chat.id, 'Вы ввели то, чего мы пока не знаем')
        c = 0


if __name__ == "main":
    bot.infinity_polling()

bot.polling(none_stop=True, interval=0)
