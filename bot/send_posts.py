
import requests

from bot.send_message import format_complex_message
from bot.consts import URL
from bot.models import Worker, Settings


def send_posts_to_groups(content, group):
    settings = Settings.objects.first()
    url = URL
    workers = Worker.objects.all()
    req = {
        'chat_id': '123',
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        'text': settings.new_post_button,
                        'callback_data': '/menu'
                    }
                ],
            ]
        }
    }
    for worker in workers:
        req, url = format_complex_message(req, url, content)
        req['chat_id'] = worker.chat_id
        r = requests.post(url, json = req)
        print(r)
        url = URL
        print('send_posts_to_groups')