import requests
import aiohttp

from . import settings

bot_settings = settings.Settings()


async def create_user(id: str, name: str, username: str) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        response = await session.post(bot_settings.CREATE_USER_URL, json={"id": id, "name": name, "username": username})
    return response


async def update_user(
    id: str,
    name: str,
    username: str,
    phone_number: str,
    english_level: str
) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            bot_settings.UPDATE_USER_URL,
            json={
                "id": id,
                "name": name,
                "username": username,
                "phone_number": phone_number,
                "english_level": english_level
            }
        )
    return response

def get_req(url: str) -> requests.Response:
    return requests.get(url)


def post_req(url: str, json: dict) -> requests.Response:
    return requests.post(url=url, json=json)


def patch_req(url: str, json: dict) -> requests.Response:
    return requests.patch(url=url, json=json)
