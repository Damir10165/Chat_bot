# -*- coding: utf-8 -*-
import telebot;

TOKEN = '2058891414:AAGbCQ1B-DDBt6p3llwB-Vuz0qxQsTmrYVo'
bot = telebot.TeleBot(TOKEN)
covid_list = ['covid', 'корона', 'ковид', 'corona']

# словарь, который хранит данные по принципу:
# словарь(id чата : словарь(id пользователя : количество повторений))
data_base = {}

# словарь, для сопоставления id пользователя и имени
name_base = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    # заносим id нового чата в базу данных
    data_base[message.chat.id] = {}

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "/stats - информация о людях, интерсовавшихся короновирусной инфекцией.")

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if data_base[message.chat.id] == {}:
        bot.send_message(message.chat.id, "Людей, интерсовавшихся короновирусной инфекцией, нет.")
    else:
        # вывод информации о людя, которые были заинтересованны в информации о коронавирусе
        Message = ''
        for i in data_base[message.chat.id]:
            Message += 'ID: ' + str(i) + ' Имя: ' + name_base[i] + ' Кол-во запросов: ' + str(data_base[message.chat.id][i]) + '\n'
        bot.send_message(message.chat.id, Message)

@bot.message_handler(content_types=['text'])
def get_message(message):

    res = -1
    # разбиваем сообщение на лексемы
    list_text = message.text.split()
    for i in list_text:
        for j in covid_list:
            # если было найденно подходящее слово, то записывем пользователя в базу данных
            res = i.lower().find(j)
            if res != -1:
               bot.reply_to(message, "Есть подозрение на наличие информации о короновиресной инфекции в вашем сообщении.")
               ID = message.from_user.id
               Name = ''
               if message.from_user.first_name is not None:
                   Name += message.from_user.first_name + ' '
               if message.from_user.last_name is not None:
                   Name += message.from_user.last_name + ' '
               if message.from_user.username is not None:
                   Name += message.from_user.username 
               if ID in data_base[message.chat.id]:
                   data_base[message.chat.id][ID] += 1
               else:
                   data_base[message.chat.id][ID] = 1
                   name_base[ID] = Name

@bot.my_chat_member_handler()
def get_message_update(message):
    new_chat = message.new_chat_member
    if new_chat.status == "left":
        del data_base[message.chat.id]
        print("delete bot from chat is successful")

bot.polling(none_stop=True, interval=0)
