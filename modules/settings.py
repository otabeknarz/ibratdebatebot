import os
import dotenv

# Loading dotenv function to detect .env file
dotenv.load_dotenv()


class Settings:
    def __init__(self):
        # Admin settings
        self.ADMINS = {
            "Otabek Narz": 5551503420,
        }

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.BASE_URL = "https://otabek.me/"
        self.API_ENDPOINT = self.BASE_URL + "api/v1/"
        # [POST] People object (dict) should be form {"ID": str, "name": str, "english_level": str, "phone_number": str}
        self.CREATE_PEOPLE_URL = self.API_ENDPOINT + "create-people/"
        # [GET] Response -> {"status": "true", "people": People} if True else {"status": "false", "detail": "there is
        # no user with this ID"}
        self.CHECK_PEOPLE_URL = self.API_ENDPOINT + "check-people/"
        # [GET] Response -> {"status": "true", "people_ID": [{"ID": "123"}, ...]}
        self.GET_PEOPLE_ID = self.API_ENDPOINT + "get-people-id/"
        # [GET] Response -> {"status": "true", [{debate_1}, {debate_2}, ...]} if True else {"status": "false",
        # "detail": "something went wrong"}
        self.GET_DEBATES_URL = self.API_ENDPOINT + "get-debates/"

        # {"people_id": "people_id", "debate_id": "debate_id"}
        self.REGISTER_PEOPLE_TO_DEBATE_URL = (
            self.API_ENDPOINT + "register-people-to-debate/"
        )

        # Debate channel
        self.IBRAT_DEBATE_CHANNEL = "@ibratdebate"

        self.TIME_ZONE = "Etc/GMT-5"

        self.ENGLISH_LEVELS = "B1-B2", "C1-C2"
