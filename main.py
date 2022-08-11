import telebot
import sqlite3
import base64
import json
import shutil
import time

print("hello")
bot = telebot.TeleBot('5227474901:AAGj1aSOg85F9f6MWyPFUkLIFZTfUfSwOdw') # Токен бота

db = sqlite3.connect('base.db', check_same_thread=False) # Открываем базу данных
sql = db.cursor()

chat = [] # Список chat_id которые подали заявку и ожидают от нас ответа
dict_with_paths_to_images = {}

TO_CHAT_ID = -1001572818047



@bot.message_handler(commands=['start']) # Обработчик команды старт
def start(message):
    print (type(message))
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard1 = telebot.types.InlineKeyboardButton(text='Создать объявление', callback_data='application')
    keyboard.add(keyboard1)
    bot.send_message(message.chat.id, 'Добро пожаловать!\n \n'
                                      'Этот бот поможет вам создать объявление для публикации в группе [Покупка Рекламы|Telegram](https://t.me/UniWoo).\n \n'
                                      'Вам нужно пройти 9 простых шагов для заполнения всей информации о продукте.'
                                      , reply_markup=keyboard, parse_mode="Markdown") # Самое первое сообщения от бота
    sql.execute('SELECT * FROM users WHERE user_id = ?', (message.chat.id,))

    if sql.fetchone() == None:
        sql.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (message.chat.id, 'none','none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', message.from_user.username, 0))
        db.commit()

@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, 'Если вы хотите опубликовать объявление, напишите /start')

@bot.callback_query_handler(func=lambda call:True)
def question(call):
    if call.data == 'application':
        sql.execute(f'SELECT * FROM users WHERE user_id = {call.message.chat.id}')
        ans = sql.fetchone()
        #status = ans[14]
        #if status == 0 or 1:
        msg = bot.send_message(chat_id=call.message.chat.id, text="*Шаг 1 из 9* \n\nПеречислите темы вашего контента в формате. \n\n#тема1 #тема2 #тема3 (не более 3-х)", parse_mode= "Markdown") # Первы # Первый вопрос

        bot.register_next_step_handler(msg, question2)
        #else:
            #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы уже подавали заявку.🚷") # Ответ если пользователь попытается подать заявку второй раз
    elif call.data == 'sent':
        sql.execute(f"""UPDATE users SET status = 1 WHERE user_id = {call.message.chat.id}""")
        db.commit()
        if (call.message.chat.id in chat):
            print(chat)
        else:
            chat.append(call.message.chat.id)
            print(chat)
        bot.send_message(chat_id=call.message.chat.id, text="Объявление размещено!") # Ответ когда пользователь отправил заявку
        sql.execute(f'SELECT * FROM users WHERE id = 1')
        ans = sql.fetchone()
        sql.execute(f'SELECT * FROM users WHERE user_id = {call.message.chat.id}')
        anss = sql.fetchone()
        ans1 = anss[2]
        ans2 = anss[3]
        ans3 = anss[4]
        ans4 = anss[5]
        ans5 = anss[6]
        ans6 = anss[7]
        ans7 = anss[8]
        ans8 = anss[9]
        ans9 = anss[10]
        ans10 = anss[11]
        username = anss[12]
        key = telebot.types.InlineKeyboardMarkup()
        key1 = telebot.types.InlineKeyboardButton(text='Принять✅', callback_data='accepted')
        key2 = telebot.types.InlineKeyboardButton(text='Отклонить❌', callback_data='reject')
        key.add(key1, key2)
        keyboard = telebot.types.InlineKeyboardMarkup()
        like_button = telebot.types.InlineKeyboardButton(text="Разместить объявление", url='t.me/PokupkaReklami_bot', callback_data='like')
        keyboard.add(like_button)

        global dict_with_paths_to_images
        with open("paths_of_images.json", "r") as read_file:
            dict_with_paths_to_images = json.load(read_file)  # Берем данные которые сейчас в json-е.
        end_of_path_of_image = dict_with_paths_to_images[str(call.message.chat.id)]
        print ("bm")
        if ans9 == 'Далее':
            bot.send_photo(TO_CHAT_ID,
                           open(str(call.message.chat.id) + '/' + end_of_path_of_image, "rb"),
                           caption=f'Объявление от @{username}:\n\n{ans1}\n*Площадка: *{ans2}\n*Описание: *{ans3}\n\n*Стоимость: *{ans5} руб.\n*Целевая аудитория:*\n{ans6}, {ans8} \n*Продукт: *{ans10}',
                           parse_mode="Markdown", reply_markup=keyboard)
            shutil.rmtree(str(call.message.chat.id))
        else:
            bot.send_photo(TO_CHAT_ID,
                           open(str(call.message.chat.id) + '/' + end_of_path_of_image, "rb"),
                           caption=f'Объявление от @{username}:\n\n{ans1}\n*Площадка: *{ans2}\n*Описание: *{ans3}\n\n*Стоимость: *{ans5} руб.\n*Целевая аудитория:*\n{ans6}, {ans8} \n*Город(а): *{ans9}\n*Продукт: *{ans10}',
                           parse_mode="Markdown", reply_markup=keyboard)
            shutil.rmtree(str(call.message.chat.id))


    if call.data == 'accepted':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы приняли заявку.✅") # Ответ если вы приняли заявку
        msm = chat[0]
        bot.send_message(msm, 'Поздравляю, вы приняты в нашу команду!✅') # Ответ тому кого вы приняли
        del chat[0]
    elif call.data == 'reject':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы отклонили заявку.❌") # Ответ если вы отклонили заявку
        msm = chat[0]
        bot.send_message(msm, 'Извините, вы нам не подходите.❌') # Ответ тому кого вы отклонили
        del chat[0]


def question2(message):
    question1 = message.text
    if question1[0] == '#':
        sql.execute(f"""UPDATE users SET answer = '{question1}' WHERE user_id = {message.chat.id}""")
        db.commit()
        msg = bot.send_message(message.chat.id,
                               '*Шаг 2 из 9* \n\nПлощадка: \n(Telegram, Ozon, ваш сайт, YouTube и т.п.)',
                               parse_mode="Markdown")  # Второй вопрос
        bot.register_next_step_handler(msg, question3)
    else:
        msg = bot.send_message(message.chat.id, 'Ошибка! Введите еще раз, используя #. Например #инвестиции')
        bot.register_next_step_handler(msg, question2)


def question3(message):
    question2 = message.text
    sql.execute(f"""UPDATE users SET answer2 = '{question2}' WHERE user_id = {message.chat.id}""")
    db.commit()
    msg = bot.send_message(message.chat.id, '*Шаг 3 из 9* \n\nКратко опишите продукт (1-2 предложения).\n\n*Например*: _Занимаюсь производством табака для кальянов и продвигаю свой аккаунт в Инстаграме._', parse_mode="Markdown")  # Второй вопрос
    bot.register_next_step_handler(msg, question4)


def question4(message):
    question3 = message.text
    sql.execute(f"""UPDATE users SET answer3 = '{question3}' WHERE user_id = {message.chat.id}""")
    db.commit()
    msg = bot.send_message(message.chat.id, '*Шаг 4 из 9* \n\nСумма, которую вы готовы *отдать* за рекламу?\n(в формате от - до, например, 1000 - 5000)', parse_mode= "Markdown") # Второй вопрос
    bot.register_next_step_handler(msg, question6)


def question6(message):
    question4 = message.text
    sql.execute(f"""UPDATE users SET answer5 = '{question4}' WHERE user_id = {message.chat.id}""")
    db.commit()
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Парни', 'Девушки', 'Неважно')
    msg = bot.send_message(message.chat.id, '*Шаг 5 из 9* \n\nЦелевая аудитория:', parse_mode= "Markdown", reply_markup=markup) # Второй вопрос
    bot.register_next_step_handler(msg, question7)

def question7(message):
    question6 = message.text
    sql.execute(f"""UPDATE users SET answer6 = '{question6}' WHERE user_id = {message.chat.id}""")
    db.commit()
    msg = bot.send_message(message.chat.id, '*Шаг 6 из 9* \n\nВозраст целевой аудитории? *ОТ* \n(в формате от - до, например, 16-40)', parse_mode= "Markdown") # Второй вопрос
    bot.register_next_step_handler(msg, question9)


def question9(message):
    question7 = message.text
    sql.execute(f"""UPDATE users SET answer8 = '{question7}' WHERE user_id = {message.chat.id}""")
    db.commit()
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Далее')
    msg = bot.send_message(message.chat.id, '*Шаг 7 из 9* \n\nГород(а):\nЕсли город не важен, нажмите Далее', parse_mode= "Markdown", reply_markup=markup) # Второй вопрос
    bot.register_next_step_handler(msg, question10)

def question10(message):
    question9 = message.text
    sql.execute(f"""UPDATE users SET answer9 = '{question9}' WHERE user_id = {message.chat.id}""")
    db.commit()
    msg = bot.send_message(message.chat.id, '*Шаг 8 из 9* \n\nУкажите ссылку на продукт, который вы хотите прорекламировать.', parse_mode= "Markdown") # Второй вопрос
    bot.register_next_step_handler(msg, question_with_photo)


def question_with_photo(message):
    question10 = message.text
    sql.execute(f"""UPDATE users SET answer10 = '{question10}' WHERE user_id = {message.chat.id}""")
    db.commit()
    bot.send_message(message.chat.id, '*Шаг 9 из 9*\n\n Отправьте *одно* фото продукта.', parse_mode= "Markdown") # Фунция finish будет вызываться из функции save_photo


def finish(message, end_of_path_of_image):
    keyboards = telebot.types.InlineKeyboardMarkup()
    keyboard2 = telebot.types.InlineKeyboardButton(text='Отправить💬', callback_data='sent')
    keyboard3 = telebot.types.InlineKeyboardButton(text='Заполнить заново🌀', callback_data='application')
    keyboards.add(keyboard2, keyboard3)

    sql.execute(f'SELECT * FROM users WHERE user_id = {message.chat.id}')
    ans = sql.fetchone()
    ans1 = ans[2]
    ans2 = ans[3]
    ans3 = ans[4]
    ans4 = ans[5]
    ans5 = ans[6]
    ans6 = ans[7]
    ans7 = ans[8]
    ans8 = ans[9]
    ans9 = ans[10]
    ans10 = ans[11]

    if ans9 == 'Далее':
        message_with_answers = f'Ваше объявление: \n\n{ans1}\n*Площадка:* {ans2}\n*Описание:* {ans3}\n\n*Стоимость:* {ans5} руб.\n*Целевая аудитория:*\n{ans6}, {ans8} \n*Продукт:* {ans10}'
        ext_photo(message, end_of_path_of_image, keyboards, message_with_answers)
    else:
        message_with_answers = f'Ваше объявление: \n\n{ans1}\n*Площадка:* {ans2}\n*Описание:* {ans3}\n\n*Стоимость:* {ans5} руб.\n*Целевая аудитория:*\n{ans6}, {ans8} \n*Город(а):* {ans9}\n*Продукт:* {ans10}'
        ext_photo(message, end_of_path_of_image, keyboards, message_with_answers)

from pathlib import Path


    #ЧАСТЬ С ФОТО
    # Сохраним изображение, которое отправил пользователь в папку `/files/%ID пользователя/photos`
@bot.message_handler(content_types=['photo'])
def save_photo(message):
    print (type(message))
    # создадим папку если её нет
    Path(str(message.chat.id) + '/photos').mkdir(parents=True, exist_ok=True)

    # сохраним изображение
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    end_of_path_of_image = file_info.file_path
    src = str(message.chat.id) + '/' + end_of_path_of_image
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    # явно указано имя файла!
    # откроем файл на чтение  преобразуем в base64
    with open(str(message.chat.id) +f'/{end_of_path_of_image}', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    # Запишем конец пути в json
    dict_with_paths_to_images[message.chat.id] = end_of_path_of_image
    with open("paths_of_images.json", "w") as write_file:
        json.dump(dict_with_paths_to_images, write_file)

    # откроем БД и запишем информацию (ID пользователя, base64, подпись к фото)
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users VALUES (?, ?, ?)', (message.chat.id, encoded_string, str(message.caption)))
    conn.commit()

    finish(message, end_of_path_of_image)


def ext_photo(message, end_of_path_of_image, keyboards, message_with_answers):
    print (end_of_path_of_image)
    # откроем БД и по ID пользователя извлечём данные base64
    conn = sqlite3.connect("test.db")
    img = conn.execute('SELECT img FROM users WHERE tlgrm_id = ?', (message.chat.id,)).fetchone()
    if img is None:
        conn.close()
        return None
    else:
        conn.close()

        # сохраним base64 в картинку и отправим пользователю
        with open(str(message.chat.id) + '/' + end_of_path_of_image, "wb") as fh:
            fh.write(base64.decodebytes(img[0]))
            bot.send_photo(message.chat.id,
                           open(str(message.chat.id) + '/' + end_of_path_of_image, "rb"),
                           caption=message_with_answers,
                           reply_markup=keyboards, parse_mode="Markdown")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(2)
            print(e)


