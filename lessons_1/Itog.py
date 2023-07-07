from sentence_transformers import SentenceTransformer, util
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(str(os.getenv("TOKEN")))
model = SentenceTransformer('all-MiniLM-L6-v2')

questions = [['Как оформить заказ?', "Чтобы оформить зака перейдите по ссылке ниже:","" ],
             ["Как заказать товар?", "Для заказа товара перейдите по ссылке ниже:"],
             ["Как купить товар?", "Для покупки товара перейдите по ссылке ниже:"],
             ["Как я могу заказать что - либо у вашей компании?", "Для заказа товара перейдите по ссылке ниже:"],
             ["Как я могу купить что - либо в вашем магазине?", "Для покупки товара перейдите по ссылке ниже:"],
             ["Как я могу приобрести что - либо в вашем магазине?", "Для покупки товара перейдите по ссылке ниже:"],
             ["Как приобрести товар?", "Для покупки товара перейдите по ссылке ниже:"]]
e = model.encode(questions)


def obrabotcka(message):
    global questions, e, model
    my_qs = message.text
    filePath1 = 'file.txt'
    file = open(filePath1, 'a')
    file.write("Пользователь: @" + str(message.from_user.username) + " Вопрос: " + my_qs + "\n\n")
    file.close()
    e2 = model.encode(my_qs)
    cos = util.cos_sim(e, e2)
    print(cos)
    sq = []
    for i in range(0, len(cos)):
        sq.append([i, cos[i]])

    sq = sorted(sq, key=lambda x: x[1], reverse=True)

    if sq[0][1] <= 0.72:
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        button = telebot.types.InlineKeyboardButton('Связь с оператором', url="https://web.telegram.org/k/#@Astro8989")
        button1 = telebot.types.InlineKeyboardButton('Главное меню', callback_data='glav')
        keyboard.add(button, button1)
        bot.send_message(message.chat.id, "Извиите, но я не совсем понял ваш вопрос :(\nПеренаправляю вас на "
                                          "оператора для дальнейшего решения вашего вопроса.", reply_markup=keyboard)
    else:
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        button = telebot.types.InlineKeyboardButton('Перейти по ссылке',
                                                    url="https://sbert.net/docs/usage/semantic_textual_similarity.html")
        button1 = telebot.types.InlineKeyboardButton('Главное меню', callback_data='glav')
        keyboard.add(button, button1)
        bot.send_message(message.chat.id, f"{questions[sq[0][0]][1]}", reply_markup=keyboard)


@bot.message_handler(commands=["spisok"])
def admin(message):
    if message.from_user.id == int(os.getenv("ID")):
        try:
            file_path = 'file.txt'  # Путь к вашему текстовому файлу
            with open(file_path, 'r') as file:
                file_content = file.read()
            bot.send_message(int(os.getenv("ID")), file_content, parse_mode="HTML")
        except Exception as e:
            bot.send_message(int(os.getenv("ID")), "Файл пуст! :(")
    else:
        bot.send_message(message.chat.id, "Вы не являетесь админом!")


@bot.message_handler(commands=["clear"])
def adm(message):
    if message.from_user.id == int(os.getenv("ID")):
        file_to_delete2 = open("file.txt", 'w')
        file_to_delete2.close()
        bot.send_message(int(os.getenv("ID")), "Всё готово!")
    else:
        bot.send_message(message.chat.id, "Вы не являетесь админом!")


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    button = telebot.types.InlineKeyboardButton('Задать вопрос', callback_data='vopros')
    keyboard.add(button)
    bot.send_message(message.chat.id,
                     "Здравствуйте! Нажмите на кнопку, если хотите задать вопрос:",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def queue(call):
    if call.data == "vopros":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Спасибо!😊",
                              reply_markup=None)
        s = bot.send_message(call.message.chat.id, "Нанишите свой вопрос, и я постараюсь ответить на него:")
        bot.register_next_step_handler(s, obrabotcka)
    if call.data == "glav":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Спасибо!😊",
                              reply_markup=None)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        button = telebot.types.InlineKeyboardButton('Задать вопрос', callback_data='vopros')
        keyboard.add(button)
        bot.send_message(call.message.chat.id,
                         "Здравствуйте! Нажмите на кнопку, если хотите задать вопрос:",
                         reply_markup=keyboard)


bot.polling()
