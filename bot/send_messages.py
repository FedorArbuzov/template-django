import requests

from bot.models import Proile

from bot.consts import TOKEN

URL = f'https://api.telegram.org/bot'

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
    for profile in profiles:
        print(profile)
        url = URL + TOKEN
        req = {
            'chat_id': 123, 
            'parse_mode': 'HTML',
        }
        req, url = format_complex_message(req, url, content)
        req['chat_id'] = profile.user_id
        results += profile.user_id + '\n'
        r = requests.post(url, json = req)
        print(r.status_code)
    return results
