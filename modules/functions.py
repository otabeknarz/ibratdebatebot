import requests

def get_req(url: str) -> requests.Response:
    return requests.get(url)


def post_req(url: str, json: dict) -> requests.Response:
    return requests.post(url=url, json=json)


def patch_req(url: str, json: dict) -> requests.Response:
    return requests.patch(url=url, json=json)
