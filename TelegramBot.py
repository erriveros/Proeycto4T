import requests
import time
import telebot
import urllib
import json
import telepot
import os
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class User:
    loggedInstagram = False
    loggedSaf = False
    loggedGmail = False

    current_screen = "main"

    instagramAccountBool = False
    safUserBool = False
    safPassBool = False
    gmailUserBool = False
    gmailPassBool = False

    instagramAccount = ""
    safUser = ""
    safPass = ""
    gmailUser = ""
    gmailPass = ""

    instagramImages = []
    pos_instagram: int = 0

    def __init__(self, id):
        self.id = id


TOKEN = "802624766:AAGFeusIY0pHAjasyJiheR14QD6mjDsIclE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

bot = telebot.TeleBot(TOKEN)


def scrap_instagram(account_name):
    print("scraping instagram account...")
    args = "--account " + account_name
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


def main_menu(chat, loggedInstagram, loggedSaf, loggedGmail, current):
    if loggedGmail or loggedInstagram or loggedSaf:
        btns = []
        # send_message("Elija alguna opcion a la que quiera ver informacion", chat)
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
        # send_inline(chat, ["Volver a Menu"], "Para volver al menu")

    return current


users = []
last_update_id = None
print("chat bot running...")
while True:
    U = None
    updates = get_updates(last_update_id)
    if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        update_info = get_last_chat_id_info(get_updates())
        text = update_info['text']
        chat = update_info['chat_id']
        user_info = update_info['user_info']
        message_id = update_info['message_id']
        for user in users:
            if user.id == chat:
                U = user
                break
        if U is None:
            U = User(chat)
            users.append(U)
        print(text)
        print(update_info)
        if text == "Volver al Menu":
            U.current_screen = 'main'
            U.current_screen = main_menu(U.id, U.loggedInstagram, U.loggedSaf, U.loggedGmail, U.current_screen)
        elif text == "Instagram" and U.loggedInstagram is False:  # Logear Instagram
            U.current_screen = "instagram account"
            bot.send_message(U.id, "Ingresa el nombre de la cuenta de Instagram que deseas seguir.")
            U.instagramAccountBool = True
        elif U.instagramAccountBool:
            U.current_screen = "instagram logged in"
            U.instagramAccount = text
            # Aqui se accede a Instagram, el nombre de la cuenta de usuario de Instagram es la variable instagramUser
            bot.send_message(U.id, "Revisando cuenta para estar al tanto de las últimas noticias")
            scrap_instagram(U.instagramAccount)
            bot.send_message(U.id, "Actualización completa")
            jsoninput = open(U.instagramAccount + "_data.json", "r")
            dataInstagram_s = jsoninput.read()
            dataInstagram = json.loads(dataInstagram_s)
            U.instagramImages = dataInstagram['media']
            temp = []
            temp = U.instagramImages[:]
            elementos_borrados = 0
            for i in range(0, len(U.instagramImages)):
                if U.instagramImages[i]['url'] == "":
                    del(temp[i-elementos_borrados])
                    elementos_borrados += 1
                if U.instagramImages[i]['post_caption'] == "":
                    del(temp[i-elementos_borrados])
                    elementos_borrados += 1
            U.instagramImages = temp[:]
            print(U.instagramImages)
            # bot.send_message(chat, "Tu usuario de Instagram es: " + text)
            U.instagramAccountBool = False
            U.loggedInstagram = True
            send_reply_keyboard(U.id, ["Ver publicaciones"], "Selecciona una opcion")

        elif text == "Saf" and U.loggedSaf is False:  # Logear Saf
            U.current_screen = "saf user"
            bot.send_message(U.id, "Ingresa el email de tu cuenta de Saf.")
            U.safUserBool = True
        elif U.safUserBool and U.safPassBool is False:
            U.current_screen = "saf pass"
            bot.send_message(U.id, "Ingresa la contraseña de tu cuenta de Saf.")
            U.safUser = text
            U.safPassBool = True
        elif U.safUserBool and U.safPassBool:
            U.current_screen = "saf logged in"
            U.safPass = text
            # Aqui se accede a Saf, el email es la variable safUser y la contraseña es la variable safPass
            # bot.send_message(chat, "Tu email es: " + safUser + " y tu contraseña es: " + safPass)
            bot.send_message(U.id, "Revisando cuenta para estar al tanto de las ultimas noticias.")
            time.sleep(3)
            bot.send_message(U.id, "Saf inicializado!")
            U.safUserBool = False
            U.safPassBool = False
            U.loggedSaf = True

        elif text == "Gmail" and U.loggedGmail is False:  # Logear Gmail
            U.current_screen = "gmail user"
            bot.send_message(U.id, "Ingresa el email de tu cuenta de Gmail.")
            U.gmailUserBool = True
        elif U.gmailUserBool and U.gmailPassBool is False:
            U.current_screen = "gmail pass"
            bot.send_message(U.id, "Ingresa la contraseña de tu cuenta de Gmail.")
            U.gmailUser = text
            U.gmailPassBool = True
        elif U.gmailUserBool and U.gmailPassBool:
            U.current_screen = "gmail logged in"
            U.gmailPass = text
            # Aqui se accede a Gmail, el email es la variable gmailUser y la contraseña es la variable gmailPass
            # bot.send_message(chat, "Tu email es: " + gmailUser + " y tu contraseña es: " + gmailPass)
            U.gmailUserBool = False
            U.gmailPassBool = False
            U.loggedGmail = True

        elif text == "Login":
            U.current_screen = "login"
            send_reply_keyboard(U.id, ["Instagram", "Saf", "Gmail"], "¿Qué servicio quieres iniciar sesion?")

        elif text == "@Instagram" and U.loggedInstagram:
            U.current_screen = "instagram options"
            send_reply_keyboard(U.id, ["Ver publicaciones"], "Selecciona una opcion")

        elif text == "Ver publicaciones" and U.loggedInstagram or U.current_screen == "watching instagram posts":
            if text == "Siguiente":
                U.pos_instagram += 1
                U.current_screen = "watching instagram posts"
                bot.send_message(U.id, U.pos_instagram)
                if U.instagramImages[U.pos_instagram]['img_text_content'] != '':
                    bot.send_message(U.id, U.instagramImages[U.pos_instagram]['img_text_content'])
                bot.send_message(U.id, U.instagramImages[U.pos_instagram]['post_caption'])
            elif text == "Anterior":
                U.pos_instagram -= 1
                U.current_screen = "watching instagram posts"
                bot.send_message(U.id, U.pos_instagram)
                if U.instagramImages[U.pos_instagram]['img_text_content'] != '':
                    bot.send_message(U.id, U.instagramImages[U.pos_instagram]['img_text_content'])
                bot.send_message(U.id, U.instagramImages[U.pos_instagram]['post_caption'])
            elif text == "Fuente original":
                bot.send_message(U.id, U.instagramImages[U.pos_instagram]['url'])
            else:
                U.current_screen = "watching instagram posts"
                bot.send_message(U.id, U.pos_instagram)
                if U.instagramImages[U.pos_instagram]['img_text_content'] != '':
                    bot.send_message(U.id, U.instagramImages[U.pos_instagram]['img_text_content'])
                bot.send_message(U.id, U.instagramImages[U.pos_instagram]['post_caption'])
            if U.pos_instagram == 0 and text != "Fuente original":
                send_inline(U.id, ["Fuente original", "Siguiente", "Volver al Menu"], "Opciones")
            elif 0 < U.pos_instagram < len(U.instagramImages) - 1 and text != "Fuente original":
                send_inline(U.id, ["Anterior", "Fuente original", "Siguiente", "Volver al Menu"], "Opciones")
            elif U.pos_instagram == len(U.instagramImages) - 1 and text != "Fuente original":
                send_inline(U.id, ["Anterior", "Fuente original", "Volver al Menu"], "Opciones")
            elif U.pos_instagram == 0 and text == "Fuente original":
                send_inline(U.id, ["Siguiente", "Volver al Menu"], "Opciones")
            elif 0 < U.pos_instagram < len(U.instagramImages) - 1 and text == "Fuente original":
                send_inline(U.id, ["Anterior", "Siguiente", "Volver al Menu"], "Opciones")
            elif U.pos_instagram == len(U.instagramImages) - 1 and text == "Fuente original":
                send_inline(U.id, ["Anterior", "Volver al Menu"], "Opciones")
        else:
            U.current_screen = "main"

            # send_message("MENSAGE HARCODIADO", chat)
        print(U.current_screen)
        if U.current_screen == 'main' and text != "Volver al Menu":
            U.current_screen = 'main'
            U.current_screen = main_menu(U.id, U.loggedInstagram, U.loggedSaf, U.loggedGmail, U.current_screen)
        if U.current_screen == "instagram logged in" or U.current_screen == "saf logged in" or U.current_screen == "gmail logged in" or (
                U.current_screen == "login" and U.loggedGmail and U.loggedSaf and U.loggedInstagram):
            send_inline(U.id, ["Volver al Menu"], "Para volver al menu")

    time.sleep(0.5)
