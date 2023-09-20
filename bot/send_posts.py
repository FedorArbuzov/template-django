
import requests

from bot.send_message import format_complex_message
from bot.consts import URL
from bot.models import Profile, Settings


def send_posts_to_groups(content):
    settings = Settings.objects.first()
    url = URL
    workers = Profile.objects.all()
    req = {
        'chat_id': '123',
    }
    for worker in workers:
        req, url = format_complex_message(req, url, content)
        req['chat_id'] = worker.user_id
        r = requests.post(url, json = req)
        print(r)
        url = URL
        print('send_posts_to_groups')