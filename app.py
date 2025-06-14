import telebot

bot = telebot.TeleBot('Token_bot')

GROUP_CHAT_ID = "Введите ID чата"

# Словарь для хранения соответствий между сообщениями и их отправителями
forwarded_messages = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот поддержки. Отправьте свой вопрос, и я перешлю его администраторам.')

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, 'Тут сообщение о помощи')

@bot.message_handler(content_types=['text', 'photo', 'video', 'document'], func=lambda message: message.chat.type == 'private')
def all_messages(message):
    forwarded_msg = bot.forward_message(GROUP_CHAT_ID, message.chat.id, message.message_id)
    # Сохраняем соответствие между ID пересланного сообщения и ID отправителя
    forwarded_messages[forwarded_msg.message_id] = message.chat.id

@bot.message_handler(content_types=['text', 'photo', 'video', 'document'], func=lambda message: message.chat.type == 'group')
def reply_to_group_message(message):
    if message.reply_to_message and message.reply_to_message.message_id in forwarded_messages:
        sender_id = forwarded_messages[message.reply_to_message.message_id]
        if message.content_type == 'text':
            bot.send_message(sender_id, message.text)
        elif message.content_type == 'photo':
            bot.send_photo(sender_id, message.photo[-1].file_id, caption=message.caption)
        elif message.content_type == 'video':
            bot.send_video(sender_id, message.video.file_id, caption=message.caption)
        elif message.content_type == 'document':
            bot.send_document(sender_id, message.document.file_id, caption=message.caption)


if __name__ == '__main__':
    bot.polling(none_stop=True)
