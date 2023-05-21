import copy
import requests
from multiprocessing.dummy import Pool as ThreadPool

from bot.models import Proile

from bot.consts import TOKEN

URL = f'https://api.telegram.org/bot'


def make_request(data):
    url = data['url']
    data.pop('url', None)
    print(data['chat_id'])
    r = requests.post(url, json = data)
    print(r.status_code)


def format_complex_message(req, url, message):
    if 'document:' in message:
        url += '/sendDocument'
        message_data= message.split('document:')
        req['caption'] = message_data[0]
        req['document'] = message_data[1]
    elif 'video:' in message:
        url += '/sendVideo'
        message_data= message.split('video:')
        req['caption'] = message_data[0]
        req['video'] = message_data[1]
    elif 'photo:' in message:
        url += '/sendPhoto'
        message_data= message.split('photo:')
        req['caption'] = message_data[0]
        req['photo'] = message_data[1]
    else:
        url += '/sendMessage'
        req['text'] = message
    return req, url

def send_message_to_group(content, group):
    profiles = []
    if group == 'ALL':
        profiles = Proile.objects.all()
    elif group == 'ADMINS':
        profiles = Proile.objects.filter(is_admin=True)
    results = ''
    url = URL + TOKEN
    req = {
        'chat_id': 123, 
        'parse_mode': 'HTML',
    }
    req, url = format_complex_message(req, url, content)
    for chunk in [profiles[i:i+10] for i in range(0,len(profiles),10)]:
        reqs = []
        for i in chunk:
            data = copy.deepcopy(req)
            data['chat_id'] = i.user_id
            data['url'] = url
            reqs.append(data)
        pool = ThreadPool(len(chunk))
        pool.map(make_request, reqs)
        pool.close()
        pool.join()
    return results
