import os
import dotenv

# Loading dotenv function to detect .env file
dotenv.load_dotenv()


class Settings:
    def __init__(self):
        # Admin settings
        self.ADMINS = {
            "Otabek Narz": 5551503420,
            "Abdulaziz": 1251979840,
            "Mirzohid": 5541894729,
            "Sherzodbek": 1431296496,
        }

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.BASE_URL = os.getenv("BASE_URL")
        self.BASE_MEDIA_URL = self.BASE_URL + "/media/"
        self.API_ENDPOINT = self.BASE_URL + "/api/v1/"
        # [POST] People object (dict) should be form {"ID": str, "name": str, "english_level": str, "phone_number": str}
        self.AUTH_USER_URL = self.API_ENDPOINT + "users/auth/"
        self.CREATE_USER_URL = self.API_ENDPOINT + "users/create/"
        self.UPDATE_USER_URL = self.API_ENDPOINT + "users/update/"
        # [GET] Response -> {"status": "true", "people": People} if True else {"status": "false", "detail": "there is
        # no user with this ID"}
        self.CHECK_USER_URL = self.API_ENDPOINT + "users/check/"
        # [GET] Response -> {"status": "true", "people_ID": [{"ID": "123"}, ...]}
        self.GET_USERS_ID = self.API_ENDPOINT + "users/get-ids/"
        # [GET] Response -> {"status": "true", [{debate_1}, {debate_2}, ...]} if True else {"status": "false",
        # "detail": "something went wrong"}
        self.GET_DEBATES_URL = self.API_ENDPOINT + "get-debates/?format=json"

        # {"people_id": "people_id", "debate_id": "debate_id"}
        self.REGISTER_PEOPLE_TO_DEBATE_URL = (
            self.API_ENDPOINT + "register-people-to-debate/"
        )

        # Debate channel
        self.IBRAT_DEBATE_CHANNEL = "@ibratdebate"
        self.UZBEKISTAN_DEBATERS_GROUP = "https://t.me/+wl-EPgQAWXNjNzI6"
        self.DEBATERS_COMMUNITY_USERNAME = "@debaters_community"

        self.TIME_ZONE = "Etc/GMT-5"

        self.ENGLISH_LEVELS = "B1-B2", "C1-C2"
        self.AGES = {
            "12-14": "12-14",
            "14-16": "14-16",
            "16-18": "16-18",
            "18 va undan yuqori": "18<",
        }

        self.SEND_FIRST_NAME_MESSAGE = "Iltimos, Ism familiyangizni to'liq yozing."
        self.SEND_PHONE_NUMBER_MESSAGE = "Telefon raqamingizni quyidagi tugmani bosib yuboring"
        self.SEND_ENGLISH_LEVEL_MESSAGE = "Ingliz tili darajangizni ushbu tugmalardan tanlab yuboring"
        self.SEND_AGE_MESSAGE = "Yoshingizni ushbu tugmalardan tanlab yuboring"

