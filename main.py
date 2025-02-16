# qpMessageBot - by t.me/qpikzz
# github - github.com/qpikzz/qpMessagesBot
# Вырезано: токен, функции зашифровки / расшифровки и админ
# Лицензия: CC BY

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
from PIL import Image
import telebot 
import json
import os


# Создание бота
token = ":D"
bot = telebot.TeleBot(token, parse_mode="html")
admin = 19


#Функции зашифровки и расшифровки id пользователя
def encode(id):
    return id

def decode(id):
    return id


# Проверка существования директории temp
os.makedirs("temp", exist_ok=True)


# Обработка команды start и команд для получения ссылки
@bot.message_handler(commands=["start", "menu", "link"])
def start(message):

    # Часто используемые переменные
    chat = message.chat
    user = message.from_user
    text = message.text 
    text = text.replace("<", "&lt;").replace(">", "&gt;")

    # Проверка на то, что бот запущен в лс
    if chat.type != "private":
        bot.send_message(chat.id,"🥹 Спасибо за добавление бота в группу / канал!\n❗ Во избежание потенциальных ошибок, используйте данную команду в ЛС!\n👉 @qpMessagesBot")
        return None

    # Добавить пользователя в Users.txt, если его там нет
    with open("users.txt","r", encoding="utf-8") as file:
        
        users = json.load(file)

        if encode(user.id) not in users:
            users.append(encode(user.id))
            with open("users.txt","w", encoding="utf-8") as file:
                json.dump(users, file, ensure_ascii=False, indent=4)


    # Если используется просто команда, без отправки сообщения кому-то
    if len(text.split()) == 1:
        k = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="✈ Переслать", url=f"https://t.me/share/url?url=t.me/qpMessagesBot?start={encode(user.id)}")
        k.add(b1)
        bot.send_message(chat.id, f"<b>🏷 Твоя ссылка:</b>\n👉 t.me/qpMessagesBot?start={encode(user.id)}\n\n🎯 Отправь её друзьям, добавь в описание профиля в соцсетях и начни получать новые сообщения!", reply_markup=k)
    
    
    # Если требуется отправка кому-то
    else:

        recip = decode(text.split()[1])

        with open("users.txt","r", encoding="utf-8") as file:
            users = json.load(file)
            if encode(recip) not in users:
                bot.send_message(chat.id, "🧐 Я не знаю такого человека!")
                return None

        if recip == user.id:
            bot.send_message(chat.id, "😕 Вы не можете отправить сообщение себе.")
            return None

        bot.send_message(chat.id,f"💭 Теперь напиши сообщение!\n\n🎞 Ты можешь отправить обычный текст, голосовое, кружок, фото или видео!\n\n🚫 Если ты передумал(а), напиши \"<code>Отмена</code>\"")
        bot.register_next_step_handler(message, lambda msg: sendMessage(msg, recip))



# Отправка сообщений
def sendMessage(message, recip):

    # Определение переменных
    chat = message.chat
    user = message.from_user
    first_name = user.first_name.replace("<", "&lt;").replace(">", "&gt;") if user.first_name else ""
    last_name = user.last_name.replace("<", "&lt;").replace(">", "&gt;") if user.last_name else ""

    if message.text:
        message.text = message.text.replace("<", "&lt;").replace(">", "&gt;")
    if message.caption:
        message.caption = message.caption.replace("<", "&lt;").replace(">", "&gt;")
    
    # Создание маркапа
    k = InlineKeyboardMarkup()
    k.row(
        InlineKeyboardButton(text="❤️", callback_data=f"reaction ❤️ {user.id}"),
        InlineKeyboardButton(text="🔥", callback_data=f"reaction 🔥 {user.id}"),
        InlineKeyboardButton(text="👍", callback_data=f"reaction 👍 {user.id}"),
        InlineKeyboardButton(text="👎", callback_data=f"reaction 👎 {user.id}"),
        InlineKeyboardButton(text="💩", callback_data=f"reaction 💩 {user.id}")
    )
    k.row(
        InlineKeyboardButton(text="🗯 Ответить", callback_data=f"answer {user.id}"),
        InlineKeyboardButton(text="💤 Игнорировать", callback_data="ignore")
    )
    # k.add(b1, b2)


    try:

        if message.content_type == "text":

            if "отмена" in message.text.lower() or "\"отмена\"" in message.text.lower():
                bot.send_message(chat.id,"❌ Отправка отменена!\n\n👁 Чтобы увидеть свою ссылку, используй команду \"/link\"")
                return None
            
            elif "/start" in message.text.lower() or "/menu" in message.text.lower() or "/link" in message.text.lower():
                bot.send_message(chat.id,"❌ Отправка отменена!")
                start(message)
                return None

            if user.username:
                bot.send_message(recip, f"📫 Новое сообщение от {first_name} {last_name} (@{user.username}):\n<blockquote><code>{message.text[:3000]}</code></blockquote>", reply_markup=k)
            
            else:
                bot.send_message(recip, f"📫 Новое сообщение от {first_name} {last_name}:\n<blockquote><code>{message.text[:3000]}</code></blockquote>", reply_markup=k)
            bot.reply_to(message, "🛩 Сообщение отправлено!\n⏱ Ожидайте ответ.\n\n📭 Чтобы увидеть вашу ссылку, используйте /link")
        

        elif message.content_type == "voice":
            
            fileId = message.voice.file_id
            
            if user.username:
                bot.send_voice(recip, fileId, caption=f"📯 Новое голосовое от {first_name} {last_name} (@{user.username}):", reply_markup=k)
            
            else:
                bot.send_voice(recip, fileId, caption=f"📯 Новое голосовое от {first_name} {last_name}:", reply_markup=k)
            
            bot.reply_to(message, "🛩 Голосовое отправлено!\n⏱ Ожидайте ответ.\n\n📭 Чтобы увидеть вашу ссылку, используйте /link")

        
        elif message.content_type == "video_note":
            
            # Конвертация кружка в видео
            fileId = message.video_note.file_id
            fileInfo = bot.get_file(fileId)
            filePath = fileInfo.file_path
            downloadFile = bot.download_file(filePath)
            with open(f"temp/{fileId}.mp4", "wb") as file:
                file.write(downloadFile)
            
            with open(f"temp/{fileId}.mp4", "rb") as video:
                if user.username:
                    bot.send_video(recip, video, caption=f"🎱 Новый кружок от {first_name} {last_name} (@{user.username}):", reply_markup=k)
                else:
                    bot.send_video(recip, video, caption=f"🎱 Новый кружок от {first_name} {last_name}:", reply_markup=k)

            bot.reply_to(message, "🎱 Кружок отправлен!\n⏱ Ожидайте ответ.\n\n📭 Чтобы увидеть вашу ссылку, используйте /link")
            
            # Удаление видео с сервера
            os.remove(f"temp/{fileId}.mp4")

        elif message.content_type == "photo":
            fileId = message.photo[-1].file_id
            if user.username:
                if message.caption:
                   bot.send_photo(recip, fileId, caption=f"💾 Новое фото от {first_name} {last_name} (@{user.username}).\n🗞 Подпись к фото: <blockquote><code>{message.caption}</code></blockquote>"[0:2000], reply_markup=k) 
                else:
                    bot.send_photo(recip, fileId, caption=f"💾 Новое фото от {first_name} {last_name} (@{user.username}):", reply_markup=k)
                
            else:
                if message.caption:
                   bot.send_photo(recip, fileId, caption=f"💾 Новое фото от {first_name} {last_name}.\n🗞 Подпись к фото: <blockquote><code>{message.caption}</code></blockquote>"[0:2000], reply_markup=k) 
                else:
                    bot.send_photo(recip, fileId, caption=f"💾 Новое фото от {first_name} {last_name}:", reply_markup=k)

            bot.reply_to(message, "💾 Фото отправлено!\n⏱ Ожидайте ответ.\n\n📭 Чтобы увидеть вашу ссылку, используйте /link")

        elif message.content_type == "video":
            if message.video.file_size > 50 * 1024 * 1024:
                bot.reply_to(message, f"😦 Слишком большое видео!\n\n Максимальный размер: 50МБ (Рекомендуем: не более двух минут)")

            fileId = message.video.file_id
            if user.username:
                if message.caption:
                   bot.send_video(recip, fileId, caption=f"🎞 Новое видео от {first_name} {last_name} (@{user.username}).\n🗞 Подпись к видео: <blockquote><code>{message.caption}</code></blockquote>"[0:2000], reply_markup=k) 
                else:
                    bot.send_video(recip, fileId, caption=f"🎞 Новое видео от {first_name} {last_name} (@{user.username}):", reply_markup=k)
                
            else:
                if message.caption:
                   bot.send_video(recip, fileId, caption=f"🎞 Новое видео от {first_name} {last_name}.\n🗞 Подпись к видео: <blockquote><code>{message.caption}</code></blockquote>"[0:2000], reply_markup=k) 
                else:
                    bot.send_video(recip, fileId, caption=f"🎞 Новое видео от {first_name} {last_name}:", reply_markup=k)
            
            bot.reply_to(message, "🎞 Видео отправлено!\n⏱ Ожидайте ответ.\n\n📭 Чтобы увидеть вашу ссылку, используйте /link")

        elif message.content_type == "sticker":

            fileId = message.sticker.file_id
            fileInfo = bot.get_file(fileId)
            downloadFile = bot.download_file(fileInfo.file_path)

            # Созданение как webp (Стандартное расширение для стикеров)
            with open(f"temp/{fileId}.webp", "wb") as file:
                file.write(downloadFile)
            
            # Конвертация из webp в png
            try:
                img = Image.open(f"temp/{fileId}.webp").convert("RGBA")
                img.save(f"temp/{fileId}.png", "PNG")
                with open(f"temp/{fileId}.png","rb") as photo:

                    if user.username:
                        bot.send_photo(recip, photo, caption=f"🏞 Новый стикер от {first_name} {last_name} (@{user.username}):", reply_markup=k)
                    
                    else:
                        bot.send_photo(recip, photo, caption=f"🏞 Новый стикер от {first_name} {last_name}:", reply_markup=k)
                    
                bot.reply_to(message, "🏞 Стикер отправлен!\n⏱ Ожидайте ответ.\n\n📭 Чтобы увидеть вашу ссылку, используйте /link")

            except:
                bot.reply_to(message, "🙇 Увы, пока бот умеет пересылать лишь статичные стикеры. Анимированные стикеры - наш план на будущие обновления!\n🚄 Выбери что-нибудь другое!")
                bot.register_next_step_handler(message, lambda msg: sendMessage(msg, recip))

            try:
                os.remove(f"temp/{fileId}.webp")
                os.remove(f"temp/{fileId}.png")
            except:
                pass

        else:
            bot.reply_to(message, "⚙ Пока мы не умеем пересылать такое!\n🔧 Возможно, это будет добавлено в будущем!")

    except ApiTelegramException:
        bot.send_message(chat.id, "🫣 Не удалось отправить сообщение!\n🤔 Возможно, пользователь заблокировал бота.")
        try:
            with open("users.txt","r", encoding="utf-8") as file:
                users = json.load(file)
                if encode(user.id) in users:
                    users.remove(encode(user.id))
                    with open("users.txt","w", encoding="utf-8") as file:
                        json.dump(users, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)

# Обработка нажатия кнопки "Игнорировать"
@bot.callback_query_handler(func=lambda call: call.data == "ignore")
def ignore(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    except ApiTelegramException:
        bot.answer_callback_query(call.id, "Не удалось удалить сообщение :(")


# Нажатие кнопки "Ответить"
@bot.callback_query_handler(func=lambda call: "answer" in call.data)
def answer(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    recip = call.data.split()[1]
    bot.send_message(call.message.chat.id,f"💭 Напиши ответное сообщение!\n\n🎞 Ты можешь отправить обычный текст, голосовое, кружок, фото или видео!\n\n🚫 Если ты передумал(а), напиши \"<code>Отмена</code>\"")
    bot.register_next_step_handler(call.message, lambda msg: sendMessage(msg, recip))

@bot.callback_query_handler(func=lambda call: "reaction" in call.data)
def reaction(call):

    message = call.message
    user = call.from_user
    first_name = user.first_name.replace("<", "&lt;").replace(">", "&gt;") if user.first_name else ""
    last_name = user.last_name.replace("<", "&lt;").replace(">", "&gt;") if user.last_name else ""

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    react = call.data.split()[1]
    recip = call.data.split()[2]
    
    if user.username:
        bot.send_message(recip, f"{first_name} {last_name} (@{user.username}) оставил реакцию {react}")

    else:
        bot.send_message(recip, f"{first_name} {last_name} оставил реакцию {react}")



# Обработка команды "/privacy"
@bot.message_handler(commands=["privacy"])
def privacy(message):
    bot.reply_to(message,"1. Собираемые данные:\n1.1. ID вашего аккаунта в зашифрованном виде – это необходимо для стабильной работы бота (чтобы нельзя было отправлять сообщения тем, кто не запустил бота).\n\n2. Мы не видим, не храним и не анализируем данные, не указанные в пункте 1, а также сообщения, отправляемые другим пользователям.\n\n3. Пользователь, которому вы отправляете сообщение, видит:\n3.1. Ваше имя, указанное в Telegram;\n3.2. Вашу фамилию, указанную в Telegram (при наличии);\n3.3. Ваш юзернейм (при наличии).")



# Обработка команды "/post"
@bot.message_handler(commands=["post"])
def post(message):
    if message.from_user.id != admin:
        print(":(")
        return None
    with open("users.txt","r", encoding="utf-8") as file:
        users = json.load(file)
    
    for user in users:
        try:
            bot.send_message(decode(user), f"📰 Новое уведомление:\n{" ".join(message.text.split(" ")[1:])}")
        except ApiTelegramException:
            try:
                with open("users.txt","r", encoding="utf-8") as file:
                    users = json.load(file)
                    if decode(user) in users:
                        users.remove(user)
                        with open("users.txt","w", encoding="utf-8") as file:
                            json.dump(users, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(e)

# Запуск бота
print("Бот запущен!")
while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f"Интернет пал :(")