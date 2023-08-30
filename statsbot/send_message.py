import requests

from statsbot.consts import URL
from statsbot.models import Settings, Profile


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


def send_pure_text_message(chat_id, message):
    req = {'chat_id': chat_id, 'text': message}
    requests.post(URL + '/sendMessage', json = req)


def send_photo_message(chat_id):
    settings = Settings.objects.first()
    url = URL
    req = {
        'chat_id': chat_id
    }

    req, url =  format_complex_message(req, url, settings.image)
    requests.post(url, json = req)


def send_start_message(chat_id):
    Profile.objects.get_or_create(user_id=chat_id)
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.start_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': settings.get_photo_btn_text,
                    'callback_data': f'/get_photo'
                }],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)
