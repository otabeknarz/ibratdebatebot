from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from .settings import Settings

bot_settings = Settings()


class Buttons:
    def __init__(self):
        # Buttons for admins
        self.admin_main_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📮 Yangi post yuborish")],
            ],
            resize_keyboard=True,
        )

        self.phone_number_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="Telefon raqamimni ulashish", request_contact=True
                    )
                ]
            ]
        )
        self.register_btn = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✍️ Ro'yxatdan o'tish")],
            ],
            resize_keyboard=True,
        )
        self.main_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✍️ Debate ga yozilish")],
                [KeyboardButton(text="👀 Kelasi Debate larni ko'rish")],
            ],
            resize_keyboard=True,
        )
        self.remove_btn = ReplyKeyboardRemove()
        self.cancel_markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ Bekor qilish")]]
        )

        self.english_level_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="A1"), KeyboardButton(text="A2")],
                [KeyboardButton(text="B1"), KeyboardButton(text="B2")],
                [KeyboardButton(text="C1"), KeyboardButton(text="C2")],
            ],
            resize_keyboard=True
        )


class InlineButtons:
    def __init__(self):
        # Inline Keyboards
        ibrat_debate_channel = InlineKeyboardButton(
            text="Ibrat Debate kanaliga obuna bo'lish",
            url="https://t.me/" + bot_settings.IBRAT_DEBATE_CHANNEL[1:],
        )
        ive_subscribed_btn = InlineKeyboardButton(
            text="A'zo bo'ldim", callback_data="subscribed"
        )
        self.subscribe_inline = InlineKeyboardMarkup(
            inline_keyboard=[[ibrat_debate_channel], [ive_subscribed_btn]]
        )
