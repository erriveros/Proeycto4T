import requests
import time
import telebot
import urllib
import json
import telepot
import os
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "802624766:AAGFeusIY0pHAjasyJiheR14QD6mjDsIclE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

bot = telebot.TeleBot(TOKEN)

def scrap_instagram(account_name):
    print("scraping instagram account...")
    args = "--account "+ account_name
    terminal_command = r"python3 Instagram\ scrapper/main.py " + args
    os.system(terminal_command)

def send_reply_keyboard(chat_id, btns, output):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard_btns = []
    for btn in btns:
        keyboard_btns.append(telebot.types.KeyboardButton(btn))
    for btn in keyboard_btns:
        keyboard.add(btn)
    if output != "":
        bot.send_message(chat_id, output, reply_markup=keyboard)


# PARA MANDAR BOTONES
def send_inline(chat_id, btns, message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for btn in btns:
        callback_button = telebot.types.InlineKeyboardButton(text=btn, callback_data=btn)
        keyboard.add(callback_button)
    bot.send_message(chat_id, message, reply_markup=keyboard)


def get_last_chat_id_info(updates):
    num_updates = len(updates["result"])

    last_update = num_updates - 1
    if 'callback_query' in updates["result"][last_update].keys():
        user_info = updates['result'][last_update]['callback_query']['from']
        chat_id = updates['result'][last_update]['callback_query']['message']['chat']['id']
        text = updates['result'][last_update]['callback_query']['data']
        reply_of = updates['result'][last_update]['callback_query']['message']['text']
        options = updates['result'][last_update]['callback_query']['message']['reply_markup']['inline_keyboard']
        print(user_info, '\n')
        print(chat_id, '\n')
        print(text, '\n')
        print(reply_of, '\n')
        print(options)
        return {'text': text, 'chat_id': chat_id, 'user_info': user_info, 'message_id': 'inline', 'reply_of': reply_of,
                'options': options}


    else:
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        user_info = updates["result"][last_update]["message"]["from"]
        message_id = updates["result"][last_update]["message"]["message_id"]

        return {'text': text, 'chat_id': chat_id, 'user_info': user_info, 'message_id': message_id}


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    print(updates)

    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def main_menu(chat,loggedInstagram, loggedSaf, loggedGmail, current):
    if loggedGmail or loggedInstagram or loggedSaf:
        btns = []
        #send_message("Elija alguna opcion a la que quiera ver informacion", chat)
        if loggedSaf:
            btns.append('@Saf')
        if loggedInstagram:
            btns.append('@Instagram')
        if loggedGmail:
            btns.append('@Gmail')
        send_reply_keyboard(chat, btns, "Elija alguna opcion a la que quiera ver informacion")
        send_inline(chat, ['Login'], 'Para iniciar sesion')
    else:
        send_message("Debe estar inicializado sesion con algun servicio para empezar", chat)
        current = 'login'
        send_reply_keyboard(chat, ["Instagram", "Saf", "Gmail"], "¿Qué servicio quieres iniciar sesion?")
        #send_inline(chat, ["Volver a Menu"], "Para volver al menu")

    return current



loggedInstagram = False
loggedSaf = False
loggedGmail = False

current="main"

instagramAccountBool = False
safUserBool = False
safPassBool = False
gmailUserBool = False
gmailPassBool = False
last_update_id = None
print("chat bot running...")
while True:
    updates = get_updates(last_update_id)
    if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        update_info = get_last_chat_id_info(get_updates())
        text = update_info['text']
        chat = update_info['chat_id']
        user_info = update_info['user_info']
        message_id = update_info['message_id']
        print(text)
        print(update_info)
        if text == "button":
            send_inline(chat)
        if text == '@Saf':
            c = ['Arquitectura de Computadores 201920', 'Introducción a la Ingeniería de Software 201920',
                 'Proyecto Software 201920']
            send_inline(chat, c, "eliga un curso para ver informacion")
        elif current == 'main' or text == "Volver a Menu":
            current = 'main'
            print('ewew')
            current = main_menu(chat, loggedInstagram, loggedSaf, loggedGmail, current)


        elif text == "Instagram":
            bot.send_message(chat, "Ingresa el nombre de la cuenta de Instagram que deseas seguir.")
            instagramAccountBool = True
        elif instagramAccountBool:
            instagramAccount = text
            # Aqui se accede a Instagram, el nombre de la cuenta de usuario de Instagram es la variable instagramUser
            bot.send_message(chat, "Revisando cuenta para estar al tanto de las últimas noticias")
            scrap_instagram(instagramAccount)
            bot.send_message(chat, "Actualización completa, ahora puedes activar notificaciones")
            # bot.send_message(chat, "Tu usuario de Instagram es: " + text)
            instagramAccountBool = False
            loggedInstagram = True

        elif text == "Saf":
            bot.send_message(chat, "Ingresa el email de tu cuenta de Saf.")
            safUserBool = True
        elif safUserBool and safPassBool is False:
            bot.send_message(chat, "Ingresa la contraseña de tu cuenta de Saf.")
            safUser = text
            safPassBool = True
        elif safUserBool and safPassBool:
            safPass = text
            # Aqui se accede a Saf, el email es la variable safUser y la contraseña es la variable safPass
            # bot.send_message(chat, "Tu email es: " + safUser + " y tu contraseña es: " + safPass)
            bot.send_message(chat, "Revisando cuenta para estar al tanto de las ultimas noticias.")
            time.sleep(3)
            bot.send_message(chat, "Saf inicializado!")
            safUserBool = False
            safPassBool = False
            loggedSaf = True

        elif text == "Gmail":
            bot.send_message(chat, "Ingresa el email de tu cuenta de Gmail.")
            gmailUserBool = True
        elif gmailUserBool and gmailPassBool is False:
            bot.send_message(chat, "Ingresa la contraseña de tu cuenta de Gmail.")
            gmailUser = text
            gmailPassBool = True
        elif gmailUserBool and gmailPassBool:
            gmailPass = text
            # Aqui se accede a Gmail, el email es la variable gmailUser y la contraseña es la variable gmailPass
            # bot.send_message(chat, "Tu email es: " + gmailUser + " y tu contraseña es: " + gmailPass)
            gmailUserBool = False
            gmailPassBool = False

            # send_message("MENSAGE HARCODIADO", chat)
        send_inline(chat, ["Volver a Menu"], "Para volver al menu")

    time.sleep(0.5)
