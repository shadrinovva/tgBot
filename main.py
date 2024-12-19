import telebot

TOKEN = '7665034171:AAGdER8_Q-JJgUhyPFDhcziHaWoWdEg8sSw'
bot = telebot.TeleBot(TOKEN)

# Вопросы для теста
questions = [
    {
        "question": "Какой любимый цвет у солнышки зайки?",
        "options": ["Красный", "Синий", "Зеленый", "Белый"],
        "correct": 3
    },
    {
        "question": "Какое блюдо цветочек любит больше всего?",
        "options": ["Пицца", "Роллы", "Паста", "Борщ"],
        "correct": 1
    },
    {
        "question": "Какой любимый сериал у Дианочки?",
        "options": ["Игра престолов", "Друзья", "Никакой", "Очень странные дела"],
        "correct": 2
    },
    {
        "question": "Какой у солнышка размер обуви?",
        "options": ["37", "38", "39", "40"],
        "correct": 2
    },
    {
        "question": "Что твоя любимая выберет на ужин?",
        "options": ["Стейк", "Салат", "Жареная картошка", "Котлеты"],
        "correct": 0
    },
    {
        "question": "Когда мы познакомились?",
        "options": ["28 февраля", "25 февраля", "12 февраля", "30 января"],
        "correct": 0
    },
    {
        "question": "Когда мы первый раз поцеловались?",
        "options": ["28 февраля", "19 апреля", "20 апреля", "30 февраля"],
        "correct": 1
    },
    {
        "question": "Кто чаще уступает в ссоре?",
        "options": ["Солнышко-зайка", "Медвеженок", "Никто", "Мы никогда не ссоримся"],
        "correct": 1
    },
    {
        "question": "Где она мечтает побывать?",
        "options": ["Анапа", "Термы НК", "Париж", "Бали"],
        "correct": 3
    },
    {
        "question": "Что солнышко зайка любит делать больше всего с Рузельчиком?",
        "options": ["Тратить его деньги", "Кусать", "Нюхать", "Издеваться"],
        "correct": 1
    },
    {
        "question": "Что Дианочку больше всего бесит?",
        "options": ["Беспорядок", "Тупые шутки", "Другие девочки", "Дота"],
        "correct": 2
    },
    {
        "question": "Какое наше первое совместное фото?",
        "options": ["В кафе на баумана", "На подоконнике", "На катамаране", "В 309"],
        "correct": 2
    },
    {
        "question": "Любимые цветочки Дианочки?",
        "options": ["Пионы", "Розы", "Пионы и розы", "Ромашки"],
        "correct": 2
    },
    {
        "question": "Какие нелюбимые цветочки у Дианочки?",
        "options": ["Лилия", "Хризаентема", "Диантусы", "Гортензия"],
        "correct": 0
    },
    {
        "question": "Какой подарок Дианочка мечтает получить в своей жизни?",
        "options": ["Порш", "Картье", "Квартиру", "Безлимитная карточка Рузеля"],
        "correct": 0
    }
]

# Словарь для хранения ответов пользователей
user_answers = {}


# Начало теста
@bot.message_handler(commands=['start', 'test'])
def start_test(message):
    chat_id = message.chat.id

    # Приветственное сообщение
    if message.text == "/start":
        bot.send_message(
            chat_id,
            "Привет, самый лучший Рузель на свете! 💖\n\n"
            "Дианочке снова пришла крутая идея в её голову, и теперь тебе обязательно надо пройти тест. "
            "Если ты не пройдёшь, значит её не любишь! 😱\n\n"
            "Нажми /test, чтобы начать. Это нужно сделать прямо сейчас! 🚀"
        )
        return

    # Начало теста
    user_answers[chat_id] = {"current_question": 0, "score": 0}  # Сброс данных
    send_question(chat_id)


# Отправка вопроса
def send_question(chat_id):
    user_data = user_answers.get(chat_id)
    if user_data is None:
        bot.send_message(chat_id, "Введите /start, чтобы начать тест!")
        return

    current_index = user_data["current_question"]

    # Если вопросы закончились, подвести итоги
    if current_index >= len(questions):
        bot.send_message(chat_id, f"Тест завершён! Ты набрал {user_data['score']} из {len(questions)} баллов!")
        user_answers.pop(chat_id)  # Очистить данные
        return

    question = questions[current_index]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in question["options"]:
        markup.add(option)

    bot.send_message(chat_id, question["question"], reply_markup=markup)


# Обработка ответа
@bot.message_handler(func=lambda message: message.chat.id in user_answers)
def handle_answer(message):
    chat_id = message.chat.id
    user_data = user_answers[chat_id]
    current_index = user_data["current_question"]
    question = questions[current_index]

    # Проверяем ответ
    if message.text == question["options"][question["correct"]]:
        user_data["score"] += 1  # Добавить балл за правильный ответ

    # Перейти к следующему вопросу
    user_data["current_question"] += 1
    send_question(chat_id)


# Запуск бота
bot.polling()
