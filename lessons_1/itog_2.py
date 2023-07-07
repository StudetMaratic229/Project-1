from sentence_transformers import SentenceTransformer, util
import telebot

bot = telebot.TeleBot("6323403215:AAHQ54wwRphWWPQVf9z5Lh8zgl9mLwNNOoI")
model = SentenceTransformer('all-MiniLM-L6-v2')

questions = {
    'Как оформить заказ?': 1,
    'Как заказать товар?': 2,
    'Как купить товар?': 3,
    'Как я могу заказать что - либо у вашей компании?': 2,
    'Как я могу купить что - либо в вашем магазине?': 3,
    'Как я могу приобрести что - либо в вашем магазине?': 3,
    'Как приобрести товар?': 3
}
answers = {
    1: 'Чтобы оформить зака перейдите по ссылке ниже:',
    2: 'Для заказа товара перейдите по ссылке ниже:',
    3: 'Для покупки товара перейдите по ссылке ниже:'
}


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    button = telebot.types.InlineKeyboardButton('Задать вопрос', callback_data='vopros')
    keyboard.add(button)
    bot.send_message(message.chat.id,
                     "Здравствуйте! Нажмите на кнопку, если хотите задать вопрос:",
                     reply_markup=keyboard)


def giveanswers(message):
    global questions, answers
    my_qs = message.text
    filePath1 = 'file.txt'
    file = open(filePath1, 'a')
    file.write("Пользователь: @" + str(message.from_user.username) + " Вопрос: " + my_qs + "\n\n")
    file.close()


@bot.callback_query_handler(func=lambda call: True)
def queue(call):
    if call.data == "vopros":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Спасибо!😊",
                              reply_markup=None)
        s = bot.send_message(call.message.chat.id, "Введите свой вопрос:")
        bot.register_next_step_handler(s, giveanswers)
