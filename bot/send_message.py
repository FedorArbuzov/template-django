import requests

from bot.consts import URL
from bot.models import Settings, Proile, Dialogs

from bot.check_user_subscribed_to_channel import check_user_suscription_to_channel



def send_image(chat_id, image_url):
    req = {'chat_id': chat_id, 'photo': image_url}
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
            'inline_keyboard': [
                [
                    {
                        'text': settings.subscribe_link,
                        'url': settings.channel_link
                    },
                ],
                [
                    {
                        'text': settings.subscribe_check,
                        'callback_data': '/subscribe_check'
                    },
                ],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)


def send_subscribe_link(chat_id):

    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.subscribe_please_message,
        'parse_mode': 'HTML',
    }
    requests.post(URL + '/sendMessage', json = req)


def send_subscribe_check(chat_id):
    settings = Settings.objects.first()
    is_user_subscribed = check_user_suscription_to_channel(chat_id)
    if is_user_subscribed:
        send_you_subscribed_message(chat_id)
        profile, _ = Proile.objects.get_or_create(user_id=chat_id)
    else:
        send_you_not_subscribed_message(chat_id)


def send_you_subscribed_message(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.you_subscribed_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.start_dialog,
                        'callback_data': '/start_dialog'
                    },
                ],
                [
                    {
                        'text': settings.generate_image_command,
                        'callback_data': '/generate_image_start'
                    },
                ],
                [
                    {
                        'text': settings.profile,
                        'callback_data': '/profile'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def generate_image_start(chat_id):
    settings = Settings.objects.first()
    profile, _ = Proile.objects.get_or_create(user_id=chat_id)
    profile.generate_image_mode = True
    profile.save()
    req = {
        'chat_id': chat_id, 
        'text': settings.generate_image_prompt,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.stop_generate_button,
                        'callback_data': '/stop_generate_mode'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)



def send_you_not_subscribed_message(chat_id):
    settings = Settings.objects.first()
    send_pure_text_message(chat_id, settings.you_not_subscribed_message)


def send_start_dialog(chat_id):
    settings = Settings.objects.first()
    profile, _ = Proile.objects.get_or_create(user_id=chat_id)
    
    if not profile.is_premium and profile.message_count > settings.max_free_requests_count:
        send_pure_text_message(chat_id, settings.get_premium_message)
        return 

    dialog, _ = Dialogs.objects.get_or_create(profile=profile)
    send_start_dialog_message(chat_id)


def send_start_dialog_message(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.dialog_started_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.stop_dialog_button,
                        'callback_data': '/stop_dialog'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def send_stop_dialog(chat_id):
    settings = Settings.objects.first()
    profile = Proile.objects.get(user_id=chat_id)
    Dialogs.objects.filter(profile=profile).delete()

    req = {
        'chat_id': chat_id, 
        'text': settings.dialog_stoped_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.start_dialog,
                        'callback_data': '/start_dialog'
                    },
                ],
                [
                    {
                        'text': settings.generate_image_command,
                        'callback_data': '/generate_image_start'
                    },
                ],
                [
                    {
                        'text': settings.profile,
                        'callback_data': '/profile'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def send_gpt_response(chat_id, text):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': text,
        'parse_mode': 'markdown',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.stop_dialog_button,
                        'callback_data': '/stop_dialog'
                    },
                ],
            ]
        }
    }
    r = requests.post(URL + '/sendMessage', json = req)
    print(r)



def set_premium(chat_id):
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': settings.get_premium_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.back_button,
                        'callback_data': '/subscribe_check'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def get_profile_info(chat_id):
    profile, _ = Proile.objects.get_or_create(user_id=chat_id)
    settings = Settings.objects.first()
    req = {
        'chat_id': chat_id, 
        'text': format_user_message(profile, settings),
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.set_preferences_button,
                        'callback_data': '/set_preferences'
                    },
                ],
                [
                    {
                        'text': settings.get_premium,
                        'callback_data': '/get_premium'
                    },
                ],
                [
                    {
                        'text': settings.back_button,
                        'callback_data': '/subscribe_check'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def format_user_message(profile, settings):
    return f"""👤 Ваш профиль

Идентификатор: {profile.user_id}

📊 Информация:
Сделано запросов: {profile.message_count}
Оставшиеся запросы: {settings.max_free_requests_count - profile.message_count if settings.max_free_requests_count - profile.message_count > 0 else 0}
Подписка: {'Активна' if profile.is_premium else 'Неактивна'}"""


def set_preferences_mode(chat_id):
    settings = Settings.objects.first()
    profile = Proile.objects.get(user_id=chat_id)
    profile.preferences_edit_mode = True
    profile.save()
    req = {
        'chat_id': chat_id, 
        'text': settings.preferences_start_edit_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.back_button,
                        'callback_data': '/stop_preferences_mode'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def stop_preferences_mode(chat_id):
    settings = Settings.objects.first()
    profile = Proile.objects.get(user_id=chat_id)
    profile.preferences_edit_mode = False
    profile.save()
    req = {
        'chat_id': chat_id, 
        'text': settings.you_subscribed_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.start_dialog,
                        'callback_data': '/start_dialog'
                    },
                ],
                [
                    {
                        'text': settings.generate_image_command,
                        'callback_data': '/generate_image_start'
                    },
                ],
                [
                    {
                        'text': settings.profile,
                        'callback_data': '/profile'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)


def stop_generate_mode(chat_id):
    settings = Settings.objects.first()
    profile = Proile.objects.get(user_id=chat_id)
    profile.preferences_edit_mode = False
    profile.save()
    req = {
        'chat_id': chat_id, 
        'text': settings.stop_generate_message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {
                        'text': settings.start_dialog,
                        'callback_data': '/start_dialog'
                    },
                ],
                [
                    {
                        'text': settings.generate_image_command,
                        'callback_data': '/generate_image_start'
                    },
                ],
                [
                    {
                        'text': settings.profile,
                        'callback_data': '/profile'
                    },
                ],
            ]
        }
    }
    requests.post(URL + '/sendMessage', json = req)

