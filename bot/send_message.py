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
    req = {
        'chat_id': chat_id, 
        'text': settings.start_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': settings.about_btn_text,
                    'callback_data': f'/about'
                }],
                [{
                    'text': settings.channel_btn_text,
                    'callback_data': f'/channel'
                }],
                [{
                    'text': settings.check_list_btn_text,
                    'callback_data': f'/subscribe_3'
                }],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_about_message(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.about,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': 'Назад',
                    'callback_data': f'/start'
                }],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_channel_info(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.close_channel,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': settings.buy_channel_btn,
                    'callback_data': f'/subscribe_1'
                }],
                [{
                    'text': settings.buy_group_btn,
                    'callback_data': f'/subscribe_2'
                }],
                [{
                    'text': 'Назад',
                    'callback_data': f'/start'
                }],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_buy_channel(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': "Дает доступ к закрытому каналу на 1 месяц (я напомню вам обновить подписку, не переживайте). ",
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': settings.close_channel_btn_text,
                    'callback_data': f'/buy_channel'
                }],
                [{
                    'text': settings.buy_channel_btn,
                    'callback_data': f'/subscribe_1'
                }]
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_about_group_message(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.about_group,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': settings.close_channel_btn_text,
                    'callback_data': f'/buy_channel'
                }],
                [{
                    'text': settings.buy_channel_btn,
                    'callback_data': f'/subscribe_1'
                }]
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_channel_msg(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': "Дает доступ к закрытому каналу на 1 месяц (я напомню вам обновить подписку, не переживайте). ",
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': settings.buy_channel_btn,
                    'callback_data': f'/subscribe_1'
                }],
                [{
                    'text': 'Мне мало',
                    'callback_data': f'/about_group'
                }],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_about_group_message(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.about_group,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': 
            [
                [{
                    'text': "Тариф «База + чат инсайтов» 2 490 Р",
                    'callback_data': f'/subscribe_2'
                }],
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
    tariff = Tariff.objects.get(number=subscribe_type)
    product_info = f"products[0][quantity]=1&products[0][name]={tariff.name}&customer_extra={tariff.name}&do=pay"
    payment_link = f"""https://mileryus.payform.ru/?order_id=order-{order.id}&customer_phone=79998887755&products[0][price]={tariff.price}&{product_info}"""
    print(payment_link)
    msg = ''
    btn_text = 'оплатить'
    if subscribe_type == 1:
        msg = settings.channel_msg
    elif subscribe_type == 2:
        msg = settings.group_msg
    elif subscribe_type == 3:
        msg = settings.check_list_text
        btn_text = settings.buy_check_list_btn_text
    r = requests.post(URL + '/sendMessage', json = {
        'chat_id': chat_id, 
        'text': msg,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': btn_text,
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

    req, url =  format_complex_message(req, url, settings.buy_check_list_text)
    requests.post(url, json = req)
