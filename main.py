import telebot
from telebot import types

bot = telebot.TeleBot("6399662421:AAGYRA_YIm52fNe5dyl1uHVNONbfDf9RhXU")


def start_markup(status):
    markup = types.InlineKeyboardMarkup(row_width=True)
    link_keyboard = types.InlineKeyboardButton(text="Barcha kanalga bittada qo'shilish", url="https://t.me/addlist/dlpwMmHRLdFhMDAy")
    link_to_the_channel = types.InlineKeyboardButton(text="Marathon kanali", url="https://t.me/+yNK1vLdpprY0YjRi")
    check_keyboard = types.InlineKeyboardButton(text="Tekshirish ✅", callback_data="check")
    link_keyboard1 = types.InlineKeyboardButton(text="Azizbek Zaripov", url="t.me/akzaripovs")
    link_keyboard2 = types.InlineKeyboardButton(text="Abrorbek Nematov", url="https://t.me/Nematov_Abrorbek")
    link_keyboard3 = types.InlineKeyboardButton(text="Adilkhan Kenpeilov", url="https://t.me/adilwithin")
    link_keyboard4 = types.InlineKeyboardButton(text="Azizbek Zaylobiddinov", url="https://t.me/abdulazizziy")
    if( status == True ):
        markup.add(link_keyboard, link_keyboard1, link_keyboard2, link_keyboard3, link_keyboard4, check_keyboard)
    elif( status == False):
        markup.add(link_to_the_channel)

    return markup
 

# def give_link():
#     markup1 = types.InlineKeyboardMarkup(row_width=True)
#     link_to_the_channel = types.InlineKeyboardButton(text="Way to 1500+", url="https://t.me/+yNK1vLdpprY0YjRi")
#     markup1.add(link_to_the_channel)
#     return markup1

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f"Assalomu alaykum {first_name}!\n \n"
                              f"Marathonga qiziqganingizdan xursandmiz. Bepul SAT Marathonimizga qo'shilish uchun quyidagi kanallarga obuna bo'lishingiz kerak 👇\n \n"
                              f"Qo'shilgandan so'ng, tekshirish tugmasini bosing. So'ng, bot sizga Marathonga qo'shilish uchun Link beradi.", reply_markup=start_markup(True))


def check(call):
    status = ['creator', 'administrator', 'member']
    for i in status:
        if i == bot.get_chat_member(chat_id="-1001861916867", user_id=call.message.chat.id).status:
            check2(call)
            break

    else:
        bot.send_message(call.message.chat.id, "Xali siz barcha kanalga obuna bo'lmagansiz. Iltimos barcha kanallarga obuna bo'ling va keyin tekshirish tugmasini bosing", reply_markup=start_markup(True))

def check2(call):
    status = ['creator', 'administrator', 'member']
    for i in status:
        if i == bot.get_chat_member(chat_id="-1001924103206", user_id=call.message.chat.id).status:
            check3(call)
            break

    else:
        bot.send_message(call.message.chat.id, "Xali siz barcha kanalga obuna bo'lmagansiz. Iltimos barcha kanallarga obuna bo'ling va keyin tekshirish tugmasini bosing", reply_markup=start_markup(True))

def check3(call):
    status = ['creator', 'administrator', 'member']
    for i in status:
        if i == bot.get_chat_member(chat_id="-1001618038051", user_id=call.message.chat.id).status:
            check4(call)
            break

    else:
        bot.send_message(call.message.chat.id, "Xali siz barcha kanalga obuna bo'lmagansiz. Iltimos barcha kanallarga obuna bo'ling va keyin tekshirish tugmasini bosing", reply_markup=start_markup(True))
        
def check4(call):
    status = ['creator', 'administrator', 'member']
    for i in status:
        if i == bot.get_chat_member(chat_id="-1001825051597", user_id=call.message.chat.id).status:
            bot.send_message(call.message.chat.id, "Juda zo'r 👏. Bepul SAT Marathonga qo'shilganingiz bilan tabriklaymiz. Pastki tugmadagi link orqali marathon kanaliga qo'shiling 👇", reply_markup=start_markup(False))
        
            break

    else:
        bot.send_message(call.message.chat.id, "Xali siz barcha kanalga obuna bo'lmagansiz. Iltimos barcha kanallarga obuna bo'ling va keyin tekshirish tugmasini bosing", reply_markup=start_markup(True))


@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    if call.data == 'check':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        check(call)


bot.polling(none_stop=True)
