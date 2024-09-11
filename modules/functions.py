import requests


def get_req(url):
    return requests.get(url)


def post_req(url, json):
    return requests.post(url=url, json=json)
