import requests

from bot.consts import URL
from bot.models import Settings, Profile, Order, Tariff
from bot.consts import GROUP_ID


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
    else:
        url += '/sendMessage'
        req['text'] = message
    return req, url


def unban_user(user_id):
    req = {'chat_id': GROUP_ID, 'user_id': user_id, 'revoke_messages': False}
    requests.post(URL + '/unbanChatMember', json = req)


def invite_link_user():
    req = {'chat_id': GROUP_ID, 'member_limit': 1, 'creates_join_request': False}
    res = requests.post(URL + '/createChatInviteLink', json = req)
    print(res.json())


def send_image(chat_id, image_url, caption):
    req = {'chat_id': chat_id, 'photo': image_url, 'caption': caption}
    requests.post(URL + '/sendPhoto', json = req)


def send_pure_text_message(chat_id, message):
    req = {'chat_id': chat_id, 'text': message}
    requests.post(URL + '/sendMessage', json = req)


def send_start_message(chat_id):
    settings = Settings.objects.first()
    profile, _ = Profile.objects.get_or_create(user_id=chat_id)
    tariffs = Tariff.objects.all()
    req = {
        'chat_id': chat_id, 
        'text': settings.start_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': tariff.name,
                    'callback_data': f'/subscribe_{tariff.number}'
                }] for tariff in tariffs
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_subscribe_link(chat_id, text):

    settings = Settings.objects.first()
    profile, _ = Profile.objects.get_or_create(user_id=chat_id)
    subscribe_type = int(text.split('_')[1])
    order = Order.objects.create(profile=profile, subscribe_type=subscribe_type)
    price = 2000
    tariff = Tariff.objects.get(number=subscribe_type)
    product_info = f"products[0][quantity]=1&products[0][name]={tariff.name}&customer_extra={tariff.name}&do=pay"
    payment_link = f"""https://mileryus.payform.ru/?order_id=order-{order.id}&customer_phone=79998887755&products[0][price]={tariff.price}&{product_info}"""
    print(payment_link)
    r = requests.post(URL + '/sendMessage', json = {
        'chat_id': chat_id, 
        'text': settings.payment_link_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'оплатить',
                        'url': payment_link
                    },
                ],
                [
                    {
                        'text': 'назад',
                        'callback_data': '/start'
                    },
                ]    
            ],
        }
    })
    print(r)

def send_invite_link_message(invite_message, chat_id, invite_link):
    r = requests.post(URL + '/sendMessage', json = {
        'chat_id': chat_id, 
        'text': invite_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': 'Вступить',
                        'url': invite_link
                    },
                ],
                [
                    {
                        'text': 'назад',
                        'callback_data': '/start'
                    },
                ]    
            ],
        }
    })
    print(r)


def send_doc(chat_id):
    settings = Settings.objects.first()
    url = URL
    req = {
        'chat_id': chat_id, 
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        'text': 'Главная',
                        'callback_data': '/start'
                    }
                ],
            ]
        }
    }

    req, url =  format_complex_message(req, url, settings.file_link)
    requests.post(url, json = req)
