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

# Промт для общения как гопник
gopnik_prompt = "Ты гопник из подворотни. Общайся в стиле гопника: используй сленг, мат, и будь слегка агрессивным. Ты должен вести себя как пацанчик, который знает всё и вся."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Проверка, упоминается ли бот в сообщении
    if "@gopnik37_bot" in message.text:
        # Убираем упоминание бота из текста сообщения
        user_input = message.text.replace("@gopnik37_bot", "").strip()

        # Создание сообщения с промтом гопника и текущим вводом пользователя
        messages = [
            {"role": "system", "content": gopnik_prompt},
            {"role": "user", "content": user_input}
        ]

        # Отправка запроса в нейронную сеть
        chat_completion = client.chat.completions.create(
            model="deepseek-coder",
            messages=messages
        )

        # Извлечение и вывод ответа нейронной сети
        ai_response_content = chat_completion.choices[0].message.content
        bot.reply_to(message, ai_response_content)

bot.polling()