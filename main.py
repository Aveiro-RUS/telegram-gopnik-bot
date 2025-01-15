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

# Словарь для хранения диалогов пользователей
dialogues = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Получаем идентификатор пользователя
    user_id = message.from_user.id

    # Проверка на ответ боту или упоминание
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id
    is_mention = f"@{bot.get_me().username}" in message.text

    if is_mention or is_reply_to_bot:
        # Убираем упоминание бота из текста сообщения
        user_input = message.text.replace(f"@{bot.get_me().username}", "").strip()

        # Если это новый пользователь, инициализируем историю диалога
        if user_id not in dialogues:
            dialogues[user_id] = [
                {"role": "system", "content": gopnik_prompt}
            ]

        # Добавляем сообщение пользователя в историю
        dialogues[user_id].append({"role": "user", "content": user_input})

        # Отправляем запрос в нейронную сеть
        chat_completion = client.chat.completions.create(
            model="deepseek-coder",
            messages=dialogues[user_id]
        )

        # Извлечение и вывод ответа нейронной сети
        ai_response_content = chat_completion.choices[0].message.content

        # Добавляем ответ бота в историю
        dialogues[user_id].append({"role": "assistant", "content": ai_response_content})

        bot.reply_to(message, ai_response_content)

bot.polling()
