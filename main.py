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

# Общая история диалога с ограничением длины
dialogue_history = [
    {"role": "system", "content": gopnik_prompt}
]

# Максимальная длина истории
dialogue_history_limit = 10

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Проверка на ответ боту или упоминание
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id
    is_mention = f"@{bot.get_me().username}" in message.text

    if is_mention or is_reply_to_bot:
        # Убираем упоминание бота из текста сообщения
        user_input = message.text.replace(f"@{bot.get_me().username}", "").strip()

        # Добавляем сообщение пользователя в общую историю
        dialogue_history.append({"role": "user", "content": user_input})

        # Ограничиваем размер истории
        if len(dialogue_history) > dialogue_history_limit:
            dialogue_history = dialogue_history[-dialogue_history_limit:]

        # Отправляем запрос в нейронную сеть
        chat_completion = client.chat.completions.create(
            model="deepseek-coder",
            messages=dialogue_history
        )

        # Извлечение и вывод ответа нейронной сети
        ai_response_content = chat_completion.choices[0].message.content

        # Добавляем ответ бота в общую историю
        dialogue_history.append({"role": "assistant", "content": ai_response_content})

        # Ограничиваем размер истории после добавления ответа
        if len(dialogue_history) > dialogue_history_limit:
            dialogue_history = dialogue_history[-dialogue_history_limit:]

        bot.reply_to(message, ai_response_content)

    else:
        # Если сообщение не адресовано боту, ничего не делаем
        pass

bot.polling()
