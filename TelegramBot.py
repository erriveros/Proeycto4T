import requests
import time
import telebot
import urllib
import json

TOKEN = "802624766:AAGFeusIY0pHAjasyJiheR14QD6mjDsIclE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

bot = telebot.TeleBot(TOKEN)


#PARA MANDAR BOTONES
def send_inline(chat_id):
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button = telebot.types.InlineKeyboardButton(text="Yo", callback_data="Yo")
    callback_button1 = telebot.types.InlineKeyboardButton(text="No", callback_data="No")
    callback_button2 = telebot.types.InlineKeyboardButton(text="SI", callback_data="SI")

    keyboard.add(callback_button,callback_button1,callback_button2)
    bot.send_message(chat_id, 'Quien pago la cuota', reply_markup=keyboard)

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
        #if(text == "button"):
        #    send_inline(chat)
        send_message("MENSAGE HARCODIADO", chat)

    time.sleep(0.5)

