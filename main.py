from openai import OpenAI
import telebot
import config

# Инициализация клиента API OpenAI с вашим API ключом из config.py
client = OpenAI(
    api_key=config.deepseek_api_key,
    base_url="https://api.deepseek.com/v1",
)

# Инициализация бота Telegram с вашим токеном из config.py
bot = telebot.TeleBot(config.telegram_bot_token)

# Имя бота в Telegram
BOT_USERNAME = "@Chat37GPT37_BOT"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Проверяем, упомянули ли бота в тексте
    if BOT_USERNAME not in message.text:
        return  # Если имя бота не упоминается, ничего не делаем

    # Убираем имя бота из текста, чтобы передать чистый запрос
    user_input = message.text.replace(BOT_USERNAME, "").strip()

    # Формируем промт для гопнического стиля
    system_prompt = (
        "Ты должен отвечать как гопник с двора: используй уличный сленг, "
        "мат, и будь слегка агрессивным. Сохраняй неформальный тон, но отвечай по делу."
    )

    # Создаем запрос с промтом и пользовательским вводом
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        # Отправка запроса в нейронную сеть
        chat_completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        # Извлечение ответа
        ai_response_content = chat_completion.choices[0].message.content

        # Отправка ответа пользователю
        bot.reply_to(message, ai_response_content)

    except Exception as e:
        # В случае ошибки отправляем сообщение об ошибке
        bot.reply_to(message, f"Ошибочка вышла, братан: {e}")

# Запуск бота
bot.polling()
