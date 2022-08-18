import os
import telebot
from telebot import types
import sqlite3
from datetime import datetime
bot = telebot.TeleBot('5238517183:AAHkdru03SWwWiPpvzSNFGLXRyXhWKl2wnw')
admin_id = ''


def convert_to_binary_data(filename):
    file = open(filename, 'rb')
    blob_data = file.read()
    return blob_data


def convert_to_not_binary_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
    img = open(file_name, 'rb')
    return img


@bot.message_handler(commands=['start'])
def start(message):
    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Регистрация")
    btn2 = types.KeyboardButton("Авторизация")
    markup_main.add(btn1, btn2)

    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text='👋Добрый день, пройдите авторизацию', reply_markup=markup_main)


@bot.message_handler(content_types=['text'])
def func(message):
    global max_count
    message_arr = message.text.split()

    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📸 Отчет")
    btn2 = types.KeyboardButton("📜 Примеры работ")
    btn3 = types.KeyboardButton("🗣️ Финансовый отдел")
    btn4 = types.KeyboardButton("🧾 График работы")
    btn5 = types.KeyboardButton("📑 Правила работы")
    btn6 = types.KeyboardButton("Функции администратора")
    markup_main.add(btn1, btn2, btn3, btn4, btn5, btn6)

    markup_return = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Вернуться в главное меню")
    markup_return.add(button1)

    markup_return_1 = types.ReplyKeyboardMarkup(resize_keyboard=True) # Случай с примерами работ
    button1_ret = types.KeyboardButton("Вернуться в глaвное меню")
    markup_return_1.add(button1_ret)

    markup_return_2 = types.ReplyKeyboardMarkup(resize_keyboard=True) # Случай с выгрузкой отчетов
    button2_ret = types.KeyboardButton("Веpнуться в глaвное меню")
    markup_return_2.add(button2_ret)

    markup_reg = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_reg = types.KeyboardButton("Регистрация")
    markup_reg.add(btn1_reg)

    markup_for_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_for_admin = types.KeyboardButton("Выгрузить отчет")
    btn2_for_admin = types.KeyboardButton("Выгрузить график")
    markup_for_admin.add(btn1_for_admin, btn2_for_admin)

    if message.text == "📸 Отчет":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='Пришлите в чат описание по примеру и фотографию:\n\nОписание\n(ВМ)Балашиха новая Павлина ул.Троицкая д2 кв186 под3 эт13. Александр.Сантехник. Установить ванну. Си нужен сегодня')

    elif message.text == "📜 Примеры работ":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=f"Пример заполнения актов:", reply_markup=markup_return_1)
        count = 1
        while count <= 5:
            if count == 3 or count == 4:
                photo = open('Primer' + str(count) + '.jpg', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo = open('Primer' + str(count) + '.1.jpg', 'rb')
                bot.send_photo(message.chat.id, photo)

            else:
                photo = open('Primer' + str(count) + '.jpg', 'rb')
                bot.send_photo(message.chat.id, photo)
            text = open('Primer' + str(count) + '.txt', 'r', encoding='utf-8')
            text = text.read()
            bot.send_message(message.chat.id, text=text)
            count += 1

    elif message.text == "🧾 График работы":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Пришлите график своей работы. Сообщение по примеру:\n\nГрафик\nРаб\n*Дни месяца через пробелы*\nВых\n*Дни месяца через пробелы*\n*Месяц*", reply_markup=markup_return)

    elif message.text == "🗣️ Финансовый отдел":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="Для связи с куратором обратитесь сюда: \n@finotdelSC",
                         reply_markup=markup_return)

    elif message.text == "📑 Правила работы":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        with open('Rules.txt', 'r', encoding='utf8') as new_file:
            rule = new_file.read()
        bot.send_message(message.chat.id, text=f"Перечень правил работы:\n{rule}", reply_markup=markup_return)

    elif str(message_arr[0]) == "Описание":
        count = 1
        message_text = ''
        while count < len(message_arr):
            message_text += str(message_arr[count]) + ' '
            count += 1
        file = open('file.txt', 'w')
        file.write(message_text)
        file.close()

    elif message.text == "Регистрация":
        id = str(message.chat.id)
        base = sqlite3.connect('Registracia.db')
        cur = base.cursor()
        info_id_list = cur.execute('SELECT id FROM UserInfo').fetchall()

        count = 0
        true = 0
        while count < len(info_id_list):
            info_id = str(info_id_list[count][0])
            if id == info_id:
                true = 1
                break
            count += 1
        if true == 1:
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text='Вы уже зарегистрированы', reply_markup=markup_return)
        else:
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text='Пришлите ваше полное ФИО по примеру:\n\nФИО\n*Фамилия Имя Отчество*')

    elif message_arr[0] == 'ФИО':
        id = str(message.chat.id)
        text = message_arr[1] + ' ' + message_arr[2] + ' ' + message_arr[3]
        base = sqlite3.connect('Registracia.db')
        cur = base.cursor()
        base.execute('CREATE TABLE IF NOT EXISTS UserInfo(id, FIO)')
        base.commit()
        cur.execute('INSERT INTO UserInfo VALUES(?, ?)', (id, text))
        base.commit()
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='Регистрация пройдена!', reply_markup=markup_return)

    elif message.text == "Авторизация":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)

        id = str(message.chat.id)
        base = sqlite3.connect('Registracia.db')
        cur = base.cursor()
        base.execute('CREATE TABLE IF NOT EXISTS UserInfo(id, FIO)')
        base.commit()
        info_id_list = cur.execute('SELECT id FROM UserInfo').fetchall()

        count = 0
        true = 0
        while count < len(info_id_list):
            info_id = str(info_id_list[count][0])
            if id == info_id:
                true = 1
                break
            count += 1
        if true == 1:
            bot.send_message(message.chat.id, text='Узнаю вас', reply_markup=markup_main)
        else:
            bot.send_message(message.chat.id, text='Первый раз вас вижу. Пройдите регистрацию', reply_markup=markup_reg)

    elif message_arr[0] == "График":
        count = 2
        while count < len(message_arr):
            if message_arr[count] == 'Вых':
                break
            count += 1
        work_day = ''
        rest_day = ''
        counter = 2
        while counter < count:
            work_day += str(message_arr[counter]) + ' '
            counter += 1
        counter = count + 1
        while counter < len(message_arr) - 1:
            rest_day += str(message_arr[counter]) + ' '
            counter += 1
        month = message_arr[-1]

        base = sqlite3.connect('Registracia.db')
        cur = base.cursor()
        id_list = cur.execute('SELECT id FROM UserInfo').fetchall()
        name_list = cur.execute('SELECT FIO FROM UserInfo').fetchall()
        id = str(message.chat.id)
        count = 0
        while count < len(id_list):
            info_id = str(id_list[count][0])
            if id == info_id:
                break
            count += 1
        table_name = str(name_list[count][0].replace(' ', ''))

        base = sqlite3.connect('GrafikRaboti.db')
        cur = base.cursor()
        base.execute('CREATE TABLE IF NOT EXISTS ' + table_name + '(month, work_day, rest_day)')
        base.commit()
        cur.execute('INSERT INTO ' + table_name + ' VALUES(?, ?, ?)', (month, work_day, rest_day))
        base.commit()
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='График работы записан!', reply_markup=markup_return)

    elif message.text == 'Функции администратора':
        id = str(message.chat.id)
        admin_id = str(message.chat.id)
        if id == admin_id:
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text='Вариант информации для выгрузки:', reply_markup=markup_for_admin)
        else:
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text='У вас нет прав', reply_markup=markup_return)

    elif message.text == 'Выгрузить отчет':
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='Для выгрузки отчета пришлите сообщение по примеру:\n\nОтчет\nИванов Иван Иваныч\nГГГГ-ММ-ЧЧ')

    elif message.text == 'Выгрузить график':
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='Для выгрузки графика работы пришлите сообщение по примеру:\n\nРабочий график\nИванов Иван Иваныч')

    elif message_arr[0] == 'Отчет':
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        table_name = message_arr[1] + message_arr[2] + message_arr[3]
        base = sqlite3.connect('OtchetInfo.db')
        cur = base.cursor()
        datetime = cur.execute('SELECT datetime FROM ' + table_name).fetchall()
        photo = cur.execute('SELECT photo FROM ' + table_name).fetchall()
        text = cur.execute('SELECT text FROM ' + table_name).fetchall()
        count = 0
        counter = 0
        while count < len(datetime):
            if str(datetime[count][0][:-6]) == message_arr[-1]:
                max_count = count
                counter += 1
            count += 1
        if counter == 0:
            bot.send_message(message.chat.id, text='Отчетов за эту дату нет', reply_markup=markup_return)
        else:
            info_about_counter = open('info_about_counter.txt', 'w')
            info_about_counter.write(str(counter))
            info_about_counter.close()
            count = 0
            photo_name = 'Фото ' + str(count + 1) + ' от ' + str(datetime[count][0][:-6]) + '.jpg'
            new_path = r"C:\Users\KOJIEHO\Desktop\Папка\PythonProject\Project_Telegramm_Bot\\" + photo_name
            schetchik = counter - 1
            while count < counter:
                mes_text = str(text[max_count - schetchik][0])
                bot.send_message(message.chat.id, text=mes_text, reply_markup=markup_return_2)
                img = convert_to_not_binary_data(photo[max_count - schetchik][0], new_path)
                bot.send_photo(message.chat.id, img)
                count += 1
                schetchik -= 1

    elif message_arr[0] == 'Рабочий':
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        table_name = message_arr[2] + message_arr[3] + message_arr[4]
        base = sqlite3.connect('GrafikRaboti.db')
        cur = base.cursor()
        month = cur.execute('SELECT month FROM ' + table_name).fetchall()
        work_day = cur.execute('SELECT work_day FROM ' + table_name).fetchall()
        rest_day = cur.execute('SELECT rest_day FROM ' + table_name).fetchall()
        text = message_arr[2] + ' ' + message_arr[3] + ' ' + message_arr[4] + '\n' + str(month[-1][0]) + '\nРабочие дни:\n' + str(work_day[-1][0]) + '\nВыходные дни:\n' + str(rest_day[-1][0])
        bot.send_message(message.chat.id, text=text, reply_markup=markup_return)

    elif message.text == "Вернуться в главное меню":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup_main)

    elif message.text == "Вернуться в глaвное меню":  # в случае с примерами
        count = 13
        while count > 0:
            bot.delete_message(message.chat.id, message.message_id - count)
            count -= 1
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup_main)

    elif message.text == "Веpнуться в глaвное меню":  # в случае с выгрузкой отчетов
        counter = open('info_about_counter.txt', 'r')
        counter = counter.read()
        count = int(counter) * 2
        while count > 0:
            bot.delete_message(message.chat.id, message.message_id - count)
            count -= 1
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup_main)

    else:
        bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=["photo"])
def handle_docs_photo(message):
    markup_return = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Вернуться в главное меню")
    markup_return.add(button1)

    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(message.photo[2].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    id = str(message.chat.id)
    date_time = str(datetime.now())[:-10]
    photo = convert_to_binary_data(name)
    text = open('file.txt', 'r')
    text = text.read()

    base = sqlite3.connect('Registracia.db')
    cur = base.cursor()
    id_list = cur.execute('SELECT id FROM UserInfo').fetchall()
    name_list = cur.execute('SELECT FIO FROM UserInfo').fetchall()
    count = 0
    while count < len(id_list):
        info_id = str(id_list[count][0])
        if id == info_id:
            break
        count += 1
    table_name = str(name_list[count][0].replace(' ', ''))

    base = sqlite3.connect('OtchetInfo.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS ' + table_name + '(datetime TEXT, photo BLOB, text TEXT)')
    base.commit()
    cur.execute('INSERT INTO ' + table_name + ' VALUES(?, ?, ?)', (date_time, photo, text))
    base.commit()
    os.remove(name)
    os.remove('file.txt')
    bot.delete_message(message.chat.id, message.message_id - 2)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text="Отчет записан", reply_markup=markup_return)


bot.polling(none_stop=True)
