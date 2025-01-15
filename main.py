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

# Список для хранения истории разговора
conversation_history = []

# Промт для общения как гопник
gopnik_prompt = "Ты гопник из подворотни. Общайся в стиле гопника: используй сленг, мат, и будь слегка агрессивным. Ты должен вести себя как пацанчик, который знает всё и вся."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Запрос ввода пользователя
    user_input = message.text

    # Добавление ввода пользователя в историю разговора
    conversation_history.append({"role": "user", "content": user_input})

    # Добавление промта гопника в историю для изменения стиля общения
    conversation_history.insert(0, {"role": "system", "content": gopnik_prompt})

    # Отправка запроса в нейронную сеть
    chat_completion = client.chat.completions.create(
        model="deepseek-coder",
        messages=conversation_history
    )

    # Извлечение и вывод ответа нейронной сети
    ai_response_content = chat_completion.choices[0].message.content
    bot.reply_to(message, ai_response_content)

    # Добавление ответа нейронной сети в историю разговора
    conversation_history.append({"role": "system", "content": ai_response_content})

bot.polling()
