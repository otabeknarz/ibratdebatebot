from aiogram.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    name = State()
    english_level = State()
    age = State()
    phone_number = State()


class RegisterToDebateState(StatesGroup):
    location_date = State()


class SendPostState(StatesGroup):
    post = State()
