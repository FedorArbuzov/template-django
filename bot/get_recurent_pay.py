from background_task import background
from models import Profile, Order, Tariff

from collections.abc import MutableMapping
from urllib.parse import urlencode

import requests


@background(schedule=60)
def get_pay(user_id, subscribe_type):
    profile = Profile.objects.get(user_id=user_id)
    order = Order.objects.create(profile=profile, subscribe_type=subscribe_type)
    tariff = Tariff.objects.get(number=subscribe_type)
    generate_payment_link(profile, order, tariff)


def generate_payment_link(profile, order, tariff):

    # URL платежной формы
    linktoform = 'https://mileryus.payform.ru/rest/payment/do/'

    # Секретный ключ. Можно найти на странице настроек, 
    # в личном кабинете платежной формы
    secret_key = '52cd7d0f21ad98b142495b385fdc0af4d53951003432731a9b45504238e7b5b1'

    data = {
    'order_id': f'order-{order.id}',
    'customer_phone': profile.phone,
    'sys': 'mileryus',
    'client_id': profile.user_id,
    'binding_id': profile.binding_id,
    'products': [
            {
                'price': tariff.price,
                'name': tariff.name,
                'quantity': 1
            }
        ],
    }

    # подписываем с помощью кастомной функции sign (см ниже)
    data['signature'] = sign(data, secret_key)

    # компануем ссылку с помощью кастомной функции http_build_query (см ниже)
    link = linktoform + '?' + urlencode(http_build_query(data))

    res = requests.get(link)
    print(res)

def sign(data, secret_key):
    import hashlib
    import hmac
    import json

    # переводим все значения data в string c помощью кастомной функции deep_int_to_string (см ниже)
    deep_int_to_string(data)

    # переводим data в JSON, с сортировкой ключей в алфавитном порядке, без пробелом и экранируем бэкслеши
    data_json = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':')).replace("/", "\\/")

    # создаем подпись с помощью библиотеки hmac и возвращаем ее
    return hmac.new(secret_key.encode('utf8'), data_json.encode('utf8'), hashlib.sha256).hexdigest()

def deep_int_to_string(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, MutableMapping):
            deep_int_to_string(value)
        elif isinstance(value, list) or isinstance(value, tuple):
            for k, v in enumerate(value):
                deep_int_to_string({str(k): v})
        else: dictionary[key] = str(value)
                
def http_build_query(dictionary, parent_key=False):
    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + '[' + key + ']' if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(http_build_query(value, new_key).items())
        elif isinstance(value, list) or isinstance(value, tuple):
            for k, v in enumerate(value):
                items.extend(http_build_query({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


