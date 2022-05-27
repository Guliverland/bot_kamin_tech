from main import  bot, dp, types

from aiogram.types import Message
from config import groupID, admin_id,WORDS,groupTO


# информирование о запуске бота
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


# команда START
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="id чата:<b>"+str(chat_id )+"</b>")

# слушаем сообщения
@dp.message_handler()
async def all_msg_handler(message: Message):
   mess= '"'+str(message.text)+ f'" \nПереслать это сообщение в тех.поддержку ?'
   text = message.text.lower()
   row = message
   for word in WORDS:
        if word in text:
            inline_btn_yes = types.InlineKeyboardButton('Да', callback_data='btn1')
            inline_btn_no = types.InlineKeyboardButton('Нет', callback_data='btn2')
            inline_kb_full = types.InlineKeyboardMarkup(row_width=2).add(inline_btn_yes, inline_btn_no)
            await bot.send_message(chat_id=groupID, text=mess, reply_markup=inline_kb_full )
            #print(message)

# обработка кнопок
@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data
    if code == "btn2":
             #await bot.answer_callback_query(callback_query.id,text='Ошибочка вышла 😉', show_alert=True)
             await bot.delete_message(chat_id=groupID, message_id=callback_query.message.message_id)


    else:
             await bot.answer_callback_query(callback_query.id,text='Отправляю', show_alert=True)
             mess_id = callback_query.message.message_id -1
             mess_user = callback_query.from_user.username
             mess_chat = callback_query.message.chat.title
             mess = "Сообщение из чата <b>"+str(mess_chat )+"</b> от пользователя <b>"+str(mess_user)+"</b>"
             inline_btn_no = types.InlineKeyboardButton('Перейти', callback_data='btn2', url='https://t.me/c/1529225672/'+str(mess_id))
             inline_kb_full = types.InlineKeyboardMarkup(row_width=1).add( inline_btn_no)
             await bot.delete_message(chat_id=groupID, message_id=callback_query.message.message_id)
             await bot.copy_message(chat_id=groupTO, from_chat_id=groupID, message_id=mess_id)
             await bot.send_message(chat_id=groupTO, text=mess, reply_markup=inline_kb_full)
             #print(callback_query)

