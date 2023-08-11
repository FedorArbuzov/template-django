import json
from datetime import timedelta, datetime

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bot.register_hook import register_webhook
from bot.check_callbacks import check_callbacks
from bot.send_message import (send_start_message, send_pure_text_message, send_subscribe_link, send_invite_link_message, send_doc, send_about_message,
                                send_channel_info, send_buy_channel, send_channel_msg, send_about_group_message)

from bot.models import Order, Settings

from bot.consts import GROUP_ID, CHANNEL_ID, URL


register_webhook()



def unban_user(user_id, id):
    req = {'chat_id': id, 'user_id': user_id, 'revoke_messages': False}
    requests.post(URL + '/unbanChatMember', json = req)


def invite_link_user(id):
    req = {'chat_id': id, 'member_limit': 1, 'creates_join_request': False}
    res = requests.post(URL + '/createChatInviteLink', json = req)
    return res.json()


@csrf_exempt
def prodamus_webhook(request):   
    data = request.body.decode('utf-8')
    order_id = None
    for item in data.split('&'):
        if 'order_num=' in item:
            order_id = int(item.split('-')[1])
            break
    order = Order.objects.get(id=order_id)
    order.paid = True
    order.save()
    profile = order.profile
    settings = Settings.objects.first()
    if order.subscribe_type == 3:
        # отправка чек-листа
        send_doc(profile.user_id)
    elif order.subscribe_type == 2:
        invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
        print(invite_link)
        send_invite_link_message(settings.invite_message_channel, order.profile.user_id, invite_link)
        
        profile.premium_bought_to = datetime.now() + timedelta(days=1*30)

    elif order.subscribe_type == 1:
        invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
        print(invite_link)
        send_invite_link_message(settings.invite_message_channel, order.profile.user_id, invite_link)

        invite_link = invite_link_user(GROUP_ID)['result']['invite_link']
        print(invite_link)
        send_invite_link_message(settings.invite_message_group, order.profile.user_id, invite_link)

        profile.premium_bought_to = datetime.now() + timedelta(days=1*30)

    # if profile.premium_bought_to:
    #     profile.premium_bought_to += timedelta(days=1*30)
    #     send_pure_text_message(profile.user_id, f"Доступ продлен")
    # else:
    #     unban_user(order.profile.user_id, CHANNEL_ID)
    #     profile.premium_bought_to = datetime.now() + timedelta(days=1*30)
    #     invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
    #     print(invite_link)
    #     send_invite_link_message(order.profile.user_id, invite_link)
    #     if order.subscribe_type == 2:
    #         unban_user(order.profile.user_id, GROUP_ID)
    #         invite_link = invite_link_user(GROUP_ID)['result']['invite_link']
    #         print(invite_link)
    #         send_invite_link_message(order.profile.user_id, invite_link)
    profile.save()
    # по ордеру находим пользователя, проставляем ему дату до какого числа он может пользоваться, и отправляем ссылку на вступление в группу
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def webhook(request):   
    
    json_data = json.loads(request.body)
    json_data = check_callbacks(json_data)

    if 'message' not in json_data:
        return JsonResponse({'status': 'ok'})
    chat_id = json_data['message']['chat']['id']
    print(chat_id)
    if chat_id < 0:
        return JsonResponse({'status': 'ok'})
    
    text = json_data['message'].get('text', '')
    if 'document' in json_data['message']:
        send_pure_text_message(chat_id, f"document:{json_data['message']['document']['file_id']}") 
        return JsonResponse({'status': 'ok'})
    if 'video' in json_data['message']:
        send_pure_text_message(chat_id, f"video:{json_data['message']['video']['file_id']}") 
        return JsonResponse({'status': 'ok'})
    if 'photo' in json_data['message']:
        send_pure_text_message(chat_id, f"photo:{json_data['message']['photo'][0]['file_id']}") 
        return JsonResponse({'status': 'ok'})
    
    # Обработка стартовой команды
    if text == '/start' or text == '/menu':
        print('start!')
        send_start_message(chat_id) 
    elif text == '/about':
        print('about')
        send_about_message(chat_id)
    elif text == '/channel':
        print('channel')
        send_channel_info(chat_id)
    elif text == '/buy_channel':
        print('buy_channel')
        send_channel_msg(chat_id)
    elif text == '/buy_channel_link':
        print('buy_channel_link')
    elif text == '/about_group':
        print('about_group')
        send_about_group_message(chat_id)
    elif text == '/group_buy':
        print('group_buy')
    elif '/subscribe_' in text: 
        send_subscribe_link(chat_id, text)
    else:
        pass
    return JsonResponse({'status': 'ok'})
