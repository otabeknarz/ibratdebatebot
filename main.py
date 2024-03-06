import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from db import Database


TOKEN = getenv("BOT_TOKEN")
bot = Bot(token="6731464739:AAF0MjIuQPQDSsruL3-bTtWN6z4G8S6AGGA")
db = Database('database.db')
form_router = Router()


class Form(StatesGroup):
    lang = State()
    # channel_followed = State()
    region = State()
    date = State()
    name = State()
    number = State()
    username = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await state.set_state(Form.lang)
    await message.answer(
        f"Tilni tanlang / Select the language",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Uzbek"),
                    KeyboardButton(text="English"),
                ]
            ],
            resize_keyboard=True,
        ),
    )
    
@form_router.message(Command("sendall"))
async def sendall(message: Message):
    if message.from_user.id == 1251979840:
        text = message.text[9:]
        users = db.get_users()
        for row in users:
            try:
                await bot.send_message(row[0], text)
                if int(row[1]) != 1:
                    db.set_active(row[0], 1)
            except:
                db.set_active(row[0], 0)
        
        await bot.send_message(message.from_user.id, "The message was sent")



@form_router.message(Form.lang, F.text.casefold() == "uzbek")
async def Uzbek(message: Message, state: FSMContext) -> None:
    await state.update_data(lang="Uzbek")
    await state.set_state(Form.region)
    await message.answer(
        f"Qaysi bir hududdagi klubga qatnashmoqchisiz ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Toshkent"),
                    KeyboardButton(text="Samarqand"),
                    KeyboardButton(text="Surxondaryo"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(Form.lang, F.text.casefold() == "english")
async def English(message: Message, state: FSMContext) -> None:
    await state.update_data(lang="English")
    await state.set_state(Form.region)
    await message.answer(
            f"Where do you want to participate ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Tashkent"),
                        KeyboardButton(text="Samarkand"),
                        KeyboardButton(text="Surxondaryo"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )





@form_router.message(lambda message: message.text.lower() in ["tashkent", "toshkent"], Form.region)
async def toshkent(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Toshkent")
    await state.set_state(Form.date)
    data = await state.get_data()
    language = data.get('lang', 'N/A')
    if(language == "Uzbek"):
        await message.answer(
            f"Qaysi bir kuni debatega qatnashmoqchisiz ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="07.03.2024 16:00dagi"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
    else:
        await message.answer(
            f"Which session you want to attend ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="on 07.03.2024 16:00"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )

    

@form_router.message(lambda message: message.text.lower() in ["samarqand", "samarkand"], Form.region)
async def samarqand(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Samarqand")
    await state.set_state(Form.date)
    data = await state.get_data()
    language = data.get('lang', 'N/A')
    if(language == "Uzbek"):
        await message.answer(
            f"Qaysi bir kuni debatega qatnashmoqchisiz ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="09.03.2024 13:30dagi"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
    else:
        await message.answer(
            f"Which session you want to attend ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="on 09.03.2024 13:30"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )


@form_router.message(lambda message: message.text.lower() in ["surxondaryo"], Form.region)
async def samarqand(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Surxondaryo")
    await state.set_state(Form.date)
    data = await state.get_data()
    language = data.get('lang', 'N/A')
    if(language == "Uzbek"):
        await message.answer(
            f"Qaysi bir kuni debatda qatnashmoqchisiz ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="09.03.2024 14:00dagi"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
    else:
        await message.answer(
            f"Which session you want to attend ?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="on 09.03.2024 14:00"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )


    


@form_router.message(Form.date)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(date="09.03.2024 or 07.03.2024")
    await state.set_state(Form.name)
    data = await state.get_data()
    language = data.get('lang', 'N/A')
    if(language == "Uzbek"):
        await message.answer(text="Ro’yxatdan o’tish uchun F.I.O yozing", reply_markup=ReplyKeyboardRemove(),)
    else:
        await message.answer(text="To register write down your full name", reply_markup=ReplyKeyboardRemove(),)


    
@form_router.message(Form.name)
async def process_number(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.number)
    data = await state.get_data()
    language = data.get('lang', 'N/A')
    if(language == "Uzbek"):
        await message.answer(text="Endi telefon raqamingizni kiriting", reply_markup=ReplyKeyboardRemove(),)
    else:
        await message.answer(text="Please, write your phone number", reply_markup=ReplyKeyboardRemove(),)



@form_router.message(Form.number)
async def send_user_info(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)

    # getting the user name
    await state.update_data(username = message.from_user.username)

    channel_id_tashkent = -1002079456954  # data channel id
    channel_id_samarkand = -1002103687550
    channel_id_surxondaryo = -1002146383510
    group_link = ""
    date = ""

    data = await state.get_data()


    message_text = f"User Information:\n\n"
    message_text += f"Region: {data.get('region', 'N/A')}\n"
    message_text += f"Name: {data.get('name', 'N/A')}\n"
    message_text += f"Telegram username: @{data.get('username', 'N/A')}\n"
    message_text += f"Phone number: {data.get('number', 'N/A')}\n"

    if data.get('region', 'N/A') == "Toshkent":
        group_link= "https://t.me/+9FsbILdXfWkwZGYy"
        date = "7-mart"
        message_text += f"Date: {date}\n"
        await bot.send_message(channel_id_tashkent, message_text)

    elif data.get('region', 'N/A') == "Samarqand":
        group_link= "https://t.me/+C5s6G4wWnMw2OTIy"
        date = "9-mart"
        message_text += f"Date: {date}\n"
        await bot.send_message(channel_id_samarkand, message_text)
    elif data.get('region', 'N/A') == "Surxondaryo":
        group_link= "https://t.me/+Iwwunl-CoEljMTBi"
        date = "9-mart"
        message_text += f"Date: {date}\n"
        await bot.send_message(channel_id_surxondaryo, message_text)



    user_id = message.from_user.id
    language = data.get('lang', 'N/A')
    if language == "Uzbek" :
        message_text = (
            f"Tabriklaymiz! Siz muvaffaqiyatli ro’yxatdan o’tdingiz.\n\n"
            f"Iltimos, klub vaqti, joylashuvi va shu kabi ko’proq ma’lumotlarni olish uchun guruxga qo’shiling:\n"
            f"{group_link}"
        )
    else: 
        message_text = (
            f"Congratulations! You have successfully registered.\n\n"
            f"Please join the group for club times, locations and more information like:\n"
            f"{group_link}\n"
            f"(Joining the group is required)"
        )

    await bot.send_message(user_id, message_text, parse_mode=ParseMode.MARKDOWN)






async def main():
    # bot = Bot(token="6731464739:AAF0MjIuQPQDSsruL3-bTtWN6z4G8S6AGGA", parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)

    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())