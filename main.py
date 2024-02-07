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

TOKEN = getenv("BOT_TOKEN")
bot = Bot(token="6731464739:AAF0MjIuQPQDSsruL3-bTtWN6z4G8S6AGGA", parse_mode=ParseMode.HTML)

form_router = Router()


class Form(StatesGroup):
    lang = State()
    region = State()
    date = State()
    name = State()
    number = State()
    username = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
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


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )




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
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.region, F.text.casefold() == "toshkent")
async def toshkent(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Toshkent")
    await state.set_state(Form.date)

    await message.answer(
        f"Qaysi bir kuni debatega qatnashmoqchisiz ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="09.02.2024 16:00dagi"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(Form.region, F.text.casefold() == "samarqand")
async def samarqand(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Samarqand")
    await state.set_state(Form.date)

    await message.answer(
        f"Qaysi bir kuni debatega qatnashmoqchisiz ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="09.02.2024 13:30dagi"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.region, F.text.casefold() == "tashkent")
async def toshkent(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Toshkent")
    await state.set_state(Form.date)

    await message.answer(
        f"Which session you want to attend ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="on 09.02.2024 16:00"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(Form.region, F.text.casefold() == "samarkand")
async def samarqand(message: Message, state: FSMContext) -> None:
    await state.update_data(region="Samarqand")
    await state.set_state(Form.date)

    await message.answer(
        f"Which session you want to attend ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="on 09.02.2024 13:30"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.date)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(date="09.02.2024")
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


    data = await state.get_data()
    message_text = f"User Information:\n\n"
    message_text += f"Region: {data.get('region', 'N/A')}\n"
    message_text += f"Date: {data.get('date', 'N/A')}\n"
    message_text += f"Name: {data.get('name', 'N/A')}\n"
    message_text += f"telegram username: @{data.get('username', 'N/A')}\n"
    message_text += f"Phone Number: {data.get('number', 'N/A')}\n"

    channel_id_tashkent = -1002079456954  # data channel id
    channel_id_samarkand = -1002103687550
    group_link = ""
    if data.get('region', 'N/A') == "Toshkent":
        await bot.send_message(channel_id_tashkent, message_text)
        group_link= "https://t.me/+9FsbILdXfWkwZGYy"
    elif data.get('region', 'N/A') == "Samarqand":
        await bot.send_message(channel_id_samarkand, message_text)
        group_link= "https://t.me/+C5s6G4wWnMw2OTIy"
    else: return True


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