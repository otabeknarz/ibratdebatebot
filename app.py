import asyncio
import logging

import pytz
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import types
from aiogram.methods import DeleteWebhook

import sys
import datetime

# Load aiogram's built in FSMContext to store state data
from aiogram.fsm.context import FSMContext

# Local modules
from modules.filters import TextEqualsFilter
from modules.functions import get_req, post_req, patch_req, create_user
from modules.keyboards import Buttons, InlineButtons
from modules.settings import Settings
from modules.states import RegistrationState, RegisterToDebateState, SendPostState
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

# Load all settings in var bot_settings
bot_settings = Settings()
BOT_TOKEN = bot_settings.BOT_TOKEN

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

buttons = Buttons()
inline_buttons = InlineButtons()


async def run_name_state_(message: types.Message, state: FSMContext):
    await message.answer(bot_settings.SEND_FIRST_NAME_MESSAGE)
    await state.clear()
    await state.set_state(RegistrationState.name)

async def run_phone_number_state_(message: types.Message, state: FSMContext):
    await message.answer(bot_settings.SEND_PHONE_NUMBER_MESSAGE, reply_markup=buttons.phone_number_btn)
    await state.clear()
    await state.set_state(RegistrationState.phone_number)


async def run_english_level_state_(message: types.Message, state: FSMContext):
    await message.answer(bot_settings.SEND_ENGLISH_LEVEL_MESSAGE, reply_markup=buttons.english_level_keyboard)
    await state.clear()
    await state.set_state(RegistrationState.english_level)


async def run_age_state_(message: types.Message, state: FSMContext):
    await message.answer(bot_settings.SEND_AGE_MESSAGE, reply_markup=buttons.ages_keyboard)
    await state.clear()
    await state.set_state(RegistrationState.age)


async def is_subscribed(bot, message: types.Message, state=None):
    """The function checks the did user subscribe the channel if so returns True else False"""
    is_subscribed_ = await bot.get_chat_member(
        chat_id=bot_settings.IBRAT_DEBATE_CHANNEL, user_id=message.chat.id
    )
    if is_subscribed_.status == "left":
        await message.answer(
            "Assalomu alaykum hurmatli debatchi,\n\n\"Ibrat Debate\" ga qo'shilish uchun birinchi qadamingiz bilan tabriklayman.\n\nBotdan foydalanishingiz uchun birinchi navbatda bizning ijtimoiy tarmoqdagi kanallarimizga a'zo bo'lishingiz kerak 👇",
            reply_markup=inline_buttons.subscribe_inline,
        )
        if state:
            await state.clear()

        return False
    return True


# Start Registration
@dp.message(CommandStart())
async def send_welcome(message: types.Message, was_not_registered=False):
    if not await is_subscribed(bot, message):
        return
    
    if message.from_user.id in bot_settings.ADMINS.values():
        await message.reply(
            f"Assalomu alaykum <strong>{message.from_user.full_name}!</strong>\nAdmin aka xush kelibsiz",
            reply_markup=buttons.admin_main_keyboard,
            parse_mode="html",
        )
    
    if was_not_registered:
        await message.reply(
            "Afsuski ma'lumotlaringizni topa olmadik 😔\nRo'yxatdan o'tish uchun quyidagi tugmani bosing.",
            reply_markup=buttons.register_btn,
        )
        return

    try:
        response = post_req(
            bot_settings.CREATE_USER_URL,
            json={
                "id": str(message.chat.id),
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name if message.from_user.last_name else "",
                "username": message.from_user.username if message.from_user.username else str(message.chat.id),
            },
        )
    except Exception as e:
        logger.error(e)
        await message.answer("Hozirda serverlarimizda tuzatish ishlari olib borilyabdi. Kamchiliklar uchun uzr so'raymiz :)")
        return

    json_response = response.json()

    if response.status_code == 201 or json_response.get("user", {}).get("phone_number") is None:
        await message.reply(
            "Assalomu alaykum Ibrat Debate ning rasmiy botiga xush kelibsiz\nRo'yxatdan o'tish uchun quyidagi tugmani bosing.",
            reply_markup=buttons.register_btn,
        )
    else:
        await message.reply(
            f"Qaytganingiz bilan <strong>{json_response.get("user").get("first_name")}!</strong>",
            reply_markup=buttons.main_keyboard,
            parse_mode="html",
        )


async def check_is_user_registered(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else user_id
    response = post_req(bot_settings.AUTH_USER_URL, {"id": user_id, "username": username})
    json_response = response.json()
    if response.status_code == 201:
        await send_welcome(message, was_not_registered=True)
        return False
    elif json_response.get("registering_is_not_completed"):
        states = {
            "first_name": (RegistrationState.name, run_name_state_),
            "english_level": (RegistrationState.english_level, run_english_level_state_),
            "age": (RegistrationState.age, run_age_state_),
            "phone_number": (RegistrationState.phone_number, run_phone_number_state_),
        }
        what_to_update = json_response.get("what_to_update")
        await state.clear()
        await state.set_state(states.get(what_to_update)[0])
        await states.get(what_to_update)[1](message, state)
        return False
    return True


@dp.callback_query()
async def check_subs_callback(callback: types.CallbackQuery):
    data = callback.data.split("|")
    if data[0] == "subscribed":
        is_subscribed = await bot.get_chat_member(
            chat_id=bot_settings.IBRAT_DEBATE_CHANNEL, user_id=callback.message.chat.id
        )
        if is_subscribed.status != "left":
            try:
                response = get_req(
                    bot_settings.CHECK_USER_URL + str(callback.message.chat.id) + "/"
                )
            except Exception as e:
                logger.error(str(e))
                await callback.answer("Something went wrong")
                return
            if response.status_code != 200:
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

    elif data[0] == "s_groups":
        _, group_link, debate_pk = data
        is_subscribed_ = await bot.get_chat_member(
            chat_id=bot_settings.DEBATERS_COMMUNITY_USERNAME, user_id=callback.message.chat.id
        )
        if is_subscribed_.status == "left":
            group_inline_buttons = inline_buttons.groups_subscribe_inline(
                "Guruh",
                group_link,
                debate_pk
            )
            await callback.message.delete()
            await callback.message.answer(
                "Ro'yxatdan o'tishni yakunlash uchun siz debatchilarning "
                "telegramdagi ikki guruhiga qo'shilishingiz kerak 👇",
                reply_markup=group_inline_buttons,
            )
        else:
            is_subscribed_ = await bot.get_chat_member(
                chat_id="@" + group_link.split("/")[-1], user_id=callback.message.chat.id
            )
            if is_subscribed_.status == "left":
                group_inline_buttons = inline_buttons.groups_subscribe_inline(
                    "Guruh",
                    group_link,
                    debate_pk
                )
                await callback.message.delete()
                await callback.message.answer(
                    "Ro'yxatdan o'tishni yakunlash uchun siz debatchilarning "
                    "telegramdagi ikki guruhiga qo'shilishingiz kerak 👇",
                    reply_markup=group_inline_buttons,
                )
            else:
                response = post_req(
                    bot_settings.REGISTER_PEOPLE_TO_DEBATE_URL,
                    {"user_id": callback.message.chat.id, "debate_id": debate_pk},
                )
                json_response = response.json()
                if response.status_code in (200, 201):
                    qr_code_path = json_response.get("qr_code_path")
                    await bot.send_photo(
                        callback.message.chat.id,
                        photo="https://ibratdebate.uz/static/images/bot-invitation.png",
                        caption="👏 Tabriklaymiz,\n\n Siz ro'yxatdan muvaffaqqiyatli o'tdingiz ✅\n\n"
                                " Sizni debatlarda kutamiz.\n\n O'zingiz bilan yaxshi kayfiyat va "
                                "maqsadlari bir bo'lgan o'rtoqlaringizni birga olib kelishni ham unutmang )",
                        reply_markup=buttons.main_keyboard,
                    )
                    await asyncio.sleep(1)
                    await bot.send_photo(
                        callback.message.chat.id,
                        bot_settings.BASE_MEDIA_URL + qr_code_path,
                        caption="Manabu sizning ticketingiz, borganingizda koordinatorlarga ushbu ticketni ko'rsatasiz, rahmat!"
                    )


@dp.message(TextEqualsFilter("✍️ Ro'yxatdan o'tish"))
async def run_name_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message):
        return

    await create_user(
        str(message.from_user.id),
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
    )

    await message.answer(
        "Iltimos, Ism familiyangizni to'liq yozing.",
        reply_markup=buttons.remove_btn,
    )

    await state.set_state(RegistrationState.name)


@dp.message(RegistrationState.name)
async def name_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message, state):
        return

    name = message.text
    await message.answer(
        "Quyidagi tugmani bosib o'z telefon raqamingizni yuboring.",
        reply_markup=buttons.phone_number_btn,
    )
    await state.update_data(first_name=name)
    await state.set_state(RegistrationState.phone_number)


@dp.message(RegistrationState.phone_number)
async def phone_number_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message, state):
        return
    
    if not message.contact or message.contact.user_id != message.from_user.id:
        await state.set_state(RegistrationState.phone_number)
        await message.answer("Iltimos quyidagi tugmani bosib o'z telefon raqamingizni yuboring", buttons.phone_number_btn)
        return

    await state.update_data(phone_number=message.contact.phone_number)
    
    await message.answer("Iingliz til darajangizni quyidagi tugmalardan tanlang!", reply_markup=buttons.english_level_keyboard)
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
        "Yoshingizni quyidagi tugmalardan tanlang!",
        reply_markup=buttons.ages_keyboard,
    )

    await state.update_data(english_level=english_level)
    await state.set_state(RegistrationState.age)


@dp.message(RegistrationState.age)
async def age_state(message: types.Message, state: FSMContext):
    if not await is_subscribed(bot, message, state):
        return

    age = message.text
    if age not in bot_settings.AGES.keys():
        await message.answer(
            "Iltimos quyidagi tugmalardan tanlang",
            reply_markup=buttons.ages_keyboard,
        )
        await state.set_state(RegistrationState.age)
        return

    await state.update_data(age=bot_settings.AGES.get(age))

    response = patch_req(bot_settings.UPDATE_USER_URL + str(message.chat.id) + "/", await state.get_data())

    if response.status_code in (201, 200):
        await message.answer(
            f"Tabriklayman <strong>{response.json().get("first_name")}</strong>, siz botdan ro'yxatdan o'tdingiz!\n"
            "Debate ga ro'yxatdan o'tish uchun '✍️ Debate ga yozilish' tugmasini bosing",
            reply_markup=buttons.main_keyboard
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
async def show_debates(message: types.Message, state: FSMContext):
    if not await check_is_user_registered(message, state):
        return
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

    await message.answer(
        "Bekor qilindi ✅",
        reply_markup=buttons.main_keyboard
        if message.chat.id not in bot_settings.ADMINS.values()
        else buttons.admin_main_keyboard,
    )
    return


@dp.message(TextEqualsFilter("✍️ Debate ga yozilish"))
async def register_debate(message: types.Message, state: FSMContext):
    if not await check_is_user_registered(message, state):
        return

    debates = get_req(bot_settings.GET_DEBATES_URL).json()
    debate_texts = [
        debate["location"]["name"]
        + " | "
        + datetime.datetime.fromisoformat(debate["date"]).strftime("%d/%m | %H:%M")
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
async def register_debate_fin(message: types.Message, state: FSMContext):
    if not await check_is_user_registered(message, state):
        return

    state_data = await state.get_data()
    if message.text not in state_data.get("debate_texts", []):
        await message.answer(
            "Quyidagi tugmalardan tanlashingiz mumkin",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=debate_text)]
                    for debate_text in state_data.get("debate_texts", [])
                ]
                + [[KeyboardButton(text="❌ Bekor qilish")]],
                resize_keyboard=True,
            ),
        )
        await state.set_state(RegisterToDebateState.location_date)
        return

    location, date, time = message.text.split(" | ")
    print(location, date, time)

    location_date = datetime.datetime(
        year=2025,
        day=int(date.split("/")[0]),
        month=int(date.split("/")[1]),
        hour=int(time.split(":")[0]),
        minute=int(time.split(":")[1]),
        tzinfo=pytz.timezone(bot_settings.TIME_ZONE),
    )
    for debate in state_data.get("debates", []):
        if debate.get("location", {}).get("name") == location:
            debate_date = datetime.datetime.fromisoformat(debate["date"])
            if location_date == datetime.datetime(
                    debate_date.year,
                    debate_date.month,
                    debate_date.day,
                    debate_date.hour,
                    debate_date.minute,
                    tzinfo=pytz.timezone(bot_settings.TIME_ZONE),
            ):
                group_inline_buttons = inline_buttons.groups_subscribe_inline(
                    debate['location']['name'],
                    debate['location']['telegram_group_link'],
                    debate['id']
                )
                await message.answer(
                    "Ro'yxatdan o'tishni yakunlash uchun siz debatchilarning "
                    "telegramdagi ikki guruhiga qo'shilishingiz kerak 👇",
                    reply_markup=group_inline_buttons,
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


@dp.message()
async def all_handler(message: types.message, state: FSMContext):
    if not await check_is_user_registered(message, state):
        return
    await message.answer("Asosiy", reply_markup=buttons.main_keyboard)


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
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, on_startup_notify=on_startup_notify)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
