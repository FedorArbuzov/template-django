import copy
import time
from multiprocessing.dummy import Pool as ThreadPool

import requests

from bot.send_message import format_complex_message
from bot.consts import URL
from bot.models import Profile, Settings


def make_request(data):
    url = data['url']
    data.pop('url', None)
    print(data['chat_id'])
    while True:
        try:
            r = requests.post(url, json=data)
            print(r.status_code)
            print('send_posts_to_groups')
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            print('Retrying in 5 seconds...')
            time.sleep(5)


def send_posts_to_groups(content):
    settings = Settings.objects.first()
    url = URL
    workers = Profile.objects.all()
    req = {
        'chat_id': '123',
        'parse_mode': 'Markdown'
    }
    req, url = format_complex_message(req, url, content)
    for chuck in [workers[i:i+10] for i in range(0,len(workers),10)]:
        reqs = []
        for i in chuck:
            data = copy.deepcopy(req)
            data['chat_id'] = i.user_id
            data['url'] = url
            reqs.append(data)
        pool = ThreadPool(len(chuck))
        pool.map(make_request, reqs)
        pool.close()
        pool.join()
        print('send_posts_to_groups')
