import requests
import random
import telegram
import os
from telebot import types, telebot  # pip install pyTelegramBotAPI
from bs4 import BeautifulSoup as b
from datetime import datetime




TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')


WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f"/webhook/{TOKEN[1:]} + '1029' " 
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


bot = telebot.TeleBot(TOKEN )
URL_news = "https://www.mk.ru/news/"
URL_weather_mail = "https://pogoda.mail.ru/prognoz/krasnodar/"
URL_ctft1me = "https://ctftime.org/event/list/upcoming"
time_sleep = 3
value = ""
old_value = ""
chat_id = [-1001503717052, -480696228, 465424337, 465424337]  
adm_list = ['W_N_S_e_e', 'bubalexoleh']  
user_list = [465424337, 495470522, -1001503717052,
             -480696228, 465424337] 
all_list = ['W_N_S_e_e', 'instructor_pamir', 'Aladins9', 'upsnake', 'Cyber_Tempest', 'kop73r', 'mqxmm', 'kot312',
            'Raymanky', 'comrade_n_co', 'IH87H3WH013FUCKIN6W0R1D', 'john_shefer',
            'cheat3r']  


URL_ctfnews = "https://ctfnews.ru/"


def news(url):
    req = requests.get(url)
    soup = b(req.text, 'html.parser')
    news_list = soup.find_all('h3', "news-listing__item-title")
    time_list = soup.find_all('span', "news-listing__item-time")
    i = []
    j = []
    new_s = ''
    time_1 = datetime.strptime(f"{datetime.now().hour}:{datetime.now().minute}:00", "%H:%M:%S")
    for c in time_list:
        i.append(str(c.text))
    for c in news_list:
        j.append(str(c.text))
    for p in range(10):
        time_2 = datetime.strptime(f'{i[p][:2]}:{i[p][3:]}:00', "%H:%M:%S")
        try:
            if int(str(time_1 - time_2)[2:4]) <= 59 and int(str(time_1 - time_2)[:1]) == 0:
                new_s += '❗' + i[p] + ' ' + j[p] + '\n'
        except:
            if int(str(time_1 - time_2)[10: 12]) <= 59 and int(str(time_1 - time_2)[8:9]) == 0:
                new_s += '❗' + i[p] + ' ' + j[p] + '\n'
    return new_s


def weather(url):
    req = requests.get(url)
    soup = b(req.text, 'html.parser')
    date = soup.find_all('div', "information__header__left__date")
    date += soup.find_all('div', "information__content__temperature")
    date += soup.find_all('div', "information__content__additional__item")
    j = ''
    for p, c in enumerate(date):
        i = str(c.text)
        if p != 8:
            new_text = ' '.join(i.split())
            j += new_text + '\n'
    return j


def ctftime(url):
    req = requests.get(url, headers={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"})
    soup = b(req.text, 'html.parser')
    challenge = soup.find_all('td')
    ad2 = 'https://ctftime.org'
    chal = ''

    for idx, c in enumerate(challenge):

        if idx <= 33:
            if (idx + 1) % 7 == 1:
                chal += "<a href='" + ad2 + str(b(str(challenge[idx]), 'lxml').a.get('href')) + "'>" + str(
                    challenge[idx])[26:-9] + " </a>"
            elif (idx + 1) % 7 != 0 and (idx + 1) % 7 != 5 and (idx + 1) % 7 != 6:
                i = str(c.text)
                new_text = ' '.join(i.split())
                chal += new_text + ' '
            else:
                chal += '\n'
    return chal


def keyboard_for_calc():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                 telebot.types.InlineKeyboardButton("C", callback_data="C"),
                 telebot.types.InlineKeyboardButton("<=", callback_data="<="),
                 telebot.types.InlineKeyboardButton("/", callback_data="/"))

    keyboard.row(telebot.types.InlineKeyboardButton("7", callback_data="7"),
                 telebot.types.InlineKeyboardButton("8", callback_data="8"),
                 telebot.types.InlineKeyboardButton("9", callback_data="9"),
                 telebot.types.InlineKeyboardButton("*", callback_data="*"))

    keyboard.row(telebot.types.InlineKeyboardButton("4", callback_data="4"),
                 telebot.types.InlineKeyboardButton("5", callback_data="5"),
                 telebot.types.InlineKeyboardButton("6", callback_data="6"),
                 telebot.types.InlineKeyboardButton("-", callback_data="-"))

    keyboard.row(telebot.types.InlineKeyboardButton("1", callback_data="1"),
                 telebot.types.InlineKeyboardButton("2", callback_data="2"),
                 telebot.types.InlineKeyboardButton("3", callback_data="3"),
                 telebot.types.InlineKeyboardButton("+", callback_data="+"))

    keyboard.row(telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                 telebot.types.InlineKeyboardButton("0", callback_data="0"),
                 telebot.types.InlineKeyboardButton(",", callback_data="."),
                 telebot.types.InlineKeyboardButton("=", callback_data="="))
    return keyboard


def keyboard_for_mes():
    keyboard = [[telegram.InlineKeyboardButton("Option 1", callback_data='1'),
                 telegram.InlineKeyboardButton("Option 2", callback_data='2')],

                [telegram.InlineKeyboardButton("Option 3", callback_data='3')]]
    return keyboard


def delete_message(seconds, messages_from_user_id, a_message_id):
    need_seconds = seconds
    current_time = datetime.now()
    last_datetime = datetime.now()

    while -int((current_time - last_datetime).total_seconds()) < need_seconds:
        last_datetime = datetime.now()
    bot.delete_message(messages_from_user_id, a_message_id)


@bot.message_handler(commands=['start']) 
def welcome(messages):
    a = bot.send_sticker(messages.from_user.id,
                         sticker='CAACAgIAAxkBAAEFmfBi_o1kldAJWHAcSbyn4x5vkWqU4gACwwEAAlLiCBpu1WPBtdfvMCkE')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('О нас')
    item2 = types.KeyboardButton("Мероприятия")
    item3 = types.KeyboardButton("Приложения")
    markup.add(item1, item2, item3)

    bot.send_message(messages.from_user.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <u>{1.first_name}</u>, "
                     "бот команды <b>Team8</b>, создан для того, чтобы помочь Вам ❗ \n"
                     .format(messages.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    bot.delete_message(messages.chat.id, messages.message_id)  # Верно
    delete_message(time_sleep, messages.from_user.id, a.message_id)

@bot.message_handler(commands=['stop'])  # Обработка команды для выхода
def bye(messages):
    hideboard = types.ReplyKeyboardRemove()
    bot.send_message(messages.from_user.id, '\ud83d\udd96'.encode('utf16', errors='surrogatepass').decode('utf16'))
    bot.send_message(messages.from_user.id,
                     "До свидания, {0.first_name}!\nМы, команда <b>Team8</b>, надеемся, что ты хорошо провел(а) время \n"
                     "P.S.: Если есть какие-то пожелания или вопросы по боту, то напиши <a href='tg://user?id=465424337'>мне</a> ".format(
                         messages.from_user, bot.get_me()), parse_mode='html', reply_markup=hideboard)
    bot.delete_message(messages.chat.id, messages.message_id)


@bot.message_handler(commands=["all"])
def allmes(messages):
    if messages.chat.type != "private":
        if messages.chat.id in chat_id:
            result = bot.get_chat_administrators(messages.chat.id)
            admin_list = []
            for Rqu in result:
                req = str(Rqu).split()
                admin_list.append(str(req[8])[1:-2])
            nick = messages.from_user.username
            # if nick not in admin_list:      # Pay function :)
            if nick not in adm_list:
                bot.send_message(messages.from_user.id, 'Ты че Олег что-ли?! 🤬')
                bot.delete_message(messages.chat.id, messages.message_id)
            else:
                bot.send_message(messages.chat.id, '@' + " @".join(all_list) + ' Ало блять❗')
                bot.delete_message(messages.chat.id, messages.message_id)

        else:
            bot.send_message(messages.from_user.id, 'Тебе не разрешен доступ, бродяга! 🤬')
            bot.delete_message(messages.chat.id, messages.message_id)
    else:
        bot.send_message(messages.from_user.id, 'Не, так дело не пойдет 🤬')
        bot.delete_message(messages.chat.id, messages.message_id)


@bot.message_handler(commands=["calculater"])
def go_send_messages(call):
    global value
    if value == "":
        bot.send_message(call.from_user.id, "0", reply_markup=keyboard_for_calc())
    else:
        bot.send_message(call.from_user.id, value, reply_markup=keyboard_for_calc())
    bot.delete_message(call.chat.id, call.message_id)


@bot.message_handler(func=lambda messages: messages.chat.id not in user_list)
def some(messages):
    a = bot.send_message(messages.chat.id, 'Не дозволено общаться с незнакомцами! 🤬')
    bot.delete_message(messages.chat.id, messages.message_id)
    delete_message(time_sleep, messages.from_user.id, a.message_id)


@bot.message_handler(func=lambda messages: True, content_types=['text'])
def go_send_messages(messages):
    if messages.text == "О нас":
        bot.send_message(messages.from_user.id, "\u270c\ufe0f")
        bot.send_message(messages.from_user.id,
                         "Команда <u>Team8</u> - настоящие хацкеры 😈", parse_mode="html")
        bot.delete_message(messages.chat.id, messages.message_id)

    elif messages.text == "Мероприятия":
        one_markup = types.InlineKeyboardMarkup(row_width=1)
        ite1 = types.InlineKeyboardButton("CTF time", callback_data="ctftime")
        ite2 = types.InlineKeyboardButton("CTF news", callback_data="ctfnews")
        one_markup.add(ite1, ite2)
        a = bot.send_message(messages.chat.id,
                             "Кажется ты хочешь позаниматься?\nМы постарались разбить их на следующие составляющие:".format(
                                 messages.from_user),
                             parse_mode="html", reply_markup=one_markup)
        bot.delete_message(messages.chat.id, messages.message_id)
        delete_message(time_sleep, messages.chat.id, a.message_id)

    elif messages.text == "Приложения":
        keyboard_p = types.InlineKeyboardMarkup(row_width=1)
        itemboo = types.InlineKeyboardButton(text="Google", url="https://google.com")
        itemboo1 = types.InlineKeyboardButton('Рандомное число', callback_data='rand')
        itemboo2 = types.InlineKeyboardButton("Калькулятор", callback_data='calc')
        itemboo3 = types.InlineKeyboardButton("Прогноз погоды на сегодня", callback_data='weather')
        itemboo4 = types.InlineKeyboardButton("Новости", callback_data='news')
        itemboo5 = types.InlineKeyboardButton("Oleg function", callback_data='oleg')

        keyboard_p.add(itemboo, itemboo1, itemboo2, itemboo3, itemboo4, itemboo5)

        a = bot.send_message(messages.chat.id,
                             "{0.first_name}, окей, смотри, что у нас тут есть:\n".format(messages.from_user),
                             reply_markup=keyboard_p)
        bot.delete_message(messages.chat.id, messages.message_id)
        delete_message(time_sleep, messages.chat.id, a.message_id)

    elif messages.text == 'get_id':
        a = bot.send_message(messages.chat.id, messages.from_user.id)
        bot.delete_message(messages.chat.id, messages.message_id)
        delete_message(time_sleep, messages.chat.id, a.message_id)


@bot.callback_query_handler(
    func=lambda call: call.data in ['ctftime', 'ctfnews', 'rand', 'calc', 'weather', 'news', 'oleg'])  # Мероприятия
def callback_inline_one(call):
    try:
        if call.message:
            if call.data == 'ctftime':  
                bot.send_message(call.from_user.id, "Ближайшие мероприятия:\n\n" + ctftime(URL_ctft1me),
                                 parse_mode="html")

            elif call.data == 'ctfnews':  
                bot.send_message(call.from_user.id, "")

            elif call.data == 'rand':
                bot.send_message(call.from_user.id, str(random.randint(0, 1000)))

            elif call.data == 'weather':
                bot.send_message(call.from_user.id, weather(URL_weather_mail))

            elif call.data == 'calc':
                bot.send_message(call.from_user.id, '/calculater')

            elif call.data == 'news':
                bot.send_message(call.from_user.id, '🧾 Ближайшие новости:\n\n' + news(URL_news))

            elif call.data == 'oleg':
                bot.send_message(call.message.chat.id, f'/all')

            elif call.data == 'callback':
                bot.answer_callback_query(
                    # call.id,
                    call.message.chat.id,
                    text='Hello! This callback.',
                    show_alert=True
                )
    except:
        bot.send_message(call.from_user.id,
                         "Вероятно, что это еще в разработке !😅")


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == "no":
        pass
    elif data == "C":
        value = ""
    elif data == "=":
        try:
            value = str(eval(value))
        except:
            value = "Ошибка!"
    else:
        value += data

    if value != old_value:
        if value == "":
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="0",
                                  reply_markup=keyboard_for_calc())
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,
                                  reply_markup=keyboard_for_calc())

    old_value = value
    if value == "Ошибка!":
        value = ""


if __name__ == "__main__":

    try:
        bot.skip_pending = True
        bot.polling(none_stop=True)
        #on_startup
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)
    finally:
        print("Здесь всё закончилось")
