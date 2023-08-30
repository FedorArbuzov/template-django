import requests

from .consts import TOKEN, HOST



def register_webhook():
    print('register webhook')
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={HOST}/statsbot-webhook/"

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)