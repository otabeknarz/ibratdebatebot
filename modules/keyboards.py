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
                [KeyboardButton(text="✍️ Debate ga yozilish")],
                [KeyboardButton(text="👀 Kelasi Debate larni ko'rish")],
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
                [KeyboardButton(text="B1-B2"), KeyboardButton(text="C1-C2")],
            ],
            resize_keyboard=True,
        )

        self.ages_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="12-14"), KeyboardButton(text="14-16")],
                [
                    KeyboardButton(text="16-18"),
                    KeyboardButton(text="18 va undan yuqori"),
                ],
            ],
            resize_keyboard=True,
        )


class InlineButtons:
    def __init__(self):
        # Inline Keyboards
        ibrat_debate_channel = InlineKeyboardButton(
            text="Ibrat Debate kanaliga obuna bo'lish",
            url="https://t.me/" + bot_settings.IBRAT_DEBATE_CHANNEL[1:],
        )
        instagram_inline_btn = InlineKeyboardButton(
            text="Instagram", url="https://www.instagram.com/ibrat.debate/"
        )
        ive_subscribed_btn = InlineKeyboardButton(
            text="A'zo bo'ldim", callback_data="subscribed"
        )
        self.subscribe_inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [ibrat_debate_channel],
                [instagram_inline_btn],
                [ive_subscribed_btn],
            ]
        )

    @staticmethod
    def groups_subscribe_inline(location_name, group_link, debate_pk) -> InlineKeyboardMarkup:
        debaters_community = InlineKeyboardButton(
            text="Uzbekistan Debaters Community",
            url="https://t.me/+wl-EPgQAWXNjNzI6",
        )
        group_inline_button = InlineKeyboardButton(
            text=location_name, url=group_link
        )
        ive_subscribed_btn = InlineKeyboardButton(
            text="A'zo bo'ldim", callback_data=f"s_groups|{group_link}|{debate_pk}"
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [debaters_community],
                [group_inline_button],
                [ive_subscribed_btn]
            ]
        )
