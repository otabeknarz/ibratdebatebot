from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


checkSubMenuUzb = InlineKeyboardMarkup(inline_keyboard=[InlineKeyboardButton(text="Obuna bo'ling", url="https://t.me/debatuz"), 
            InlineKeyboardButton(text="Tekshirish✅", callback_data="subchanneldone")])



btnUrlChannelEng = InlineKeyboardButton(text="Subsribe", url="https://t.me/debatuz")
btnDoneSubEng = InlineKeyboardButton(text="Done✅", callback_data="subchanneldone")

checkSubMenuEng = InlineKeyboardMarkup(row_width=1)
checkSubMenuEng.add(btnUrlChannelEng)
checkSubMenuEng.add(btnDoneSubEng)