#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import config
import utils
import telebot
import sqlalchemy
from telebot import types
import pickle
import time

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["menu"])
def send_menu(message, session):
    if (session.loginWait == True):
        send_start(message)
    else:
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        btns.append(types.InlineKeyboardButton(text="График", callback_data="time"))
        btns.append(types.InlineKeyboardButton(text="Контакты",callback_data="contacts"))
        btns.append(types.InlineKeyboardButton(text="Корректировка",callback_data="edit"))
        keyboard.add(*btns)

        bot.send_message(message.chat.id, utils.help_text, parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def send_start(message):
    try:
        session = utils.sessions[message.chat.id]
    except Exception:
        session = utils.simpleSession(message.chat.id)
        utils.sessions[message.chat.id] = session
        output = open('data.pkl', 'wb')
        pickle.dump(utils.sessions, output, 2)
        output.close()
    if (session.loginWait):
        bot.send_message(message.chat.id,'Введи код:')

    else:
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        btns.append(types.InlineKeyboardButton(text="Перейти в меню", callback_data="menu"))
        keyboard.add(*btns)
        bot.send_message(message.chat.id, utils.start_text, parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(commands=["time","t","ti","tim"])
def send_time(message, session):
    if (session.loginWait == True):
        send_start(message)
    else:
        utils.updateTime()
        bot.send_message(message.chat.id, utils.free_time, parse_mode='Markdown', reply_markup=time_keyboard(utils.time))


# функция выхода
@bot.message_handler(commands=["x","up"])
def exit_func(message, session): 
    session.contactWait = False
    session.timeWait = False
    #utils.sessions[message.chat.id] = session
    #output = open('data.pkl', 'wb')
    #pickle.dump(utils.sessions, output, 2)
    #output.close()
    send_menu(message, session)


# функция внесения изменений
@bot.message_handler(commands=["edit"])
def edit_func(message, session): 
    if (session.loginWait == True):
        send_start(message)
    else:
	    session.editWait = True
	    session.timeWait = False
	    session.contactWait = False
	    utils.sessions[message.chat.id] = session
	    output = open('data.pkl', 'wb')
	    pickle.dump(utils.sessions, output, 2)
	    output.close()
	    bot.send_message(message.chat.id, "Введи корректировку:")

@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
	"""обработчик нажатия инлайн кнопок"""
	try:
		session = utils.sessions[c.message.chat.id]
	except Exception:
		session = utils.simpleSession(c.message.chat.id)
		utils.sessions[c.message.chat.id] = session
	#print(c.data)
	utils.updateTime()
	for x in utils.time:
			if c.data == x.dateText:
				if session.name != '':
					keyboard = types.InlineKeyboardMarkup()
					btns = []
					btns.append(types.InlineKeyboardButton(text=session.name, callback_data="byName"))
					keyboard.add(*btns)
					bot.send_message(c.message.chat.id, "Введи фамилию:", parse_mode='Markdown', reply_markup=keyboard)
				else:
					bot.send_message(c.message.chat.id, "Введи фамилию:")
				session.timeWait = True
				session.contactWait = False
				session.time = c.data
				utils.sessions[c.message.chat.id] = session
	if c.data == "menu":
		send_menu(c.message, session)
	if c.data == "time":
		send_time(c.message, session)
	if c.data == "back":
		exit_func(c.message, session)
	if c.data == "contacts":
		send_contacts(c.message,session)
	if c.data == "byName":
		send_time_by_name(c.message, session)
	if c.data == "edit":
		edit_func(c.message, session)
	output = open('data.pkl', 'wb')
	pickle.dump(utils.sessions, output, 2)
	output.close()


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    btns.append(types.InlineKeyboardButton(text="Назад", callback_data="back"))
    keyboard.add(*btns)

    keyboardPH = types.InlineKeyboardMarkup()
    btnsPH = []
    btnsPH.append(types.InlineKeyboardButton(text="Перейти в меню", callback_data="menu"))
    keyboardPH.add(*btnsPH)
    try:
        session = utils.sessions[message.chat.id]
    except Exception:
        session = utils.simpleSession(message.chat.id)
        utils.sessions[message.chat.id] = session
        output = open('data.pkl', 'wb')
        pickle.dump(utils.sessions, output, 2)
        output.close()


    
    if session.timeWait == True:
         time = session.time.split('.')[0]
         timeText = utils.getDashboard(message.text,time)
         session.name = message.text
         bot.send_message(message.chat.id, session.time+"\n"+timeText, parse_mode='Markdown', reply_markup=keyboard)
         #session.timeWait = False
         utils.sessions[message.chat.id] = session
    if session.loginWait == True:
        if (message.text == utils.code_word):
            session.loginWait = False
            utils.sessions[message.chat.id] = session
            bot.send_message(message.chat.id, utils.start_text, parse_mode='Markdown', reply_markup=keyboardPH)
        else:
            send_start(message)
    elif session.editWait == True:
    	tempText = message.text
    	utils.makeEdit(tempText)
    	session.editWait=False
    	utils.sessions[message.chat.id] = session
    	bot.send_message(message.chat.id, "Скорректировано успешно", parse_mode='Markdown', reply_markup=keyboard)

    output = open('data.pkl', 'wb')
    pickle.dump(utils.sessions, output, 2)
    output.close()

def time_keyboard(time):
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    for x in time:
        btns.append(types.InlineKeyboardButton(text=(x.d), callback_data=(x.dateText)))
    keyboard.add(*btns)
    return keyboard

def send_time_by_name(message, session):
	keyboard = types.InlineKeyboardMarkup()
	btns = []
	btns.append(types.InlineKeyboardButton(text="Назад", callback_data="back"))
	keyboard.add(*btns)
	time = session.time.split('.')[0]

	print(time)
	timeText = utils.getDashboard(session.name,time)
	bot.send_message(message.chat.id, session.time+"\n"+timeText, parse_mode='Markdown', reply_markup=keyboard)
    #session.timeWait = False
	utils.sessions[message.chat.id] = session

def send_contacts(message, session):
    if (session.loginWait == True):
        send_start(message)
    else:
        session.contactWait = True
        session.timeWait = False
        bot.send_message(message.chat.id, "Введи фамилию:")


if __name__ == '__main__':
    while True:

        try:
        	input = open('data.pkl', 'rb')
        	utils.sessions = pickle.load(input)
        	input.close()
        	print ("Working...")
        	bot.polling(none_stop=True)
        	
        except Exception as e:
        	#print (e)
        	
        	time.sleep(15)
