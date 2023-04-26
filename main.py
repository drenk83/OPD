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

for index in data:
    voprosi.append(index[1])

for index in data:
    otveti.append(index[2])

#Словарь
# data = {i[1]: i[2] for i in data}
# print(data)

bot = telebot.TeleBot('6235533628:AAFh0CL3s52ToNoSQdrMMj2T68vjjfW4HYY') #Сюда надо вставить короч хуйню (токен)

def pars_string(mesg):
    mesg = mesg.lower()
    lst = []
    st = ''
    for sym in mesg:
        if sym.isalpha():
            st += sym
        else:
            lst.append(st)
            st = ''
    for i in lst:
        if i == '':
            lst.remove('')
    return lst

@bot.message_handler(content_types=["text"])
def any_msg(message):
    #message = message.text
    #message = message.lower
    helper = difflib.get_close_matches(message, voprosi, n=1, cutoff=0.4)

    #helper = ['system-1']

    if helper != []:
        msg = str(helper[0])
        print(msg)
        indx = voprosi.index(msg)
        print(indx)

    if msg in voprosi:
        print(message, '------------')
        bot.send_message(message.chat.id, str(otveti[indx]))
    else:
        print(message.text, '- прекол не понят')
        bot.send_message(message.chat.id, 'прекол не понят')


if __name__ == "__main__":
    bot.infinity_polling()

bot.polling(none_stop=True, interval=0)
