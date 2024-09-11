import asyncio
import logging

import pytz
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import types

import sys
import datetime

# Load aiogram's built in FSMContext to store state data
from aiogram.fsm.context import FSMContext

# Local modules
from modules.filters import TextEqualsFilter
from modules.functions import get_req, post_req
from modules.keyboards import Buttons, InlineButtons
from modules.settings import Settings
from modules.states import RegistrationState, RegisterToDebateState, SendPostState
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import json

# Load all settings in var bot_settings
bot_settings = Settings()
BOT_TOKEN = bot_settings.BOT_TOKEN

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

buttons = Buttons()
inline_buttons = InlineButtons()


async def is_subscribed(bot, message: types.Message, state=None):
    """The function checks the did user subscribe the channel if so returns True else False"""
    is_subscribed_ = await bot.get_chat_member(
        chat_id=bot_settings.IBRAT_DEBATE_CHANNEL, user_id=message.chat.id
    )
    if is_subscribed_.status == "left":
        await message.answer(
            "Botdan foydalanishingiz uchun birinchi navbatda bizning kanalga a'zo bo'lishingiz kerak",
            reply_markup=inline_buttons.subscribe_inline,
        )
        if state:
            await state.clear()

        return False
    return True


# Start Registration
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    if not await is_subscribed(bot, message):
        return

    try:
        response = get_req(
            bot_settings.CHECK_PEOPLE_URL + str(message.chat.id) + "/"
        ).json()
    except:
        await message.answer("Something went wrong :)")
        return

    if message.chat.id in bot_settings.ADMINS.values():
        await message.reply(
            f"Assalomu alaykum <strong>{message.from_user.full_name}!</strong>",
            reply_markup=buttons.admin_main_keyboard,
            parse_mode="html",
        )
    elif response["status"] == "false":
        await message.reply(
            "Assalomu alaykum!\nDebate ga qatnashishdan oldin botdan ro'yxatdan o'ting",
            reply_markup=buttons.register_btn,
        )
    else:
        await message.reply(
            f"Qaytganingiz bilan <strong>{response['people']['name']}!</strong>",
            reply_markup=buttons.main_keyboard,
            parse_mode="html",
        )


@dp.callback_query()
async def check_subs_callback(callback: types.CallbackQuery):
    if callback.data == "subscribed":
        is_subscribed = await bot.get_chat_member(
            chat_id=bot_settings.IBRAT_DEBATE_CHANNEL, user_id=callback.message.chat.id
        )
        if is_subscribed.status != "left":
            try:
                response = get_req(
                    bot_settings.CHECK_PEOPLE_URL + str(callback.message.chat.id) + "/"
                ).json()
            except:
                await callback.answer("Something went wrong")
                return
            if response["status"] == "false":
                await callback.message.reply(
                    f"Assalomu alaykum\n"
                    f"Debate ga qatnashishdan oldin botdan ro'yxatdan o'ting",
                    reply_markup=buttons.register_btn,
                )
            else:
                await callback.message.answer(
                    "Botdan foydalanishingiz mumkin.",
                    reply_markup=buttons.main_keyboard,
                )
        else:
            await bot.answer_callback_query(
                callback.id,
                "Botdan foydalanishingiz uchun birinchi navbatda bizning kanalga a'zo bo'lishingiz kerak",
                show_alert=True,
            )
            await callback.message.delete()
            await callback.message.answer(
                "Botdan foydalanishingiz uchun birinchi navbatda bizning kanalga a'zo bo'lishingiz kerak",
                reply_markup=inline_buttons.subscribe_inline,
            )


@dp.message(TextEqualsFilter("✍️ Ro'yxatdan o'tish"))
async def run_name_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message):
        return

    await message.answer(
        "Ism familiyangizni to'liq yozing",
        reply_markup=buttons.remove_btn,
    )

    await state.set_state(RegistrationState.name)


@dp.message(RegistrationState.name)
async def name_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message, state):
        return

    name = message.text
    await message.answer(
        "Endi ingliz til darajangizni quyidagi tugmalardan tanlang!",
        reply_markup=buttons.english_level_keyboard,
    )
    await state.update_data(ID=str(message.chat.id), name=name)
    await state.set_state(RegistrationState.english_level)


@dp.message(RegistrationState.english_level)
async def english_level_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message, state):
        return

    english_level = message.text
    if english_level not in bot_settings.ENGLISH_LEVELS:
        await message.answer(
            "Iltimos quyidagi tugmalardan tanlang",
            reply_markup=buttons.english_level_keyboard,
        )
        await state.set_state(RegistrationState.english_level)
        return

    await message.answer(
        "Endi telefon raqamingizni yuboring buning uchun quyidagi tugamni bosing!",
        reply_markup=buttons.phone_number_btn,
    )

    await state.update_data(english_level=english_level)
    await state.set_state(RegistrationState.phone_number)


@dp.message(RegistrationState.phone_number)
async def phone_number_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message, state):
        return

    await state.update_data(phone_number=message.contact.phone_number)
    response = post_req(bot_settings.CREATE_PEOPLE_URL, await state.get_data())
    if response.status_code == 201:
        await message.answer(
            "Siz ro'yxatdan o'tdingiz", reply_markup=buttons.main_keyboard
        )
    else:
        await message.answer(
            "Xatolik yuz berdi qaytadan urinib ko'ring",
            reply_markup=buttons.register_btn,
        )
    await state.clear()


# End Registration


# Show Debates
@dp.message(TextEqualsFilter("👀 Kelasi Debate larni ko'rish"))
async def show_debates(message: types.Message):
    debates = get_req(bot_settings.GET_DEBATES_URL).json()
    msg = "<b>Bizda kelasi debate lar:</b>\n"
    for key, debate in enumerate(debates):
        date = datetime.datetime.fromisoformat(debate["date"])
        msg += (
            f"<b>{key + 1}. </b>"
            + debate["location"]["name"]
            + " "
            + date.strftime("%d/%m, %H:%M")
            + "\n"
        )

    await message.answer(msg)


@dp.message(TextEqualsFilter("❌ Bekor qilish"))
async def cancel_all(message: types.Message, state: FSMContext = None):
    if state:
        await state.clear()

    await message.answer("Bekor qilindi ✅", reply_markup=buttons.main_keyboard)
    return


@dp.message(TextEqualsFilter("✍️ Debate ga yozilish"))
async def register_debate(message: types.Message, state: FSMContext):
    debates = get_req(bot_settings.GET_DEBATES_URL).json()
    debate_texts = [
        debate["location"]["name"]
        + " "
        + datetime.datetime.fromisoformat(debate["date"]).strftime("%d/%m %H:%M")
        for debate in debates
    ]
    debates_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=debate_text)] for debate_text in debate_texts]
        + [[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True,
    )

    await message.answer(
        "Bu yerda bizda tez kunda bo'ladigan debate larimizning ro'yxati",
        reply_markup=debates_markup,
    )

    await state.update_data(debates=debates, debate_texts=debate_texts)
    await state.set_state(RegisterToDebateState.location_date)


@dp.message(RegisterToDebateState.location_date)
async def regitser_debate_fin(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if message.text not in state_data["debate_texts"]:
        await message.answer(
            "Quyidagi tugmalardan tanlashingiz mumkin",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=debate_text)]
                    for debate_text in state_data["debate_texts"]
                ]
                + [[KeyboardButton(text="❌ Bekor qilish")]],
                resize_keyboard=True,
            ),
        )
        await state.set_state(RegisterToDebateState.location_date)
        return

    location, date, time = message.text.split(" ")

    location_date = datetime.datetime(
        year=2024,
        day=int(date.split("/")[0]),
        month=int(date.split("/")[1]),
        hour=int(time.split(":")[0]),
        minute=int(time.split(":")[1]),
        tzinfo=pytz.timezone(bot_settings.TIME_ZONE),
    )
    for debate in state_data["debates"]:
        if debate["location"]["name"] == location:
            if location_date == datetime.datetime.fromisoformat(debate["date"]):
                if (
                    post_req(
                        bot_settings.REGISTER_PEOPLE_TO_DEBATE_URL,
                        {"people_id": message.chat.id, "debate_id": debate["pk"]},
                    ).json()["status"]
                    == "true"
                ):
                    await message.answer(
                        f"Ro'yxatdan o'tdingiz\n"
                        f"Joylashuv: {location}\n"
                        f"Sana va vaqt: {date}, {time}\n"
                        f"Telegram guruh uchun link: {debate['location']['telegram_group_link']}",
                        reply_markup=buttons.main_keyboard,
                    )

    await state.clear()


# Handlers for admins


@dp.message(TextEqualsFilter("📮 Yangi post yuborish"))
async def send_post_set(message: types.Message, state: FSMContext):
    if message.chat.id not in bot_settings.ADMINS.values():
        return
    await message.answer(
        "Ok, Postingizni jo'nating!", reply_markup=buttons.cancel_markup
    )
    await state.set_state(SendPostState.post)


@dp.message(SendPostState.post)
async def send_post(message: types.Message, state: FSMContext):
    if message.chat.id not in bot_settings.ADMINS.values():
        return
    text = message.text
    if text == "❌ Bekor qilish" or text == "📮 Yangi post yuborish":
        await state.clear()
        await message.answer("Bekor qilindi", reply_markup=buttons.admin_main_keyboard)
        return

    people_id = get_req(bot_settings.GET_PEOPLE_ID).json()
    unregistered_people_count = 0
    posted_people_count = 0
    await message.answer("Post yuborilmoqda...")
    for people in people_id["people_ID"]:
        try:
            await message.send_copy(people["ID"])
            posted_people_count += 1
        except:
            unregistered_people_count += 1

    await message.answer("Post jo'natildi", reply_markup=buttons.admin_main_keyboard)
    if unregistered_people_count:
        await message.answer(
            f"{posted_people_count} ta foydalanuvchiga post jo'natildi\n"
            f"{unregistered_people_count} ta ro'yxatdan o'tgan foydalanuvchi hozir botni ishlatmayapti"
        )
    await state.clear()


async def on_startup_notify(arg):
    for admin in bot_settings.ADMINS.values():
        try:
            await bot.send_message(
                admin,
                f"Bot has been ran successfully\n{datetime.datetime.now().strftime('%H:%M %d/%m/%Y')}",
            )
        except:
            print(f"Message wasn't sent to admin {admin}")


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot, on_startup_notify=on_startup_notify)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
